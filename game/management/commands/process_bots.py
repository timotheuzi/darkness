#!/usr/bin/env python3
"""
Bot AI Processor - Runs continuously to make bots act like human players.
Run this as a background daemon: python manage.py process_bots
"""
import random
import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from game.models import Player, Room, NPC, Item, InventoryItem, Party, PartyMembership
from game import services


class Command(BaseCommand):
    help = "Process AI behavior for all online bots (runs continuously)"

    def handle(self, *args, **kwargs):
        self.stdout.write("Bot AI processor starting...")
        
        try:
            while True:
                # Get all online bots
                bots = Player.objects.filter(is_bot=True, online=True)
                
                if bots.exists():
                    actions_taken = 0
                    
                    for bot in bots:
                        # Use the existing process_bot_ai function
                        # It now handles combat ticks for bots in combat
                        result = services.process_bot_ai(bot)
                        
                        if result:
                            actions_taken += 1
                    
                    if actions_taken > 0:
                        self.stdout.write(f"[{timezone.now().strftime('%H:%M:%S')}] Processed {actions_taken} bot actions")
                
                # Sleep for 3 seconds before next tick
                time.sleep(3)
                
        except KeyboardInterrupt:
            self.stdout.write("\nBot AI processor stopped.")