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
