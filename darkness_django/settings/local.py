from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-dev-secret-key'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# For development, we use console email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable password validators for development to make testing easier
AUTH_PASSWORD_VALIDATORS = []
