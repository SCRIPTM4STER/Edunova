web: gunicorn edunova.wsgi:application --bind 0.0.0.0:$PORT --workers 3
release: python manage.py migrate
worker: celery -A edunova worker -l info

