from pathlib import Path
import os
from datetime import timedelta
from dotenv import dotenv_values

# ======================================================
# ENVIRONMENT CONFIG
# ======================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file (if exists), then from OS environment
# This allows the .env file to work locally while Railway environment variables work in production
env_file = dotenv_values(".env") or {}
env_vars = {**env_file, **os.environ}

SECRET_KEY = env_vars.get("SECRET_KEY", "django-insecure-dev-key")
DEBUG = env_vars.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = [host.strip() for host in env_vars.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")]

ENVIRONMENT = env_vars.get("ENVIRONMENT", "development")
POSTGRES_LOCALLY = env_vars.get("POSTGRES_LOCALLY", "False") == "True"

# CSRF Trusted Origins - Required for secure frontend-to-backend communication
CSRF_TRUSTED_ORIGINS = [
    origin.strip() 
    for origin in env_vars.get("CSRF_TRUSTED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    if origin.strip()
]

# ======================================================
# APPLICATIONS
# ======================================================

INSTALLED_APPS = [
    # Admin UI
    'jazzmin',

    # Core Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Custom apps
    'accounts',
    'notebook',
    'PDFs',
    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'corsheaders',
    'drf_spectacular',
    'django_filters',
    'django_extensions',
    'health_check',
    'health_check.db',
    'health_check.storage',
]

# ======================================================
# MIDDLEWARE
# ======================================================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'edunova.middleware.CustomErrorMiddleware',
]


ROOT_URLCONF = 'edunova.urls'

# ======================================================
# TEMPLATES
# ======================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'edunova.wsgi.application'


# ======================================================
# DATABASE
# ======================================================

# Determine which database to use
# PostgreSQL is used if:
# 1. POSTGRES_LOCALLY is True
# 2. ENVIRONMENT is production
# 3. DB_HOST is set (Railway and other platforms set this automatically)
use_postgres = POSTGRES_LOCALLY or ENVIRONMENT == 'production' or env_vars.get("DB_HOST")

if use_postgres:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env_vars.get("DB_NAME", "django_quickstart"),
            'USER': env_vars.get("DB_USER", "postgres"),
            'PASSWORD': env_vars.get("DB_PASSWORD", "password"),
            'HOST': env_vars.get("DB_HOST", "localhost"),
            'PORT': env_vars.get("DB_PORT", "5432"),
        }
    }
else:
    # SQLite fallback for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ======================================================
# AUTHENTICATION
# ======================================================

AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    }
}

# ======================================================
# REST FRAMEWORK / JWT
# ======================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'edunova.exceptions.custom_exception_handler',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=50),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
}

# ======================================================
# API DOCUMENTATION
# ======================================================

SPECTACULAR_SETTINGS = {
    'TITLE': 'EduNova API',
    'DESCRIPTION': 'A comprehensive education platform API built with Django REST Framework',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/v1/',
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    'SERVE_AUTHENTICATION': None,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'displayOperationId': False,
        'defaultModelsExpandDepth': 2,
        'defaultModelExpandDepth': 2,
    },
    'SCHEMA_PATH_PREFIX_TRIM': True,
}

# ======================================================
# INTERNATIONALIZATION
# ======================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ======================================================
# STATIC & MEDIA
# ======================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
TEMP_UPLOAD_DIR = os.path.join(MEDIA_ROOT, "temp")
os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================================================
# EMAIL CONFIGURATION
# ======================================================

if ENVIRONMENT == 'production' or POSTGRES_LOCALLY:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env_vars.get('EMAIL_ADDRESS', '')
    EMAIL_HOST_PASSWORD = env_vars.get('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = f'Awesome <{EMAIL_HOST_USER}>'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ======================================================
# SECURITY
# ======================================================

SECURE_SSL_REDIRECT = env_vars.get("SECURE_SSL_REDIRECT", "False") == "True"
SESSION_COOKIE_SECURE = env_vars.get("SESSION_COOKIE_SECURE", "False") == "True"
CSRF_COOKIE_SECURE = env_vars.get("CSRF_COOKIE_SECURE", "False") == "True"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Media and Static Files Security
# Prevent direct access to sensitive files
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB

# ======================================================
# CORS
# ======================================================

# CORS Configuration
# In production, set CORS_ALLOW_ALL_ORIGINS=False and configure CORS_ALLOWED_ORIGINS
CORS_ALLOW_ALL_ORIGINS = env_vars.get("CORS_ALLOW_ALL_ORIGINS", "True") == "True"
if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = [
        origin.strip() 
        for origin in env_vars.get("CORS_ALLOWED_ORIGINS", "").split(",")
        if origin.strip()
    ]

# ======================================================
# DJANGO CACHE BACKEND (IN-MEMORY)
# ======================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# ======================================================
# LOGGING
# ======================================================

LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{'
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'django_errors.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'root': {
        'handlers': ['console', 'file', 'error_file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'edunova': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'accounts': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'notebook': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'PDFs': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}
