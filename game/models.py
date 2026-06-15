from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    item_type = models.CharField(max_length=50) # weapon, armor, consumable, misc
    price = models.IntegerField(default=0)
    
    # Weapon/Armor stats
    attack_bonus = models.IntegerField(default=0)
    defense_bonus = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    exits = models.JSONField(default=dict)
    shop_name = models.CharField(max_length=255, null=True, blank=True)
    safe_zone = models.BooleanField(default=False)
    items = models.ManyToManyField(Item, blank=True, related_name='rooms')

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
    
    attack = models.IntegerField(default=10)
    defense = models.IntegerField(default=5)
    
    location = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    race = models.CharField(max_length=50)
    game_class = models.CharField(max_length=50)
    online = models.BooleanField(default=False)
    
    inventory = models.ManyToManyField(Item, through='InventoryItem')

    def __str__(self):
        return self.user.username

class InventoryItem(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    equipped = models.BooleanField(default=False)

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
    
    drops = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    sender = models.ForeignKey(Player, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
