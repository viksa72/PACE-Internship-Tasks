# LearnHub — Online Learning Platform

LearnHub is a full-featured Django web application that allows teachers to create and sell courses, and students to purchase and learn from them. 

## Features
- **Custom Authentication:** Email-based login with a secure 2-Factor Authentication (OTP) sent to the user's email.
- **User Roles:** Separate experiences for Students and Teachers.
- **Course Management:** Teachers have a dedicated dashboard to create courses, topics, and lessons (supporting YouTube embeds and rich text).
- **Payment Gateway:** Real PayPal Sandbox integration for course purchases.
- **Notifications system:** Automated emails via Django Signals when a new lesson is added or a teacher publishes a new course.
- **Modern UI:** Built with Bootstrap 5 featuring a custom dark theme, glassmorphism, and responsive layouts.

## Tech Stack
- **Backend:** Python 3.x, Django 5.x
- **Database:** SQLite (Development)
- **Frontend:** HTML5, Vanilla CSS, JS, Bootstrap 5
- **Payments:** PayPal REST SDK
- **Environment:** python-dotenv

---

## Local Setup Instructions

### 1. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a file named `.env` in the root folder (next to `manage.py`) and configure the following:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Email Configuration (for OTP and Notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-google-app-password
DEFAULT_FROM_EMAIL=LearnHub <noreply@learnhub.com>

# PayPal Sandbox Credentials
PAYPAL_CLIENT_ID=your-paypal-sandbox-client-id
PAYPAL_CLIENT_SECRET=your-paypal-sandbox-client-secret
PAYPAL_MODE=sandbox
```
*(If you do not want real emails to be sent during testing, change `EMAIL_BACKEND` to `django.core.mail.backends.console.EmailBackend`)*

### 3. Setup Database
Apply the database migrations:
```bash
python manage.py migrate
```

### 4. Create an Admin Account
Create a superuser to access the Django backend:
```bash
python manage.py createsuperuser
```

### 5. Run the Server
Start the development server:
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser. To add course categories, visit `http://127.0.0.1:8000/admin/`.
