#!/usr/bin/env python

import os
import sys

# Add the site-packages of the chosen virtualenv to the path - Using Linux path conventions
site_packages = os.path.join(os.environ['HOME'], 'site', 'wwwroot', 'env', 'lib', 'python3.12', 'site-packages')
if os.path.exists(site_packages):
    sys.path.append(site_packages)

# Add the app's directory to the PYTHONPATH - Using Linux path conventions
sys.path.append(os.environ['HOME'] + "/site/wwwroot")

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings.prod'
os.environ.setdefault('DJANGO_ENV', 'prod')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()