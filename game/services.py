import json
import random
from django.utils import timezone
from .models import Player, Room, NPC, Item, InventoryItem, ChatMessage

# Class Ability Definitions - Learned every 4 levels until Lv 29
CLASS_MOVES = {
    'Street Samurai': [
        (1, 'blade', 'Precise physical strike'),
        (5, 'oni_strike', 'Massive fire damage'),
        (9, 'zansetsu', 'High-critical physical strike'),
        (13, 'mirage', 'Boost defense significantly'),
        (17, 'whirlwind', 'Multiple physical strikes'),
        (21, 'dragon_lunge', 'Heavy fire-elemental pierce'),
        (25, 'bladestorm', 'Massive AOE physical damage'),
        (29, 'omnislash', 'Ultimate physical combo'),
    ],
    'Netrunner': [
        (1, 'hack', 'System water/ice damage'),
        (5, 'overload', 'High air damage pulse'),
        (9, 'synapse_burn', 'Burn target memory (Fire)'),
        (13, 'logic_bomb', 'Heavy air system corruption'),
        (17, 'blackout', 'Lower target attack and defense'),
        (21, 'databreach', 'Siphon credits and deal damage'),
        (25, 'icebreaker', 'Massive water damage strike'),
        (29, 'zero_day', 'Critical system failure damage'),
    ],
    'Techie': [
        (1, 'calibrate', 'Earth damage via drones'),
        (5, 'turret', 'Continuous physical fire'),
        (9, 'overclock', 'Boost attack and speed'),
        (13, 'nanobot_swarm', 'Continuous healing and earth damage'),
        (17, 'plasma_arc', 'Heavy fire damage'),
        (21, 'tesla_coil', 'Stun target and air damage'),
        (25, 'orbital_strike', 'Massive air damage'),
        (29, 'singularity', 'Ultimate gravity collapse (Earth)'),
    ],
    'Medie': [
        (1, 'patch', 'Biological repair (Heal)'),
        (5, 'detox', 'Cleanse addiction points'),
        (9, 'adrenaline', 'Boost attack and speed'),
        (13, 'biocortical_shock', 'High water damage to nervous system'),
        (17, 'regeneration', 'Powerful over-time healing'),
        (21, 'viral_burst', 'Heavy rot damage over time'),
        (25, 'resuscitate', 'Restore massive HP and clear status'),
        (29, 'nanomachine_army', 'Ultimate survival and damage boost'),
    ],
    'Fixer': [
        (1, 'scheme', 'Drain credits from target'),
        (5, 'call_in', 'Heavy air-strike damage'),
        (9, 'bribe', 'Lower target defense with credits'),
        (13, 'contract_kill', 'Execute high physical damage'),
        (17, 'market_crash', 'Siphon massive credits'),
        (21, 'reinforcements', 'Summon allies for extra hits'),
        (25, 'insider_trading', 'Gain stats and damage boost'),
        (29, 'hostile_takeover', 'Ultimate credit and soul drain'),
    ],
    'Thief': [
        (1, 'backstab', 'Critical physical strike from the shadows'),
        (4, 'stealth', 'Become hidden from sight with high success rate'),
        (9, 'poison_dart', 'Earth damage over time'),
        (13, 'smoke_bomb', 'Massive defense boost'),
        (17, 'shadow_strike', 'Critical physical hit from stealth'),
        (21, 'assassinate', 'Execute target with low HP'),
        (25, 'ghost_protocol', 'Immunity to damage for one turn'),
        (29, 'death_mark', 'Ultimate physical assassination'),
    ],
    'Heavy': [
        (1, 'smash', 'Heavy physical damage'),
        (5, 'taunt', 'Lower target defense'),
        (9, 'iron_skin', 'Boost defense significantly'),
        (13, 'seismic_toss', 'Heavy earth damage'),
        (17, 'juggernaut', 'Boost attack and defense'),
        (21, 'avalanche', 'Massive earth AOE'),
        (25, 'colossus_strike', 'Unstoppable physical force'),
        (29, 'earthshaker', 'Ultimate earth-shattering blow'),
    ],
    'Psycher': [
        (1, 'mind_bolt', 'Will-based energy damage'),
        (5, 'soul_drain', 'Damage target, heal self'),
        (9, 'psionic_shield', 'Boost defense with mind power'),
        (13, 'pyrokinesis', 'Massive fire mind damage'),
        (17, 'telekinesis', 'High physical mind damage'),
        (21, 'mind_control', 'Target hits themselves'),
        (25, 'astral_projection', 'Massive air damage'),
        (29, 'soul_annihilation', 'Ultimate psychic collapse'),
    ],
    'Warlock': [
        (1, 'curse', 'Weaken target (Attack/HP)'),
        (5, 'chaos_bolt', 'Random high-energy surge'),
        (9, 'blood_pact', 'Sacrifice HP for massive damage'),
        (13, 'shadow_bolt', 'Dark water damage'),
        (17, 'necrosis', 'High rot damage over time'),
        (21, 'demonic_tether', 'Siphon HP and Mana'),
        (25, 'abyssal_rift', 'Massive fire/dark damage'),
        (29, 'armageddon', 'Ultimate chaotic destruction'),
    ],
    'Priest': [
        (1, 'heal', 'Holy restoration of HP'),
        (5, 'bless', 'Fortify soul (Defense/Attack)'),
        (9, 'purify', 'Clear addiction and heal'),
        (13, 'holy_fire', 'Fire damage to the wicked'),
        (17, 'divine_shield', 'Invulnerability for one turn'),
        (21, 'judgment', 'Massive air damage based on karma'),
        (25, 'resurrection', 'Full HP recovery'),
        (29, 'heavenly_ascent', 'Ultimate divine power'),
    ],
    'Trickster': [
        (1, 'bamboozle', 'Confuse target (Lower Defense)'),
        (4, 'sneak', 'Attempt to hide in the shadows'),
        (5, 'jackpot', 'Massive damage or credits'),
        (9, 'sleight_of_hand', 'Steal item or credits'),
        (13, 'mirror_image', 'Boost defense significantly'),
        (17, 'wild_card', 'Random effect from any class'),
        (21, 'gaslight', 'Lower all target stats'),
        (25, 'grand_illusion', 'Stun and massive damage'),
        (29, 'royal_flush', 'Ultimate luck-based destruction'),
    ]
}

def get_reputation_title(karma):
    if karma >= 80: return "Saint"
    if karma >= 50: return "Paragon"
    if karma >= 20: return "Lawful"
    if karma > -20: return "Neutral"
    if karma > -50: return "Renegade"
    if karma > -80: return "Outlaw"
    return "Utter Villain"

def get_status_str(player):
    rep = get_reputation_title(player.karma)
    status = f"HP:{player.hp}/{player.hp_max}|MA:{player.mana}/{player.mana_max}|LV:{player.lvl}|CR:{player.money}|[{rep}]"
    if player.stat_points > 0:
        status += f"|STATS:{player.stat_points}"
    if player.addiction_points > 0:
        status += f"|ADDICT:{player.addiction_points}%"
    return status

def get_help(player):
    room = player.location
    sb = ["\n=== GRID COMMAND PROTOCOLS ==="]
    
    sb.append("L/LOOK        : Scan current sector")
    sb.append("L/LOOK <target>: Examine entity or item")
    sb.append("WHO           : List active terminal nodes")
    sb.append("TOP           : Display top 10 adventurers")
    sb.append("I/INVENTORY   : List equipped and stored hardware")
    sb.append("ST/STATUS     : Detailed user profile data")
    sb.append("SAY <msg>     : Broadcast to current sector")
    sb.append("HELP/?        : Display this manual")
    sb.append("USE <item>    : Use hardware/consumable/drug/scroll")
    sb.append("TRAIN <stat>  : Spend stat points (STR, INT, WIL, AGI, HEA, CHA)")
    sb.append("EXIT          : Log out and disconnect from the grid")

    if room.exits:
        sb.append(f"MOV/DIRS      : Navigation: {', '.join(room.exits.keys()).upper()}")
    
    if room.items.exists():
        sb.append("G/GET <item>  : Retrieve hardware from ground")
    
    npcs_exist = NPC.objects.filter(location=room, hp__gt=0).exists()
    players_exist = Player.objects.filter(location=room, online=True).exclude(id=player.id).exists()
    if npcs_exist or players_exist:
        sb.append(f"A/KILL <target>: Combat mode (NPCs or Users +/- 3 Lvls)")
    
    if InventoryItem.objects.filter(player=player).exists():
        sb.append("EQUIP <item>  : Attach/Detach hardware")
        sb.append("DROP <item>   : Discard hardware in current sector")
    
    if room.shop_name:
        sb.append(f"LIST/LI       : View {room.shop_name} catalog")
        sb.append("BUY <item>    : Purchase hardware")
        sb.append("SELL <item>   : Liquidate hardware for credits")
        
    dealer = NPC.objects.filter(location=room, npc_type='dealer', hp__gt=0).first()
    if dealer:
        sb.append(f"SELL <drug> to {dealer.name} : Illegal trade")

    sb.append("\n=== CLASS ABILITIES ===")
    moves = CLASS_MOVES.get(player.game_class, [])
    for lvl, name, desc in moves:
        if player.lvl >= lvl:
            sb.append(f"  {name.upper():15} (Lv {lvl}): {desc}")

    return "\n".join(sb)

def get_top_ten():
    top_players = Player.objects.order_by('-lvl', '-exp')[:10]
    sb = ["\n=== TOP 10 ADVENTURERS ==="]
    for i, p in enumerate(top_players, 1):
        sb.append(f"{i:2}. {p.user.username:15} | Lvl: {p.lvl:2} | Class: {p.game_class}")
    return "\n".join(sb)

def get_procedural_desc(obj):
    if isinstance(obj, Player):
        armor = InventoryItem.objects.filter(player=obj, equipped=True, item__item_type='armor').first()
        weapon = InventoryItem.objects.filter(player=obj, equipped=True, item__item_type='weapon').first()
        
        rep = get_reputation_title(obj.karma)
        desc = f"A {obj.race} {obj.game_class} known as a {rep}. "
        if armor: desc += f"Wearing {armor.item.name}. "
        else: desc += "Wearing standard-issue synth-rags. "
        
        if weapon: desc += f"Wielding {weapon.item.name}. "
        
        if obj.hp < obj.hp_max * 0.3: desc += "Their health critical, systems flickering."
        elif obj.hp < obj.hp_max * 0.7: desc += "They show signs of recent combat."
        else: desc += "They look ready for action."
        return desc

    if isinstance(obj, NPC):
        desc = f"{obj.description} "
        if obj.hp < obj.hp_max * 0.3: desc += "It's badly damaged and near failure."
        elif obj.hp < obj.hp_max * 0.7: desc += "It looks somewhat worn down."
        
        if obj.npc_type == 'boss': desc += " It radiates a crushing aura of power. Caution advised."
        elif obj.npc_type == 'dealer': desc += " They keep looking over their shoulder."
        
        if obj.karma_alignment > 50: desc += " It seems to represent local law and order."
        elif obj.karma_alignment < -50: desc += " It has a distinctly predatory and malevolent presence."
        
        return desc

    if isinstance(obj, Item):
        desc = obj.description
        desc += f" [Rarity: {obj.rarity.upper()}]"
        if obj.item_type == 'weapon': desc += f" [ATK +{obj.attack_bonus}]"
        elif obj.item_type == 'armor': desc += f" [DEF +{obj.defense_bonus}]"
        return desc

    return "No detailed data available."

def get_look(player, target_name=None):
    room = player.location
    if not room: return "THE VOID."
    
    if target_name:
        # Look at NPC
        npc = NPC.objects.filter(location=room, name__icontains=target_name, hp__gt=0).first()
        if npc:
            return f"\n[SCAN: {npc.name}]\n{get_procedural_desc(npc)}"
        
        # Look at Player
        other = Player.objects.filter(location=room, user__username__icontains=target_name, online=True).exclude(id=player.id).first()
        if other:
            return f"\n[SCAN: {other.user.username}]\n{get_procedural_desc(other)}"
        
        # Look at Item in room
        item = room.items.filter(name__icontains=target_name).first()
        if item:
            return f"\n[SCAN: {item.name}]\n{get_procedural_desc(item)}"
            
        # Look at Item in inventory
        ii = InventoryItem.objects.filter(player=player, item__name__icontains=target_name).first()
        if ii:
            return f"\n[SCAN: {ii.item.name}]\n{get_procedural_desc(ii.item)}"

        return f"Target '{target_name}' not detected in local sector."

    sb = [f"\n[Location] {room.name}"]
    sb.append(f"DATA: {room.description}")
    
    if room.shop_name:
        sb.append(f"\n[TERMINAL] A commerce node is active here: {room.shop_name}")
    
    npcs = NPC.objects.filter(location=room, hp__gt=0)
    if npcs.exists():
        sb.append("\nDETECTED ENTITIES:")
        for n in npcs:
            indicator = " [BOSS]" if n.npc_type == 'boss' else ""
            sb.append(f"  > {n.name} (Lvl {n.lvl}){indicator}")
    
    if room.exits:
        sb.append(f"\n[Exits: {', '.join(room.exits.keys()).upper()}]")
    
    items = room.items.all()
    for item in items:
        sb.append(f"[Hardware] {item.name} is here.")

    others = Player.objects.filter(location=room, online=True).exclude(id=player.id)
    for o in others:
        sb.append(f"[User] {o.user.username} (Lvl {o.lvl}) is here.")
        
    return "\n".join(sb)

def process_addiction(player):
    output = ""
    if player.addiction_points > 0:
        player.withdrawal_timer += 1
        if player.withdrawal_timer > 10:
            dmg = random.randint(1, player.addiction_points // 5 + 2)
            player.hp -= dmg
            output += f"\n[WITHDRAWAL] Your systems are crashing. -{dmg} HP."
            if player.hp <= 0:
                output += "\n[CRITICAL ERROR] SYSTEM FAILURE: OVERDOSE/WITHDRAWAL."
                player.hp = player.hp_max // 2
                player.money = max(0, player.money - 20)
                player.addiction_points = max(0, player.addiction_points - 10)
                player.location = Room.objects.get(id=1)
                output += "\nRebooted at The Neon Hub."
        
        if player.withdrawal_timer > 50:
            player.addiction_points = max(0, player.addiction_points - 1)
            player.withdrawal_timer = 40 
            
    player.save()
    return output

def respawn_npcs(room):
    if not room.respawn_npcs: return ""
    
    now = timezone.now()
    if room.last_npc_spawn and (now - room.last_npc_spawn).total_seconds() < room.respawn_timer:
        return ""
        
    room.last_npc_spawn = now
    room.save()
    
    # Respawn existing dead NPCs
    dead_npcs = NPC.objects.filter(location=room, hp__lte=0, respawnable=True)
    respawned_count = 0
    for n in dead_npcs:
        n.hp = n.hp_max
        n.save()
        respawned_count += 1
        
    # Occasionally generate a new random NPC if none exist
    alive_npcs = NPC.objects.filter(location=room, hp__gt=0)
    if not alive_npcs.exists() and room.zone != 'hub' and random.random() < 0.4:
        is_boss = random.random() < 0.05
        is_miniboss = not is_boss and random.random() < 0.15
        
        npc_names = ["Rogue Drone", "Scavenger", "Corporate Enforcer", "Street Punk", "Glitch-Hulk", "Vigilante", "Paladin-Mech", "Cyber-Assassin"]
        name = random.choice(npc_names)
        lvl = random.randint(1, 10)
        
        karma_alignment = random.randint(-100, 100)
        
        npc_type = 'drone'
        if is_boss:
            npc_type = 'boss'
            name = f"ELITE: {name.upper()}"
            lvl += 5
        elif is_miniboss:
            npc_type = 'mini-boss'
            name = f"VETERAN: {name}"
            lvl += 2
        else:
            if "Vigilante" in name or "Paladin" in name:
                npc_type = 'vigilante'
                karma_alignment = random.randint(50, 100)
            elif "Assassin" in name or "Punk" in name:
                npc_type = 'gang'
                karma_alignment = random.randint(-100, -50)
            else:
                npc_type = random.choice(['drone', 'gang', 'corporate'])

        multiplier = 4 if is_boss else (2 if is_miniboss else 1)
        
        npc = NPC.objects.create(
            name=f"{name} {random.randint(100, 999)}",
            description=f"A hostile {name.lower()} wandering the grid.",
            location=room,
            attack=(5 + lvl * 2) * (2 if is_boss else 1),
            defense=(2 + lvl) * multiplier,
            hp=(20 + lvl * 10) * multiplier * 2,
            hp_max=(20 + lvl * 10) * multiplier * 2,
            lvl=lvl,
            money_drop=lvl * 10 * multiplier,
            exp_drop=lvl * 40 * multiplier,
            aggressive=(random.random() < 0.3 or is_boss), # Lower default aggression, let karma handle it
            karma_alignment=karma_alignment,
            npc_type=npc_type
        )
        
        # Add rare drops for bosses
        if is_boss or is_miniboss:
            rarity_filter = ['epic', 'legendary'] if is_boss else ['rare']
            rare_items = Item.objects.filter(rarity__in=rarity_filter, item_type__in=['weapon', 'armor'])
            if rare_items.exists():
                npc.drops.add(random.choice(rare_items))
        
        return f"\n[SENSORS] {'MASSIVE ' if is_boss else ''}NEW ENTITIES DETECTED."
        
    if respawned_count > 0:
        return "\n[SENSORS] Local entities have rebooted."
    return ""

def move_player(player, direction):
    dir_map = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}
    direction = dir_map.get(direction, direction)
    
    if direction not in player.location.exits:
        return "PATH BLOCKED."
    
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
        
        # If hidden and moving, re-roll stealth detection for the new room
        stealth_break_msg = ""
        if player.hidden:
            npcs = NPC.objects.filter(location=player.location, hp__gt=0)
            max_npc_lvl = max([n.lvl for n in npcs]) if npcs.exists() else 0
            players_here = Player.objects.filter(location=player.location, online=True).exclude(id=player.id)
            max_player_lvl = max([p.lvl for p in players_here]) if players_here.exists() else 0
            threat_lvl = max(max_npc_lvl, max_player_lvl)
            
            stay_chance = 40 + player.agi_stat // 3
            if threat_lvl > 0:
                lvl_penalty = max(0, (threat_lvl - player.lvl) * 15)
                stay_chance -= lvl_penalty
            
            if random.randint(1, 100) > stay_chance:
                player.hidden = False
                player.save()
                stealth_break_msg = f"\n[ALERT] Your cover is blown in the new sector! ({stay_chance}% stay hidden)"
            else:
                player.save()
                stealth_break_msg = f"\n[STEALTH] You remain hidden. ({stay_chance}% stay hidden)"
        
        respawn_msg = respawn_npcs(player.location)
        look_text = get_look(player)
        addiction_msg = process_addiction(player)
        
        auto_attack_msg = ""
        if not player.location.safe_zone and player.lvl >= 5 and not player.hidden:
            # NPC Aggression Logic - hidden players avoid auto-attack
            npcs = NPC.objects.filter(location=player.location, hp__gt=0)
            attacker = None
            for npc in npcs:
                if npc.aggressive:
                    attacker = npc
                    break
                if npc.karma_alignment > 40 and player.karma < -40:
                    attacker = npc
                    break
                if npc.karma_alignment < -40 and player.karma > 40:
                    attacker = npc
                    break
                if abs(npc.karma_alignment - player.karma) > 130:
                    attacker = npc
                    break

            if attacker:
                auto_attack_msg = f"\n[DANGER] {attacker.name} detects your presence and engages!"
                auto_attack_msg += "\n" + attack_npc(player, attacker.name, is_auto=True)

        return look_text + stalk_msg + stealth_break_msg + addiction_msg + respawn_msg + auto_attack_msg
    except Room.DoesNotExist:
        return "NAVIGATION ERROR."

def calculate_damage(atk, dfn, element='physical', weakness='none', resistance='none'):
    base_dmg = max(1, atk - dfn // 2)
    dmg = random.randint(max(1, base_dmg - 2), base_dmg + 2)
    
    strong_against = {'fire': 'air', 'air': 'earth', 'earth': 'water', 'water': 'fire'}
    
    if element != 'physical':
        if weakness == element or strong_against.get(element) == weakness:
            dmg = int(dmg * 1.5)
        elif resistance == element:
            dmg = int(dmg * 0.5)
            
    return dmg

def attack_player(player, target_name):
    if not target_name: return "Specify target."
    if player.location.safe_zone: return "Violence is prohibited in this sector."
    
    target = Player.objects.filter(location=player.location, user__username__icontains=target_name, online=True).exclude(id=player.id).first()
    if not target:
        return None 

    if abs(player.lvl - target.lvl) > 3:
        return f"Target level too distant ({target.lvl}). You can only attack users within 3 levels of your own."

    output = f"\n*** PVP COMBAT INITIATED: {player.user.username} VS {target.user.username} ***"
    player.karma -= 10 # Murder is bad
    player.save()
    
    # Backstab bonus: if hidden, first round is free with no counter
    backstab_round = player.hidden
    if backstab_round:
        player.hidden = False
        player.save()
        output += "\n[BACKSTAB] You catch them completely off guard!"
    
    first_round = True
    for _ in range(3):
        # Player attacks first
        equipped_weapon = InventoryItem.objects.filter(player=player, equipped=True, item__item_type='weapon').first()
        speed_bonus = equipped_weapon.item.speed_bonus if equipped_weapon else 0
        agi_attacks = player.agi_stat // 10
        base_attacks = 1 + (speed_bonus // 10) if speed_bonus > 0 else 1
        p_attacks = base_attacks + agi_attacks
        
        for _ in range(p_attacks):
            dmg = calculate_damage(player.attack, target.defense)
            target.hp -= dmg
            target.save()
            output += f"\nYou hit {target.user.username} for {dmg} damage."
            if target.hp <= 0: break
            
        if target.hp <= 0:
            exp_gain = target.lvl * 50
            player.exp += exp_gain
            stolen = target.money // 4
            player.money += stolen
            player.save()
            hub = Room.objects.get(id=1)
            target.hp = target.hp_max // 2
            target.money -= stolen
            target.location = hub
            target.save()
            output += f"\nYou neutralized {target.user.username}! +{exp_gain} exp, +{stolen} credits."
            output += check_level_up(player)
            return output

        # Skip target's counter-attack on backstab round (first round only)
        if backstab_round and first_round:
            first_round = False
            continue
        
        # Target counter-attacks
        t_weapon = InventoryItem.objects.filter(player=target, equipped=True, item__item_type='weapon').first()
        t_speed = t_weapon.item.speed_bonus if t_weapon else 0
        t_agi_attacks = target.agi_stat // 10
        t_base_attacks = 1 + (t_speed // 10) if t_speed > 0 else 1
        t_attacks = t_base_attacks + t_agi_attacks
        
        for _ in range(t_attacks):
            counter_dmg = calculate_damage(target.attack, player.defense)
            player.hp -= counter_dmg
            player.save()
            output += f"\n{target.user.username} hits you for {counter_dmg} damage."
            if player.hp <= 0: break

        if player.hp <= 0:
            output += "\n[CRITICAL ERROR] YOU HAVE BEEN NEUTRALIZED."
            stolen = player.money // 4
            target.money += stolen
            target.exp += player.lvl * 50
            target.save()
            hub = Room.objects.get(id=1)
            player.hp = player.hp_max // 2
            player.money -= stolen
            player.location = hub
            player.save()
            output += f"\nRespawned at The Neon Hub. {target.user.username} took {stolen} credits."
            return output
        
        first_round = False

    return output

def attack_target(player, target_name):
    res = attack_player(player, target_name)
    if res is not None:
        return res
    return attack_npc(player, target_name)

def attack_npc(player, target_name, is_auto=False):
    if not target_name: return "Specify target."
    npc = NPC.objects.filter(location=player.location, name__icontains=target_name, hp__gt=0).first()
    if not npc: return "Target not found."

    output = ""
    rounds = 1 if is_auto else 5
    
    equipped_weapon = InventoryItem.objects.filter(player=player, equipped=True, item__item_type='weapon').first()
    speed_bonus = equipped_weapon.item.speed_bonus if equipped_weapon else 0
    agi_attacks = player.agi_stat // 10
    
    # Backstab bonus: if hidden, first round is a free attack with no counter
    backstab_round = player.hidden
    if backstab_round:
        player.hidden = False
        player.save()
        output += "\n[BACKSTAB] Strike from the shadows! They never saw you coming."
    
    for round_num in range(rounds):
        base_attacks = 1 + (speed_bonus // 10) if speed_bonus > 0 else 1
        p_attacks = base_attacks + agi_attacks
        
        # Backstab bonus damage on first hit
        first_hit = True
        for _ in range(p_attacks):
            dmg = calculate_damage(player.attack, npc.defense, element='physical', weakness=npc.weakness, resistance=npc.resistance)
            if backstab_round and first_hit:
                dmg = int(dmg * 1.5)
                first_hit = False
            npc.hp -= dmg
            npc.save()
            output += f"\nYou hit {npc.name} for {dmg} damage."

            if npc.hp <= 0:
                player.exp += npc.exp_drop
                player.money += npc.money_drop
                player.last_combat_npc = None
                player.stalk_count = 0
                
                if npc.karma_alignment < -30: player.karma += 5
                elif npc.karma_alignment > 30: player.karma -= 10
                else: player.karma += 1
                
                player.karma = max(-100, min(100, player.karma))
                player.save()
                
                output += f"\nTarget neutralized! +{npc.exp_drop} exp, +{npc.money_drop} credits."
                for item in npc.drops.all():
                    ii, created = InventoryItem.objects.get_or_create(player=player, item=item)
                    if not created: ii.quantity += 1
                    ii.save()
                    output += f"\nRetrieved: {item.name}"
                output += check_level_up(player)
                return output
        
        # No counter on backstab round
        if backstab_round:
            backstab_round = False
            continue
        
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
            player.stalk_count = 4 
            player.save()

    return output

def use_ability(player, ability_name, target_name):
    ability_name = ability_name.lower()
    
    # Universal sneak/stealth - works for any class, but success varies
    if ability_name in ('stealth', 'sneak'):
        if player.last_combat_npc or player.stalk_count > 0:
            return "\nCannot hide while engaged or stalking targets."
        if player.location.safe_zone:
            return "\nNo need to hide in a safe sector."
        
        npcs = NPC.objects.filter(location=player.location, hp__gt=0)
        max_npc_lvl = max([n.lvl for n in npcs]) if npcs.exists() else 0
        players_here = Player.objects.filter(location=player.location, online=True).exclude(id=player.id)
        max_player_lvl = max([p.lvl for p in players_here]) if players_here.exists() else 0
        threat_lvl = max(max_npc_lvl, max_player_lvl)
        
        # Base chance: Thief/Trickster get better rates, everyone else struggles
        if player.game_class in ('Thief', 'Trickster') and player.lvl >= 4:
            base_chance = 70 + player.agi_stat // 2
        else:
            # Low-level or non-stealth classes have poor success
            base_chance = 30 + player.agi_stat // 4
            if player.lvl < 4:
                base_chance = max(5, base_chance - 20)
        
        if threat_lvl > 0:
            lvl_penalty = max(0, (threat_lvl - player.lvl) * 10)
            base_chance -= lvl_penalty
        
        base_chance = max(5, min(95, base_chance))
        
        if random.randint(1, 100) <= base_chance:
            player.hidden = True
            player.save()
            return f"\nYou melt into the shadows. Hidden! ({base_chance}% success)"
        else:
            player.hidden = False
            player.save()
            return f"\nFailed to hide. You remain visible. ({base_chance}% chance)"
    
    # Check if this command is actually a move for this class
    moves = CLASS_MOVES.get(player.game_class, [])
    req_lvl = 999
    ability_data = None
    for lvl, name, desc in moves:
        if name.lower() == ability_name:
            req_lvl = lvl
            ability_data = (name, desc)
            break
    
    if req_lvl == 999: # Not a move for this class
        return None

    if player.lvl < req_lvl:
        return f"Level {req_lvl} required for {ability_name.upper()}."

    npc = None
    target_player = None
    if target_name:
        npc = NPC.objects.filter(location=player.location, name__icontains=target_name, hp__gt=0).first()
        target_player = Player.objects.filter(location=player.location, user__username__icontains=target_name, online=True).exclude(id=player.id).first()

    if target_player:
        if player.lvl < 5:
            return "Neural safety lock engaged. Level 5 required to target users with class abilities."
        if abs(player.lvl - target_player.lvl) > 3:
            return f"Target level too distant ({target_player.lvl}). Range: +/- 3 levels."
        if player.location.safe_zone:
            return "Violence is prohibited in this sector."

    target = npc or target_player
    cost = 5 + (req_lvl // 2)
    if player.mana < cost: return "INSUFFICIENT BUFFER (MANA)."
    
    player.mana -= cost
    player.save()
    
    res = f"You use {ability_name.upper()}."
    
    # Damage calculation helper
    def deal_dmg(mult, element='physical'):
        nonlocal res
        if not target: 
            res += "\nTarget required."
            return
        
        dmg = calculate_damage(int(player.attack * mult) if element == 'physical' else int((player.int_stat if player.int_stat > player.wil_stat else player.wil_stat) * mult), target.defense, element=element)
        target.hp -= dmg
        
        if isinstance(target, Player):
            player.karma -= 2 # Penalty for PVP move usage
            player.save()
            target.save()
            res += f"\nYou hit {target.user.username} for {dmg} {element} damage."
            if target.hp <= 0:
                exp_gain = target.lvl * 50
                player.exp += exp_gain
                stolen = target.money // 4
                player.money += stolen
                player.save()
                
                hub = Room.objects.get(id=1)
                target.hp = target.hp_max // 2
                target.money -= stolen
                target.location = hub
                target.save()
                res += f"\nYou neutralized {target.user.username}! +{exp_gain} exp, +{stolen} credits."
        else:
            target.save()
            res += f"\nYou hit {target.name} for {dmg} {element} damage."
            if target.hp <= 0:
                player.exp += target.exp_drop
                player.money += target.money_drop
                player.save()
                res += f"\nTarget neutralized! +{target.exp_drop} exp, +{target.money_drop} credits."
                for item in target.drops.all():
                    ii, created = InventoryItem.objects.get_or_create(player=player, item=item)
                    if not created: ii.quantity += 1
                    ii.save()
                    res += f"\nRetrieved: {item.name}"
                res += check_level_up(player)
        return

    # Abilities Logic - High level mappings
    if ability_name == 'blade': deal_dmg(1.2)
    elif ability_name == 'oni_strike': deal_dmg(2.5, 'fire')
    elif ability_name == 'zansetsu': deal_dmg(3.0)
    elif ability_name == 'mirage': player.defense += 30; player.save(); res += "\nDefense boosted significantly."
    elif ability_name == 'whirlwind': deal_dmg(1.5); deal_dmg(1.5)
    elif ability_name == 'dragon_lunge': deal_dmg(4.0, 'fire')
    elif ability_name == 'bladestorm': deal_dmg(5.0)
    elif ability_name == 'omnislash': deal_dmg(2.0); deal_dmg(2.0); deal_dmg(2.0); deal_dmg(2.0)
    
    elif ability_name == 'hack': deal_dmg(2.0, 'water')
    elif ability_name == 'overload': deal_dmg(2.5, 'air')
    elif ability_name == 'synapse_burn': deal_dmg(3.0, 'fire')
    elif ability_name == 'logic_bomb': deal_dmg(3.5, 'air')
    elif ability_name == 'blackout': 
        if target: target.attack = max(1, target.attack - 10); target.defense = max(1, target.defense - 10); target.save(); res += "\nTarget systems crippled."
        else: res += "\nTarget required."
    elif ability_name == 'databreach':
        if npc: stolen = random.randint(10, 50); player.money += stolen; player.save(); res += f"\nSiphoned {stolen} credits!"
        deal_dmg(3.0, 'water')
    elif ability_name == 'icebreaker': deal_dmg(5.0, 'water')
    elif ability_name == 'zero_day': deal_dmg(10.0, 'water')

    elif ability_name == 'patch': heal = 20 + player.int_stat; player.hp = min(player.hp_max, player.hp + heal); player.save(); res += f"\nRepaired {heal} HP."
    elif ability_name == 'detox': player.addiction_points = max(0, player.addiction_points - 15); player.save(); res += "\nToxins cleared."
    elif ability_name == 'heal': heal = 40 + player.wil_stat; player.hp = min(player.hp_max, player.hp + heal); player.save(); res += f"\nHealed {heal} HP."
    elif ability_name == 'bless': player.defense += 10; player.attack += 5; player.save(); res += "\nYou are blessed."
    
    # Generic keyword-based handlers for other moves
    elif any(x in ability_name for x in ['strike', 'slash', 'blade', 'lunge', 'storm', 'whirlwind', 'stab', 'smash', 'toss', 'bolt', 'burn', 'plasma', 'arc', 'shock', 'flare', 'pulse', 'assassinate', 'judgment', 'annihilation', 'destruction', 'armageddon']):
        mult = 2.0 + (req_lvl / 10.0)
        elem = 'physical'
        if any(x in ability_name for x in ['bolt', 'pulse', 'arc', 'tesla']): elem = 'air'
        if any(x in ability_name for x in ['burn', 'fire', 'flare', 'oni', 'plasma', 'armageddon']): elem = 'fire'
        if any(x in ability_name for x in ['seismic', 'earth', 'singularity', 'dart', 'nanobot']): elem = 'earth'
        if any(x in ability_name for x in ['hack', 'water', 'ice', 'black', 'zero', 'siphon']): elem = 'water'
        deal_dmg(mult, elem)
    elif any(x in ability_name for x in ['boost', 'shield', 'iron', 'protocol', 'vanish', 'smoke', 'mirage', 'image', 'bless']):
        buff = 10 + req_lvl
        player.defense += buff; player.save(); res += f"\nDefense boosted by {buff}."
    elif any(x in ability_name for x in ['heal', 'patch', 'purify', 'restoration', 'resuscitate', 'regeneration']):
        heal = 20 + req_lvl * 2; player.hp = min(player.hp_max, player.hp + heal); player.save(); res += f"\nHealed for {heal} HP."
    elif ability_name == 'soul_drain':
        if target:
            dmg = calculate_damage(int(player.wil_stat * 1.5), target.defense, element='water')
            target.hp -= dmg; player.hp = min(player.hp_max, player.hp + dmg // 2); target.save(); player.save()
            res += f"\nDrained {dmg} HP!"
        else: res += "\nTarget required."
    elif ability_name == 'scheme' or ability_name == 'sleight_of_hand':
        if npc: stolen = random.randint(1, 10) + player.cha_stat; player.money += stolen; player.save(); res += f"\nDrained {stolen} credits."
        else: res = "Requires NPC target."
    elif ability_name == 'jackpot':
        if target:
            if random.random() > 0.5: dmg = int(player.cha_stat * 4); target.hp -= dmg; target.save(); res += f"\nJACKPOT! {dmg} damage!"
            else: loot = random.randint(50, 200); player.money += loot; player.save(); res += f"\nJACKPOT! {loot} credits!"
        else: res += "\nTarget required."
    elif ability_name == 'bamboozle':
        if target: target.defense = max(1, target.defense - 15); target.save(); res += "\nTarget bamboozled!"
        else: res += "\nTarget required."
    else:
        # Fallback for anything else in CLASS_MOVES
        deal_dmg(1.5 + (req_lvl / 15.0))

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
        player.str_stat += item.str_bonus
        player.int_stat += item.int_bonus
        player.wil_stat += item.wil_bonus
        player.agi_stat += item.agi_bonus
        player.hea_stat += item.hea_bonus
        player.cha_stat += item.cha_bonus
        
        player.attack += item.str_bonus * 2
        player.defense += item.agi_bonus
        player.hp_max += item.hea_bonus * 10
        player.mana_max += item.int_bonus * 5
        
        player.hp = min(player.hp_max, player.hp + 20)
        player.withdrawal_timer = 0
        if random.random() < item.addiction_chance:
            player.addiction_points += 20
            output += "\n[DANGER] Neuro-dependency increased."
        output += "\nNeural spike detected. Systems modified."
        
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

def train_stat(player, stat):
    if player.stat_points <= 0:
        return "You have no stat points to spend."
    
    stat = stat.upper()
    if stat == "STR": player.str_stat += 1; player.attack += 2
    elif stat == "INT": player.int_stat += 1; player.mana_max += 5
    elif stat == "WIL": player.wil_stat += 1; player.mana_max += 5
    elif stat == "AGI": player.agi_stat += 1; player.defense += 1
    elif stat == "HEA": player.hea_stat += 1; player.hp_max += 10
    elif stat == "CHA": player.cha_stat += 1
    else: return "Invalid stat. Choose STR, INT, WIL, AGI, HEA, or CHA."
    
    player.stat_points -= 1
    player.save()
    return f"You trained {stat}. Points remaining: {player.stat_points}"

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
            'x': r.map_x, 'y': r.map_y, 
            'current': (r.id == room.id),
            'players': Player.objects.filter(location=r, online=True).exclude(id=player.id).count(),
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
    sb.append(f"Credits: {player.money} | Stat Points: {player.stat_points} | Karma: {player.karma} ({get_reputation_title(player.karma)})")
    sb.append(f"Path (Race): {player.race} | Class: {player.game_class}")
    if player.addiction_points > 0:
        sb.append(f"ADDICTION: {player.addiction_points}%")
    sb.append(f"Stats: STR:{player.str_stat} INT:{player.int_stat} WIL:{player.wil_stat} AGI:{player.agi_stat} HEA:{player.hea_stat} CHA:{player.cha_stat}")
    sb.append(f"Combat: ATK:{player.attack} DEF:{player.defense}")
    
    sb.append("\nLearned Moves:")
    moves = CLASS_MOVES.get(player.game_class, [])
    found = False
    for lvl, name, desc in moves:
        if player.lvl >= lvl:
            sb.append(f"  {name.upper():15} (Lv {lvl}): {desc}")
            found = True
    if not found: sb.append("  None")
    
    return "\n".join(sb)

def check_level_up(player):
    output = ""
    while player.exp >= player.lvl * 120:
        player.exp -= player.lvl * 120
        player.lvl += 1
        player.stat_points += 1 
        player.hp_max += 20
        player.hp = player.hp_max
        player.mana_max += 10
        player.mana = player.mana_max
        player.save()
        output += f"\n*** LEVEL UP! Now level {player.lvl}! ***"
        output += f"\nGranted 1 stat point. Use TRAIN <stat> to spend it."
        
        # Notify about new moves
        moves = CLASS_MOVES.get(player.game_class, [])
        for lvl, name, desc in moves:
            if player.lvl == lvl:
                output += f"\n[SYSTEM] New move unlocked: {name.upper()}!"

        if player.lvl == 5: output += "\n[NEW ABILITIES UNLOCKED! Type HELP for details]"
        if player.lvl == 5: output += "\n[ALERT] NPC AGGRESSION PROTOCOLS ACTIVATED."
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
        player.str_stat -= ii.item.str_bonus
        player.int_stat -= ii.item.int_bonus
        player.wil_stat -= ii.item.wil_bonus
        player.agi_stat -= ii.item.agi_bonus
        player.hea_stat -= ii.item.hea_bonus
        player.cha_stat -= ii.item.cha_bonus
        ii.save()
        player.save()
        return f"Unequipped {ii.item.name}."
    
    if ii.item.item_type == 'weapon':
        old = InventoryItem.objects.filter(player=player, equipped=True, item__item_type='weapon').first()
        if old:
            player.attack -= old.item.attack_bonus
            player.str_stat -= old.item.str_bonus
            player.int_stat -= old.item.int_bonus
            player.wil_stat -= old.item.wil_bonus
            player.agi_stat -= old.item.agi_bonus
            player.hea_stat -= old.item.hea_bonus
            player.cha_stat -= old.item.cha_bonus
            old.equipped = False
            old.save()
    elif ii.item.item_type == 'armor':
        old = InventoryItem.objects.filter(player=player, equipped=True, item__item_type='armor').first()
        if old:
            player.defense -= old.item.defense_bonus
            player.str_stat -= old.item.str_bonus
            player.int_stat -= old.item.int_bonus
            player.wil_stat -= old.item.wil_bonus
            player.agi_stat -= old.item.agi_bonus
            player.hea_stat -= old.item.hea_bonus
            player.cha_stat -= old.item.cha_bonus
            old.equipped = False
            old.save()
            
    ii.equipped = True
    player.attack += ii.item.attack_bonus
    player.defense += ii.item.defense_bonus
    player.str_stat += ii.item.str_bonus
    player.int_stat += ii.item.int_bonus
    player.wil_stat += ii.item.wil_bonus
    player.agi_stat += ii.item.agi_bonus
    player.hea_stat += ii.item.hea_bonus
    player.cha_stat += ii.item.cha_bonus
    ii.save()
    player.save()
    return f"Equipped {ii.item.name}."

def list_shop(player):
    if not player.location.shop_name: return "No terminal shop detected."
    
    if player.location.shop_inventory.exists():
        items = player.location.shop_inventory.all().order_by('item_type', 'name')
    else:
        # Default shops only sell common and uncommon items
        items = Item.objects.filter(price__gt=0).exclude(rarity__in=['rare', 'epic', 'legendary']).order_by('item_type', 'name')
    
    # Limit to ~12 items to avoid scrolling
    items = items[:12]
    
    sb = [f"\n=== {player.location.shop_name} Inventory ==="]
    
    current_type = None
    for item in items:
        if item.item_type != current_type:
            current_type = item.item_type
            sb.append(f"\n[{current_type.upper()}]")
        sb.append(f"  {item.name:25} {item.price} CR")
    return "\n".join(sb)

def buy_item(player, item_name):
    if not player.location.shop_name: return "No shop here."
    
    if player.location.shop_inventory.exists():
        item = player.location.shop_inventory.filter(name__icontains=item_name, price__gt=0).first()
    else:
        item = Item.objects.filter(name__icontains=item_name, price__gt=0).exclude(rarity__in=['rare', 'epic', 'legendary']).first()
        
    if not item: return "Item not in database or unavailable at this terminal."
    if player.money < item.price: return "Insufficient credits."
    player.money -= item.price
    player.save()
    ii, created = InventoryItem.objects.get_or_create(player=player, item=item)
    if not created:
        ii.quantity += 1
        ii.save()
    return f"Purchased {item.name}."

def sell_item(player, item_name):
    # Selling to shop or NPC dealer
    target_npc = None
    if ' to ' in item_name.lower():
        parts = item_name.lower().split(' to ')
        item_name = parts[0].strip()
        npc_name = parts[1].strip()
        target_npc = NPC.objects.filter(location=player.location, name__icontains=npc_name, hp__gt=0).first()
        if not target_npc: return f"Target '{npc_name}' not found."

    ii = InventoryItem.objects.filter(player=player, item__name__icontains=item_name).first()
    if not ii: return "You don't have that."
    if ii.equipped: return "Unequip first."
    
    if target_npc:
        if target_npc.npc_type == 'dealer' and ii.item.item_type == 'drug':
            price = int(ii.item.price * 1.2) # Dealers pay more for drugs
            player.money += price
            player.karma -= 5 # Selling drugs is significantly bad
            player.save()
            name = ii.item.name
            if ii.quantity > 1: ii.quantity -= 1; ii.save()
            else: ii.delete()
            return f"Sold {name} to {target_npc.name} for {price} credits. [Karma -5]"
        return f"{target_npc.name} doesn't want that."

    if not player.location.shop_name: return "No shop here to sell to."
    
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
    cutoff = timezone.now() - timezone.timedelta(seconds=30)
    msgs = ChatMessage.objects.filter(room=player.location, timestamp__gt=cutoff).order_by('timestamp')
    chat = [{"player": m.sender.user.username, "message": m.message} for m in msgs]
    npcs = list(NPC.objects.filter(location=player.location, hp__gt=0).values('id', 'name', 'hp', 'hp_max', 'lvl', 'npc_type'))
    room_items = list(player.location.items.all().values('id', 'name')) if player.location else []
    players_here = list(Player.objects.filter(location=player.location, online=True).exclude(id=player.id).values('id', 'user__username', 'lvl', 'game_class'))
    return {
        "chat": chat, "npcs": npcs, "items": room_items, "players": players_here,
        "status": get_status_str(player), "location": player.location.name if player.location else "Unknown",
    }
