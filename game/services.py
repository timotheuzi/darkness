import json
from django.utils import timezone
from .models import Player, Room, NPC, Item, InventoryItem, ChatMessage

def get_status_str(player):
    return f"HP:{player.hp}/{player.hp_max}|MA:{player.mana}/{player.mana_max}|LV:{player.lvl}|CR:{player.money}|BSY:0"

def get_help(player):
    room = player.location
    sb = ["\n=== GRID COMMAND PROTOCOLS ==="]
    
    sb.append("L/LOOK        : Scan current sector")
    sb.append("WHO           : List active terminal nodes")
    sb.append("I/INVENTORY   : List equipped and stored hardware")
    sb.append("ST/STATUS     : Detailed user profile data")
    sb.append("SAY <msg>     : Broadcast to current sector")
    sb.append("HELP/?        : Display this manual")

    if room.exits:
        sb.append(f"MOV/DIRS      : Navigation available: {', '.join(room.exits.keys()).upper()}")
    
    if room.items.exists():
        sb.append("G/GET <item>  : Retrieve hardware from ground")
    
    npcs = NPC.objects.filter(location=room, hp__gt=0)
    if npcs.exists():
        npc_names = ", ".join([n.name for n in npcs])
        sb.append(f"A/KILL <target>: Combat mode (Targets: {npc_names})")
    
    if InventoryItem.objects.filter(player=player).exists():
        sb.append("EQUIP <item>  : Attach/Detach hardware")
        sb.append("DROP <item>   : Discard hardware in current sector")
    
    if room.shop_name:
        sb.append(f"LIST/LI       : View {room.shop_name} catalog")
        sb.append("BUY <item>    : Purchase hardware")
        sb.append("SELL <item>   : Liquidate hardware for credits")

    return "\n".join(sb)

def get_look(player):
    room = player.location
    if not room: return "THE VOID."
    
    sb = [f"\n[Location] {room.name}", f"{room.description}\n"]
    
    if room.exits:
        sb.append(f"[Exits: {', '.join(room.exits.keys())}]")
    
    items = room.items.all()
    for item in items:
        sb.append(f"[Hardware] {item.name} is here.")

    others = Player.objects.filter(location=room, online=True).exclude(id=player.id)
    for o in others:
        sb.append(f"[User] {o.user.username} is here.")
        
    npcs = NPC.objects.filter(location=room, hp__gt=0)
    for n in npcs:
        sb.append(f"[Entity] {n.name} (Lvl {n.lvl}) is here.")
        
    return "\n".join(sb)

def move_player(player, direction):
    dir_map = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}
    direction = dir_map.get(direction, direction)
    
    if direction not in player.location.exits:
        return "PATH BLOCKED."
    
    new_room_id = player.location.exits[direction]
    try:
        player.location = Room.objects.get(id=new_room_id)
        player.save()
        return get_look(player)
    except Room.DoesNotExist:
        return "NAVIGATION ERROR."

def attack_npc(player, target_name):
    if not target_name: return "Specify target."
    npc = NPC.objects.filter(location=player.location, name__icontains=target_name, hp__gt=0).first()
    if not npc: return "Target not found."
    
    dmg = max(1, player.attack - npc.defense // 2)
    npc.hp -= dmg
    npc.save()
    output = f"You hit {npc.name} for {dmg} damage."
    
    if npc.hp <= 0:
        player.exp += npc.exp_drop
        player.money += npc.money_drop
        player.save()
        output += f"\nTarget neutralized! Gained {npc.exp_drop} exp and {npc.money_drop} credits."
        for item in npc.drops.all():
            InventoryItem.objects.create(player=player, item=item)
            output += f"\nRetrieved: {item.name}"
    else:
        npc_dmg = max(1, npc.attack - player.defense // 2)
        player.hp -= npc_dmg
        player.save()
        output += f"\n{npc.name} hits you for {npc_dmg} damage."
        if player.hp <= 0:
            output += "\nCRITICAL ERROR: SYSTEM RESET."
            player.hp = player.hp_max // 2
            player.location = Room.objects.get(id=1)
            player.save()
    return output

def handle_say(player, message):
    if not message: return "Say what?"
    ChatMessage.objects.create(sender=player, room=player.location, message=message)
    return f"You broadcast: {message}"

def get_recent_chat(player):
    cutoff = timezone.now() - timezone.timedelta(seconds=30)
    msgs = ChatMessage.objects.filter(room=player.location, timestamp__gt=cutoff).exclude(sender=player).order_by('timestamp')
    if not msgs: return ""
    return "\n".join([f"[Broadcast] {m.sender.user.username}: {m.message}" for m in msgs])

def get_inventory(player):
    items = InventoryItem.objects.filter(player=player)
    if not items.exists(): return "Memory slots empty."
    sb = ["\n=== Hardware Inventory ==="]
    for ii in items:
        sb.append(f"  {ii.item.name} {'(EQUIPPED)' if ii.equipped else ''}")
    return "\n".join(sb)

def get_status_detailed(player):
    return (f"\n=== User Profile: {player.user.username} ===\n"
            f"Level: {player.lvl} | Data: {player.exp}\n"
            f"Integrity: {player.hp}/{player.hp_max} | Buffer: {player.mana}/{player.mana_max}\n"
            f"Credits: {player.money}\n"
            f"Path: {player.race} | Class: {player.game_class}\n"
            f"Stats: STR:{player.str_stat} INT:{player.int_stat} WIL:{player.wil_stat} AGI:{player.agi_stat} HEA:{player.hea_stat}\n"
            f"Combat: ATK:{player.attack} DEF:{player.defense}")

def get_item(player, item_name):
    if not item_name: return "Get what?"
    item = player.location.items.filter(name__icontains=item_name).first()
    if not item: return "Item not found."
    player.location.items.remove(item)
    InventoryItem.objects.create(player=player, item=item)
    return f"Retrieved {item.name}."

def drop_item(player, item_name):
    if not item_name: return "Drop what?"
    ii = InventoryItem.objects.filter(player=player, item__name__icontains=item_name).first()
    if not ii: return "You don't have that."
    if ii.equipped: return "Unequip first."
    player.location.items.add(ii.item)
    name = ii.item.name
    ii.delete()
    return f"Discarded {name}."

def equip_item(player, item_name):
    if not item_name: return "Equip what?"
    ii = InventoryItem.objects.filter(player=player, item__name__icontains=item_name).first()
    if not ii: return "Not in inventory."
    if ii.equipped:
        ii.equipped = False
        player.attack -= ii.item.attack_bonus
        player.defense -= ii.item.defense_bonus
        ii.save()
        player.save()
        return f"Unequipped {ii.item.name}."
    
    if ii.item.item_type == 'weapon':
        old = InventoryItem.objects.filter(player=player, equipped=True, item__item_type='weapon').first()
        if old:
            player.attack -= old.item.attack_bonus
            old.equipped = False
            old.save()
    elif ii.item.item_type == 'armor':
        old = InventoryItem.objects.filter(player=player, equipped=True, item__item_type='armor').first()
        if old:
            player.defense -= old.item.defense_bonus
            old.equipped = False
            old.save()
            
    ii.equipped = True
    player.attack += ii.item.attack_bonus
    player.defense += ii.item.defense_bonus
    ii.save()
    player.save()
    return f"Equipped {ii.item.name}."

def list_shop(player):
    if not player.location.shop_name: return "No terminal shop detected."
    items = Item.objects.filter(price__gt=0)
    sb = [f"\n=== {player.location.shop_name} Inventory ==="]
    for item in items:
        sb.append(f"  {item.name:25} {item.price} CR")
    return "\n".join(sb)

def buy_item(player, item_name):
    if not player.location.shop_name: return "No shop here."
    item = Item.objects.filter(name__icontains=item_name, price__gt=0).first()
    if not item: return "Item not in database."
    if player.money < item.price: return "Insufficient credits."
    player.money -= item.price
    player.save()
    InventoryItem.objects.create(player=player, item=item)
    return f"Purchased {item.name}."

def sell_item(player, item_name):
    if not player.location.shop_name: return "No shop here."
    ii = InventoryItem.objects.filter(player=player, item__name__icontains=item_name).first()
    if not ii: return "You don't have that."
    if ii.equipped: return "Unequip first."
    price = ii.item.price // 2
    player.money += price
    player.save()
    name = ii.item.name
    ii.delete()
    return f"Sold {name} for {price} credits."
