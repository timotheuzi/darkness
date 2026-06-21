from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    item_type = models.CharField(max_length=50)  # weapon, armor, consumable, misc, drug, scroll
    price = models.IntegerField(default=0)
    rarity = models.CharField(max_length=20, default='common')  # common, uncommon, rare, epic, legendary

    # Weapon/Armor stats
    attack_bonus = models.IntegerField(default=0)
    defense_bonus = models.IntegerField(default=0)
    speed_bonus = models.IntegerField(default=0)
    heal_amount = models.IntegerField(default=0)

    # Stat bonuses
    str_bonus = models.IntegerField(default=0)
    int_bonus = models.IntegerField(default=0)
    wil_bonus = models.IntegerField(default=0)
    agi_bonus = models.IntegerField(default=0)
    hea_bonus = models.IntegerField(default=0)
    cha_bonus = models.IntegerField(default=0)
    
    # Elemental stats
    element = models.CharField(max_length=20, default='physical') # physical, fire, water, earth, air
    
    # Drug/Scroll effects
    addiction_chance = models.FloatField(default=0.0)
    warp_to_room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True, related_name='warp_items')

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    exits = models.JSONField(default=dict)
    shop_name = models.CharField(max_length=255, null=True, blank=True)
    safe_zone = models.BooleanField(default=False)
    zone = models.CharField(max_length=100, default='hub')  # zone identifier
    theme = models.CharField(max_length=100, default='urban')  # visual theme
    map_x = models.IntegerField(default=0)  # grid position for map
    map_y = models.IntegerField(default=0)
    items = models.ManyToManyField(Item, blank=True, related_name='rooms')
    # Procedural flags
    respawn_npcs = models.BooleanField(default=True)
    respawn_timer = models.IntegerField(default=300)  # seconds until NPC respawn
    last_npc_spawn = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lvl = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    money = models.IntegerField(default=25)
    hp = models.IntegerField(default=100)
    hp_max = models.IntegerField(default=100)
    mana = models.IntegerField(default=20)
    mana_max = models.IntegerField(default=20)

    # Stats
    str_stat = models.IntegerField(default=10)
    int_stat = models.IntegerField(default=10)
    wil_stat = models.IntegerField(default=10)
    agi_stat = models.IntegerField(default=10)
    hea_stat = models.IntegerField(default=10)
    cha_stat = models.IntegerField(default=10)
    
    stat_points = models.IntegerField(default=0)

    attack = models.IntegerField(default=10)
    defense = models.IntegerField(default=5)

    location = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    race = models.CharField(max_length=50) # Cyborg, Bio-hacked, Android, Mutant, PureBlood
    game_class = models.CharField(max_length=50) # Street Samurai, Netrunner, Techie, Medie, Fixer
    online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    # Karma / alignment
    karma = models.IntegerField(default=0)

    inventory = models.ManyToManyField(Item, through='InventoryItem')
    
    # Drug/Addiction System
    addiction_points = models.IntegerField(default=0) # 0 to 100
    withdrawal_timer = models.IntegerField(default=0) # ticks since last use
    
    # Combat/Stalking state
    last_combat_npc = models.ForeignKey('NPC', on_delete=models.SET_NULL, null=True, blank=True, related_name='stalking_players')
    stalk_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class InventoryItem(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    equipped = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)


class NPC(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(Room, on_delete=models.CASCADE)
    attack = models.IntegerField()
    defense = models.IntegerField()
    hp = models.IntegerField()
    hp_max = models.IntegerField()
    lvl = models.IntegerField()
    money_drop = models.IntegerField()
    exp_drop = models.IntegerField()
    aggressive = models.BooleanField(default=True)
    npc_type = models.CharField(max_length=50, default='drone')  # drone, gang, corporate, boss
    respawnable = models.BooleanField(default=True)
    
    # Elemental system
    element = models.CharField(max_length=20, default='physical')
    weakness = models.CharField(max_length=20, default='none')
    resistance = models.CharField(max_length=20, default='none')

    drops = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    sender = models.ForeignKey(Player, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']


class GameWorld(models.Model):
    """Singleton model to store world generation metadata."""
    seed = models.IntegerField(default=0)
    generated_at = models.DateTimeField(auto_now=True)
    total_rooms = models.IntegerField(default=0)
    total_npcs = models.IntegerField(default=0)
    total_items = models.IntegerField(default=0)
    version = models.IntegerField(default=1)
