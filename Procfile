web: gunicorn edunova.wsgi:application --config gunicorn_config.py
release: python manage.py migrate
worker: celery -A edunova worker -l info

