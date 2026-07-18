# Darkness BBS

A professional multi-user, terminal-style cyberpunk RPG (MUD) built with Django. Explore a procedurally generated grid, engage in tactical combat, and compete with other users in a gritty neon-soaked world.

## Project Structure

- `darkness_django/`: Project configuration, middleware, and environment settings.
- `game/`: The core engine, featuring procedural generation, combat services, and player progression.
- `templates/`: ANSI-themed terminal interface using standard 16-color palettes.
- `static/`: Frontend assets including CSS scanline effects and terminal fonts.

## Core Features

- **Procedural Sectors**: 8 distinct zones from Corporate Plazas to the Undercity.
- **Deep Progression**: 10 Races and 11 Classes with unique abilities and stat modifiers.
- **Manual Training**: Earn 1 stat point per level to manually improve STR, INT, WIL, AGI, HEA, or CHA.
- **Tactical Combat**: PvP support (within 3 levels), weapon speed mechanics, and elemental damage (fire > air > earth > water > fire).
- **Karma System**: Alignment ranges from -100 (Villain) to 100 (Saint), affecting NPC aggression.
- **Stealth System**: Hide in shadows to perform backstab attacks with bonus damage.
- **Drug & Addiction System**: Temporary stat boosts with risk of dependency and withdrawal damage.
- **Unique Loot**: Sector bosses drop legendary gear not found in shops.
- **Leaderboards**: Use the `TOP` command to see the grid's most elite adventurers.
- **AI Bot System**: Autonomous AI-controlled players with cyberpunk names that wander, fight, and interact with players.

## Setup

### Prerequisites
- Python 3.11+
- pip
- make (optional)

### Local Setup
```bash
# Clone and enter directory
git clone https://github.com/timotheuzi/darknesses.git
cd darknesses

# Create environment
make venv
source .venv/bin/activate

# Install dependencies
make setup

# Nuke database and build fresh schema
make clean

# Generate world data
make init

# Start the grid
make run
```

### Make Commands
- `make clean`: **Destructive**. Nukes the DB, clears migration history, and rebuilds the schema.
- `make init`: Procedurally generates 200+ rooms, NPCs, bosses, and items.
- `make run`: Launches the Django development server on port 8008.

## Quick Start

1. Navigate to the terminal in your browser.
2. Click **"Initialize New Profile"** to create a character.
3. Select your **Race** and **Class**, then optionally customize your 6 base stats.
4. Log in and arrive at **The Neon Hub**, the grid's central safe zone.

### AI Bots
The grid is populated with AI-controlled players that:
- Have cyberpunk-themed names (e.g., Neon_Shade, Chrome_Wraith, Glitch_Monk)
- Automatically wander the grid and fight NPCs
- May attack players based on their karma alignment
- Can invite players to parties
- Appear in the `WHO` list and `TOP` rankings with a `(bot)` marker

## Documentation

For a full manual of commands, combat formulas, and world lore, see the [USER_GUIDE.md](USER_GUIDE.md).
