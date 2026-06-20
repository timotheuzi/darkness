# PythonAnywhere Deployment Guide

This guide will help you deploy the Darkness MUD application to PythonAnywhere.

## Prerequisites

- A PythonAnywhere account (free or paid)
- Your code pushed to a Git repository (GitHub, GitLab, etc.)

## Step 1: Upload Your Code

### Option A: Using Git (Recommended)

1. Log in to PythonAnywhere
2. Open a Bash console
3. Clone your repository:
   ```bash
   cd ~
   git clone https://github.com/YOUR_USERNAME/darknesses.git
   cd darknesses
   ```

### Option B: Using the Files Tab

1. Go to the **Files** tab in PythonAnywhere
2. Navigate to your home directory
3. Upload all project files

## Step 2: Set Up Virtual Environment

In your Bash console:

```bash
cd ~/darknesses
python -m venv venv
source venv/bin/activate
pip install -r requirements/prod.txt
```

## Step 3: Configure Environment Variables

Create a `.env` file in your project directory:

```bash
cd ~/darknesses
nano .env
```

Add the following (replace with your actual values):

```env
# Django Settings
DJANGO_SECRET_KEY=your-very-secure-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com

# Database (optional - PythonAnywhere provides free MySQL)
# DATABASE_URL=mysql://username:password@username.mysql.pythonanywhere.com/username$darkness
```

**Important**: Generate a secure secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 4: Set Up Database

### Option A: Use SQLite (Simple, but not recommended for production)

```bash
make deploy-init
```

Or manually:
```bash
python manage.py makemigrations --settings=darkness_django.settings.production
python manage.py migrate --settings=darkness_django.settings.production
python manage.py init_game --settings=darkness_django.settings.production
```

### Option B: Use MySQL (Recommended for PythonAnywhere)

1. Go to the **Databases** tab in PythonAnywhere
2. Set a password for your MySQL database
3. Note your database credentials:
   - Username: your PythonAnywhere username
   - Password: the password you just set
   - Database name: `yourusername$darkness`
   - Host: `yourusername.mysql.pythonanywhere.com`

4. Update your `.env` file:
   ```env
   DATABASE_URL=mysql://username:password@username.mysql.pythonanywhere.com/username$darkness
   ```

5. Install MySQL client:
   ```bash
   pip install mysqlclient
   ```

6. Run migrations using the Makefile (recommended):
   ```bash
   make deploy-init
   ```
   
   Or manually:
   ```bash
   python manage.py makemigrations --settings=darkness_django.settings.production
   python manage.py migrate --settings=darkness_django.settings.production
   python manage.py init_game --settings=darkness_django.settings.production
   ```

## Step 5: Collect Static Files

```bash
python manage.py collectstatic --settings=darkness_django.settings.production --noinput
```

## Step 6: Configure Web App

### Using the Web Tab

1. Go to the **Web** tab in PythonAnywhere
2. Click **Add a new web app**
3. Choose your domain (e.g., `yourusername.pythonanywhere.com`)
4. Select **Manual configuration**
5. Choose **Python 3.11** (or latest available)

### Configure WSGI File

1. In the **Web** tab, find the **WSGI configuration file** section
2. Click on the link to edit your WSGI file
3. Replace the entire contents with:

```python
import os
import sys

# Add your project directory to the sys.path
project_home = '/home/darknesses/darknesses'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'darkness_django.settings.production'
os.environ['DJANGO_SECRET_KEY'] = 'your-very-secure-secret-key-here'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'darknesses.pythonanywhere.com'

# If using MySQL, also set:
# os.environ['DATABASE_URL'] = 'mysql://username:password@username.mysql.pythonanywhere.com/username$darkness'

# Activate virtual environment (Python 3.11+ compatible)
import sys, os, glob
venv_path = '/home/darknesses/darknesses/venv'
sp = glob.glob(os.path.join(venv_path, 'lib', 'python*', 'site-packages'))
if sp:
    sys.path.insert(0, sp[0])

# Serve Django via WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Important**: Replace `yourusername` with your actual PythonAnywhere username and update the secret key.

### Configure Static Files

In the **Web** tab, scroll to the **Static files** section:

1. **URL**: `/static/`
2. **Directory**: `/home/yourusername/darknesses/staticfiles`

Click **Add** to save.

### Configure Media Files (if needed)

If your app uses user-uploaded files:

1. **URL**: `/media/`
2. **Directory**: `/home/yourusername/darknesses/media`

## Step 7: Configure Environment Variables (Alternative Method)

Instead of hardcoding in WSGI, you can use PythonAnywhere's environment variables:

1. In the **Web** tab, find the **Environment** section
2. Add environment variables:
   - `DJANGO_SECRET_KEY`: your secret key
   - `DJANGO_ALLOWED_HOSTS`: your domain
   - `DATABASE_URL`: (if using MySQL)

## Step 8: Test Your Configuration

1. In the **Web** tab, click the **Reload** button
2. Visit `https://yourusername.pythonanywhere.com`
3. Check for any errors in the error log

## Step 9: Set Up Scheduled Tasks (Optional)

If your game needs periodic tasks:

1. Go to the **Tasks** tab
2. Set up scheduled tasks if needed

## Troubleshooting

### Common Issues

1. **Static files not loading**:
   - Ensure you ran `collectstatic`
   - Verify static files configuration in Web tab
   - Check that `STATIC_ROOT` is set correctly

2. **Database errors**:
   - Verify database credentials
   - Ensure MySQL client is installed if using MySQL
   - Check that migrations were run with correct settings

3. **Import errors**:
   - Verify virtual environment is activated in WSGI file
   - Check that all dependencies are installed
   - Ensure `sys.path` includes your project directory

4. **Permission errors**:
   - Ensure files have correct permissions
   - Check that the web user can read your files

### Checking Logs

- **Error log**: Available in the **Web** tab
- **Server log**: Available in the **Web** tab
- **Access log**: Available in the **Web** tab

## Security Notes

1. Never commit `.env` file to version control
2. Use strong, unique `DJANGO_SECRET_KEY`
3. Keep `DEBUG = False` in production
4. Use HTTPS (PythonAnywhere provides this automatically)
5. Regularly backup your database

## Maintenance

### Updating Your App

When you push new code:

```bash
cd ~/darknesses
git pull origin main
source venv/bin/activate
pip install -r requirements/prod.txt
make deploy-migrate
python manage.py collectstatic --settings=darkness_django.settings.production --noinput
```

Then click **Reload** in the **Web** tab.

### Database Backups

1. Go to the **Databases** tab
2. Set up automatic backups or export manually

## Free vs Paid Accounts

### Free Account Limitations
- Can only run one web app
- Limited to subdomain (yourusername.pythonanywhere.com)
- Must wake up manually after inactivity
- Limited CPU/bandwidth

### Paid Account Benefits
- Custom domains
- Always-on web apps
- More resources
- Multiple web apps

## Additional Resources

- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [PythonAnywhere Django Tutorial](https://help.pythonanywhere.com/pages/DeployingDjango/)