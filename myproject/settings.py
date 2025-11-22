import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from a local .env file, if present.
# This avoids adding extra dependencies while still supporting
# simple configuration for development and deployment.
env_path = BASE_DIR / ".env"
if env_path.exists():
    with env_path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)

# Quick-start development settings - unsuitable for production

SECRET_KEY = os.getenv("SECRET_KEY", "1234567890")
DEBUG = os.getenv("DEBUG", "True").lower() in {"1", "true", "yes", "on"}

ALLOWED_HOSTS = []

# Local government domain configuration
LGA_DOMAIN = os.getenv("LGA_DOMAIN", "murweh.qld.gov.au").lstrip("@")
BYPASS_LOGIN = os.getenv("BYPASS_LOGIN", "False").lower() in {"1", "true", "yes", "on"}

# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Core / project apps
    'myapp',
    'accounts',
    'fleet',
    'dwqmp',
    'journeys',
    'flood',
    'mqtt_broker',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# SQLite for development as requested

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

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


# Internationalization

LANGUAGE_CODE = 'en-au'
TIME_ZONE = 'Australia/Brisbane'
USE_I18N = True
USE_TZ = True


# Static files

STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)
STATIC_URL = 'static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Authentication / login

LOGIN_URL = 'accounts:request_link'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email settings
# For development this defaults to console backend so magic-link
# emails are printed to the console instead of being sent.

EMAIL_BACKEND = os.getenv(
    'DJANGO_EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend',
)
DEFAULT_FROM_EMAIL = os.getenv(
    'DJANGO_DEFAULT_FROM_EMAIL',
    f'no-reply@{LGA_DOMAIN}',
)


# Simple JWT-like settings for email login

EMAIL_LOGIN_JWT_EXPIRY_DAYS = int(os.getenv('EMAIL_LOGIN_JWT_EXPIRY_DAYS', '7'))


# MQTT broker defaults (used by mqtt_broker and flood apps)

MQTT_BROKER_HOST = os.getenv('MQTT_BROKER_HOST', '127.0.0.1')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', '1883'))

# Optional Google Maps key for floodway map
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
