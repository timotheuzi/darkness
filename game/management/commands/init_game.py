#!/usr/bin/env python3
"""
Procedural Cyberpunk World Generator for Darkness BBS.
Generates rooms, items, NPCs, and maps with seeded RNG.
"""
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from game.models import NPC, Item, Room, GameWorld


# ── Data Tables ──────────────────────────────────────────────────────────────

WEAPON_TABLE = [
    ("Stun Baton", "Standard issue security baton.", 5, 50, "common"),
    ("Mono-Blade", "Vibrating edge for clean cuts.", 12, 300, "uncommon"),
    ("Heavy Slugger", "High-caliber kinetic pistol.", 20, 750, "uncommon"),
    ("Laser Drill", "Industrial tool repurposed for violence.", 15, 450, "uncommon"),
    ("Plasma Caster", "Superheated plasma bolt launcher.", 28, 1200, "rare"),
    ("Neural Spike", "Disrupts cybernetic implants.", 35, 2000, "rare"),
    ("Railgun", "Electromagnetic accelerator.", 50, 5000, "epic"),
    ("Void Blade", "Cuts through dimensions.", 80, 15000, "legendary"),
    ("EMP Grenade", "Disables electronics in radius.", 10, 200, "common"),
    ("Cyber Katana", "Monomolecular edge blade.", 25, 900, "rare"),
    ("Golden Axe", "A shiny axe", 100, 500, "rare"),
]

ARMOR_TABLE = [
    ("Mesh Vest", "Basic kinetic protection.", 8, 150, "common"),
    ("Riot Shield", "Reinforced alloy shield.", 20, 1000, "uncommon"),
    ("Synth-Leathers", "Tough street fabric.", 4, 80, "common"),
    ("Titanium Exo-Frame", "Full body exoskeleton.", 35, 3000, "rare"),
    ("Ghost Cloak", "Active camouflage tech.", 15, 2500, "rare"),
    ("Neural Shield", "Anti-hacking defense.", 10, 1500, "uncommon"),
    ("Adamantine Plate", "Near-indestructible armor.", 50, 8000, "epic"),
]

CONSUMABLE_TABLE = [
    ("Dog meat", "Fido tastes good.", 25, "common", 30),
    ("Health Stim", "Nanobot healing injection.", 25, "common", 30),
    ("Data Spike", "Buffer boost chip.", 60, "common", 0),
    ("Adrenaline Shot", "AGI boost injection.", 80, "uncommon", 0),
    ("Nano Repair Kit", "Full body repair unit.", 200, "rare", 100),
    ("Synth-Meat", "Synthetic protein bar.", 10, "common", 15),
    ("Neural Booster", "WIL enhancement chip.", 120, "uncommon", 0),
    ("Med-Kit", "Standard medical kit.", 75, "common", 50),
]

MISC_TABLE = [
    ("Data Chip", "Encrypted data storage.", 0, "common"),
    ("Broken Cybernetic", "Salvaged cybernetic part.", 0, "common"),
    ("Access Keycard", "Opens locked doors.", 0, "uncommon"),
    ("Holographic Map", "Shows part of the grid.", 0, "rare"),
    ("Black Market Token", "Underground currency.", 0, "uncommon"),
    ("Golden Ticket", "Underground currency.", 0, "rare"),
]

ZONE_TEMPLATES = [
    {
        "name": "The Slums",
        "desc": "Gritty rain-soaked streets and rusted pipes.",
        "min_lvl": 1, "max_lvl": 3, "theme": "urban", "zone_id": "slums",
        "npc_prefix": "Street", "npc_types": ["drone", "gang"],
        "shop": "Black Market Stall",
        "room_names": ["Alley", "Street", "Block", "Corner", "Junction"],
        "room_details": [
            "Neon signs flicker above puddles of dirty water.",
            "Rusted fire escapes climb the walls like skeletal fingers.",
            "The smell of synthetic noodles hangs in the air.",
            "Graffiti covers every surface. Some of it glows.",
            "Trash fires provide the only warmth in the cold rain.",
        ],
    },
    {
        "name": "Industrial Zone",
        "desc": "Hissing steam, clanking machinery, and toxic fumes.",
        "min_lvl": 3, "max_lvl": 6, "theme": "industrial", "zone_id": "industrial",
        "npc_prefix": "Factory", "npc_types": ["drone", "gang"],
        "shop": "Scrapyard Exchange",
        "room_names": ["Factory", "Warehouse", "Dock", "Plant", "Mill"],
        "room_details": [
            "Steam vents hiss from cracked pipes overhead.",
            "Conveyor belts carry unknown objects into darkness.",
            "The air tastes of ozone and burning metal.",
            "Heavy machinery drones echo through the chamber.",
            "Chemical runoff glows faintly in the shadows.",
        ],
    },
    {
        "name": "Corporate Plaza",
        "desc": "Clean, sterile glass towers. Heavily guarded.",
        "min_lvl": 6, "max_lvl": 10, "theme": "corporate", "zone_id": "corporate",
        "npc_prefix": "Corp", "npc_types": ["corporate", "drone"],
        "shop": "Corp Supply Depot",
        "room_names": ["Tower", "Office", "Lobby", "Suite", "Lab"],
        "room_details": [
            "Polished floors reflect the cold fluorescent lights.",
            "Security cameras track every movement.",
            "Holographic displays show stock tickers and news.",
            "The air is filtered and sterile. No warmth here.",
            "Glass walls reveal the city sprawling below.",
        ],
    },
    {
        "name": "The Under-Grid",
        "desc": "Scrambled data-scapes and flickering holograms.",
        "min_lvl": 8, "max_lvl": 12, "theme": "cyber", "zone_id": "undergrid",
        "npc_prefix": "Glitch", "npc_types": ["drone", "gang"],
        "shop": "Data Market",
        "room_names": ["Node", "Port", "Terminal", "Gateway", "Matrix"],
        "room_details": [
            "Reality pixelates at the edges of vision.",
            "Data streams flow like rivers of light.",
            "Holographic ghosts flicker in and out of existence.",
            "The floor seems to shift between solid and code.",
            "Wireless signals buzz like electric insects.",
        ],
    },
    {
        "name": "Neon District",
        "desc": "Bright neon lights, crowded streets, hidden alleys.",
        "min_lvl": 2, "max_lvl": 5, "theme": "neon", "zone_id": "neon",
        "npc_prefix": "Neon", "npc_types": ["gang", "drone"],
        "shop": "Neon Bazaar",
        "room_names": ["Club", "Bar", "Lounge", "Arcade", "Stage"],
        "room_details": [
            "Neon lights paint everything in pink and blue.",
            "Bass-heavy music thumps through the walls.",
            "Crowds of augmented humans push past.",
            "Street vendors sell glowing street food.",
            "Prostitute bots line the alleyways.",
        ],
    },
    {
        "name": "The Wastes",
        "desc": "Desolate wasteland. Mutants and scavengers roam.",
        "min_lvl": 10, "max_lvl": 15, "theme": "wasteland", "zone_id": "wastes",
        "npc_prefix": "Waste", "npc_types": ["gang", "drone"],
        "shop": None,
        "room_names": ["Ruin", "Camp", "Outpost", "Bunker", "Crater"],
        "room_details": [
            "Acid rain pools in craters of fused glass.",
            "Rusted vehicles lie overturned in the dust.",
            "The wind howls through broken structures.",
            "Scavenger camps dot the horizon.",
            "Toxic clouds drift across the dead sky.",
        ],
    },
    {
        "name": "Data Nexus",
        "desc": "A massive server farm. Data streams flow like light.",
        "min_lvl": 12, "max_lvl": 18, "theme": "cyber", "zone_id": "nexus",
        "npc_prefix": "Data", "npc_types": ["drone", "corporate"],
        "shop": "Data Exchange",
        "room_names": ["Server", "Core", "Relay", "Hub", "Vault"],
        "room_details": [
            "Rows of servers blink in perfect synchronization.",
            "Cooling fans create a constant drone.",
            "Fiber optic cables snake across the floor.",
            "The heat from the processors is intense.",
            "Holographic data visualizations float in mid-air.",
        ],
    },
    {
        "name": "The Undercity",
        "desc": "Deep underground. Dark, damp, full of secrets.",
        "min_lvl": 15, "max_lvl": 20, "theme": "underground", "zone_id": "undercity",
        "npc_prefix": "Shadow", "npc_types": ["gang", "drone"],
        "shop": "Shadow Market",
        "room_names": ["Tunnel", "Cave", "Chamber", "Crypt", "Passage"],
        "room_details": [
            "Water drips from the cavern ceiling above.",
            "Bioluminescent fungi provide eerie light.",
            "Old subway tracks disappear into darkness.",
            "The walls are covered in ancient graffiti.",
            "Something moves in the shadows ahead.",
        ],
    },
]

# NPC name parts for procedural generation
NPC_ADJECTIVES = [
    "Abend", "Chromeo", "Neon", "Shadow", "Binary", "Cyber", "Dark", "Electric",
    "Glitch", "Hollow", "Iron", "Jacked", "Knotted", "Laser-brain", "Malware",
    "Neural", "Optic", "Phantom", "Quantum", "Rogue", "Static", "Turbo",
    "Void", "Wired", "Xeno", "Zero", "Blazed", "Corroded", "Digital",
]
NPC_NOUNS = [
    "Runner", "Hound", "Ghost", "Pilot", "Razor", "Strike", "Pulse",
    "Wraith", "Shade", "Spy", "Drone", "Bot", "Hunter", "Stalker",
    "Phantom", "Reaper", "Hacker", "Fixer", "Dealer", "Thug",
    "Sentinel", "Ward", "Guard", "Scout", "Flayer", "Spinner",
]


class Command(BaseCommand):
    help = "Procedurally generate the Cyberpunk world"

    def add_arguments(self, parser):
        parser.add_argument('--seed', type=int, default=None)
        parser.add_argument('--rooms', type=int, default=40)
        parser.add_argument('--zones', type=int, default=5)

    def handle(self, *args, **kwargs):
        seed = kwargs.get('seed') or random.randint(1, 999999)
        num_rooms = kwargs.get('rooms')
        num_zones = min(kwargs.get('zones'), len(ZONE_TEMPLATES))
        random.seed(seed)

        self.stdout.write(f"Seed: {seed}")
        self.stdout.write("Purging existing grid data...")
        NPC.objects.all().delete()
        Room.objects.all().delete()
        Item.objects.all().delete()

        items = self._create_items()
        zones = ZONE_TEMPLATES[:num_zones]
        rooms = self._create_rooms(zones, num_rooms)
        self._create_npcs(rooms, zones, items)

        GameWorld.objects.all().delete()
        GameWorld.objects.create(
            seed=seed,
            total_rooms=Room.objects.count(),
            total_npcs=NPC.objects.count(),
            total_items=Item.objects.count(),
        )

        self.stdout.write(self.style.SUCCESS(
            f"Done: {Room.objects.count()} rooms, "
            f"{NPC.objects.count()} NPCs, {Item.objects.count()} items"
        ))

    def _create_items(self):
        pool = []
        for name, desc, atk, price, rarity in WEAPON_TABLE:
            pool.append(Item.objects.create(
                name=name, description=desc, item_type='weapon',
                attack_bonus=atk, price=price, rarity=rarity))
        for name, desc, dfn, price, rarity in ARMOR_TABLE:
            pool.append(Item.objects.create(
                name=name, description=desc, item_type='armor',
                defense_bonus=dfn, price=price, rarity=rarity))
        for name, desc, price, rarity, heal in CONSUMABLE_TABLE:
            pool.append(Item.objects.create(
                name=name, description=desc, item_type='consumable',
                price=price, rarity=rarity, heal_amount=heal))
        for name, desc, price, rarity in MISC_TABLE:
            pool.append(Item.objects.create(
                name=name, description=desc, item_type='misc',
                price=price, rarity=rarity))
        return pool

    def _create_rooms(self, zones, target_count):
        all_rooms = []
        opp = {"north": "south", "south": "north", "east": "west", "west": "east"}

        # Hub
        hub = Room.objects.create(
            id=1, name="The Neon Hub",
            description="Central nerve center. Terminals flicker with green text. "
                        "The air hums with data. All paths lead outward from here.",
            safe_zone=True, shop_name="Central Exchange",
            zone="hub", theme="urban", map_x=0, map_y=0)
        all_rooms.append(hub)

        rooms_per_zone = max(3, target_count // len(zones))
        current_entry = hub
        x_pos = 0

        for zone in zones:
            x_pos += 1
            zone_rooms = []
            count = rooms_per_zone + (1 if len(zone_rooms) == 0 else 0)

            # Entry room
            entry = Room.objects.create(
                name=f"{zone['name']} - Entry",
                description=f"Entry to {zone['name']}. {zone['desc']}",
                zone=zone['zone_id'], theme=zone['theme'],
                map_x=x_pos, map_y=0)
            if zone.get('shop'):
                entry.shop_name = zone['shop']
            entry.save()

            # Connect hub/previous to entry
            dirs = [d for d in ["north", "south", "east", "west"] if d not in current_entry.exits]
            if dirs:
                d = random.choice(dirs)
                current_entry.exits[d] = entry.id
                entry.exits[opp[d]] = current_entry.id
                current_entry.save()
                entry.save()

            zone_rooms.append(entry)
            prev = entry

            for i in range(1, count):
                rname = f"{zone['name']} - {random.choice(zone['room_names'])} {chr(64+i)}"
                detail = random.choice(zone['room_details'])
                rdesc = f"{zone['desc']} {detail}"
                new_room = Room.objects.create(
                    name=rname, description=rdesc,
                    zone=zone['zone_id'], theme=zone['theme'],
                    map_x=x_pos, map_y=i)

                dirs = [d for d in ["north", "south", "east", "west"] if d not in prev.exits]
                if dirs:
                    d = random.choice(dirs)
                    prev.exits[d] = new_room.id
                    new_room.exits[opp[d]] = prev.id
                    prev.save()
                    new_room.save()

                # Random cross-link
                if len(zone_rooms) > 2 and random.random() > 0.6:
                    other = random.choice(zone_rooms[:-1])
                    avail = [d for d in ["north", "south", "east", "west"]
                             if d not in new_room.exits and d not in other.exits]
                    if avail:
                        d = random.choice(avail)
                        new_room.exits[d] = other.id
                        other.exits[opp[d]] = new_room.id
                        new_room.save()
                        other.save()

                zone_rooms.append(new_room)
                prev = new_room

            all_rooms.extend(zone_rooms)
            current_entry = random.choice(zone_rooms[1:]) if len(zone_rooms) > 1 else entry

        return all_rooms

    def _create_npcs(self, rooms, zones, items):
        opp = {"north": "south", "south": "north", "east": "west", "west": "east"}
        zone_map = {z['zone_id']: z for z in zones}
        npc_count = 0

        for room in rooms:
            if room.safe_zone:
                continue
            zone = zone_map.get(room.zone, zones[0])
            if random.random() > 0.45:
                continue  # Skip ~55% of rooms

            lvl = random.randint(zone['min_lvl'], zone['max_lvl'])
            npc_type = random.choice(zone['npc_types'])
            adj = random.choice(NPC_ADJECTIVES)
            noun = random.choice(NPC_NOUNS)
            name = f"{zone['npc_prefix']} {adj} {noun}"
            if npc_type == "boss" or (lvl > zone['max_lvl'] - 1 and random.random() > 0.7):
                name = f"[BOSS] {name}"
                lvl += 3

            npc = NPC.objects.create(
                name=name,
                description=f"A hostile {npc_type} patrolling {zone['name']}.",
                location=room, attack=lvl * 5, defense=lvl * 2,
                hp=lvl * 20, hp_max=lvl * 20, lvl=lvl,
                money_drop=lvl * 10, exp_drop=lvl * 15,
                aggressive=(lvl > 2), npc_type=npc_type)
            if random.random() > 0.6:
                npc.drops.add(random.choice(items))
            npc_count += 1

            # Boss rooms sometimes get a second NPC
            if "BOSS" in name and random.random() > 0.5:
                adj2 = random.choice(NPC_ADJECTIVES)
                noun2 = random.choice(NPC_NOUNS)
                NPC.objects.create(
                    name=f"{zone['npc_prefix']} {adj2} {noun2} Elite",
                    description=f"Elite guard of {zone['name']}.",
                    location=room, attack=lvl * 4, defense=lvl * 3,
                    hp=lvl * 15, hp_max=lvl * 15, lvl=lvl,
                    money_drop=lvl * 8, exp_drop=lvl * 12,
                    aggressive=True, npc_type=npc_type)