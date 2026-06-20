"""
WSGI config for darkness_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# We set the default settings module, but it can be overridden by environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'darkness_django.settings.local')

application = get_wsgi_application()
