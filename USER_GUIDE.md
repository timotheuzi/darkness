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
10. [Karma & Reputation](#karma--reputation)
11. [Stealth System](#stealth-system)
12. [Drug & Addiction System](#drug--addiction-system)
13. [NPC Aggression & Stalking](#npc-aggression--stalking)
14. [Server Administration](#server-administration)

---

## Overview

**Darkness BBS** is a multi-user, terminal-style cyberpunk RPG inspired by classic BBS games like MajorMUD. Players explore a procedurally generated grid, engage in tactical combat, customize their builds via manual stat training, and compete with other users in a gritty, neon-soaked world.

Key Features:
- **Massive Procedural World**: 8 distinct sectors with 200+ rooms.
- **Deep Character Customization**: 10 races and 11 classes with unique abilities.
- **Manual Stat Training**: Earn 1 point per level to spend on specific attributes.
- **Tactical Combat**: PvP support (+/- 3 levels), weapon speed, and elemental damage (fire > air > earth > water > fire).
- **Karma System**: Alignment from -100 (Villain) to 100 (Saint).
- **Stealth System**: Hide and perform backstab attacks with bonus damage.
- **Drug & Addiction**: Temporary stat boosts with dependency risk and withdrawal damage.
- **Leaderboards**: Competitive ranking of the top adventurers on the grid.
- **Boss Encounters**: Sector-specific bosses with unique legendary loot.

---

## Getting Started

1. Navigate to the terminal in your browser.
2. Click **"Initialize New Profile"** to create a character.
3. Enter a handle (username) and password.
4. Select your **Race** (Augmentation Path) and **Class** (Operational Class).
5. Optionally customize your 6 base stats (STR, INT, WIL, AGI, HEA, CHA) — total must not exceed 85 points.
6. Log in and arrive at **The Neon Hub**, the grid's central safe zone.

---

## Installation

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

---

## Login & Registration

### Races (Augmentation Paths)
Each race grants a specific set of stat modifiers applied on top of the player's base stats:

| Race | Stat Modifiers | Description |
|------|---------------|-------------|
| **Human** | CHA +10, WIL +5, STR -5, HEA -5 | High social influence, physically frail. |
| **Elf** | AGI +8, WIL +4, HEA -5 | Quick and mentally resilient. |
| **Goblin** | CHA +10, AGI +5, STR -8 | Small, charming, and evasive. |
| **Mutant** | Random distribution (+7/-3) | Unpredictable but balanced. |
| **Cyborg** | STR +5, HEA +2, AGI -2, INT +2 | Enhanced physical power with a neural edge. |
| **Android** | INT +8, WIL +2, CHA -5, HEA -2 | High processing capability, low empathy. |
| **Void-Walker** | WIL +12, AGI +5, STR -8, HEA -4 | Masters of the ethereal data-stream. |
| **Synth-Soul** | INT +15, CHA -10 | Extreme technical capability, socially inept. |
| **Chrome-Crawler** | STR +10, AGI +10, INT -10, CHA -5 | Specialized in high-speed physical combat. |
| **Bio-hacked** | HEA +5, STR +2, CHA -2 | Enhanced biological durability. |

### Classes (Operational Classes)
Each class grants unique stat bonuses at character creation and access to exclusive abilities learned at levels 1, 5, 9, 13, 17, 21, 25, and 29:

| Class | Starting Bonuses | Focus |
|-------|-----------------|-------|
| **Street Samurai** | ATK +5, STR +3, AGI +2 | Physical Melee |
| **Netrunner** | INT +5, Mana Max +20 | Intelligence/Mana |
| **Techie** | INT +3, WIL +2, DEF +3 | Drone Warfare |
| **Medie** | HEA +3, HP Max +20 | Healing & Vitality |
| **Fixer** | CHA +5, Money +50 | Credits & Commerce |
| **Thief** | AGI +6, ATK +2 | Stealth & Criticals |
| **Heavy** | STR +5, HEA +5, DEF +5, HP Max +30 | Tanking |
| **Psycher** | WIL +8, Mana Max +40 | Willpower/Psychic |
| **Warlock** | INT +5, WIL +5, Mana Max +30 | Debuffs / Elemental |
| **Priest** | WIL +6, HEA +4, HP Max +25 | Restoration |
| **Trickster** | CHA +15, AGI +5 | Charm & Luck |

---

## Game Commands

### Navigation & Session
- `N`, `S`, `E`, `W`: Standard movement (North, South, East, West).
- `EXIT`: Safely logs out and returns to the login screen, clearing local cache.

### Information
- `LOOK` / `L`: Scan the current sector for entities, players, items, and exits.
- `LOOK <target>` / `L <target>`: Examine a specific NPC, player, or item.
- `WHO`: Lists all active users currently linked to the grid (shows level and class).
- `TOP`: Displays the Top 10 adventurers by level and experience.
- `ST` / `STATUS`: Detailed profile view showing all stats, karma, addiction, and learned abilities.
- `I` / `INVENTORY`: Lists equipped `[E]` and stored hardware with quantities.
- `HELP` / `?`: Displays all available commands and class abilities.

### Communication
- `SAY <message>` / `' <message>`: Broadcast a message to all players in the current sector.

### Combat & Action
- `A` / `KILL <target>`: Engage an NPC or player in combat.
- `<ABILITY> <target>`: Execute a class-specific ability (e.g., `HACK DRONE`, `BLADE TARGET`).
- `STEALTH` / `SNEAK`: Attempt to hide in the shadows (available to all classes, best for Thief/Trickster).
- `BACKSTAB`: Automatic when attacking from stealth — first round deals 1.5x damage with no counter.

### Items & Equipment
- `USE <item>`: Consume an item (heals, drugs, scrolls).
- `GET <item>` / `G <item>`: Retrieve an item from the ground.
- `DROP <item>`: Discard an item in the current sector.
- `EQUIP <item>`: Equip or unequip a weapon or armor piece.
- `LIST` / `LI`: View a shop's catalog.
- `BUY <item>`: Purchase an item from the current shop.
- `SELL <item>`: Sell an item to the current shop (50% of price).
- `SELL <item> to <dealer>`: Sell items (especially drugs) to a dealer NPC for a premium.

### Character Progression
- `TRAIN <stat>`: Spend 1 stat point on **STR**, **INT**, **WIL**, **AGI**, **HEA**, or **CHA**.

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

Each sector has an **Entry** room, connected to another zone, and a **Boss Lair** at the deepest room. Some sectors also feature shops (e.g., Black Market Stall, Corp Supply Depot, Data Market).

---

## Combat System

### Damage Calculation
Base damage is calculated as: `max(1, ATK - DEF/2)` with random variance of ±2.

### Elemental System
The combat system uses a rock-paper-scissors elemental wheel:
- **Fire** beats **Air**
- **Air** beats **Earth**
- **Earth** beats **Water**
- **Water** beats **Fire**

If your attack element is strong against the target (elementally beats or matches target's weakness), damage is multiplied by **1.5x**. If the target resists your element, damage is halved (**0.5x**).

### Weapon Speed
Each weapon has a Speed Bonus. Every 10 points of Speed Bonus grants one additional attack per round. Agility also grants bonus attacks: `AGI // 10` extra attacks per round.

### PvP Protocol
- Combat is allowed in all sectors except **The Neon Hub** (safe zone).
- You can only attack players within **3 levels** of your own.
- Winning a PvP fight steals **25% of the target's credits** and grants `target.level * 50` EXP.
- Each PvP attack costs **-10 Karma** (murder penalty).

### Death & Reset
If your HP reaches 0:
- **PvE Death**: You respawn at **The Neon Hub** with 50% HP and lose **10 credits**.
- **PvP Death**: You respawn at **The Neon Hub** with 50% HP and lose **25% of your credits** (stolen by victor).
- Withdrawal/Overdose Death: Lose **20 credits** and 10 addiction points.
- NPC stalking is cleared on death.

---

## Items & Equipment

### Item Types
- **Weapon**: Provides attack bonus, speed bonus, and stat bonuses when equipped.
- **Armor**: Provides defense bonus and stat bonuses when equipped.
- **Consumable**: Heals HP on use (e.g., Health Stim, Med-Kit, Nano Repair Kit).
- **Drug**: Provides temporary stat boosts with addiction risk (see Addiction System).
- **Scroll**: Teleports the player to a specific room (e.g., warp to hub).
- **Misc**: Quest/collectible items (e.g., Data Chip, Black Market Token, Strange Artifact).

### Rarity Levels
- Common, Uncommon, Rare, Epic, Legendary

### Unique Boss Drops
Every sector features a **Boss Lair** with high-level guardians. They drop unique weapons that cannot be purchased in shops:

| Sector | Boss Weapons |
|--------|-------------|
| **The Slums** | Street King's Shiv, Gutter Brawler's Knuckles |
| **Industrial Zone** | Forge-Master's Wrench, Steam-Powered Piercer |
| **Corporate Plaza** | CEO's Golden Handgun, Director's Neural Whip |
| **The Under-Grid** | Source Code Fragment, Malware Spike |
| **Neon District** | Diva's Sonic Lash, Club Owner's Cane |
| **The Wastes** | Wasteland Harvester, Scavenger's Crossbow |
| **Data Nexus** | Nexus Core Blade, Protocol Breaker |
| **The Undercity** | Shadow's Embrace, Crypt-Keeper's Scythe |

### Drug Effects
Drugs provide stat boosts with a random chance of addiction:
- **Neuro-Jack**: INT +5, WIL +3, STR -2, HEA -2 (25% addiction)
- **Combat-Rush**: STR +6, AGI +4, WIL -3, CHA -3 (30% addiction)
- **Synth-Ghost**: AGI +8, HEA -5, STR -3 (20% addiction)
- **Neon-Glow**: CHA +10, INT -4, WIL -2 (15% addiction)
- **Over-Clock**: All stats +4 (50% addiction)
- **Iron-Skin**: HEA +10, AGI -5, CHA -2 (35% addiction)

---

## Character Progression

### Leveling Up
- Defeating targets grants EXP (`npc.lvl * 15` for normal NPCs, `npc.lvl * 100` for bosses, `target.lvl * 50` for PvP).
- Level up requires: `current_level * 120` EXP.
- Each level-up grants: **+20 HP Max**, **+10 Mana Max**, full HP/Mana restore, and **1 Stat Point**.
- New class abilities unlock at levels 1, 5, 9, 13, 17, 21, 25, and 29.
- At level 5, NPC aggression protocols activate — enemies in non-safe zones may attack on sight.

### Stat Training
Use `TRAIN <stat>` to spend stat points:
- **STR**: +2 Attack per point.
- **INT**: +5 Max Mana per point.
- **WIL**: +5 Max Mana per point.
- **AGI**: +1 Defense per point.
- **HEA**: +10 Max HP per point.
- **CHA**: No direct combat bonus, affects Trickster abilities and karma interactions.

### Class Abilities
Each class has 8 unique abilities unlocked at specific levels. Type `HELP` or `ST` in-game to see your available moves. All class abilities consume Mana (`5 + ability_level // 2` cost).

Universal abilities available to all classes:
- `STEALTH` / `SNEAK`: Attempt to hide. Base success depends on class (Thief/Trickster: 70% + AGI/2, others: 30% + AGI/4). Low-level characters have a -20 penalty.

---

## Karma & Reputation

Karma ranges from **-100 (Villain)** to **+100 (Saint)** and determines your reputation title:

| Karma Range | Title |
|-------------|-------|
| +80 to +100 | Saint |
| +50 to +79 | Paragon |
| +20 to +49 | Lawful |
| -19 to +19 | Neutral |
| -49 to -20 | Renegade |
| -79 to -50 | Outlaw |
| -100 to -80 | Utter Villain |

### Karma Effects
- **NPC Aggression**: NPCs with positive karma alignment attack negative karma players and vice versa. If the absolute difference between your karma and an NPC's karma alignment exceeds 130, they may attack on sight.
- **PvP Penalty**: Attacking another player costs **-10 Karma**. Using class abilities in PvP costs **-2 Karma** per use.
- **Karma from PvE**: Killing NPCs with negative alignment (< -30) grants **+5 Karma**. Killing lawful NPCs (> +30) costs **-10 Karma**. Neutral NPCs grant **+1 Karma**.
- **Drug Dealing**: Selling drugs to dealers costs **-5 Karma**.

---

## Stealth System

Players can attempt to hide using `STEALTH` or `SNEAK`:
- **Success chance** depends on class and AGI stat. Thief/Trickster classes get higher base rates.
- Higher-level threats in the room reduce success chance (`(threat_lvl - player_lvl) * 10` penalty).
- While hidden, moving to a new room triggers a re-roll based on `40 + AGI // 3` minus threat level penalties.
- Hidden players avoid **auto-attacks** from aggressive NPCs when entering a room.
- Attacking from stealth triggers **backstab**: first round is free (no counter-attack) with **1.5x damage**.
- Cannot hide while stalking an NPC or in a safe zone.

---

## Drug & Addiction System

Using drugs provides temporary stat boosts but risks addiction:
- On drug use, there is a chance (`addiction_chance` on the item) to gain **+20 addiction points**.
- Addiction points accumulate from 0 to 100.
- Every 10+ ticks since last use, withdrawal kicks in: lose `1 to addiction//5 + 2` HP per tick.
- After 50 withdrawal ticks, addiction slowly decreases (1 point every 10 ticks).
- If withdrawal drains HP to 0, you overdose: respawn at hub with 50% HP, lose 20 credits and 10 addiction points.
- Use `DETOX` (Medie class ability) to cleanse 15 addiction points.

---

## NPC Aggression & Stalking

### Auto-Aggression
At level 5+, NPCs may auto-attack when you enter their room if you are not hidden. Aggression triggers if:
- The NPC is flagged as `aggressive`.
- There is a large karma alignment difference (`abs(npc.karma_alignment - player.karma) > 130`).
- The NPC is lawful (karma > 40) and the player is chaotic (karma < -40), or vice versa.

### Stalking
After engaging an NPC in manual combat (non-auto), the NPC will **stalk** you for 4 room transitions, following you through exits. The stalk count decreases by 1 per move. Being defeated resets stalking.

### NPC Respawn
Dead NPCs respawn after a room-specific timer (default 300 seconds). Rooms can also spawn new random NPCs if empty. Boss Lairs always have their bosses present after regeneration.

---

## Server Administration

### Atomic Reset
If you update the models or wish to generate a new map layout:
```bash
# Completely nuke and rebuild the database/migrations
make clean

# Generate a new random world (default 200 rooms, configurable with --rooms)
make init
```

You can also specify a seed for reproducible generation:
```bash
python manage.py init_game --seed 12345 --rooms 200
```

The `init_game` algorithm ensures the central Hub is always linked to every sector entry point, preventing player isolation. Data is submitted as a single atomic transaction.