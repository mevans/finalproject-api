"""
WSGI config for tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/qdeployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_module = "tracker.production" if 'PRODUCTION' in os.environ else 'tracker.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
