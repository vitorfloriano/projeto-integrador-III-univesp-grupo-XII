from .base import *

# Development settings
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# CSRF settings - adicionar essa configuração
CSRF_TRUSTED_ORIGINS = ['https://localhost:8000', 'http://localhost:8000', 'http://127.0.0.1:8000']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Development database - SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Simplified password validation for development
AUTH_PASSWORD_VALIDATORS = []

# Additional development-specific settings
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Security settings - relaxed for development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
