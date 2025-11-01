# Deployment Guide

This guide covers deploying the EduNova Django project to production.

## Prerequisites

- Python 3.11+
- PostgreSQL database
- Environment variables configured

## Environment Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Configure your `.env` file with production values:
   ```env
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   ENVIRONMENT=production
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   ```

## Database Setup

1. Create PostgreSQL database:
   ```bash
   createdb your_db_name
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

## Static Files

Collect static files for production:
```bash
python manage.py collectstatic --noinput
```

## Running with Gunicorn

### Development
```bash
gunicorn edunova.wsgi:application --reload
```

### Production
```bash
gunicorn edunova.wsgi:application --config gunicorn_config.py
```

Or use the Procfile:
```bash
gunicorn edunova.wsgi:application --config gunicorn_config.py
```

## Deployment Platforms

### Render

1. Create a new Web Service
2. Connect your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn edunova.wsgi:application --config gunicorn_config.py`
5. Add environment variables from `.env`
6. Add PostgreSQL database as an addon

### Railway

1. Create a new project
2. Add PostgreSQL service
3. Deploy from Git repository
4. Railway will auto-detect the Procfile
5. Add environment variables in settings

### Heroku

1. Create Heroku app:
   ```bash
   heroku create your-app-name
   ```

2. Add PostgreSQL addon:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   # ... add other variables
   ```

4. Deploy:
   ```bash
   git push heroku main
   ```

5. Run migrations:
   ```bash
   heroku run python manage.py migrate
   ```

6. Collect static files:
   ```bash
   heroku run python manage.py collectstatic --noinput
   ```

## Health Check

Test the health check endpoint:
```bash
curl http://localhost:8000/api/health/
```

## API Documentation

Access Swagger UI at:
- `/api/docs/` - Swagger UI
- `/api/redoc/` - ReDoc
- `/api/schema/` - OpenAPI schema

## Security Checklist

- [ ] `SECRET_KEY` is set and secure
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] `CSRF_TRUSTED_ORIGINS` includes your frontend domain
- [ ] SSL/TLS is enabled (`SECURE_SSL_REDIRECT=True`)
- [ ] Database credentials are secure
- [ ] Static files are served via CDN or web server
- [ ] Media files are secured (not publicly accessible if sensitive)

## Monitoring

- Health check endpoint: `/api/health/`
- Detailed health check: `/api/health/detailed/`
- Logs are written to `logs/` directory
- Error logs: `logs/django_errors.log`

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists and user has permissions

### Static Files Not Loading
- Run `python manage.py collectstatic --noinput`
- Verify `STATIC_ROOT` is set correctly
- Check web server configuration for static file serving

### 500 Errors
- Check `logs/django_errors.log`
- Verify `DEBUG=False` in production (don't expose errors to users)
- Review environment variables

### CORS Issues
- Verify `CSRF_TRUSTED_ORIGINS` includes frontend domain
- Check `CORS_ALLOW_ALL_ORIGINS` setting (should be `False` in production)
- Configure `CORS_ALLOWED_ORIGINS` with specific domains

