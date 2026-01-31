"""
Saliva-Based Hormonal Tracking System - Flask Application
==========================================================
Production-ready Flask application with:
1. User authentication (register, login, logout)
2. Hormone data input with demographic context
3. AI-powered prediction with detailed insights
4. Dashboard with visualizations and health tracking

Academic Project - Uses realistic simulated hormone data
"""

from flask import (
    Flask, render_template, request, redirect, 
    url_for, flash, session, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
import os
from datetime import datetime

# Import our ML model module
from model import predict_status, load_model

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'saliva-hormone-tracking-2024-production-key')

# Database configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')

# Load ML model at startup
ML_MODEL = None
ML_SCALER = None


def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database with tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Hormone records table with enhanced fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hormone_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            cortisol REAL NOT NULL,
            estrogen REAL NOT NULL,
            testosterone REAL NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            time_of_day TEXT DEFAULT 'Morning',
            prediction TEXT NOT NULL,
            confidence REAL,
            insights TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized")


def login_required(f):
    """Decorator for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """Get current logged-in user."""
    if 'user_id' not in session:
        return None
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?', 
        (session['user_id'],)
    ).fetchone()
    conn.close()
    
    return dict(user) if user else None


# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route('/')
def index():
    """Home/Landing page."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        age = request.form.get('age', type=int)
        gender = request.form.get('gender', '')
        
        # Validation
        errors = []
        if not name:
            errors.append('Name is required.')
        if not email:
            errors.append('Email is required.')
        if not password:
            errors.append('Password is required.')
        if password != confirm_password:
            errors.append('Passwords do not match.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if not age or age < 18 or age > 100:
            errors.append('Valid age (18-100) is required.')
        if not gender:
            errors.append('Gender is required.')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html')
        
        conn = get_db_connection()
        existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        
        if existing:
            conn.close()
            flash('Email already registered.', 'warning')
            return redirect(url_for('login'))
        
        hashed_password = generate_password_hash(password)
        
        try:
            conn.execute(
                'INSERT INTO users (name, email, password, age, gender) VALUES (?, ?, ?, ?, ?)',
                (name, email, hashed_password, age, gender)
            )
            conn.commit()
            conn.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conn.close()
            flash(f'Registration failed.', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please enter both email and password.', 'warning')
            return render_template('login.html')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_age'] = user['age']
            session['user_gender'] = user['gender']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Log out user."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password - step 1: enter email."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user:
            # Store email in session for reset
            session['reset_email'] = email
            session['reset_user_id'] = user['id']
            session['reset_verified'] = True
            flash('Email verified! Please set your new password.', 'success')
            return redirect(url_for('reset_password'))
        else:
            flash('No account found with that email address.', 'danger')
    
    return render_template('forgot_password.html')


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Reset password - step 2: set new password."""
    if not session.get('reset_verified'):
        flash('Please enter your email first.', 'warning')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('reset_password.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('reset_password.html')
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        conn.execute(
            'UPDATE users SET password = ? WHERE id = ?',
            (hashed_password, session['reset_user_id'])
        )
        conn.commit()
        conn.close()
        
        # Clear reset session data
        session.pop('reset_email', None)
        session.pop('reset_user_id', None)
        session.pop('reset_verified', None)
        
        flash('Password updated successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', email=session.get('reset_email'))


# ============================================
# DASHBOARD AND DATA ROUTES
# ============================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard."""
    user = get_current_user()
    
    conn = get_db_connection()
    records = conn.execute(
        '''SELECT * FROM hormone_records 
           WHERE user_id = ? 
           ORDER BY date DESC, time DESC
           LIMIT 50''',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    
    latest_record = dict(records[0]) if records else None
    
    # Get insights for latest record
    latest_insights = None
    if latest_record:
        prediction_result = predict_status(
            latest_record['cortisol'],
            latest_record['estrogen'],
            latest_record['testosterone'],
            ML_MODEL, ML_SCALER,
            user.get('age', 35),
            user.get('gender', 'Male'),
            latest_record.get('time_of_day', 'Morning')
        )
        latest_insights = prediction_result['insights']
        latest_insights['hormone_analysis'] = prediction_result['hormone_analysis']
        latest_insights['probabilities'] = prediction_result.get('probabilities', {})
    
    # Calculate statistics
    stats = {
        'total_records': len(records),
        'normal_count': len([r for r in records if r['prediction'] == 'Normal']),
        'imbalance_count': len([r for r in records if 'Imbalance' in r['prediction']]),
    }
    
    return render_template(
        'dashboard.html',
        user=user,
        records=[dict(r) for r in records],
        latest_record=dict(latest_record) if latest_record else None,
        latest_insights=latest_insights,
        stats=stats
    )


@app.route('/add_data', methods=['GET', 'POST'])
@login_required
def add_data():
    """Add hormone data with AI analysis."""
    user = get_current_user()
    
    if request.method == 'POST':
        try:
            cortisol = float(request.form.get('cortisol', 0))
            estrogen = float(request.form.get('estrogen', 0))
            testosterone = float(request.form.get('testosterone', 0))
            date = request.form.get('date', '')
            time = request.form.get('time', '')
            time_of_day = request.form.get('time_of_day', 'Morning')
            
            # Validation
            if cortisol <= 0 or estrogen <= 0 or testosterone <= 0:
                flash('All hormone values must be positive.', 'danger')
                return render_template('add_data.html', user=user)
            
            if not date or not time:
                flash('Please select date and time.', 'danger')
                return render_template('add_data.html', user=user)
            
            # Get AI prediction with user context
            prediction_result = predict_status(
                cortisol, estrogen, testosterone,
                ML_MODEL, ML_SCALER,
                user.get('age', 35),
                user.get('gender', 'Male'),
                time_of_day
            )
            
            # Save to database
            conn = get_db_connection()
            conn.execute(
                '''INSERT INTO hormone_records 
                   (user_id, cortisol, estrogen, testosterone, date, time, time_of_day, prediction, confidence, insights)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    session['user_id'],
                    cortisol, estrogen, testosterone,
                    date, time, time_of_day,
                    prediction_result['status'],
                    prediction_result['confidence'],
                    prediction_result['insights']['title']
                )
            )
            conn.commit()
            conn.close()
            
            # Flash with appropriate color
            status = prediction_result['status']
            if status == 'Normal':
                flash_type = 'success'
            elif 'Mild' in status:
                flash_type = 'warning'
            else:
                flash_type = 'danger'
            
            flash(
                f'Analysis complete! Status: {status} ({prediction_result["confidence"]}% confidence)',
                flash_type
            )
            return redirect(url_for('dashboard'))
            
        except ValueError:
            flash('Please enter valid numeric values.', 'danger')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    today = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M')
    
    # Determine time of day
    hour = datetime.now().hour
    if hour < 12:
        default_time_of_day = 'Morning'
    elif hour < 17:
        default_time_of_day = 'Afternoon'
    else:
        default_time_of_day = 'Evening'
    
    return render_template(
        'add_data.html', 
        user=user,
        today=today, 
        current_time=current_time,
        default_time_of_day=default_time_of_day
    )


@app.route('/api/hormone_data')
@login_required
def api_hormone_data():
    """API for chart data."""
    conn = get_db_connection()
    records = conn.execute(
        '''SELECT date, cortisol, estrogen, testosterone, prediction, time_of_day
           FROM hormone_records 
           WHERE user_id = ? 
           ORDER BY date ASC, time ASC
           LIMIT 100''',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    
    data = {
        'labels': [],
        'cortisol': [],
        'estrogen': [],
        'testosterone': [],
        'predictions': []
    }
    
    for record in records:
        data['labels'].append(record['date'])
        data['cortisol'].append(record['cortisol'])
        data['estrogen'].append(record['estrogen'])
        data['testosterone'].append(record['testosterone'])
        data['predictions'].append(record['prediction'])
    
    return jsonify(data)


@app.route('/api/stats')
@login_required
def api_stats():
    """API for dashboard statistics."""
    user = get_current_user()
    
    conn = get_db_connection()
    records = conn.execute(
        'SELECT * FROM hormone_records WHERE user_id = ? ORDER BY date DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    
    stats = {
        'total_records': len(records),
        'status_distribution': {},
        'avg_cortisol': 0,
        'avg_estrogen': 0,
        'avg_testosterone': 0
    }
    
    if records:
        for r in records:
            status = r['prediction']
            stats['status_distribution'][status] = stats['status_distribution'].get(status, 0) + 1
        
        stats['avg_cortisol'] = round(sum(r['cortisol'] for r in records) / len(records), 2)
        stats['avg_estrogen'] = round(sum(r['estrogen'] for r in records) / len(records), 2)
        stats['avg_testosterone'] = round(sum(r['testosterone'] for r in records) / len(records), 2)
    
    return jsonify(stats)


@app.route('/delete_record/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    """Delete a hormone record."""
    conn = get_db_connection()
    record = conn.execute(
        'SELECT user_id FROM hormone_records WHERE id = ?',
        (record_id,)
    ).fetchone()
    
    if record and record['user_id'] == session['user_id']:
        conn.execute('DELETE FROM hormone_records WHERE id = ?', (record_id,))
        conn.commit()
        flash('Record deleted.', 'info')
    else:
        flash('Access denied.', 'danger')
    
    conn.close()
    return redirect(url_for('dashboard'))


@app.route('/profile')
@login_required
def profile():
    """User profile page."""
    user = get_current_user()
    
    conn = get_db_connection()
    record_count = conn.execute(
        'SELECT COUNT(*) as count FROM hormone_records WHERE user_id = ?',
        (session['user_id'],)
    ).fetchone()['count']
    conn.close()
    
    return render_template('profile.html', user=user, record_count=record_count)


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('login.html'), 404


@app.errorhandler(500)
def internal_error(e):
    flash('An error occurred.', 'danger')
    return redirect(url_for('index'))


# ============================================
# APPLICATION STARTUP
# ============================================

if __name__ == '__main__':
    init_db()
    
    print("Loading ML model...")
    ML_MODEL, ML_SCALER = load_model()
    print("✓ ML model loaded")
    
    print("\n" + "=" * 50)
    print("🧬 Saliva-Based Hormonal Tracking System")
    print("=" * 50)
    print("Server: http://localhost:5000")
    print("=" * 50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
