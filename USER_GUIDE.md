# Darkness BBS — User Guide

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Installation](#installation)
4. [Login & Registration](#login--registration)
5. [Game Commands](#game-commands)
6. [World Structure](#world-structure)
7. [Combat System](#combat-system)
8. [Items & Equipment](#items--equipment)
9. [Shops & Economy](#shops--economy)
10. [Multi-User Features](#multi-user-features)
11. [Map System](#map-system)
12. [Character Progression](#character-progression)
13. [Server Administration](#server-administration)
14. [Architecture & Technical Details](#architecture--technical-details)

---

## Overview

Darkness BBS is a multi-user, terminal-style cyberpunk RPG inspired by classic BBS games like MajorMUD. Players connect through a web-based terminal interface, explore a procedurally generated world, fight hostile entities, collect hardware (items), and interact with other players in real-time.

The game features:
- **Procedurally generated world** — rooms, NPCs, items, and maps are generated with seeded RNG
- **Real-time multi-user** — see other players, chat in rooms, fight in the same zones
- **Polling-based architecture** — fast async updates every 2 seconds (no WebSockets required)
- **Cyberpunk theme** — every element is flavored with cyberpunk lore (chrome, neon, data-streams)
- **ASCII mini-map** — live canvas rendering of nearby rooms with color-coded indicators

---

## Getting Started

1. Open the game in your browser
2. You'll see the **Darkness BBS** login screen with ASCII art
3. Click **"Initialize New Profile"** to create a new character
4. Choose your **Augmentation Path** (race) and **Operational Class** (job)
5. Click **"Initialize"** to register
6. Log in with your handle and access code
7. You'll appear in **The Neon Hub** — the central spawn point

---

## Installation

### Prerequisites

- Python 3.13+
- pip
- make (optional, for convenience commands)

### Setup

```bash
# Clone the repository
git clone https://github.com/timotheuzi/darkness.git
cd darkness

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements/dev.txt

# Run migrations
make migrate

# Initialize the game world
make init

# Start the server
make run
```

The server starts at `http://localhost:8008`.

### Make Commands

| Command | Description |
|---------|-------------|
| `make run` | Run database migrations and start the dev server on port 8008 |
| `make init` | Run migrations and regenerate the game world |
| `make repair` | Delete the database, regenerate migrations, and reinitialize everything |
| `make migrate` | Run makemigrations and migrate only |
| `make clean` | Remove Python cache files |
| `make lint` | Run flake8 linting |
| `make test` | Run Django tests |

---

## Login & Registration

### Creating a Character

When registering, you choose:

**Augmentation Path (Race):**
| Path | Description |
|------|-------------|
| Human | Baseline. Balanced stats. |
| Cyborg | Enhanced with cybernetic implants. |
| Android | Fully synthetic body. |
| Synth | Bio-synthetic hybrid. |

**Operational Class:**
| Class | Description |
|-------|-------------|
| Street Samurai | Melee and close-quarters combat specialist. |
| Netrunner | Data intrusion and hacking expert. |
| Enforcer | Heavy weapons and brute force. |
| Fixer | Deal-making and resourceful survivor. |

Your character starts at **Level 1** with:
- 100 HP
- 20 Mana
- 10 Attack / 5 Defense
- 25 Credits
- All base stats at 10

---

## Game Commands

### Navigation

| Command | Description |
|---------|-------------|
| `N` / `NORTH` | Move north |
| `S` / `SOUTH` | Move south |
| `E` / `EAST` | Move east |
| `W` / `WEST` | Move west |

Short forms: `n`, `s`, `e`, `w`

### Information

| Command | Description |
|---------|-------------|
| `LOOK` / `L` | Scan current sector. Shows room name, description, exits, items, players, and NPCs. |
| `WHO` | List all active terminal nodes (online players). |
| `I` / `INVENTORY` | List equipped and stored hardware (items). |
| `ST` / `STATUS` | Detailed user profile with all stats. |
| `MAP` | Display ASCII mini-map of nearby rooms. |
| `HELP` / `?` | Display all available commands. |

### Interaction

| Command | Description |
|---------|-------------|
| `SAY <message>` / `'<message>` | Broadcast a message to all players in the current room. |

### Combat

| Command | Description |
|---------|-------------|
| `A/KILL <target>` | Attack a target NPC. Use partial name matching (e.g., `k chrome` to attack any NPC with "chrome" in its name). |

### Items

| Command | Description |
|---------|-------------|
| `GET <item>` / `G <item>` | Pick up hardware from the ground. |
| `DROP <item>` | Drop hardware in the current sector. |
| `EQUIP <item>` | Attach or detach hardware. Auto-unequips previous weapon/armor. |
| `USE <item>` | Use a consumable item (e.g., Health Stim, Med-Kit). |

### Shops

| Command | Description |
|---------|-------------|
| `LIST` / `LI` | View shop inventory (only works in rooms with shops). |
| `BUY <item>` | Purchase hardware from the shop. |
| `SELL <item>` | Sell hardware for credits (50% of purchase price). |

---

## World Structure

The game world is procedurally generated with a hub-and-spoke layout:

```
                    [The Neon Hub] (Spawn / Safe Zone)
                         |
            +------------+------------+
            |            |            |
      [Slums]    [Neon District]  [Industrial Zone]
         |                         |
   [Corporate Plaza]        [The Under-Grid]
         |                         |
      [The Wastes]          [Data Nexus]
                                   |
                           [The Undercity]
```

### Zones

| Zone | Level Range | Theme | Shop |
|------|-------------|-------|------|
| The Neon Hub | 1 | Urban (safe) | Central Exchange |
| The Slums | 1–3 | Urban | Black Market Stall |
| Neon District | 2–5 | Neon | Neon Bazaar |
| Industrial Zone | 3–6 | Industrial | Scrapyard Exchange |
| Corporate Plaza | 6–10 | Corporate | Corp Supply Depot |
| The Under-Grid | 8–12 | Cyber | Data Market |
| The Wastes | 10–15 | Wasteland | None |
| Data Nexus | 12–18 | Cyber | Data Exchange |
| The Undercity | 15–20 | Underground | Shadow Market |

Each zone contains 5–10 rooms connected in a network with cross-links for non-linear navigation.

### Room Types

- **Entry Room** — First room in each zone, usually has a shop
- **Inner Rooms** — Combat areas with NPCs and loot
- **Hub** — Safe zone where players respawn after death

---

## Combat System

### How Combat Works

1. Use `LOOK` or `L` to see NPCs in your room
2. Use `A/KILL <npc_name>` to attack (partial name matching)
3. Damage is calculated: `ATK - (NPC_DEF / 2) ± random(3)`
4. NPC retaliates if still alive: `NPC_ATK - (your_DEF / 2) ± random(2)`
5. If NPC dies: gain EXP + credits + possible item drops
6. If you die: respawn at The Neon Hub, lose 10 credits

### Damage Formula

```
Player damage = random(ATK - 3, ATK + 3) - NPC_DEF/2
NPC damage   = random(NPC_ATK - 2, NPC_ATK + 2) - player_DEF/2
```

### Death

When HP reaches 0:
- Respawn at The Neon Hub
- HP restored to 50% of max
- Lose 10 credits
- All equipped items are preserved

---

## Items & Equipment

### Item Types

| Type | Description |
|------|-------------|
| Weapon | Increases attack damage. One weapon equipped at a time. |
| Armor | Increases defense. One armor equipped at a time. |
| Consumable | Single-use items (healing, buffs). |
| Misc | Tradeable items, quest tokens, data chips. |

### Rarity Tiers

| Rarity | Color | Example |
|--------|-------|---------|
| Common | White | Stun Baton, Mesh Vest |
| Uncommon | Green | Mono-Blade, Riot Shield |
| Rare | Blue | Plasma Caster, Ghost Cloak |
| Epic | Purple | Railgun, Adamantine Plate |
| Legendary | Gold | Void Blade |

### Notable Items

**Weapons:**
- Stun Baton (ATK +5, 50 CR) — Starter weapon
- Mono-Blade (ATK +12, 300 CR) — Solid mid-tier
- Railgun (ATK +50, 5000 CR) — End-game powerhouse
- Void Blade (ATK +80, 15000 CR) — Legendary

**Armor:**
- Synth-Leathers (DEF +4, 80 CR) — Light stealth
- Mesh Vest (DEF +8, 150 CR) — Standard protection
- Adamantine Plate (DEF +50, 8000 CR) — Near-indestructible

**Consumables:**
- Health Stim (30 HP, 25 CR) — Basic healing
- Med-Kit (50 HP, 75 CR) — Standard medical
- Nano Repair Kit (100 HP, 200 CR) — Full repair

---

## Shops & Economy

### Credits

Credits (CR) are earned by:
- Killing NPCs (level × 10 credits)
- Selling items (50% of buy price)
- Starting bonus: 25 credits

Credits are spent at shops to buy equipment and consumables.

### Shop Locations

Each zone (except The Wastes) has a shop at its entry room. You must be in the shop room to use `LIST`, `BUY`, or `SELL`.

---

## Multi-User Features

### Real-Time Updates

The game uses **polling** (every 2 seconds) to update:
- Room state (items, NPCs, their HP)
- Other players in the room
- Chat messages

### Side Panel (Desktop)

On desktop browsers, a side panel shows:
- **STATUS** — HP, Mana, Level, Credits, EXP
- **ENTITIES** — NPCs in current room with HP bars
- **USERS** — Other players in the room
- **ITEMS** — Items on the ground
- **MAP** — Canvas-rendered mini-map

### Chat

Use `SAY <message>` or `'<message>` to broadcast to the current room. Messages appear in real-time for all players in the same room.

### Command History

Use **Arrow Up/Down** to cycle through previously entered commands.

---

## Map System

The `MAP` command displays an ASCII mini-map on the side panel canvas:

| Dot Color | Meaning |
|-----------|---------|
| Bright Green | Your current location |
| Cyan | Safe zone |
| Red | Room contains hostile NPCs |
| Green (dim) | Room contains other players |
| Gray | Empty/unknown room |

The map shows rooms within 3 hops of your current location, with connection lines between adjacent rooms.

---

## Character Progression

### Leveling Up

- Earn EXP by killing NPCs (level × 15 EXP per kill)
- Level up requires: `current_level × 100` EXP
- Each level grants:
  +10 max HP (and full heal)
  +5 max Mana (and full restore)
  +2 Attack
  +1 Defense
  +1 to all stats (STR, INT, WIL, AGI, HEA)

### Stats

| Stat | Effect |
|------|--------|
| STR | Physical power |
| INT | Technical ability |
| WIL | Mental resilience |
| AGI | Speed and evasion |
| HEA | Physical endurance |
| CHA | Social interaction |

---

## Server Administration

### Regenerating the World

```bash
make init    # Re-run migrations and generate a new random world
make repair  # Complete reset: delete DB, regenerate everything
```

### Custom Seed

To generate a reproducible world:

```bash
.venv/bin/python manage.py init_game --seed=12345 --settings=darkness_django.settings.local
```

### World Parameters

```bash
.venv/bin/python manage.py init_game --rooms=60 --zones=8 --settings=darkness_django.settings.local
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--seed` | Random | RNG seed for reproducible worlds |
| `--rooms` | 40 | Approximate number of rooms |
| `--zones` | 5 | Number of zones (max 8) |

### Database

The game uses SQLite by default (`db.sqlite3`). The database stores:
- User accounts and player data
- Generated rooms, NPCs, items
- Chat messages
- World metadata (seed, version)

---

## Architecture & Technical Details

### Backend

- **Framework:** Django 4.2.18
- **Database:** SQLite3
- **Python:** 3.13+
- **Async model:** HTTP polling (no WebSockets)

### Frontend

- **jQuery 3.7.1** for AJAX requests
- **Vanilla JS** for map rendering (Canvas API)
- **CSS** with ANSI color palette and scanline effects
- **No external dependencies** beyond jQuery CDN

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Game page |
| `/login/` | POST | Authenticate player |
| `/register/` | POST | Create new character |
| `/command/` | POST | Execute game command (JSON body: `{command: "..."}`) |
| `/poll/` | GET | Real-time room state (chat, NPCs, players, items) |
| `/map/` | GET | Map data for canvas rendering |
| `/player/info/` | GET | Current player info |

### Polling Architecture

The client polls `/poll/` every 2 seconds to receive:
```json
{
  "chat": [{"player": "name", "message": "text"}],
  "npcs": [{"id": 1, "name": "...", "hp": 100, "hp_max": 100, "lvl": 3}],
  "items": [{"id": 1, "name": "..."}],
  "players": [{"id": 1, "user__username": "...", "lvl": 5, "game_class": "Netrunner"}],
  "status": "HP:100/100|MA:20/20|LV:1|CR:25|EXP:0",
  "location": "The Neon Hub"
}
```

### Procedural Generation

The world generator uses Python's `random` module with optional seeded RNG:
1. Creates item pool (32 items across 4 types)
2. Generates zone structures (8 zone templates with themes)
3. Creates rooms with procedural names and descriptions
4. Connects rooms with bidirectional exits and cross-links
5. Spawns NPCs with zone-appropriate types and levels
6. Stores world metadata in GameWorld singleton model

### File Structure

```
darkness/
├── darkness_django/          # Django project settings
│   ├── settings/             # Environment-specific settings
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py / asgi.py     # Server entry points
├── game/                     # Main game app
│   ├── management/commands/
│   │   └── init_game.py      # Procedural world generator
│   ├── migrations/           # Database migrations
│   ├── models.py             # Data models (Player, Room, NPC, Item, etc.)
│   ├── services.py           # Game logic (combat, movement, inventory, etc.)
│   ├── views.py              # HTTP endpoints
│   └── urls.py               # App URL routes
├── static/game/
│   └── css/style.css         # ANSI terminal styles
├── templates/
│   └── game.html             # Main game page (also in game/templates/)
├── requirements/
│   ├── base.txt              # Core dependencies
│   ├── dev.txt               # Development dependencies
│   └── prod.txt              # Production dependencies
├── Makefile                  # Build and run commands
├── manage.py                 # Django management script
└── USER_GUIDE.md             # This file