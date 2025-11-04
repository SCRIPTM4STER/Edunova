## EduNova Backend (Django + DRF)

Production-ready REST API for notes, PDFs, and authentication.

### Prerequisites
- Python 3.11+
- pip / venv
- Optional: PostgreSQL 14+

### Environment Variables (.env)
Create a `.env` in project root (same folder as `manage.py`).

```
# Core
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
ENVIRONMENT=development

# Database (PostgreSQL only; otherwise SQLite is used automatically)
POSTGRES_LOCALLY=False
DB_NAME=edunova
DB_USER=postgres
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

# CORS/CSRF
CORS_ALLOW_ALL_ORIGINS=True
CSRF_TRUSTED_ORIGINS=http://localhost:3000, http://127.0.0.1:3000

# Email (production)
EMAIL_ADDRESS=
EMAIL_HOST_PASSWORD=

# Social Auth
GOOGLE_CLIENT_ID=your-google-oauth-client-id.apps.googleusercontent.com
```

If `POSTGRES_LOCALLY=True`, PostgreSQL will be used. Otherwise, SQLite is used for local development by default.

### Setup
```
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Database & Static
```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

### Run
```
python manage.py runserver
```

### Health & Docs
- Health: GET `/` or `/api/health/`
- Health (detailed): GET `/api/health/detailed/`
- OpenAPI schema: GET `/api/schema/`
- Swagger UI: GET `/api/docs/`
- Redoc: GET `/api/redoc/`

### Apps & Endpoints (v1)
- Accounts: `/api/v1/auth/`
  - JWT: `token/`, `token/refresh/`
  - Register: `register/`
  - Profile (current user): `profile/me/`
  - Change password: `change-password/` (requires reauth session flag)
  - Google auth: `google/` (requires `GOOGLE_CLIENT_ID`)
- Notebook: `/api/v1/notebook/`
  - `notebooks/`, `notes/`, `notes/<uuid:pk>/`, `notes/<uuid:pk>/generate-pdf/`
- PDFs: `/api/v1/pdf/`
  - `upload/`, `` (list) ``, `<uuid:pk>/`, `<uuid:pk>/download/`

### Development Notes
- Custom user model at `accounts.User` (email is the login field).
- Media served from `/media/` in DEBUG; ensure Pillow is installed.
- Static assets are in `staticfiles/` (collected via `collectstatic`).

### Common Commands
```
python manage.py check --deploy
python manage.py showmigrations
python manage.py createsuperuser
```

### Deployment
- Set `DEBUG=False` and proper `ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS`.
- Ensure PostgreSQL env vars are set.
- Run `collectstatic` and configure a static file server or CDN.


