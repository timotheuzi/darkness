# Darkness BBS

A professional multi-user, terminal-style cyberpunk RPG (MUD) built with Django. Explore a procedurally generated grid, engage in tactical combat, and compete with other users in a gritty neon-soaked world.

## Project Structure

- `darkness_django/`: Project configuration, middleware, and environment settings.
- `game/`: The core engine, featuring procedural generation, combat services, and player progression.
- `templates/`: ANSI-themed terminal interface using standard 16-color palettes.
- `static/`: Frontend assets including CSS scanline effects and terminal fonts.

## Quick Start

The project uses a `Makefile` to simplify setup and maintenance.

1. **Environment Setup**:
   ```bash
   make venv
   source .venv/bin/activate
   make setup
   ```

2. **Clean Initialization** (Recommended for first run):
   ```bash
   # This nukes the database, clears old migrations, and builds a fresh schema
   make clean
   ```

3. **Generate the Grid**:
   ```bash
   # Generates 200+ rooms, bosses, and unique items
   make init
   ```

4. **Run the Grid**:
   ```bash
   make run
   ```
   Access the terminal at `http://localhost:8008`.

## Core Features

- **Procedural Sectors**: 8 distinct zones from Corporate Plazas to the Undercity.
- **Deep Progression**: 10 Races and 11 Classes with unique abilities and stat modifiers.
- **Manual Training**: Earn 5 stat points per level to manually improve STR, INT, WIL, AGI, HEA, or CHA.
- **Tactical Combat**: PvP support (within 3 levels), weapon speed mechanics, and elemental RPS.
- **Unique Loot**: Sector bosses drop legendary gear not found in shops.
- **Leaderboards**: Use the `TOP` command to see the grid's most elite adventurers.

## Development & Maintenance

- **Reset Environment**: `make clean` (rebuilds DB and migrations from scratch).
- **Run Tests**: `make test`.
- **Static Analysis**: `make lint`.
- **Deep Repair**: `make repair` (reinstalls virtual environment).

## Deployment

Detailed instructions for production environments can be found in [DEPLOY_PYTHONANYWHERE.md](DEPLOY_PYTHONANYWHERE.md).

Quick production update:
```bash
git pull
make deploy-init
python manage.py collectstatic --settings=darkness_django.settings.production --noinput
```

## Documentation

For a full manual of commands, combat formulas, and world lore, see the [USER_GUIDE.md](USER_GUIDE.md).
