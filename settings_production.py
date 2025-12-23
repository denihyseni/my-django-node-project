"""
PRODUCTION SETTINGS FOR PYTHONANYWHERE DEPLOYMENT
==================================================

This is a comprehensive Django settings file optimized for PythonAnywhere deployment.
It includes:
- Environment variable support for sensitive configuration
- Static file serving with WhiteNoise
- Security hardening for production
- JWT token authentication
- Session security with timeouts
- CORS and CSRF protection
- Database configuration for SQLite (dev) or PostgreSQL (prod)
- Logging configuration
- Email configuration (optional)

USAGE:
------
1. Copy this file to: project/settings_production.py
2. Update PythonAnywhere WSGI config to use: settings.settings_production
3. Set environment variables on PythonAnywhere (Web > Environment variables)
4. Ensure .env file is NOT in version control (add to .gitignore)
5. Run: python manage.py collectstatic --noinput (on PythonAnywhere)
"""

import os
from pathlib import Path
from datetime import timedelta

# ============================================================================
# ENVIRONMENT VARIABLES & DEBUG MODE
# ============================================================================

# Load environment variables from .env file (if it exists)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# DEBUG SETTING - CRITICAL FOR PRODUCTION
# Set to False on PythonAnywhere
# On PythonAnywhere web console: 
#   export DEBUG='False'
#   or set in Environment variables section
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

# ============================================================================
# SECURITY - SECRET KEY
# ============================================================================

# SECRET KEY should NEVER be committed to version control
# Generate a new one: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# On PythonAnywhere, set via Environment variables section
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-change-me-on-pythonanywhere-DO-NOT-USE-IN-PRODUCTION'
)

if not DEBUG and SECRET_KEY.startswith('django-insecure-'):
    raise ValueError(
        "SECRET_KEY not set properly for production! "
        "Set SECRET_KEY environment variable on PythonAnywhere."
    )

# ============================================================================
# ALLOWED HOSTS & DOMAIN CONFIGURATION
# ============================================================================

# PythonAnywhere domains
# Format: yourusername.pythonanywhere.com
# Also add your custom domain if you have one
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,yourusername.pythonanywhere.com'
).split(',')

# Clean up whitespace
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS]

# ============================================================================
# PROJECT PATHS
# ============================================================================

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Project root (where manage.py is located)
PROJECT_ROOT = BASE_DIR

# ============================================================================
# INSTALLED APPS
# ============================================================================

INSTALLED_APPS = [
    # Django admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    
    # Your apps
    'app',
    'university',
]

# ============================================================================
# MIDDLEWARE
# ============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    # WhiteNoise must come AFTER SecurityMiddleware for optimal compression
    # WhiteNoise serves static files efficiently in production
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # CORS must come before CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================================================
# ROOT URLCONF & TEMPLATES
# ============================================================================

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ============================================================================
# WSGI APPLICATION
# ============================================================================

WSGI_APPLICATION = 'project.wsgi.application'

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# DEFAULT: SQLite (works on PythonAnywhere)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# OPTIONAL: PostgreSQL (recommended for production)
# Uncomment to use PostgreSQL instead of SQLite
# On PythonAnywhere: Create PostgreSQL database from Dashboard > Databases
# Set DATABASE_URL environment variable: postgres://user:password@host/dbname
#
# DATABASE_URL = os.environ.get('DATABASE_URL', None)
# if DATABASE_URL:
#     import dj_database_url
#     DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}
#
# OR manually:
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'yourusername$database_name'),
#         'USER': os.environ.get('DB_USER', 'yourusername'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', ''),
#         'HOST': os.environ.get('DB_HOST', 'yourusername.mysql.pythonanywhere-services.com'),
#         'PORT': os.environ.get('DB_PORT', '3306'),
#         'ATOMIC_REQUESTS': True,
#     }
# }

# ============================================================================
# PASSWORD VALIDATION
# ============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================================================
# INTERNATIONALIZATION
# ============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ============================================================================
# STATIC FILES CONFIGURATION (Critical for PythonAnywhere)
# ============================================================================

# URL that handles the static files (e.g., /static/)
STATIC_URL = '/static/'

# Absolute filesystem path where collectstatic will collect static files for deployment
# On PythonAnywhere: /home/yourusername/mysite/static/
STATIC_ROOT = BASE_DIR / 'static'

# Additional locations of static files (development)
STATICFILES_DIRS = [
    BASE_DIR / 'frontend' / 'src',  # React app static files
]

# WhiteNoise static file storage with compression
# This compresses CSS/JS files and adds hashes for caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# WhiteNoise caching settings
WHITENOISE_MANIFEST_STRICT = False  # Don't break if some files are missing
WHITENOISE_MAX_AGE = 31536000  # 1 year (cache static files aggressively)

# ============================================================================
# MEDIA FILES CONFIGURATION
# ============================================================================

# URL that handles the media files (e.g., /media/)
MEDIA_URL = '/media/'

# Absolute filesystem path for uploaded media files
# On PythonAnywhere: /home/yourusername/mysite/media/
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================================
# DEFAULT PRIMARY KEY TYPE
# ============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# REST FRAMEWORK CONFIGURATION
# ============================================================================

REST_FRAMEWORK = {
    # Default authentication method for API views
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    # Default permission class (require authentication for all API views)
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    
    # Filtering and search
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# ============================================================================
# JWT AUTHENTICATION CONFIGURATION
# ============================================================================

SIMPLE_JWT = {
    # Access token validity (15 minutes)
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    
    # Refresh token validity (7 days)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    
    # Rotate refresh token on each use (security best practice)
    'ROTATE_REFRESH_TOKENS': True,
    
    # Blacklist tokens after rotation
    'BLACKLIST_AFTER_ROTATION': True,
    
    # Update last login on token obtain
    'UPDATE_LAST_LOGIN': False,
    
    # Algorithm for token signing
    'ALGORITHM': 'HS256',
    
    # Token claims (data included in token)
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    
    # Signing key (uses SECRET_KEY by default)
    # To use a different key: 'SIGNING_KEY': 'your-signing-key',
    
    # Authentication header prefix
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
}

# ============================================================================
# CORS CONFIGURATION (Frontend Communication)
# ============================================================================

# Allowed origins for frontend requests
# Format: https://domain.com
# On PythonAnywhere set: CORS_ALLOWED_ORIGINS='https://yourdomain.com,https://www.yourdomain.com'
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://localhost:8000'
).split(',')

CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS]

# Allow credentials (cookies) in cross-origin requests
CORS_ALLOW_CREDENTIALS = True

# Allow only specific HTTP methods for CORS
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# ============================================================================
# CSRF PROTECTION
# ============================================================================

# Trusted origins for CSRF (to allow these domains to make POST requests)
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost:3000,http://localhost:8000'
).split(',')

CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS]

# CSRF cookie settings for security
CSRF_COOKIE_SECURE = not DEBUG  # Only send over HTTPS in production
CSRF_COOKIE_HTTPONLY = False  # Frontend needs to read CSRF token
CSRF_COOKIE_SAMESITE = 'Strict'  # Prevent cross-site cookie sending

# ============================================================================
# SESSION CONFIGURATION (Security & Timeout)
# ============================================================================

# Session cookie settings
SESSION_COOKIE_AGE = 15 * 60  # 15 minutes (in seconds)
SESSION_COOKIE_SECURE = not DEBUG  # Only send over HTTPS in production
SESSION_COOKIE_HTTPONLY = True  # JavaScript cannot access session cookie
SESSION_COOKIE_SAMESITE = 'Strict'  # Prevent CSRF attacks
SESSION_SAVE_EVERY_REQUEST = True  # Update session expiry on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Delete session when browser closes
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Store sessions in database

# ============================================================================
# SECURITY HEADERS (Production Only)
# ============================================================================

if not DEBUG:
    # Force HTTPS in production
    SECURE_SSL_REDIRECT = True
    
    # Enable HSTS (HTTP Strict Transport Security)
    # Browsers will only access site over HTTPS
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Secure cookies in production
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Content Security Policy (optional - comment out if causing issues)
    # SECURE_CONTENT_SECURITY_POLICY = {
    #     'default-src': ("'self'",),
    #     'script-src': ("'self'", "'unsafe-inline'"),
    #     'style-src': ("'self'", "'unsafe-inline'"),
    # }
    
    # X-Frame-Options header
    X_FRAME_OPTIONS = 'DENY'

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'university': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ============================================================================
# EMAIL CONFIGURATION (Optional)
# ============================================================================

# Email backend for sending emails
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Print to console

# For real email on PythonAnywhere, uncomment and set environment variables:
#
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
# EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
# DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@university.com')

# ============================================================================
# PYTHONANYWHERE SPECIFIC SETTINGS
# ============================================================================

# On PythonAnywhere, collect static files to serve via web app:
# 1. SSH into PythonAnywhere console
# 2. Navigate to project directory
# 3. Run: python manage.py collectstatic --noinput
#
# This copies all static files to STATIC_ROOT directory,
# which is then served by PythonAnywhere's web app configuration.

# Database file location should be writable:
# - SQLite: /home/yourusername/mysite/db.sqlite3
# - Make sure /home/yourusername/mysite/static/ is configured in web app

# ============================================================================
# ENVIRONMENT VARIABLES REFERENCE
# ============================================================================

"""
Set these in PythonAnywhere > Web > Environment variables section:

Required:
---------
DEBUG=False                                    # Always False on production
SECRET_KEY=your-generated-secret-key-here     # Generate new key!
ALLOWED_HOSTS=yourusername.pythonanywhere.com,yourdomain.com

Frontend URLs:
--------------
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

Optional - PostgreSQL:
----------------------
DB_NAME=yourusername$database_name
DB_USER=yourusername
DB_PASSWORD=your-database-password
DB_HOST=yourusername.mysql.pythonanywhere-services.com
DB_PORT=3306

Optional - Email:
-----------------
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

Run on PythonAnywhere bash console to set environment variables:
$ export SECRET_KEY='your-key-here'
$ export DEBUG='False'
$ export ALLOWED_HOSTS='yourusername.pythonanywhere.com'
"""

# ============================================================================
# POST-DEPLOYMENT CHECKLIST
# ============================================================================

"""
After deploying to PythonAnywhere:

1. [ ] SSH into PythonAnywhere console
2. [ ] Activate virtual environment: workon mysite
3. [ ] Run migrations: python manage.py migrate
4. [ ] Create superuser: python manage.py createsuperuser
5. [ ] Collect static files: python manage.py collectstatic --noinput
6. [ ] Test database: python manage.py dbshell
7. [ ] Reload web app from Dashboard > Web tab
8. [ ] Test API: curl https://yourdomain.com/api/
9. [ ] Check logs: tail -f /var/log/yourusername.pythonanywhere.com.error.log
10. [ ] Verify HTTPS works: https://yourdomain.com
11. [ ] Test admin: https://yourdomain.com/admin/
12. [ ] Monitor performance using PythonAnywhere dashboard

Common Issues:
- Static files not loading? Run collectstatic and check STATIC_ROOT path in web app
- 500 errors? Check error logs in PythonAnywhere web app console
- Database errors? Ensure database is created and migrated
- CORS errors? Check CORS_ALLOWED_ORIGINS matches frontend URL
- JWT errors? Verify TOKEN_VERIFY is not set to False
"""
