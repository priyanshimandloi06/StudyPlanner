# Study Planner & Tracker

Study Planner & Tracker is a Django-based web application designed to help students manage weekly study schedules, track daily progress, and monitor study consistency through measurable performance metrics.

The app enables users to define a recurring 7-day timetable, add study slots, log time spent on each subject, and review their weekly performance through an interactive dashboard and report page.

## Features

- Secure user authentication with signup, login, and logout
- Per-user data isolation for individual study plans
- Weekly timetable planning across 7-day cycles
- Subject-based study slot management
- Daily logging of study minutes or full completion status
- Browser-based timer for quick study tracking
- Progress metrics such as planned vs studied time and follow percentage
- Status classification for each slot: Done, Partial, Missed, or Pending
- Weekly analytics dashboard with Chart.js visualizations
- New-week cycle support with optional timetable duplication

## Tech Stack

- Python
- Django
- MySQL
- Bootstrap 5
- Chart.js

## Project Structure

```text
studyplanner/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── planner/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── stats.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── plan.html
│   ├── report.html
│   └── registration/
│       ├── login.html
│       └── signup.html
├── manage.py
├── requirements.txt
└── README.md
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+ installed
- MySQL Server installed and running locally
- A database created for the project
- Virtual environment support enabled

## Setup

1. Clone the repository

```bash
git clone https://github.com/priyanshimandloi06/StudyPlanner.git
cd StudyPlanner
```

2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure MySQL environment variables

Windows PowerShell:

```powershell
$env:DB_NAME = "studyplanner"
$env:DB_USER = "studyplanneruser"
$env:DB_PASSWORD = "StrongPassword123"
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "3306"
```

5. Create the MySQL database

```sql
CREATE DATABASE studyplanner CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

If you use a separate database user, grant privileges as needed:

```sql
CREATE USER 'studyplanneruser'@'localhost' IDENTIFIED BY 'StrongPassword123';
GRANT ALL PRIVILEGES ON studyplanner.* TO 'studyplanneruser'@'localhost';
FLUSH PRIVILEGES;
```

6. Run database migrations

```bash
python manage.py migrate
```

7. Start the development server

```bash
python manage.py runserver
```

Open the application in your browser at:

```text
http://127.0.0.1:8000
```

## Usage

1. Sign up for a new account or log in.
2. Create your weekly timetable by adding study slots for each day.
3. Log study time manually or use the built-in timer feature.
4. Mark a slot as fully completed when needed.
5. Visit the dashboard to review progress for the current day.
6. Open the weekly report to view performance analytics across the week.

## Testing

Run the Django test suite with:

```bash
python manage.py test
```

## Notes

This project is meant for personal study tracking and academic productivity. It can be extended with features such as:

- subject categories
- recurring goals
- exam calendars
- monthly analytics
- notifications and reminders

## Contributing

Contributions are welcome. If you want to improve the app, open a pull request with a clear description of the changes.
