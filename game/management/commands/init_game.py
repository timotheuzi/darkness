import random
from django.core.management.base import BaseCommand
from game.models import Room, NPC, Item

class Command(BaseCommand):
    help = 'Procedurally generate the CyberMUD world'

    def handle(self, *args, **kwargs):
        self.stdout.write("Purging existing grid data...")
        NPC.objects.all().delete()
        Room.objects.all().delete()
        Item.objects.all().delete()

        # 1. Base Hardware (Items)
        weapons = [
            Item.objects.create(name="Stun Baton", description="Standard issue security baton.", item_type="weapon", attack_bonus=5, price=50),
            Item.objects.create(name="Mono-Blade", description="Vibrating edge for clean cuts.", item_type="weapon", attack_bonus=12, price=300),
            Item.objects.create(name="Heavy Slugger", description="High-caliber kinetic pistol.", item_type="weapon", attack_bonus=20, price=750),
            Item.objects.create(name="Laser Drill", description="Industrial tool repurposed for violence.", item_type="weapon", attack_bonus=15, price=450),
        ]
        armors = [
            Item.objects.create(name="Mesh Vest", description="Basic kinetic protection.", item_type="armor", defense_bonus=8, price=150),
            Item.objects.create(name="Riot Shield", description="Heavily reinforced alloy.", item_type="armor", defense_bonus=20, price=1000),
            Item.objects.create(name="Synth-Leathers", description="Tough fabric for street life.", item_type="armor", defense_bonus=4, price=80),
        ]
        consumables = [
            Item.objects.create(name="Health Stim", description="Nanobot healing injection.", item_type="consumable", price=25),
            Item.objects.create(name="Data Spike", description="Temporary buffer boost.", item_type="consumable", price=60),
        ]

        # 2. Procedural Generation Config
        sectors = [
            {"name": "The Slums", "desc": "Gritty, rain-soaked streets and rusted pipes.", "min_lvl": 1, "max_lvl": 3},
            {"name": "Industrial Zone", "desc": "Hissing steam, clanking machinery, and toxic fumes.", "min_lvl": 3, "max_lvl": 6},
            {"name": "Corporate Plaza", "desc": "Clean, sterile, and heavily guarded glass towers.", "min_lvl": 6, "max_lvl": 10},
            {"name": "The Under-Grid", "desc": "Scrambled data-scapes and flickering holograms.", "min_lvl": 8, "max_lvl": 12},
        ]

        # Create The Neon Hub (Spawn)
        hub = Room.objects.create(
            id=1,
            name="The Neon Hub",
            description="The central nerve center of the grid. All nodes start here. Terminals flicker with green text.",
            safe_zone=True,
            shop_name="Central Exchange"
        )
        hub.items.add(consumables[0]) # Start with stims in shop

        def connect_rooms(r1, r2, direction):
            opp = {"north": "south", "south": "north", "east": "west", "west": "east"}
            r1.exits[direction] = r2.id
            r2.exits[opp[direction]] = r1.id
            r1.save()
            r2.save()

        def get_random_dir(existing_exits):
            dirs = ["north", "south", "east", "west"]
            available = [d for d in dirs if d not in existing_exits]
            return random.choice(available) if available else None

        current_entry = hub
        all_rooms = [hub]

        self.stdout.write("Constructing sectors...")
        for sector_cfg in sectors:
            sector_rooms = []
            num_rooms = random.randint(5, 8)
            
            # Create first room of sector and connect to previous entry
            first_room = Room.objects.create(
                name=f"{sector_cfg['name']} - Entry Way",
                description=f"Entry point to {sector_cfg['name']}. {sector_cfg['desc']}"
            )
            d = get_random_dir(current_entry.exits)
            if d:
                connect_rooms(current_entry, first_room, d)
            
            sector_rooms.append(first_room)
            prev_room = first_room
            
            for i in range(num_rooms - 1):
                new_room = Room.objects.create(
                    name=f"{sector_cfg['name']} - Node {chr(65+i)}",
                    description=f"A sector of {sector_cfg['name']}. {sector_cfg['desc']}"
                )
                
                d = get_random_dir(prev_room.exits)
                if d:
                    connect_rooms(prev_room, new_room, d)
                else:
                    # If stuck, try to connect to any room in this sector
                    retry_room = random.choice(sector_rooms)
                    d = get_random_dir(retry_room.exits)
                    if d:
                        connect_rooms(retry_room, new_room, d)
                
                # Populating NPCs
                if random.random() > 0.4:
                    lvl = random.randint(sector_cfg['min_lvl'], sector_cfg['max_lvl'])
                    npc = NPC.objects.create(
                        name=f"{sector_cfg['name']} Drone #{random.randint(100, 999)}",
                        description=f"A hostile entity patrolling {sector_cfg['name']}.",
                        location=new_room,
                        attack=lvl * 5,
                        defense=lvl * 2,
                        hp=lvl * 20,
                        hp_max=lvl * 20,
                        lvl=lvl,
                        money_drop=lvl * 10,
                        exp_drop=lvl * 15,
                        aggressive=(lvl > 2)
                    )
                    # Random loot
                    if random.random() > 0.7:
                        npc.drops.add(random.choice(weapons + armors + consumables))

                sector_rooms.append(new_room)
                prev_room = new_room
            
            all_rooms.extend(sector_rooms)
            # Entry for next sector is a random room from this sector
            current_entry = random.choice(sector_rooms)

        self.stdout.write(self.style.SUCCESS(f"Successfully generated grid with {Room.objects.count()} nodes and {NPC.objects.count()} entities."))
