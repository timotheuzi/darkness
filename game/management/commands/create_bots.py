#!/usr/bin/env python3
"""
AI Bot Generator for Darkness BBS.
Creates AI-controlled bot players with cyberpunk names that wander, fight, and interact.
"""
import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from game.models import Player, User, Room, Item, InventoryItem


# Cyberpunk-themed bot names (using camelCase instead of underscores)
BOT_NAMES = [
    "NeonShade",
    "ChromeWraith",
    "GlitchMonk",
    "wut",
    "CircuitBreaker",
    "SynthRunner",
    "DataPhantom",
    "VoltStriker",
    "ZeroCool",
    "PixelSlayer",
    "RogueAI",
    "NeuralJack",
    "CyberWitch",
    "BinaryStorm",
    "QuantumShade",
    "EchoProtocol",
    "VoidWalker",
    "drama",
    "LaserMonk",
    "Innit",
    "NovaBlade",
    "CipherPunk",
    "DriftWire",
    "FluxCore",
    "Geostomping",
    "JadeSpirit",
    "KiraCode",
    "LynxSystem",
    "MakoShift",
    "NexusFlame",
    "OnyxData",
    "PrismHack",
    "QuakeBot",
    "RiftWalker",
    "SparkAgent",
    "TalonNet",
    "Derpydo",
    "ViperCode",
    "fuuu",
    "x",
    "YuriShift",
    "ZenHacker",
    "Some Guy",
    "Blitz",
    "CrackShell",
    "DuskLoader",
    "EmberSync",
    "FrostByte",
    "GrimAccess",
    "Tim Bob",
]

# Sensible race/class combinations
RACE_CLASS_COMBOS = [
    ("Cyborg", "Street Samurai"),
    ("Cyborg", "Heavy"),
    ("Android", "Netrunner"),
    ("Android", "Techie"),
    ("Bio-hacked", "Medie"),
    ("Bio-hacked", "Psycher"),
    ("Mutant", "Heavy"),
    ("Mutant", "Jade Dragon"),
    ("Human", "Fixer"),
    ("Human", "Trickster"),
    ("Elf", "Thief"),
    ("Elf", "Jade Dragon"),
    ("Goblin", "Thief"),
    ("Goblin", "Trickster"),
    ("Void-Walker", "Psycher"),
    ("Void-Walker", "Warlock"),
    ("Synth-Soul", "Netrunner"),
    ("Synth-Soul", "Warlock"),
    ("Chrome-Crawler", "Street Samurai"),
    ("Chrome-Crawler", "Heavy"),
]


class Command(BaseCommand):
    help = "Create AI bot players with cyberpunk names"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=15, help="Number of bots to create (3-20)")
        parser.add_argument("--reset", action="store_true", help="Delete all existing bots first")

    def handle(self, *args, **kwargs):
        count = min(max(3, kwargs.get("count", 15)), 20)  # Clamp between 3-20
        reset = kwargs.get("reset", False)

        with transaction.atomic():
            if reset:
                self.stdout.write("Removing existing bots...")
                # Delete bot users and their players
                bot_players = Player.objects.filter(is_bot=True)
                for bp in bot_players:
                    bp.user.delete()
                self.stdout.write(self.style.SUCCESS(f"Removed {bot_players.count()} bots."))

            # Get rooms organized by zone level ranges for appropriate bot placement
            zone_rooms = {}
            for room in Room.objects.filter(safe_zone=False):
                zone = room.zone
                if zone not in zone_rooms:
                    zone_rooms[zone] = []
                zone_rooms[zone].append(room)

            if not zone_rooms:
                self.stdout.write(self.style.WARNING("No rooms available. Run init_game first."))
                return

            # Get all items for equipping bots
            all_items = list(Item.objects.all())
            weapons = [i for i in all_items if i.item_type == "weapon"]
            armor = [i for i in all_items if i.item_type == "armor"]

            created_count = 0
            used_names = set(
                Player.objects.filter(is_bot=True).values_list("user__username", flat=True)
            )

            for _ in range(count):
                # Find unused bot name
                available_names = [n for n in BOT_NAMES if n not in used_names]
                if not available_names:
                    self.stdout.write(self.style.WARNING("Ran out of unique bot names!"))
                    break

                bot_name = random.choice(available_names)
                used_names.add(bot_name)

                # Random race/class combo
                race, game_class = random.choice(RACE_CLASS_COMBOS)

                # Random level 1-15
                lvl = random.randint(1, 15)

                # Random karma/alignment (-100 to 100)
                karma = random.randint(-100, 100)

                # Bot behavior traits
                aggression = random.randint(0, 100)  # Likelihood to attack players
                social = random.randint(0, 100)  # Likelihood to party with players

                # Create user
                user = User.objects.create_user(username=bot_name, password="bot")

                # Choose level-appropriate room based on bot level
                appropriate_rooms = []
                for zone, rooms in zone_rooms.items():
                    # Match bot level to zone (simplified logic)
                    if lvl <= 5 and zone in ["slums", "neon", "hub"]:
                        appropriate_rooms.extend(rooms)
                    elif lvl <= 10 and zone in ["slums", "neon", "industrial", "corporate"]:
                        appropriate_rooms.extend(rooms)
                    elif lvl <= 15 and zone in ["industrial", "corporate", "undergrid"]:
                        appropriate_rooms.extend(rooms)
                    elif lvl >= 10:
                        # High level bots can go anywhere
                        appropriate_rooms.extend(rooms)

                # Fallback to any room if no appropriate rooms found
                if not appropriate_rooms:
                    appropriate_rooms = list(Room.objects.filter(safe_zone=False))

                location = random.choice(appropriate_rooms)

                # Calculate stats based on level
                str_stat = random.randint(8, 12 + lvl)
                int_stat = random.randint(8, 12 + lvl)
                wil_stat = random.randint(8, 12 + lvl)
                agi_stat = random.randint(8, 12 + lvl)
                hea_stat = random.randint(8, 12 + lvl)
                cha_stat = random.randint(8, 12 + lvl)

                attack = 10 + (str_stat // 2) + lvl
                defense = 5 + (agi_stat // 2) + lvl
                hp_max = 100 + (hea_stat * 2) + (lvl * 20)
                mana_max = 20 + (wil_stat * 2) + (lvl * 10)

                # Create bot player
                bot = Player.objects.create(
                    user=user,
                    race=race,
                    gender=random.choice(["Male", "Female", "Other"]),
                    game_class=game_class,
                    location=location,
                    lvl=lvl,
                    exp=random.randint(0, lvl * 120),
                    money=random.randint(25, 200 + (lvl * 50)),
                    hp=hp_max,
                    hp_max=hp_max,
                    mana=mana_max,
                    mana_max=mana_max,
                    str_stat=str_stat,
                    int_stat=int_stat,
                    wil_stat=wil_stat,
                    agi_stat=agi_stat,
                    hea_stat=hea_stat,
                    cha_stat=cha_stat,
                    attack=attack,
                    defense=defense,
                    karma=karma,
                    online=True,
                    is_bot=True,
                    bot_karma=karma,
                    bot_aggression=aggression,
                    bot_social=social,
                    stat_points=random.randint(0, lvl // 2),
                    last_bot_action=timezone.now()
                    - timezone.timedelta(seconds=random.randint(30, 60)),
                )

                # Equip bot with random gear
                if weapons and random.random() < 0.7:  # 70% chance to have weapon
                    weapon = random.choice(weapons)
                    InventoryItem.objects.create(player=bot, item=weapon, equipped=True)

                if armor and random.random() < 0.5:  # 50% chance to have armor
                    armor_piece = random.choice(armor)
                    InventoryItem.objects.create(player=bot, item=armor_piece, equipped=True)

                created_count += 1
                self.stdout.write(f"Created bot: {bot_name} ({race} {game_class}, Lv {lvl})")

            self.stdout.write(self.style.SUCCESS(f"\nCreated {created_count} AI bots."))
