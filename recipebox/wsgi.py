"""
WSGI config for recipebox project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use production settings if DB_PASSWORD is set, otherwise local
if 'DB_PASSWORD' in os.environ:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipebox.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipebox.settings.local')

application = get_wsgi_application()
