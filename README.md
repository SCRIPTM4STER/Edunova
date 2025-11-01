# EduNova - Education Platform API

A comprehensive Django REST Framework API for an education platform with notebooks, notes, and PDF management.

## Features

- **User Authentication**: JWT-based authentication with social login (Google)
- **Notebooks & Notes**: Organize notes in notebooks with rich content
- **PDF Management**: Upload, manage, and generate PDFs from notes
- **Admin Interface**: Customized Django admin with advanced filtering
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Health Checks**: Monitoring endpoints for server status
- **Production Ready**: Gunicorn configuration, logging, error handling

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd Project__Edu

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# At minimum, set SECRET_KEY
```

### 3. Database Setup

For development (SQLite - default):
```bash
python manage.py migrate
python manage.py createsuperuser
```

For production (PostgreSQL):
- Set `POSTGRES_LOCALLY=True` in `.env`
- Configure database credentials in `.env`
- Run migrations: `python manage.py migrate`

### 4. Run Development Server

```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - Register new user
- `POST /api/v1/auth/token/` - Get JWT token
- `POST /api/v1/auth/token/refresh/` - Refresh JWT token
- `POST /api/v1/auth/google/` - Google OAuth login

### Notebooks
- `GET /api/v1/notebook/notebooks/` - List notebooks
- `POST /api/v1/notebook/notebooks/` - Create notebook

### Notes
- `GET /api/v1/notebook/notes/` - List notes
- `POST /api/v1/notebook/notes/` - Create note
- `GET /api/v1/notebook/notes/<id>/` - Get note
- `PATCH /api/v1/notebook/notes/<id>/` - Update note
- `DELETE /api/v1/notebook/notes/<id>/` - Delete note
- `POST /api/v1/notebook/notes/<id>/generate-pdf/` - Generate PDF from note

### PDFs
- `GET /api/v1/pdf/` - List PDFs
- `POST /api/v1/pdf/upload/` - Upload PDF
- `GET /api/v1/pdf/<id>/` - Get PDF
- `PATCH /api/v1/pdf/<id>/` - Update PDF
- `DELETE /api/v1/pdf/<id>/` - Delete PDF
- `GET /api/v1/pdf/<id>/download/` - Download PDF

### Health & Documentation
- `GET /api/health/` - Health check
- `GET /api/health/detailed/` - Detailed health check
- `GET /api/docs/` - Swagger UI documentation
- `GET /api/redoc/` - ReDoc documentation

## Project Structure

```
Project__Edu/
├── accounts/          # User authentication & profiles
├── notebook/          # Notebooks and notes management
├── PDFs/             # PDF upload and management
├── edunova/          # Project settings & configuration
├── media/            # User-uploaded files
├── staticfiles/      # Collected static files
├── logs/             # Application logs
├── manage.py
├── requirements.txt
├── gunicorn_config.py
├── Procfile
└── .env.example
```

## Development

### Running Tests

```bash
python manage.py test
```

### Collecting Static Files

```bash
python manage.py collectstatic
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

Quick deployment commands:
```bash
# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn edunova.wsgi:application --config gunicorn_config.py
```

## Security

- JWT authentication for API access
- CSRF protection configured
- Secure file upload validation
- Environment-based configuration
- Database indexes for performance
- Custom error handling middleware

## Environment Variables

Key environment variables (see `.env.example`):

- `SECRET_KEY` - Django secret key (required)
- `DEBUG` - Debug mode (False in production)
- `ALLOWED_HOSTS` - Allowed hostnames
- `CSRF_TRUSTED_ORIGINS` - Trusted origins for CSRF
- Database credentials (if using PostgreSQL)
- Email configuration (for production)

## License

[Your License Here]

## Support

For issues and questions, please open an issue in the repository.

