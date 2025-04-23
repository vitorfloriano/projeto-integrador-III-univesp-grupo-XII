"""
Configurações específicas para o ambiente de produção no Azure App Service
Este arquivo sobrescreve algumas configurações do settings.py padrão
"""

import os
from .settings import *

# Configurações de segurança
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    'autoitaapp.azurewebsites.net',
    os.environ.get('WEBSITE_HOSTNAME', '')
]

# Configuração de banco de dados para PostgreSQL (se configurado)
if os.environ.get('DATABASE_ENGINE') == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DATABASE_NAME'),
            'USER': os.environ.get('DATABASE_USER'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
            'HOST': os.environ.get('DATABASE_HOST'),
            'PORT': os.environ.get('DATABASE_PORT', '5432'),
        }
    }

# Configuração de arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Middleware de segurança adicionais
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para servir arquivos estáticos
] + MIDDLEWARE

# Configuração do WhiteNoise para arquivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuração para HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Proteção CSRF e XSS
CSRF_TRUSTED_ORIGINS = [
    'https://autoitaapp.azurewebsites.net',
    f'https://{os.environ.get("WEBSITE_HOSTNAME", "")}',
]

# Logging aprimorado para o Azure
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}