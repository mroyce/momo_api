"""
WSGI config for momo_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


# Get whether we are in development, staging, or production
stage = os.environ.get('STAGE', 'development')

# Point to the settings file
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "momo_api.settings")

# This application object is used by any WSGI server configured to use this
# file.  This includes Django's development server, if the WSGI_APPLICATION
# setting points here
application = get_wsgi_application()
