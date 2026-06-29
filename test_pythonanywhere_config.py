#!/usr/bin/env python
"""
Test script to verify PythonAnywhere deployment configuration
"""
import os
import sys

# Test 1: Verify WSGI path configuration
print("=" * 60)
print("TEST 1: WSGI Configuration")
print("=" * 60)

wsgi_path = 'darkness_django/wsgi.py'
with open(wsgi_path, 'r') as f:
    wsgi_content = f.read()

if 'darkness_django.settings' in wsgi_content:
    print("✓ WSGI file has correct settings module path")
else:
    print("✗ WSGI file has incorrect settings module path")
    sys.exit(1)

if 'project_home' in wsgi_content:
    print("✓ WSGI file has project_home configuration")
else:
    print("✗ WSGI file missing project_home configuration")
    sys.exit(1)

# Test 2: Verify production settings
print("\n" + "=" * 60)
print("TEST 2: Production Settings")
print("=" * 60)

prod_path = 'darkness_django/settings/production.py'
with open(prod_path, 'r') as f:
    prod_content = f.read()

if 'DEBUG = False' in prod_content:
    print("✓ Production DEBUG is set to False")
else:
    print("✗ Production DEBUG not set correctly")
    sys.exit(1)

if 'SECRET_KEY' in prod_content and 'os.environ.get' in prod_content:
    print("✓ SECRET_KEY reads from environment variable")
else:
    print("✗ SECRET_KEY not properly configured")
    sys.exit(1)

if 'ALLOWED_HOSTS' in prod_content and 'os.environ.get' in prod_content:
    print("✓ ALLOWED_HOSTS reads from environment variable")
else:
    print("✗ ALLOWED_HOSTS not properly configured")
    sys.exit(1)

if 'STATIC_ROOT' in prod_content:
    print("✓ STATIC_ROOT is configured")
else:
    print("✗ STATIC_ROOT not configured")
    sys.exit(1)

# Test 3: Verify base settings use django-environ
print("\n" + "=" * 60)
print("TEST 3: Base Settings (django-environ)")
print("=" * 60)

base_path = 'darkness_django/settings/base.py'
with open(base_path, 'r') as f:
    base_content = f.read()

if 'import environ' in base_content:
    print("✓ django-environ is imported")
else:
    print("✗ django-environ not imported")
    sys.exit(1)

if "env = environ.Env(" in base_content:
    print("✓ environ.Env() is initialized")
else:
    print("✗ environ.Env() not initialized")
    sys.exit(1)

if 'env.db(' in base_content:
    print("✓ Database configuration uses environ")
else:
    print("✗ Database configuration doesn't use environ")
    sys.exit(1)

# Test 4: Verify requirements
print("\n" + "=" * 60)
print("TEST 4: Requirements")
print("=" * 60)

with open('requirements/prod.txt', 'r') as f:
    prod_reqs = f.read()

if 'django-environ' in prod_reqs or 'base.txt' in prod_reqs:
    print("✓ django-environ in production requirements")
else:
    print("✗ django-environ missing from production requirements")
    sys.exit(1)

if 'gunicorn' in prod_reqs:
    print("✓ gunicorn in production requirements")
else:
    print("✗ gunicorn missing from production requirements")
    sys.exit(1)

if 'whitenoise' in prod_reqs:
    print("✓ whitenoise in production requirements")
else:
    print("✗ whitenoise missing from production requirements")
    sys.exit(1)

# Test 5: Verify .gitignore
print("\n" + "=" * 60)
print("TEST 5: .gitignore")
print("=" * 60)

with open('.gitignore', 'r') as f:
    gitignore = f.read()

if 'db.sqlite3' in gitignore or '*.sqlite3' in gitignore:
    print("✓ Database files are ignored")
else:
    print("✗ Database files not in .gitignore")
    sys.exit(1)

if 'staticfiles' in gitignore:
    print("✓ staticfiles directory is ignored")
else:
    print("✗ staticfiles directory not in .gitignore")
    sys.exit(1)

if '.env' in gitignore:
    print("✓ .env file is ignored")
else:
    print("✗ .env file not in .gitignore")
    sys.exit(1)

# Test 6: Verify deployment documentation
print("\n" + "=" * 60)
print("TEST 6: Deployment Documentation")
print("=" * 60)

if os.path.exists('DEPLOY_PYTHONANYWHERE.md'):
    print("✓ DEPLOY_PYTHONANYWHERE.md exists")
    with open('DEPLOY_PYTHONANYWHERE.md', 'r') as f:
        deploy_doc = f.read()

    if 'WSGI' in deploy_doc:
        print("✓ Deployment doc includes WSGI configuration")
    else:
        print("✗ Deployment doc missing WSGI configuration")
        sys.exit(1)

    if 'static' in deploy_doc.lower():
        print("✓ Deployment doc includes static files configuration")
    else:
        print("✗ Deployment doc missing static files configuration")
        sys.exit(1)
else:
    print("✗ DEPLOY_PYTHONANYWHERE.md not found")
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("✓ All configuration tests passed!")
print("\nYour Django app is ready for PythonAnywhere deployment.")
print("\nNext steps:")
print("1. Push code to GitHub")
print("2. Follow DEPLOY_PYTHONANYWHERE.md for deployment")
print("3. Set DJANGO_SECRET_KEY and DJANGO_ALLOWED_HOSTS environment variables")
print("4. Configure static files in PythonAnywhere Web tab")
