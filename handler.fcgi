#!/usr/bin/env python

import os
import sys

# Add the site-packages of the chosen virtualenv to the path
site_packages = os.path.join(os.environ['HOME'], 'site', 'wwwroot', 'env', 'Lib', 'site-packages')
if os.path.exists(site_packages):
    sys.path.append(site_packages)

# Add the app's directory to the PYTHONPATH
sys.path.append(os.environ['HOME'] + "/site/wwwroot")

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings.prod'
os.environ.setdefault('DJANGO_ENV', 'prod')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()