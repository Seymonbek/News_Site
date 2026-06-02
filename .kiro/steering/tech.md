# Tech Stack

## Framework & Language
- Python 3.11+
- Django 5.0.4

## Key Libraries
| Package | Version | Purpose |
|---|---|---|
| django-modeltranslation | 0.18.11 | uz/ru/en field translations |
| django-hitcount | 1.3.5 | Article view counting |
| whitenoise | 6.6.0 | Static files in production |
| python-decouple | 3.8 | .env config management |
| gunicorn | 22.0.0 | Production WSGI server |
| pillow | 10.3.0 | Image handling |
| psycopg2-binary | 2.9.x | PostgreSQL driver (optional) |

## Database
- Development: SQLite (`db.sqlite3`)
- Production: SQLite (small sites) or PostgreSQL via `.env`

## Frontend
- Pure CSS (`static/css/news.css`) — custom news site design
- No CSS framework (Bootstrap removed)
- Google Fonts: Inter (body)
- Font Awesome 5.15.4 (icons)
- jQuery 3.6.0 (back-to-top only)
- CSS Variables for theming

## Common Commands
```bash
# Development server
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Collect static (production)
python manage.py collectstatic --noinput

# Compile translations
python manage.py compilemessages

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

## Virtual Environment
```bash
source vrenv/bin/activate   # Linux/Mac
vrenv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Environment Variables (.env)
```
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DB_ENGINE=django.db.backends.sqlite3
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
```
