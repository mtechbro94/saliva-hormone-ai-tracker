# 🧬 Saliva-Based Hormonal Tracking System Using Artificial Intelligence

An academic healthcare web application that tracks saliva-based hormone levels (Cortisol, Estrogen, Testosterone) and uses AI/ML to classify hormonal status.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![License](https://img.shields.io/badge/License-Academic-orange.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [How to Use](#-how-to-use)
- [AI/ML Model Explained](#-aiml-model-explained)
- [Database Schema](#-database-schema)
- [Screenshots](#-screenshots)
- [API Endpoints](#-api-endpoints)

---

## ✨ Features

### 👤 User Authentication
- Secure user registration with profile details (Name, Age, Gender)
- Password hashing using Werkzeug security
- Session-based login/logout system

### 🧪 Hormone Data Tracking
- Input saliva-based hormone values:
  - **Cortisol** (ng/mL) - Stress hormone
  - **Estrogen** (pg/mL) - Sex hormone
  - **Testosterone** (ng/dL) - Sex hormone
- Date and time stamping for each sample
- Historical record management

### 🤖 AI-Powered Analysis
- Machine learning classification of hormonal status:
  - ✅ **Normal** - Healthy hormone balance
  - ⚠️ **Borderline** - Values near threshold limits
  - ❌ **Abnormal** - Values outside normal ranges
- Confidence scores for each prediction
- Personalized health recommendations

### 📊 Interactive Dashboard
- Real-time hormonal status display
- Individual hormone analysis cards
- Chart.js trend visualizations:
  - Individual hormone line charts
  - Combined comparison chart
- Historical records table with delete functionality

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | HTML5, CSS3, JavaScript |
| **Backend** | Python Flask |
| **Database** | SQLite |
| **AI/ML** | Scikit-learn (Random Forest) |
| **Charts** | Chart.js |
| **Authentication** | Session-based with Werkzeug |
| **Styling** | Custom CSS (Healthcare Theme) |

---

## 📁 Project Structure

```
saliva-hormone-ai/
│
├── app.py                 # Main Flask application
├── model.py               # AI/ML module (training & prediction)
├── hormone_data.csv       # Simulated training dataset
├── hormone_model.pkl      # Trained ML model (generated)
├── database.db            # SQLite database (generated)
├── requirements.txt       # Python dependencies
├── README.md              # This file
│
├── templates/             # HTML templates
│   ├── base.html          # Base template with nav & footer
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # Main dashboard
│   └── add_data.html      # Hormone input form
│
└── static/                # Static assets
    ├── css/
    │   └── style.css      # Healthcare-themed styles
    └── js/
        └── charts.js      # Chart.js visualizations
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Installation

1. **Navigate to the project directory**
   ```bash
   cd c:\Users\Mtechbro-94\Desktop\HealthCare_App
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # OR
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the AI model & generate dataset**
   ```bash
   python model.py
   ```
   This will create:
   - `hormone_data.csv` - 500 simulated hormone samples
   - `hormone_model.pkl` - Trained Random Forest model

5. **Run the Flask application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   ```
   http://localhost:5000
   ```

---

## 📖 How to Use

### 1. Register a New Account
1. Go to the registration page
2. Fill in your details (Name, Age, Gender, Email, Password)
3. Click "Create Account"

### 2. Login
1. Enter your email and password
2. Click "Sign In"

### 3. Add Hormone Data
1. Click "Add New Sample" from the dashboard
2. Enter your hormone values:
   - **Cortisol**: 0-50 ng/mL (normal: 3-10)
   - **Estrogen**: 0-1000 pg/mL (normal: 15-350)
   - **Testosterone**: 0-200 ng/dL (normal: 15-70)
3. Select the date and time of the sample
4. Click "Analyze & Save"

### 4. View Results
- The AI will instantly classify your hormonal status
- View detailed analysis on the dashboard
- Track trends over time with charts

---

## 🤖 AI/ML Model Explained

### Overview
The system uses a **Random Forest Classifier** to analyze hormone levels and predict overall hormonal health status.

### Training Data
- **500 simulated samples** generated with realistic hormone distributions
- Three classes with the following distribution:
  - Normal (40%): Mid-range hormone values
  - Borderline (30%): Values near threshold limits
  - Abnormal (30%): Values outside normal ranges

### Normal Hormone Ranges (Reference)

| Hormone | Normal Range | Unit |
|---------|-------------|------|
| Cortisol | 3-10 | ng/mL |
| Estrogen | 15-350 | pg/mL |
| Testosterone | 15-70 | ng/dL |

### Model Architecture
```
Random Forest Classifier
├── n_estimators: 100 trees
├── max_depth: 10
├── min_samples_split: 5
└── Features: [cortisol, estrogen, testosterone]
```

### Prediction Flow
```
Input Values → Feature Extraction → Random Forest → Status + Confidence
                                                      ↓
                                              Health Insights
```

### Model Performance
- Training/Test Split: 80/20
- Accuracy: ~95% on test set
- Uses stratified sampling for balanced evaluation

---

## 🗄 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,          -- Hashed with Werkzeug
    age INTEGER,
    gender TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Hormone Records Table
```sql
CREATE TABLE hormone_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    cortisol REAL NOT NULL,          -- ng/mL
    estrogen REAL NOT NULL,          -- pg/mL
    testosterone REAL NOT NULL,       -- ng/dL
    date TEXT NOT NULL,              -- Sample date
    time TEXT NOT NULL,              -- Sample time
    prediction TEXT NOT NULL,        -- Normal/Borderline/Abnormal
    confidence REAL,                 -- AI confidence %
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

---

## 📸 Screenshots

### Login Page
![Login Page](screenshots/login.png)
*Clean, healthcare-themed login interface with branding*

### Registration Page
![Register Page](screenshots/register.png)
*Comprehensive registration form with profile fields*

### Dashboard - Normal Status
![Dashboard Normal](screenshots/dashboard-normal.png)
*Dashboard showing normal hormonal status with recommendations*

### Dashboard - Charts
![Dashboard Charts](screenshots/dashboard-charts.png)
*Interactive Chart.js visualizations for hormone trends*

### Add Hormone Data
![Add Data](screenshots/add-data.png)
*Input form for recording new hormone samples*

### AI Prediction Result
![AI Prediction](screenshots/ai-prediction.png)
*Detailed AI analysis with confidence score and health insights*

> **Note**: Create a `screenshots/` folder and add actual screenshots after running the application.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home/redirect |
| GET/POST | `/login` | User login |
| GET/POST | `/register` | User registration |
| GET | `/logout` | User logout |
| GET | `/dashboard` | Main dashboard |
| GET/POST | `/add_data` | Add hormone record |
| GET | `/api/hormone_data` | JSON API for chart data |
| POST | `/delete_record/<id>` | Delete a record |

---

## 📝 Academic Notes

### Disclaimer
This is an **academic project** for educational purposes. The hormone values are simulated/dataset-based and should **NOT** be used for actual medical diagnosis.

### Key Learning Outcomes
1. **Full-stack web development** with Flask
2. **Machine Learning integration** with Scikit-learn
3. **Database design** with SQLite
4. **Data visualization** with Chart.js
5. **User authentication** and session management
6. **Responsive web design** principles

### Future Improvements
- Real sensor/lab integration
- More sophisticated ML models (Neural Networks)
- Time-series analysis for trend prediction
- Mobile-responsive PWA version
- Export reports as PDF

---

## � CI/CD Pipeline & Deployment

### GitHub Actions Workflows

This project includes automated CI/CD pipelines for quality assurance and deployment:

#### 1. **CI/CD Pipeline** (`.github/workflows/ci-cd.yml`)
Runs on every push and pull request:
- ✅ **Multi-version testing** (Python 3.11, 3.12)
- ✅ **Code linting** (Flake8)
- ✅ **Code formatting** (Black, isort)
- ✅ **Security scanning** (Bandit, Safety)
- ✅ **Unit testing** (Pytest)
- ✅ **Coverage reporting** (Codecov)

#### 2. **Deployment Pipeline** (`.github/workflows/deploy.yml`)
Runs on main branch pushes and version tags:
- ✅ Final testing before deployment
- ✅ Package creation and compression
- ✅ Artifact upload (30-day retention)
- ✅ GitHub release creation
- ✅ Build notification

### Deployment Steps

1. **Commit and Push**
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

2. **Automated Testing**
   - GitHub Actions automatically runs all checks
   - View results in "Actions" tab on GitHub

3. **Create Release Tag** (Optional - for production)
   ```bash
   git tag -a v1.0.0 -m "Production Release v1.0.0"
   git push origin v1.0.0
   ```

4. **View Build Artifacts**
   - Go to GitHub Actions
   - Select the workflow run
   - Download artifacts (healthcare-app-build)

### Local Testing Before Push

```bash
# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8 isort

# Run tests
pytest

# Check code formatting
black . --check
isort . --check-only

# Run linter
flake8 .
```

---

## �📄 License

This project is created for **academic purposes**. Feel free to use and modify for educational projects.

---

## 👨‍💻 Author

**Academic Healthcare Project**  
Saliva-Based Hormonal Tracking System Using Artificial Intelligence

---

*Built with ❤️ using Flask, Scikit-learn, and Chart.js*
