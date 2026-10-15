# Study Planner & Tracker (Django)

A student creates a weekly timetable once and then follows it for 7 days.
The dashboard shows each day: how much was studied, planned vs studied, follow percentage, and slot status.
The weekly report includes a bar chart and day-by-day follow percentage.

## Run
    python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
    pip install -r requirements.txt

    # MySQL setup (example)
    set DB_NAME=studyplanner
    set DB_USER=root
    set DB_PASSWORD=your_password
    set DB_HOST=127.0.0.1
    set DB_PORT=3306

    python manage.py migrate
    python manage.py runserver
Open http://127.0.0.1:8000 -> Sign up -> Add slots in the timetable.

## Features
- Authentication (signup/login/logout) with per-user data
- Weekly timetable with a 7-day cycle (start date + 6 days)
- Daily logging: manual minutes, "Full done", or a browser timer
- Follow % = sum(min(studied, planned)) / planned
- Slot status: Done / Partial / Missed / Pending
- Weekly report with Chart.js and a "New week" timetable copy feature
- Tests: python manage.py test
