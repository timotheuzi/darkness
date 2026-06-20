# Darkness

A professional CyberMUD (Multi-User Dungeon) built with Django.

## Project Structure

- `darkness_django/`: Project configuration and settings.
- `game/`: Main application logic, models, and game engine.
- `templates/`: HTML templates for the terminal interface.
- `static/`: Static assets (CSS, JS, Images).

## Quick Start

1. **Install Dependencies**:
   ```bash
   make setup
   ```

2. **Initialize the Database**:
   ```bash
   make migrate
   ```

3. **Generate the World**:
   ```bash
   make init
   ```

4. **Run the Server**:
   ```bash
   make run
   ```

## Development

- **Testing**: `make test`
- **Linting**: `make lint`
- **Cleaning Cache**: `make clean`

## Deployment

See [DEPLOY_PYTHONANYWHERE.md](DEPLOY_PYTHONANYWHERE.md) for detailed instructions on deploying to PythonAnywhere.

Quick deployment steps:
1. Push code to GitHub
2. Clone on PythonAnywhere
3. Set up virtual environment: `python -m venv venv && source venv/bin/activate && pip install -r requirements/prod.txt`
4. Configure `.env` file with production settings
5. Initialize database: `make deploy-init`
6. Collect static files: `python manage.py collectstatic --settings=darkness_django.settings.production --noinput`
7. Configure WSGI file in PythonAnywhere Web tab
8. Reload web app
