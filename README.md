# Saliva-Based Hormonal Tracking System Using Artificial Intelligence

An academic healthcare web application that tracks saliva-based hormone levels (Cortisol, Estrogen, Testosterone) and uses machine learning to classify hormonal status.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![License](https://img.shields.io/badge/License-Academic-orange.svg)

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [AI/ML Model](#aiml-model)
- [CI/CD Pipeline](#cicd-pipeline)
- [Database Schema](#database-schema)

## Features

**User Authentication**
- Secure user registration with profile details
- Password hashing using Werkzeug security
- Session-based login/logout system

**Hormone Data Tracking**
- Input saliva-based hormone values: Cortisol, Estrogen, Testosterone
- Date and time stamping for each sample
- Historical record management with deletion capability

**AI-Powered Analysis**
- Machine learning classification of hormonal status
- Confidence scores for each prediction
- Personalized health recommendations

**Interactive Dashboard**
- Real-time hormonal status display
- Hormone analysis cards with current values
- Chart.js trend visualizations
- Historical records table

**Responsive Design**
- Professional healthcare-themed UI
- Mobile-responsive layout
- Accessibility compliant design

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Flask (Python 3.11+) |
| Database | SQLite |
| ML Framework | Scikit-learn |
| Frontend | HTML5, CSS3, JavaScript |
| Charts | Chart.js |
| Authentication | Flask-Login, Werkzeug |
| Data Processing | Pandas, NumPy |

## Project Structure

```
HealthCare_App/
├── app.py                    # Flask application entry point
├── model.py                  # ML model training and predictions
├── requirements.txt          # Python dependencies
├── hormone_data.csv          # Dataset for training
├── hormone_model.pkl         # Pre-trained model
├── scaler.pkl               # Feature scaler
├── encoder.pkl              # Label encoder
├── README.md                # This file
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── home.html           # Landing page
│   ├── dashboard.html      # Main dashboard
│   ├── add_data.html       # Add hormone data
│   ├── forgot_password.html
│   └── reset_password.html
├── static/                  # Static files
│   ├── css/
│   │   └── style.css       # Responsive styling
│   ├── js/
│   │   └── charts.js       # Chart.js visualizations
│   └── images/             # UI images
└── .github/
    └── workflows/          # GitHub Actions CI/CD
        ├── ci-cd.yml
        └── deploy.yml
```

## Setup and Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Installation Steps

1. Clone the repository
```bash
git clone https://github.com/mtechbro94/saliva-hormone-ai-tracker.git
cd HealthCare_App
```

2. Create and activate virtual environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python app.py
```

5. Open browser and navigate to
```
http://localhost:5000
```

## Usage

### Creating an Account
1. Click "Register" on the login page
2. Enter your name, email, age, and gender
3. Create a secure password
4. Click "Register" to create your account

### Adding Hormone Data
1. Log in to your account
2. Click "Add Hormone Data"
3. Enter cortisol, estrogen, and testosterone values
4. Specify the date and time of sample
5. Click "Submit" for AI analysis

### Viewing Dashboard
1. After logging in, you see your dashboard
2. Current hormone status is displayed with analysis cards
3. Charts show historical trends
4. Historical records table lists all previous entries

### AI Prediction
The machine learning model analyzes your hormone values and returns:
- Classification: Normal / Borderline / Abnormal
- Confidence Score: Prediction confidence percentage
- Health Recommendations: Personalized advice based on analysis

## AI/ML Model

### Model Type
Random Forest Classifier with 100 trees

### Features Used
- Cortisol (ng/mL)
- Estrogen (pg/mL)
- Testosterone (ng/dL)

### Preprocessing
- StandardScaler for feature normalization
- LabelEncoder for target classification

### Classification Output
- Normal: Healthy hormone balance
- Borderline: Values near threshold
- Abnormal: Values outside normal ranges

### Performance
- Multi-class classification
- High confidence scores for predictions
- Trained on comprehensive healthcare dataset

### Files
- hormone_model.pkl: Trained model
- scaler.pkl: Feature scaler
- encoder.pkl: Label encoder

## CI/CD Pipeline

### GitHub Actions Workflows

**CI/CD Pipeline** (`.github/workflows/ci-cd.yml`)
- Multi-version testing (Python 3.11, 3.12)
- Code linting with Flake8
- Code formatting with Black and isort
- Security scanning with Bandit and Safety
- Unit testing with Pytest
- Coverage reporting

**Deployment Pipeline** (`.github/workflows/deploy.yml`)
- Final testing before deployment
- Package creation
- Artifact upload
- GitHub release creation

### Local Testing

```bash
# Install dev dependencies
pip install pytest black flake8 isort bandit safety

# Run tests
pytest

# Check code formatting
black . --check
isort . --check-only

# Run linter
flake8 .

# Security check
bandit -r .
```

## Database Schema

### Users Table
- id: Primary key
- name: User's name
- email: Unique email address
- password: Hashed password
- age: User age
- gender: User gender
- created_at: Registration timestamp

### Hormone Records Table
- id: Primary key
- user_id: Foreign key to users table
- cortisol: Cortisol value (ng/mL)
- estrogen: Estrogen value (pg/mL)
- testosterone: Testosterone value (ng/dL)
- date: Sample collection date
- time: Sample collection time
- prediction: Classification result
- confidence: AI confidence percentage
- created_at: Record timestamp

## Important Notes

### Disclaimer
This is an academic project for educational purposes only. The hormone values are simulated and should NOT be used for actual medical diagnosis. Always consult healthcare professionals for medical decisions.

### Educational Use
This project demonstrates:
- Full-stack web development with Flask
- Machine learning integration with Scikit-learn
- Database design with SQLite
- Data visualization with Chart.js
- User authentication and session management
- Responsive web design principles

### What's Included
- Flask web application with authentication
- SQLite database for data persistence
- Machine learning model for hormone analysis
- Interactive dashboard with visualizations
- Responsive healthcare-themed UI
- Automated CI/CD pipeline with GitHub Actions
- Pre-trained model files
- Complete documentation

## Repository

GitHub: https://github.com/mtechbro94/saliva-hormone-ai-tracker

## Support

For issues or questions, please open an issue on the GitHub repository.

## License

This project is created for academic purposes. Feel free to use and modify for educational projects.

---

Built with Flask, Scikit-learn, and Chart.js
