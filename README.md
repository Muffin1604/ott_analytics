
# OTT Analytics - Django Project (SQLite)

This is a ready-to-run Django project that implements a simple analytics dashboard for an OTT platform.
It uses SQLite for storage and includes a management command to seed sample data.

## What's included
- Django project: `ott_analytics/`
- App: `analytics/` with models: User, Video, WatchSession
- Templates with Chart.js visualizations: general, user, and video analytics
- Management command `seed_data` to generate sample data using Faker
- `db.sqlite3` is not included (you will create it via migrations)

## Setup (local)
```bash
# create venv and activate (example for Unix/macOS)
python -m venv venv
source venv/bin/activate

# install deps
pip install -r requirements.txt

# apply migrations
python manage.py migrate

# create superuser (optional, to access admin)
python manage.py createsuperuser

# seed sample data
python manage.py seed_data

# run server
python manage.py runserver
```
Open dashboards:
- General: http://127.0.0.1:8000/dashboard/general/
- Users:   http://127.0.0.1:8000/dashboard/users/
- Videos:  http://127.0.0.1:8000/dashboard/videos/

## Notes
- Charts use Chart.js CDN.
- SQLite is used for simplicity. For production, switch to Postgres/MySQL.
- The seed command creates ~10 users, 20 videos, 150 watch sessions.
