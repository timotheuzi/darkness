#!/usr/bin/env python3
"""
Clean world data while preserving human players.
Deletes bots, rooms, NPCs, and items for a fresh world generation.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from game.models import (
    Player,
    NPC,
    Room,
    Item,
    ChatMessage,
    ProceduralWeaponSpawn,
    Party,
    GameWorld,
)


class Command(BaseCommand):
    help = "Clean all world data (bots, maps, NPCs, items) while preserving human players"

    def add_arguments(self, parser):
        parser.add_argument(
            "--confirm", action="store_true", help="Confirm deletion without prompt"
        )
        parser.add_argument(
            "--keep-players", action="store_true", help="Keep all players (both human and bot)"
        )

    def handle(self, *args, **kwargs):
        keep_players = kwargs.get("keep_players", False)

        if not kwargs.get("confirm"):
            if keep_players:
                self.stdout.write("WARNING: This will delete ALL rooms, NPCs, and items.")
                self.stdout.write("ALL players (both human and bot) will be preserved.")
            else:
                self.stdout.write("WARNING: This will delete ALL bots, rooms, NPCs, and items.")
                self.stdout.write(
                    "Human players will be preserved but their inventory will be cleared."
                )
            confirm = input("Are you sure? (yes/no): ")
            if confirm.lower() != "yes":
                self.stdout.write("Aborted.")
                return

        with transaction.atomic():
            self.stdout.write("Cleaning world data...")

            # Delete all bots (unless --keep-players is set)
            if not keep_players:
                bot_count = Player.objects.filter(is_bot=True).count()
                Player.objects.filter(is_bot=True).delete()
                self.stdout.write(f"Deleted {bot_count} bots")
            else:
                # Reset all players to hub and clear combat state
                all_players = Player.objects.all()
                for player in all_players:
                    player.location = Room.objects.filter(id=1).first()
                    player.last_combat_npc = None
                    player.last_combat_player = None
                    player.auto_attack = False
                    player.resting = False
                    player.hidden = False
                    player.notification = ""
                    player.party_invite = None
                    player.save()
                self.stdout.write(f"Reset {all_players.count()} players to hub")

            # Delete all NPCs
            npc_count = NPC.objects.count()
            NPC.objects.all().delete()
            self.stdout.write(f"Deleted {npc_count} NPCs")

            # Delete all rooms (except hub if it exists)
            room_count = Room.objects.exclude(id=1).count()
            Room.objects.exclude(id=1).delete()
            self.stdout.write(f"Deleted {room_count} rooms")

            # Delete only items not owned by players (preserve player inventory items)
            items_to_delete = Item.objects.exclude(inventoryitem__player__isnull=False)
            item_count = items_to_delete.count()
            items_to_delete.delete()
            self.stdout.write(f"Deleted {item_count} unowned items (preserved player items)")

            # Now clear player inventories (items still exist, just not linked)
            if not keep_players:
                human_players = Player.objects.filter(is_bot=False)
                for player in human_players:
                    player.inventory.clear()
                self.stdout.write(f"Reset {human_players.count()} human players")

            # Delete chat messages
            chat_count = ChatMessage.objects.count()
            ChatMessage.objects.all().delete()
            self.stdout.write(f"Deleted {chat_count} chat messages")

            # Delete procedural weapon spawns
            spawn_count = ProceduralWeaponSpawn.objects.count()
            ProceduralWeaponSpawn.objects.all().delete()
            self.stdout.write(f"Deleted {spawn_count} procedural spawns")

            # Delete parties
            party_count = Party.objects.count()
            Party.objects.all().delete()
            self.stdout.write(f"Deleted {party_count} parties")

            # Delete game world metadata
            GameWorld.objects.all().delete()

            self.stdout.write(
                self.style.SUCCESS("World cleaned successfully. Run 'make init' to regenerate.")
            )
