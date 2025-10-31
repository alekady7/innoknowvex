"""
Django settings for innoknowvex_site project.

Adapted to work in both development (DEBUG=True) and production (DEBUG=False, e.g. Render).
"""

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY / ENVIRONMENT ---------------------------------------------------
# Use environment variables for production secrets. Fallback to dev-safe values.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-key-change-me')
# Set DJANGO_DEBUG env var to 'False' on Render / production
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Allows controlling hosts from env (comma/space separated)

# ALLOWED_HOSTS: accept comma-separated list from env var, fallback to localhost
_allowed = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
if _allowed:
    # allow "example.com,sub.example.com" or "example.com sub.example.com"
    # normalize by splitting on comma and stripping whitespace
    ALLOWED_HOSTS = [h.strip() for h in _allowed.replace(',', ' ').split() if h.strip()]
else:
    ALLOWED_HOSTS = ['innoknowvex.onrender.com', 'localhost', '127.0.0.1']

# When behind a proxy (Render, etc.) allow Django to detect HTTPS via X-Forwarded-Proto
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# --- APPLICATIONS ------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lms',
    'accounts',
]

# --- MIDDLEWARE --------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise should be directly after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'innoknowvex_site.urls'

# --- TEMPLATES ---------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'lms' / 'templates' ],   # your custom templates dir
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

WSGI_APPLICATION = 'innoknowvex_site.wsgi.application'

# --- DATABASE (default sqlite; override using DATABASE_URL in production) ----
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

# --- AUTH / VALIDATION ------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# --- INTERNATIONALIZATION ---------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'   # keep local timezone as project expects
USE_I18N = True
USE_TZ = True

# --- LOGIN REDIRECTS --------------------------------------------------------
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# --- STATIC FILES -----------------------------------------------------------
# URL path where static files are served from
STATIC_URL = '/static/'

# Local static files (development)
STATICFILES_DIRS = [ BASE_DIR / 'lms' / 'static' ]

# Production: where `collectstatic` will gather all static files.
# Use a single folder named 'staticfiles' (Render convention), but Path object is fine.
if not DEBUG:
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    # Use WhiteNoise's storage backend to serve compressed files and hashed filenames.
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    # Development: don't set STATIC_ROOT typically; collectstatic not required.
    STATIC_ROOT = BASE_DIR / 'staticfiles'    # safe to keep defined for local collectstatic tests.

# --- DEFAULT AUTO FIELD -----------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
