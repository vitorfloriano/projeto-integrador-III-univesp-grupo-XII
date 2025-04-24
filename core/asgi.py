"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Set the appropriate environment based on Azure detection
if 'WEBSITE_HOSTNAME' in os.environ:
    os.environ.setdefault('DJANGO_ENV', 'prod')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.prod')
else:
    os.environ.setdefault('DJANGO_ENV', 'dev')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')

application = get_asgi_application()
