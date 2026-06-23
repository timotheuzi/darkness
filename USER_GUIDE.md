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
9. [Character Progression](#character-progression)
10. [Server Administration](#server-administration)

---

## Overview

**Darkness BBS** is a multi-user, terminal-style cyberpunk RPG inspired by classic BBS games like MajorMUD. Players explore a procedurally generated grid, engage in tactical combat, customize their builds via manual stat training, and compete with other users in a gritty, neon-soaked world.

Key Features:
- **Massive Procedural World**: 8 distinct sectors with 200+ rooms.
- **Deep Character Customization**: 10 races and 11 classes with unique abilities.
- **Manual Stat Training**: Earn 5 points per level to spend on specific attributes.
- **Tactical Combat**: PvP support (+/- 3 levels), weapon speed, and elemental damage.
- **Leaderboards**: Competitive ranking of the top adventurers on the grid.
- **Boss Encounters**: Sector-specific bosses with unique legendary loot.

---

## Getting Started

1. Navigate to the terminal in your browser.
2. Click **"Initialize New Profile"** to create a character.
3. Select your **Augmentation Path** (Race) and **Operational Class**.
4. Log in and arrive at **The Neon Hub**, the grid's central safe zone.

---

## Installation

### Prerequisites
- Python 3.11+
- pip
- make (optional)

### Local Setup
```bash
# Clone and enter directory
git clone https://github.com/timotheuzi/darkness.git
cd darkness

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

---

## Login & Registration

### Augmentation Paths (Races)
| Race | Key Stats | Description |
|------|-----------|-------------|
| **PureBlood** | CHA / WIL | High social influence, physically frail. |
| **Elf** | AGI / WIL | Quick and mentally resilient. |
| **Goblin** | CHA / AGI | Small, charming, and evasive. |
| **Mutant** | **Random** | Randomized yet balanced stat distribution. |
| **Cyborg** | STR / HEA | Enhanced physical power. |
| **Android** | INT / WIL | High processing capability. |
| **Void-Walker**| WIL / AGI | Masters of the ethereal data-stream. |
| **Synth-Soul** | INT | Extreme technical capability. |
| **Chrome-Crawler**| STR / AGI| Specialized in high-speed physical combat. |
| **Bio-hacked** | HEA / STR | Enhanced biological durability. |

### Operational Classes
| Class | Unique Ability | Focus |
|-------|----------------|-------|
| **Street Samurai** | `BLADE` / `ONI_STRIKE` | Physical Melee |
| **Netrunner** | `HACK` / `OVERLOAD` | Intelligence/Mana |
| **Trickster** | `BAMBOOZLE` / `JACKPOT`| **Charm Specialist** |
| **Warlock** | `CURSE` / `CHAOS_BOLT` | Debuffs / Elemental |
| **Priest** | `HEAL` / `BLESS` | Restoration |
| **Heavy** | `SMASH` / `TAUNT` | Tanking |
| **Psycher** | `MIND_BOLT` / `SOUL_DRAIN`| Willpower/Psychic |
| **Infiltrator** | `STAB` / `VANISH` | Stealth & Criticals |
| **Fixer** | `SCHEME` / `CALL_IN` | Credits & Air Strikes |
| **Techie** | `CALIBRATE` / `TURRET` | Drone Warfare |
| **Medie** | `PATCH` / `DETOX` | Healing & Addiction |

---

## Game Commands

### Navigation & Session
- `N`, `S`, `E`, `W`: Standard movement (North, South, East, West).
- `EXIT`: Safely logs out and returns to the login screen, clearing local cache.

### Information
- `LOOK` / `L`: Scans the sector for entities, players, items, and exits.
- `WHO`: Lists all active users currently linked to the grid.
- `TOP`: Displays the Top 10 adventurers by level and experience.
- `ST` / `STATUS`: Detailed profile view showing base stats and available **Stat Points**.
- `I` / `INVENTORY`: Lists equipped [E] and stored hardware.

### Action & Progression
- `A` / `KILL <target>`: Engage an NPC or Player in combat.
- `TRAIN <stat>`: Spend points on **STR, INT, WIL, AGI, HEA,** or **CHA**.
- `<ABILITY> <target>`: Execute a class-specific ability (e.g., `HACK DRONE`).
- `USE <item>`: Trigger a consumable effect.
- `GET <item>`: Retrieve hardware from the ground.

---

## World Structure

The grid contains 8 distinct sectors, each with unique themes and level ranges:
1. **The Slums** (Lv 1-3)
2. **Neon District** (Lv 2-5)
3. **Industrial Zone** (Lv 3-6)
4. **Corporate Plaza** (Lv 6-10)
5. **The Under-Grid** (Lv 8-12)
6. **The Wastes** (Lv 10-15)
7. **Data Nexus** (Lv 12-18)
8. **The Undercity** (Lv 15-20)

---

## Combat System

### Damage & Weapon Speed
Combat rounds are influenced by your equipped weapon's **Speed Bonus**.
- **+10 Speed**: Grants +1 additional attack per combat round.
- **Stat Scaling**: Your Attack scales with **STR**, and Defense scales with **AGI**.

### PvP Protocol
- Combat is allowed in all sectors except **The Neon Hub**.
- You can only attack players within **3 levels** of your own.
- Winning a PvP fight steals **25% of the target's credits** and yields high EXP.

### Death & Reset
If your HP reaches 0:
- You respawn at **The Neon Hub**.
- HP is restored to 50% of maximum.
- You lose 10 credits (PvE) or 25% of credits (PvP).

---

## Items & Equipment

### Stat Modifiers
Modern hardware provides direct boosts to your base attributes. Equipping a *Reflective Trenchcoat* may increase your **CHA**, while a *Void Blade* might grant massive **AGI** and **WIL** bonuses.

### Unique Boss Drops
Every sector features a **Boss Lair** with high-level guardians. They drop unique weapons that cannot be purchased in shops:
- **CEO's Golden Handgun** (Corporate)
- **Shadow's Embrace** (Undercity)
- **Source Code Fragment** (Under-Grid)

---

## Character Progression

### Leveling Up
- Neutralizing targets grants EXP.
- Each level-up grants **5 Stat Points**.
- Attributes can be improved manually using the `TRAIN` command:
    - **STR**: Increases Attack.
    - **INT/WIL**: Increases Max Mana and Ability Damage.
    - **AGI**: Increases Defense.
    - **HEA**: Increases Max HP.
    - **CHA**: Increases Trickster ability success.

---

## Server Administration

### Atomic Reset
If you update the models or wish to generate a new map layout:
```bash
# Completely nuke and rebuild the database/migrations
make clean

# Generate a new random world (default 200 rooms)
make init
```

The `init_game` algorithm ensures the central Hub is always linked to every sector entry point, preventing player isolation.
