import json
import random
from django.utils import timezone
from .models import Player, Room, NPC, Item, InventoryItem, ChatMessage

def get_status_str(player):
    # Prompt requested HP instead of Integrity
    status = f"HP:{player.hp}/{player.hp_max}|MA:{player.mana}/{player.mana_max}|LV:{player.lvl}|CR:{player.money}|EXP:{player.exp}"
    if player.addiction_points > 0:
        status += f"|ADDICT:{player.addiction_points}%"
    return status

def get_help(player):
    room = player.location
    sb = ["\n=== GRID COMMAND PROTOCOLS ==="]
    
    sb.append("L/LOOK        : Scan current sector")
    sb.append("WHO           : List active terminal nodes")
    sb.append("I/INVENTORY   : List equipped and stored hardware")
    sb.append("ST/STATUS     : Detailed user profile data")
    sb.append("SAY <msg>     : Broadcast to current sector")
    sb.append("HELP/?        : Display this manual")
    # MAP removed from help as requested
    sb.append("USE <item>    : Use hardware/consumable/drug/scroll")

    if room.exits:
        sb.append(f"MOV/DIRS      : Navigation: {', '.join(room.exits.keys()).upper()}")
    
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

    sb.append("\n=== CLASS ABILITIES ===")
    if player.game_class == 'Street Samurai':
        sb.append("  BLADE (Level 1)   : Precise physical strike")
        if player.lvl >= 5: sb.append("  ONI_STRIKE (Lv 5): Massive fire damage")
    elif player.game_class == 'Netrunner':
        sb.append("  HACK (Level 1)    : System water/ice damage")
        if player.lvl >= 5: sb.append("  OVERLOAD (Lv 5)  : Air damage pulse")
    elif player.game_class == 'Techie':
        sb.append("  CALIBRATE (Lv 1) : Earth damage via drones")
        if player.lvl >= 5: sb.append("  TURRET (Lv 5)    : Continuous physical fire")
    elif player.game_class == 'Medie':
        sb.append("  PATCH (Level 1)   : Biological repair (Heal)")
        if player.lvl >= 5: sb.append("  DETOX (Lv 5)     : Cleanse addiction points")
    elif player.game_class == 'Fixer':
        sb.append("  SCHEME (Level 1)  : Drain credits from target")
        if player.lvl >= 5: sb.append("  CALL_IN (Lv 5)   : Heavy air-strike damage")

    return "\n".join(sb)

def get_look(player):
    room = player.location
    if not room: return "THE VOID."
    
    sb = [f"\n[SECTOR] {room.name}"]
    sb.append(f"DATA: {room.description}")
    
    # NPCs appear above exits as requested
    npcs = NPC.objects.filter(location=room, hp__gt=0)
    if npcs.exists():
        sb.append("\nDETECTED ENTITIES:")
        for n in npcs:
            sb.append(f"  > {n.name} (Lvl {n.lvl}) - {n.description}")
    
    if room.exits:
        sb.append(f"\n[AVAILABLE EXITS: {', '.join(room.exits.keys()).upper()}]")
    
    items = room.items.all()
    for item in items:
        sb.append(f"[Hardware] {item.name} is here.")

    others = Player.objects.filter(location=room, online=True).exclude(id=player.id)
    for o in others:
        sb.append(f"[User] {o.user.username} is here.")
        
    return "\n".join(sb)

def process_addiction(player):
    output = ""
    if player.addiction_points > 0:
        player.withdrawal_timer += 1
        if player.withdrawal_timer > 15:
            dmg = random.randint(1, player.addiction_points // 4 + 1)
            player.hp -= dmg
            output += f"\n[WITHDRAWAL] Your systems are failing. -{dmg} HP."
            if player.hp <= 0:
                output += "\n[CRITICAL ERROR] SYSTEM FAILURE: OVERDOSE/WITHDRAWAL."
                player.hp = player.hp_max // 2
                player.money = max(0, player.money - 20)
                player.addiction_points = max(0, player.addiction_points - 20)
                player.location = Room.objects.get(id=1)
                output += "\nRebooted at The Neon Hub."
        
        if player.withdrawal_timer > 30:
            player.addiction_points = max(0, player.addiction_points - 1)
    player.save()
    return output

def move_player(player, direction):
    dir_map = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}
    direction = dir_map.get(direction, direction)
    
    if direction not in player.location.exits:
        return "PATH BLOCKED."
    
    # Stalking logic: NPC follows if player runs
    stalk_msg = ""
    if player.last_combat_npc and player.stalk_count > 0:
        npc = player.last_combat_npc
        if npc.hp > 0:
            npc.location = player.location
            npc.save()
            player.stalk_count -= 1
            stalk_msg = f"\n[ALERT] {npc.name} is following you!"
        else:
            player.last_combat_npc = None
            player.stalk_count = 0
            
    new_room_id = player.location.exits[direction]
    try:
        player.location = Room.objects.get(id=new_room_id)
        player.save()
        
        look_text = get_look(player)
        addiction_msg = process_addiction(player)
        
        # Auto-attack logic (Level 5+)
        auto_attack_msg = ""
        if not player.location.safe_zone:
            aggressive_npc = NPC.objects.filter(location=player.location, hp__gt=0, aggressive=True).first()
            if aggressive_npc and player.lvl >= 5:
                auto_attack_msg = f"\n[DANGER] {aggressive_npc.name} intercepts you!"
                auto_attack_msg += "\n" + attack_npc(player, aggressive_npc.name, is_auto=True)

        return look_text + stalk_msg + addiction_msg + auto_attack_msg
    except Room.DoesNotExist:
        return "NAVIGATION ERROR."

def calculate_damage(atk, dfn, element='physical', weakness='none', resistance='none'):
    base_dmg = max(1, atk - dfn // 2)
    dmg = random.randint(max(1, base_dmg - 2), base_dmg + 2)
    
    # Elemental RPS Logic: Fire > Air > Earth > Water > Fire
    strong_against = {'fire': 'air', 'air': 'earth', 'earth': 'water', 'water': 'fire'}
    
    if element != 'physical':
        if weakness == element or strong_against.get(element) == weakness:
            dmg = int(dmg * 1.5)
        elif resistance == element:
            dmg = int(dmg * 0.5)
            
    return dmg

def attack_npc(player, target_name, is_auto=False):
    if not target_name: return "Specify target."
    npc = NPC.objects.filter(location=player.location, name__icontains=target_name, hp__gt=0).first()
    if not npc: return "Target not found."

    output = ""
    # Automatic combat loop
    # In a real-time system this would be separate, but here we'll do rounds
    # To satisfy "automatic until run", we'll do up to 5 rounds per command
    # or until someone dies.
    rounds = 1 if is_auto else 5
    
    for _ in range(rounds):
        # Player attacks NPC
        dmg = calculate_damage(player.attack, npc.defense, element='physical', weakness=npc.weakness, resistance=npc.resistance)
        npc.hp -= dmg
        npc.save()
        output += f"\nYou hit {npc.name} for {dmg} damage."

        if npc.hp <= 0:
            player.exp += npc.exp_drop
            player.money += npc.money_drop
            player.last_combat_npc = None
            player.stalk_count = 0
            player.save()
            output += f"\nTarget neutralized! +{npc.exp_drop} exp, +{npc.money_drop} credits."
            for item in npc.drops.all():
                ii, created = InventoryItem.objects.get_or_create(player=player, item=item)
                if not created: ii.quantity += 1
                ii.save()
                output += f"\nRetrieved: {item.name}"
            output += check_level_up(player)
            break
        
        # NPC attacks Player (FIX: Damage applied to HP)
        npc_dmg = calculate_damage(npc.attack, player.defense, element=npc.element)
        player.hp -= npc_dmg
        player.save()
        output += f"\n{npc.name} hits you for {npc_dmg} damage."
        
        if player.hp <= 0:
            output += "\n[CRITICAL ERROR] SYSTEM RESET."
            player.hp = player.hp_max // 2
            player.money = max(0, player.money - 10)
            player.location = Room.objects.get(id=1)
            player.last_combat_npc = None
            player.stalk_count = 0
            player.save()
            output += "\nRespawned at The Neon Hub. Lost 10 credits."
            break
            
        if not is_auto:
            player.last_combat_npc = npc
            player.stalk_count = 4 # Follow for up to 4 rooms
            player.save()

    return output

def use_ability(player, ability_name, target_name):
    ability_name = ability_name.lower()
    npc = None
    if target_name:
        npc = NPC.objects.filter(location=player.location, name__icontains=target_name, hp__gt=0).first()

    cost = 5
    if player.mana < cost: return "INSUFFICIENT BUFFER (MANA)."
    
    player.mana -= cost
    player.save()
    
    res = f"You use {ability_name.upper()}."
    
    # Simple ability logic
    if ability_name in ['blade', 'oni_strike']:
        if not npc: return "Target required."
        element = 'physical' if ability_name == 'blade' else 'fire'
        mult = 1.2 if ability_name == 'blade' else 2.5
        dmg = calculate_damage(int(player.attack * mult), npc.defense, element=element, weakness=npc.weakness, resistance=npc.resistance)
        npc.hp -= dmg
        npc.save()
        res += f"\n{npc.name} takes {dmg} {element} damage!"
    elif ability_name in ['hack', 'overload']:
        if not npc: return "Target required."
        element = 'water' if ability_name == 'hack' else 'air'
        dmg = calculate_damage(int(player.int_stat * 2), npc.defense, element=element, weakness=npc.weakness, resistance=npc.resistance)
        npc.hp -= dmg
        npc.save()
        res += f"\n{npc.name} system corrupted for {dmg} {element} damage!"
    elif ability_name == 'patch':
        heal = 20 + player.int_stat
        player.hp = min(player.hp_max, player.hp + heal)
        player.save()
        res += f"\nRepaired systems for {heal} HP."
    elif ability_name == 'detox':
        player.addiction_points = max(0, player.addiction_points - 15)
        player.save()
        res += "\nSystem flushed of toxins."
    elif ability_name == 'scheme':
        if not npc: return "Target required."
        stolen = random.randint(1, 10) + player.cha_stat // 2
        player.money += stolen
        player.save()
        res += f"\nDrained {stolen} credits from {npc.name}."
    else:
        res = "Ability not recognized or not available for your class."

    # If NPC still alive, it fights back
    if npc and npc.hp > 0:
        npc_dmg = calculate_damage(npc.attack, player.defense, element=npc.element)
        player.hp -= npc_dmg
        player.save()
        res += f"\n{npc.name} counters for {npc_dmg} damage!"
        
    return res

def use_item(player, item_name):
    if not item_name: return "Use what?"
    ii = InventoryItem.objects.filter(player=player, item__name__icontains=item_name).first()
    if not ii: return "Not in inventory."
        
    item = ii.item
    output = f"You use {item.name}."
    
    if item.item_type == 'consumable':
        if item.heal_amount > 0:
            player.hp = min(player.hp_max, player.hp + item.heal_amount)
            output += f"\nRestored HP. ({player.hp}/{player.hp_max})"
    elif item.item_type == 'drug':
        player.hp = min(player.hp_max + 10, player.hp + 30)
        player.withdrawal_timer = 0
        if random.random() < item.addiction_chance:
            player.addiction_points += 15
            output += "\n[DANGER] Neuro-dependency increased."
        output += "\nNeural spike detected. Efficiency increased."
    elif item.item_type == 'scroll':
        target_room = item.warp_to_room or Room.objects.get(id=1)
        player.location = target_room
        player.save()
        return output + f"\n[TELEPORT] Transferred to {player.location.name}.\n" + get_look(player)

    ii.quantity -= 1
    if ii.quantity <= 0: ii.delete()
    else: ii.save()
    player.save()
    return output

def get_map_data(player):
    room = player.location
    if not room: return "[]"
    visited = set()
    to_visit = [(room, 0)]
    room_data = []
    while to_visit:
        r, depth = to_visit.pop(0)
        if r.id in visited or depth > 4: continue
        visited.add(r.id)
        room_data.append({
            'id': r.id, 'name': r.name, 
            'x': r.map_x, 'y': -r.map_y, # Flip Y: North (+Y) is Up (-Y in screen space)
            'current': (r.id == room.id),
            'players': Player.objects.filter(location=r, online=True).count(),
            'npcs': NPC.objects.filter(location=r, hp__gt=0).count(),
            'safe': r.safe_zone,
        })
        for direction, rid in r.exits.items():
            try:
                nr = Room.objects.get(id=rid)
                if nr.id not in visited: to_visit.append((nr, depth + 1))
            except Room.DoesNotExist: pass
    return json.dumps(room_data)

def get_status_detailed(player):
    sb = [f"\n=== User Profile: {player.user.username} ==="]
    sb.append(f"Level: {player.lvl} | Data (EXP): {player.exp}")
    sb.append(f"HP: {player.hp}/{player.hp_max} | Buffer (Mana): {player.mana}/{player.mana_max}")
    sb.append(f"Credits: {player.money}")
    sb.append(f"Path (Race): {player.race} | Class: {player.game_class}")
    if player.addiction_points > 0:
        sb.append(f"ADDICTION: {player.addiction_points}%")
    sb.append(f"Stats: STR:{player.str_stat} INT:{player.int_stat} WIL:{player.wil_stat} AGI:{player.agi_stat} HEA:{player.hea_stat}")
    sb.append(f"Combat: ATK:{player.attack} DEF:{player.defense}")
    return "\n".join(sb)

def check_level_up(player):
    output = ""
    while player.exp >= player.lvl * 120:
        player.exp -= player.lvl * 120
        player.lvl += 1
        player.hp_max += 20
        player.hp = player.hp_max
        player.mana_max += 10
        player.mana = player.mana_max
        player.attack += 4
        player.defense += 2
        player.save()
        output += f"\n*** LEVEL UP! Now level {player.lvl}! ***"
        if player.lvl == 5: output += "\n[NEW ABILITIES UNLOCKED! Type HELP for details]"
    return output

# Remaining utility functions
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
        eq = " [E]" if ii.equipped else ""
        qty = f" x{ii.quantity}" if ii.quantity > 1 else ""
        sb.append(f"  {ii.item.name}{qty}{eq}")
    return "\n".join(sb)

def get_item(player, item_name):
    if not item_name: return "Get what?"
    item = player.location.items.filter(name__icontains=item_name).first()
    if not item: return "Item not found."
    player.location.items.remove(item)
    ii, created = InventoryItem.objects.get_or_create(player=player, item=item)
    if not created: ii.quantity += 1
    ii.save()
    return f"Retrieved {item.name}."

def drop_item(player, item_name):
    if not item_name: return "Drop what?"
    ii = InventoryItem.objects.filter(player=player, item__name__icontains=item_name).first()
    if not ii: return "You don't have that."
    if ii.equipped: return "Unequip first."
    player.location.items.add(ii.item)
    name = ii.item.name
    if ii.quantity > 1:
        ii.quantity -= 1
        ii.save()
    else: ii.delete()
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
    ii, created = InventoryItem.objects.get_or_create(player=player, item=item)
    if not created:
        ii.quantity += 1
        ii.save()
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
    if ii.quantity > 1:
        ii.quantity -= 1
        ii.save()
    else: ii.delete()
    return f"Sold {name} for {price} credits."

def get_poll_data(player):
    cutoff = timezone.now() - timezone.timedelta(seconds=3)
    msgs = ChatMessage.objects.filter(room=player.location, timestamp__gt=cutoff).order_by('timestamp')
    chat = [{"player": m.sender.user.username, "message": m.message} for m in msgs]
    npcs = list(NPC.objects.filter(location=player.location, hp__gt=0).values('id', 'name', 'hp', 'hp_max', 'lvl'))
    room_items = list(player.location.items.all().values('id', 'name')) if player.location else []
    players_here = list(Player.objects.filter(location=player.location, online=True).exclude(id=player.id).values('id', 'user__username', 'lvl', 'game_class'))
    return {
        "chat": chat, "npcs": npcs, "items": room_items, "players": players_here,
        "status": get_status_str(player), "location": player.location.name if player.location else "Unknown",
    }
