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
14. [Party System](#party-system)
15. [Server Administration](#server-administration)

---

## Overview

**Darkness BBS** is a multi-user, terminal-style cyberpunk RPG inspired by classic BBS games like MajorMUD. Players explore a procedurally generated grid, engage in tactical combat, customize their builds via manual stat training, and compete with other users in a gritty, neon-soaked world.

Key Features:
- **Massive Procedural World**: 8 distinct sectors with 200+ rooms.
- **Deep Character Customization**: 10 races and 13 classes with unique abilities and traits.
- **Manual Stat Training**: Earn 1 point per level to spend on specific attributes.
- **Tactical Combat**: PvP support (+/- 3 levels), weapon speed, and elemental damage (fire > air > earth > water > fire).
- **Karma System**: Alignment from -100 (Villain) to +100 (Saint).
- **Stealth System**: Hide and perform backstab attacks with bonus damage.
- **Drug & Addiction**: Temporary stat boosts with dependency risk and withdrawal damage.
- **Leaderboards**: Competitive ranking of the top adventurers and a "Wall of Death".
- **Party System**: Team up with up to 3 players to explore the grid together.
- **AI Bot System**: Autonomous AI players that wander, fight, and interact.

---

## Getting Started

1. Navigate to the terminal in your browser.
2. Click **"Initialize New Profile"** to create a character.
3. Enter a handle (username) and password.
4. Select your **Race** (Augmentation Path) and **Class** (Operational Class).
5. Optionally customize your 6 base stats (STR, INT, WIL, AGI, HEA, CHA) — total must not exceed 85 points.
6. Log in and arrive at **The Neon Hub**, the grid's central safe zone.

---

## Login & Registration

### Races (Augmentation Paths)
Each race grants a specific set of stat modifiers and a unique **Race Trait**:

| Race | Modifiers | Special Trait |
|------|-----------|---------------|
| **Cyborg** | STR+5, HEA+2, AGI-2, INT+2 | **Cybernetic Resilience**: +10% resistance to debuffs. |
| **Bio-hacked** | HEA+5, STR+2, CHA-2 | **Adrenal Efficiency**: 20% faster healing, reduced addiction. |
| **Android** | INT+8, WIL+2, CHA-5, HEA-2 | **Systematic Mind**: +15% mana efficiency, mental immunity. |
| **Mutant** | Random (+7/-3) | **Adaptive Biology**: Stats can exceed normal caps by 5. |
| **Human** | CHA+10, WIL+5, STR-5, HEA-5 | **Versatile Potential**: Gains 1.5x stat points on level up. |
| **Void-Walker** | WIL+12, AGI+5, STR-8, HEA-4 | **Phase Shift**: 10% chance to dodge any attack. |
| **Synth-Soul** | INT+15, CHA-10 | **Digital Presence**: +20% stealth effectiveness. |
| **Orc, AGI+10, INT-10, CHA-5 | **Overclocked**: +1 extra attack per combat round. |
| **Elf** | AGI+8, WIL+4, HEA-5 | **Ancient Grace**: +10% critical hit chance. |
| **Goblin** | CHA+10, AGI+5, STR-8 | **Street Cunning**: +15% chance for extra loot. |

### Stats Reference
- **STR (Strength)**: Physical power. Increases Attack and carrying capacity. Essential for melee classes.
- **AGI (Agility)**: Speed and reflexes. Increases Defense, crit chance, and stealth effectiveness. Key for dodging and Thief/Ninja.
- **HEA (Health)**: Physical resilience. Increases max HP. Vital for survivability.
- **INT (Intelligence)**: Mental acuity. Powers tech, netrunning, and spellcasting. Increases mana for some classes.
- **WIL (Willpower)**: Mental fortitude. Increases max Mana and resistance to mind effects. Core for Priests.
- **CHA (Charisma)**: Social presence. Used by Fixers and Tricksters. Affects NPC interactions and some abilities.

### Classes (Operational Classes)
Abilities are learned at levels 1, 5, 10, 15, 20, 25, and 30.

| Class | Starting Focus | Specialization | Gear Restrictions |
|-------|----------------|----------------|-----------------|
| **Street Samurai** | ATK, STR, AGI | Multi-strike Melee | All armor, One/Two-handed weapons |
| **Netrunner** | INT, Mana | System Hacking (Water/Air) | Leather/Light armor, One-handed weapons |
| **Techie** | INT, WIL, DEF | Drones & Engineering | Leather/Light armor, One-handed weapons |
| **Medie** | HEA, HP | Healing & Detoxification | Leather/Light armor, One-handed weapons |
| **Fixer** | CHA, Money | Credit Siphoning & Contracts | Leather/Light armor, One-handed weapons |
| **Thief** | AGI, ATK | Stealth & Backstabbing | Leather armor, One-handed weapons |
| **Heavy** | STR, HEA, DEF | Tanking & Earth Damage | All armor, One/Two-handed weapons |
| **Psycher** | WIL, Mana | Neural Energy & Mind Control | Leather/Light armor, One-handed weapons |
| **Warlock** | INT, WIL, Mana | Debuffs & Chaos | Leather/Light armor, One-handed weapons |
| **Priest** | WIL, HEA, HP | Divine Restoration & Air Damage | Leather/Light armor, One-handed weapons |
| **Trickster** | CHA, AGI | Luck & Confusion | Leather/Light armor, One-handed weapons |
| **Jade Dragon** | AGI, STR, DEF | Unarmed Martial Arts | Light armor only, Jade weapons |
| **Ninja** | AGI, ATK | Stealth & Thrown Weapons | Light armor only, Ninja weapons |

**Class Strategies:**
- **Street Samurai**: Physical combat specialist. High attack, excels in direct confrontations.
- **Netrunner**: Tech-hacker. Uses water/ice and air-based attacks. High mana pool, debuffs enemies.
- **Techie**: Drone operator. Earth and fire damage, can heal with nanobots.
- **Medie**: Field medic. Healing and support abilities, can deal water/rot damage.
- **Fixer**: Social manipulator. Drains credits, calls in attacks.
- **Thief**: Stealth assassin. Backstab crits, poison, smoke bombs.
- **Heavy**: Tank specialist. High HP and defense, earth-based AOE attacks.
- **Psycher**: Psychic warrior. Mind-based attacks, telekinesis, shields.
- **Warlock**: Dark spellcaster. Curses, chaos damage, blood pacts.
- **Priest**: Holy healer. Healing, blessings, divine shields.
- **Trickster**: Chaos agent. Random effects, stealth, luck-based abilities.
- **Jade Dragon**: Martial artist. Chi-based attacks, unarmed combat bonus.
- **Ninja**: Shadow warrior. Stealth, teleport, kunai throws, high crit from concealment.

---

## Game Commands

### Navigation
- `N`, `S`, `E`, `W`: Movement.
- `EXIT`: Log out safely.

### Information
- `L` / `LOOK`: Scan sector. `LOOK <target>`: Examine entity.
- `WHO`: List active nodes.
- `TOP`: Top 25 ranking.
- `WALL`: Top 25 deaths.
- `ST` / `STATUS`: Detailed profile.
- `I` / `INVENTORY`: List gear.
- `HELP` / `?`: Command manual.

### Communication
- `SAY <msg>`: Local chat.
- `BROADCAST <msg>`: Global chat.

### Combat & Action
- `A <target>`: Attack one round.
- `AA <target>`: Auto-attack until victory/defeat.
- `<ABILITY> <target>`: Use class skill (e.g., `HCK`, `BLD`, `PTC`).
- `STEALTH` / `SNEAK`: Hide (influenced by AGI and Class).
- `REST`: Recover HP/Mana (requires standing still).

### Items
- `USE <item>`: Consumables/Drugs.
- `GET <item>` / `DROP <item>`: Ground interaction.
- `EQUIP <item>`: Manage hardware.
- `LIST` / `BUY` / `SELL`: Commerce.

---

## Combat System

### Damage & Crits
Damage: `max(1, ATK - DEF/2)` ± variance. 
Critical Hits: 2.0x damage. Chance based on AGI (physical) or INT (abilities).

### Elemental Wheel
- **Fire** > **Air** > **Earth** > **Water** > **Fire**
- Strength: 1.5x damage. Weakness: 0.5x damage.

### Weapon Speed
10 Speed Bonus = 1 extra attack/round.
10 Agility = 1 extra attack/round.

---

## Party System

Team up with other players to explore and move together.

- `PARTY CREATE`: Start a new party as leader.
- `PARTY INVITE <player>`: Invite a player in your current room.
- `PARTY ACCEPT`: Join a party after receiving an invite.
- `PARTY LEAVE`: Exit your current party.
- `PARTY STATUS`: See current members.
- **Group Movement**: When the leader moves, all online party members move with them.

---

## Server Administration

- `make repair`: Full database reset (wipes players).
- `make clean`: Wipes world data but **keeps players**.
- `make init`: Generates new world state.
- `python manage.py process_bots`: Starts the AI daemon.
