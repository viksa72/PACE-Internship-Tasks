#  Resume Builder

A Django web application that enables HR teams and managers to manage employee profiles, projects, and generate professional PDF resumes with a single click.

---

##  Features

- **Employee Management** — Create, view, edit, and delete employee profiles (personal info, skills, education, certifications)
- **Project Management** — Maintain a central library of company projects with client and technology details
- **Employee–Project Mapping** — Assign employees to projects with custom roles, responsibilities, and durations
- **PDF Resume Generation** — Instantly generate a formatted, downloadable PDF resume for any employee
- **Dashboard with Metrics** — Overview of total employees, projects, and mappings
- **Live Search** — AJAX-powered instant search for finding employees by name or ID

---

##  Tech Stack

| Layer      | Technology                  |
|------------|-----------------------------|
| Backend    | Python 3, Django 6          |
| Database   | SQLite3 (default)           |
| PDF Gen    | ReportLab (via `pdf_generator.py`) |
| Frontend   | HTML5, CSS3, Vanilla JS     |

---

##  Project Structure

```
Project-Resume Builder/
├── manage.py               # Django management entry point
├── seed_db.py              # Script to populate the database with sample data
├── db.sqlite3              # SQLite database file (auto-generated)
│
├── resume_builder/         # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── resumes/                # Core Django app
│   ├── models.py           # Employee, Project, EmployeeProjectMapping models
│   ├── views.py            # All CRUD + PDF generation views
│   ├── forms.py            # Django ModelForms
│   ├── urls.py             # App-level URL routing
│   ├── pdf_generator.py    # ReportLab PDF generation logic
│   ├── admin.py            # Django admin registration
│   ├── tests.py            # Unit tests
│   ├── migrations/         # Database migration files
│   ├── templates/resumes/  # HTML templates
│   └── static/             # App-specific static files (CSS, JS)
│
└── static/                 # Project-wide static files
```

---

##  Getting Started

### Prerequisites

- Python 3.10+
- pip

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd "Project-Resume Builder"
```

### 2. Create & Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django reportlab
```

> If a `requirements.txt` is present, use:
> ```bash
> pip install -r requirements.txt
> ```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. (Optional) Seed the Database with Sample Data

```bash
python seed_db.py
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to **http://127.0.0.1:8000/**

---

##  Data Models

### `Employee`
| Field                | Type        | Description                              |
|----------------------|-------------|------------------------------------------|
| `employee_id`        | CharField   | Unique employee identifier               |
| `name`               | CharField   | Full name                                |
| `designation`        | CharField   | Job title                                |
| `professional_summary` | TextField | Brief bio/summary                        |
| `email`              | EmailField  | Contact email                            |
| `phone`              | CharField   | Contact number                           |
| `address`            | TextField   | Office/home address (optional)           |
| `technical_skills`   | JSONField   | Categorised skills dict                  |
| `education`          | JSONField   | List of education records                |
| `certifications`     | JSONField   | List of certification records            |

### `Project`
| Field               | Type      | Description                          |
|---------------------|-----------|--------------------------------------|
| `name`              | CharField | Project name                         |
| `description`       | TextField | Project overview                     |
| `technologies_used` | CharField | Comma-separated list of technologies |
| `client`            | CharField | Client name (optional)               |
| `duration`          | CharField | e.g. "3 Months" or "Jan–Apr 2024"    |

### `EmployeeProjectMapping`
| Field                    | Type          | Description                           |
|--------------------------|---------------|---------------------------------------|
| `employee`               | FK→Employee   | Employee being mapped                 |
| `project`                | FK→Project    | Project being mapped                  |
| `role_and_responsibilities` | TextField  | Bullet-point roles (one per line)     |
| `duration`               | CharField     | Employee-specific duration override   |
| `client`                 | CharField     | Employee-specific client override     |
| `order`                  | IntegerField  | Display order in resume               |

---

##  Running Tests

```bash
python manage.py test resumes
```

---

##  Configuration

Key settings are in [`resume_builder/settings.py`](resume_builder/settings.py):

- **`SECRET_KEY`** — Replace with a secure key before deploying to production
- **`DEBUG`** — Set to `False` in production
- **`ALLOWED_HOSTS`** — Add your domain/IP for production deployments
- **`DATABASES`** — Defaults to SQLite; can be swapped for PostgreSQL or MySQL
- **`MEDIA_ROOT`** / **`MEDIA_URL`** — For uploaded media files

---
