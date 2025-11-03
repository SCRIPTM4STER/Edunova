#!/bin/bash
# Wait for DB to be ready
echo "Waiting for database..."
sleep 5  # simple wait, can be replaced with proper DB check

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files (optional, if using)
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn edunova.wsgi:application --bind 0.0.0.0:8000 --workers 3
