# Hospital Management System v2 (Full)

AppDev1 project created by Sairam Ramakrishnan (24F2006201) - Hospital Mgmt System built with Flask to demonstrate CRUD for Doctors, Patients and appointments.

## Features

### User Roles & Capabilities
- **Admin Dashboard**
  - Manage doctors and patients
  - View analytics and statistics
  - Access appointment logs
  - Generate reports
  - Chart.js visualizations
  
- **Doctor Portal**
  - Manage availability (weekly slots)
  - View upcoming appointments
  - Update appointment status
  - Access patient history
  
- **Patient Features**
  - Book appointments
  - View appointment history
  - Update personal information

### Technical Features
- Flask-based backend with SQLAlchemy ORM
- Role-based authentication using Flask-Login
- Responsive Bootstrap UI with custom CSS
- Interactive sidebar navigation
- JSON-based doctor availability management
- Chart.js integration for analytics
- Sample data for testing (3 doctors, 5 patients, 10 appointments)

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/Sai-ITMDS/MAD1.git
   cd MAD1
   ```

2. Create and activate virtual environment
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask server
   ```bash
   python app.py
   ```

2. Open in browser: http://127.0.0.1:5000

## Quick Login Credentials

### Admin Access
- Username: admin
- Password: admin

### Sample Doctor Account
- Username: doctor1
- Password: doctor1

### Sample Patient Account
- Username: patient1
- Password: patient1

## Project Structure
```
├── app.py              # Main application file
├── forms.py            # Flask-WTF form definitions
├── models.py           # SQLAlchemy database models
├── utils.py            # Utility functions
├── requirements.txt    # Project dependencies
├── static/            
│   └── style.css      # Custom CSS styles
└── templates/          # Jinja2 HTML templates
    ├── admin_dashboard.html
    ├── doctor_dashboard.html
    ├── patient_dashboard.html
    └── ...
```

## Dependencies
- Flask 2.3.3
- Werkzeug 2.3.7
- Flask-SQLAlchemy 3.0.5
- Flask-Login 0.6.2

## Development

### Setting Up Development Environment
1. Fork the repository
2. Create a new branch for your feature
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Push to your fork and submit a pull request

### Coding Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Update documentation for significant changes
