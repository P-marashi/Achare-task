#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "Collect static files"
python manage.py collectstatic --clear --noinput
python manage.py collectstatic --noinput

# Start server
echo "--> Starting web process"
gunicorn --reload --timeout=30 --workers=10 --bind 0.0.0.0:8010 config.wsgi:application
