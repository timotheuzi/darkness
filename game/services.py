import json
import random
from django.utils import timezone
from django.db.models import Q
from .models import Player, Room, NPC, Item, InventoryItem, ChatMessage, ProceduralWeaponSpawn, Party, PartyMembership

# Race Special Characteristics
RACE_CHARACTERISTICS = {
    'Cyborg': 'Cybernetic Resilience: +10% resistance to debuffs and status effects.',
    'Bio-hacked': 'Adrenal Efficiency: Natural healing 20% faster, reduced addiction.',
    'Android': 'Systematic Mind: +15% mana efficiency, immune to mind-affecting effects.',
    'Mutant': 'Adaptive Biology: Stats can exceed normal caps by 5 points.',
    'Human': 'Versatile Potential: Gains 1.5x stat points on level up.',
    'Void-Walker': 'Phase Shift: Can dodge 10% of incoming attacks.',
    'Synth-Soul': 'Digital Presence: +20% stealth effectiveness, reduced physical stats.',
    'Chrome-Crawler': 'Overclocked: +1 extra attack per combat round.',
    'Elf': 'Ancient Grace: +10% crit chance, natural affinity for precision.',
    'Goblin': 'Street Cunning: +15% chance to find extra loot from NPCs.',
}


# Class Ability Definitions - Learned every 5 levels until Lv 30
# Format: (level, ability_name, acronym, description)
CLASS_MOVES = {
    'Street Samurai': [
        (1, 'blade', 'BLD', 'Precise physical strike. Scales with STR/ATK.'),
        (5, 'oni_strike', 'ONI', 'Fire-elemental strike. Scales with STR/ATK.'),
        (10, 'zansetsu', 'ZAN', 'High-critical physical strike. Scales with STR/ATK.'),
        (15, 'mirage', 'MIR', 'Technological displacement. Boosts Defense significantly based on AGI.'),
        (20, 'whirlwind', 'WHL', 'Multiple physical strikes. Scales with STR/ATK.'),
        (25, 'dragon_lunge', 'DRG', 'Heavy fire-elemental pierce. Scales with STR/ATK.'),
        (30, 'omnislash', 'OMN', 'Ultimate physical combo. Scales with STR/ATK.'),
    ],
    'Netrunner': [
        (1, 'hack', 'HCK', 'System water/ice damage. Scales with INT.'),
        (5, 'overload', 'OVR', 'High air damage pulse. Scales with INT.'),
        (10, 'synapse_burn', 'SYN', 'Burn target memory (Fire). Scales with INT.'),
        (15, 'logic_bomb', 'LGC', 'Heavy air system corruption. Scales with INT.'),
        (20, 'blackout', 'BKO', 'Neural interference. Lowers target stats based on INT.'),
        (25, 'databreach', 'DBR', 'Siphon credits and deal water damage. Scales with INT.'),
        (30, 'zero_day', 'ZER', 'Critical system failure damage. Scales with INT.'),
    ],
    'Techie': [
        (1, 'calibrate', 'CAL', 'Drone earth damage. Scales with INT/AGI.'),
        (5, 'turret', 'TUR', 'Automated physical fire. Scales with INT/ATK.'),
        (10, 'overclock', 'OVC', 'System boost. Increases Attack and Speed based on INT.'),
        (15, 'nanobot_swarm', 'NAN', 'Healing and earth damage. Scales with INT.'),
        (20, 'plasma_arc', 'PLA', 'Heavy fire damage. Scales with INT.'),
        (25, 'tesla_coil', 'TES', 'Stun and air damage. Scales with INT.'),
        (30, 'singularity', 'SIN', 'Ultimate gravity collapse (Earth). Scales with INT.'),
    ],
    'Medie': [
        (1, 'patch', 'PTC', 'Biological repair. Heals based on INT.'),
        (5, 'detox', 'DTX', 'Cleanse toxins. Heals and clears addiction.'),
        (10, 'adrenaline', 'ADR', 'Boost stats. Increases Attack and Defense based on HEA.'),
        (15, 'biocortical_shock', 'BIO', 'Water damage to nervous system. Scales with INT/HEA.'),
        (20, 'regeneration', 'REG', 'Continuous cellular repair. Large heal based on HEA.'),
        (25, 'viral_burst', 'VIR', 'Heavy rot damage over time. Scales with HEA/INT.'),
        (30, 'nanomachine_army', 'NMA', 'Ultimate survival boost. Massive HP recovery based on HEA.'),
    ],
    'Fixer': [
        (1, 'scheme', 'SCH', 'Drain credits from target. Scales with CHA.'),
        (5, 'call_in', 'CAL', 'Air-strike damage. Scales with CHA/ATK.'),
        (10, 'bribe', 'BRI', 'Lower target defense with credits. Effectiveness based on CHA.'),
        (15, 'contract_kill', 'CTK', 'High physical damage assassination. Scales with CHA/ATK.'),
        (20, 'market_crash', 'MKT', 'Siphon massive credits. Scales with CHA.'),
        (25, 'reinforcements', 'REF', 'Summon allies for extra hits. Scales with CHA/ATK.'),
        (30, 'hostile_takeover', 'HTK', 'Ultimate credit and soul drain. Scales with CHA.'),
    ],
    'Thief': [
        (1, 'backstab', 'BSB', 'Critical strike from shadows. Scales with AGI/ATK.'),
        (5, 'stealth', 'STL', 'Become hidden. Success chance scales with AGI.'),
        (10, 'poison_dart', 'PSN', 'Earth damage over time. Scales with AGI/INT.'),
        (15, 'smoke_bomb', 'SMB', 'Defense boost and escape. Scales with AGI.'),
        (20, 'shadow_strike', 'SHD', 'Critical hit from stealth. Scales with AGI/ATK.'),
        (25, 'assassinate', 'ASN', 'Execute target with low HP. Scales with AGI/ATK.'),
        (30, 'death_mark', 'DMK', 'Ultimate physical assassination. Scales with AGI/ATK.'),
    ],
    'Heavy': [
        (1, 'smash', 'SMH', 'Heavy physical damage. Scales with STR.'),
        (5, 'taunt', 'TNT', 'Focus enemy attention. Lowers enemy stats based on HEA.'),
        (10, 'iron_skin', 'IRN', 'Harden armor. Boosts Defense based on HEA.'),
        (15, 'seismic_toss', 'SMT', 'Heavy earth damage. Scales with STR/HEA.'),
        (20, 'juggernaut', 'JUG', 'Boost Attack and Defense based on HEA/STR.'),
        (25, 'avalanche', 'AVL', 'Massive earth AOE. Scales with STR/HEA.'),
        (30, 'earthshaker', 'EQK', 'Ultimate earth blow. Scales with STR/HEA.'),
    ],
    'Psycher': [
        (1, 'mind_bolt', 'MND', 'Intelligence-based energy damage. Scales with INT.'),
        (5, 'soul_drain', 'SDL', 'Damage target, heal self. Scales with INT.'),
        (10, 'psionic_shield', 'PSI', 'Psychic barrier. Boosts Defense based on INT.'),
        (15, 'pyrokinesis', 'PYR', 'Massive fire mind damage. Scales with INT.'),
        (20, 'telekinesis', 'TEK', 'High physical mind damage. Scales with INT.'),
        (25, 'mind_control', 'MNC', 'Target strikes themselves. Effectiveness based on INT.'),
        (30, 'soul_annihilation', 'SOL', 'Ultimate psychic collapse. Scales with INT.'),
    ],
    'Warlock': [
        (1, 'curse', 'CRS', 'Weaken target. Lowers ATK/DEF based on INT.'),
        (5, 'chaos_bolt', 'CHB', 'Random high-energy surge. Scales with INT.'),
        (10, 'blood_pact', 'BLP', 'Sacrifice HP for massive damage. Scales with INT/Current HP.'),
        (15, 'shadow_bolt', 'SDB', 'Dark water damage. Scales with INT.'),
        (20, 'necrosis', 'NEC', 'High rot damage over time. Scales with INT.'),
        (25, 'demonic_tether', 'DMT', 'Siphon HP and Mana. Scales with INT.'),
        (30, 'armageddon', 'ARM', 'Ultimate chaotic destruction. Scales with INT.'),
    ],
    'Priest': [
        (1, 'heal', 'HEL', 'Holy restoration. Heals based on WIL.'),
        (5, 'bless', 'BLS', 'Soul fortification. Boosts ATK/DEF based on WIL.'),
        (10, 'purify', 'PUR', 'Clear addiction and heal. Scales with WIL.'),
        (15, 'holy_fire', 'HLF', 'Fire damage to the wicked. Scales with WIL.'),
        (20, 'divine_shield', 'DSH', 'Temporary invulnerability. Large DEF boost based on WIL.'),
        (25, 'judgment', 'JUD', 'Air damage based on Karma and WIL.'),
        (30, 'heavenly_ascent', 'HVA', 'Ultimate divine power. Massive heal and damage based on WIL.'),
    ],
    'Trickster': [
        (1, 'bamboozle', 'BAM', 'Confuse target. Lowers DEF based on CHA/LUCK.'),
        (5, 'sneak', 'SNK', 'Attempt to hide. Chance based on AGI/CHA.'),
        (10, 'jackpot', 'JAK', 'Massive damage or credits. Scales with CHA.'),
        (15, 'sleight_of_hand', 'SOH', 'Steal item or credits. Success based on CHA.'),
        (20, 'mirror_image', 'MIR', 'Illusionary defense. Large DEF boost based on CHA.'),
        (25, 'wild_card', 'WCD', 'Random effect. Scaling based on primary stats.'),
        (30, 'royal_flush', 'RFL', 'Ultimate luck-based destruction. Scales with CHA.'),
    ],
    'Jade Dragon': [
        (1, 'palm_strike', 'PLM', 'Open-palm chi strike. Scales with AGI/STR. Unarmed bonus when no weapon equipped.'),
        (5, 'crane_kick', 'CRK', 'Soaring aerial kick. Scales with AGI/STR.'),
        (10, 'iron_palm', 'IRP', 'Reinforced chi palm. Boosts Defense based on AGI.'),
        (15, 'tiger_claw', 'TGR', 'Rending claw strikes. Scales with AGI/STR.'),
        (20, 'dragon_kick', 'DGK', 'Explosive spinning kick. Scales with AGI/STR.'),
        (25, 'chi_burst', 'CHI', 'Internal energy blast. Air damage. Scales with AGI/INT.'),
        (30, 'jade_ascension', 'JDA', 'Ultimate martial trance. Massive combo. Scales with AGI/STR.'),
    ]
}

# Gear Restrictions
GEAR_LIMITS = {
    'Thief': {'armor': ['leather'], 'weapon': ['one-handed']},
    'Netrunner': {'armor': ['leather', 'light'], 'weapon': ['one-handed']},
    'Trickster': {'armor': ['leather', 'light'], 'weapon': ['one-handed']},
    'Heavy': {'armor': ['leather', 'light', 'medium', 'heavy'],
              'weapon': ['one-handed', 'two-handed']},
    'Street Samurai': {'armor': ['leather', 'light', 'medium', 'heavy'],
                       'weapon': ['one-handed', 'two-handed']},
    'Jade Dragon': {'armor': ['leather', 'light'], 'weapon': ['jade']},
}


def get_reputation_title(karma):
    if karma >= 80:
        return "Saint"
    if karma >= 50:
        return "Paragon"
    if karma >= 20:
        return "Lawful"
    if karma > -20:
        return "Neutral"
    if karma > -50:
        return "Renegade"
    if karma > -80:
        return "Outlaw"
    return "Utter Villain"


def get_attribute_desc(stat_name, val):
    if stat_name == 'str':
        if val < 8:
            return "feeble and scrawny"
        if val < 13:
            return "of average build"
        if val < 18:
            return "visibly toned and athletic"
        if val < 25:
            return "powerful and heavily muscled"
        return "a titan of pure physical power"
    if stat_name == 'agi':
        if val < 8:
            return "clumsy and awkward"
        if val < 13:
            return "steady on their feet"
        if val < 18:
            return "lithe and graceful"
        if val < 25:
            return "incredibly swift and precise"
        return "moving with supernatural speed"
    if stat_name == 'int':
        if val < 8:
            return "slow-witted"
        if val < 13:
            return "of average intelligence"
        if val < 18:
            return "sharp and analytical"
        if val < 25:
            return "brilliant and calculating"
        return "possessing a mind like a supercomputer"
    if stat_name == 'wil':
        if val < 8:
            return "easily swayed"
        if val < 13:
            return "of average resolve"
        if val < 18:
            return "determined and focused"
        if val < 25:
            return "unshakeable in their will"
        return "radiating an aura of absolute mental dominance"
    if stat_name == 'cha':
        if val < 8:
            return "unpleasant and abrasive"
        if val < 13:
            return "plain and unremarkable"
        if val < 18:
            return "charming and charismatic"
        if val < 25:
            return "strikingly beautiful"
        return "possessing an almost divine, otherworldly beauty"
    if stat_name == 'hea':
        if val < 8:
            return "sickly and fragile"
        if val < 13:
            return "reasonably healthy"
        if val < 18:
            return "tough and resilient"
        if val < 25:
            return "exceptionally hardy"
        return "virtually indestructible"
    return "average"


def get_combat_desc(atk, dfn, is_self=False):
    pronoun = "You" if is_self else "They"
    if atk < 15:
        atk_desc = "minimal combat capability"
    elif atk < 30:
        atk_desc = "competent offensive skills"
    elif atk < 60:
        atk_desc = "deadly precision"
    elif atk < 100:
        atk_desc = "devastating power"
    else:
        atk_desc = "unstoppable destructive force"

    if dfn < 10:
        dfn_desc = "fragile defenses"
    elif dfn < 25:
        dfn_desc = "solid protection"
    elif dfn < 50:
        dfn_desc = "impenetrable shielding"
    else:
        dfn_desc = "the resilience of a fortress"

    return f"{pronoun} exhibit {atk_desc} and {dfn_desc}."


def get_threat_desc(lvl):
    if lvl < 5:
        return "minimal threat"
    if lvl < 10:
        return "moderate threat"
    if lvl < 15:
        return "significant threat"
    if lvl < 25:
        return "lethal threat"
    return "apocalyptic threat"


def get_rarity_desc(rarity):
    return rarity.upper()


def get_item_bonus_desc(bonus):
    if bonus <= 0:
        return "no noticeable"
    if bonus < 5:
        return "slight"
    if bonus < 10:
        return "modest"
    if bonus < 20:
        return "significant"
    return "massive"


def get_status_str(player):
    rep = get_reputation_title(player.karma)
    status = (f"HP:{player.hp}/{player.hp_max}|MA:{player.mana}/{player.mana_max}|"
              f"LV:{player.lvl}|CR:{player.money}|[{rep}]")
    if player.stat_points > 0:
        status += f"|STATS:{player.stat_points}"
    if player.addiction_points > 0:
        status += f"|ADDICT:{player.addiction_points}%"
    return status


def get_help(player):
    room = player.location
    sb = ["\n=== GRID COMMAND PROTOCOLS ==="]

    sb.append("L/LOOK        : Scan current sector")
    sb.append("L/LOOK <target>: Examine entity, item, or yourself (LOOK ME)")
    sb.append("WHO           : List active terminal nodes")
    sb.append("TOP           : Display top 25 adventurers")
    sb.append("WALL          : View the Wall of Death (most deaths)")
    sb.append("I/INVENTORY   : List equipped and stored hardware")
    sb.append("ST/STATUS     : Detailed user profile data")
    sb.append("SAY <msg>     : Message to current sector")
    sb.append("BROADCAST <msg>: Message to the entire world")
    sb.append("HELP/?        : Display this manual")
    sb.append("USE <item>    : Use hardware/consumable/drug/scroll")
    sb.append("TRAIN <stat>  : Spend stat points (STR, INT, WIL, AGI, HEA, CHA)")
    sb.append("REST          : Rest to recover HP (broken by movement/combat/full HP)")
    sb.append("PARTY <cmd>   : Party system (CREATE, INVITE <player>, ACCEPT, LEAVE, STATUS)")
    sb.append("EXIT          : Log out and disconnect from the grid")

    if room.exits:
        sb.append(f"MOV/DIRS      : Navigation: {', '.join(room.exits.keys()).upper()}")

    if room.items.exists():
        sb.append("G/GET <item>  : Retrieve hardware from ground")

    npcs_exist = NPC.objects.filter(location=room, hp__gt=0).exists()
    players_exist = Player.objects.filter(location=room, online=True).exclude(id=player.id).exists()
    if npcs_exist or players_exist:
        sb.append("A/KILL <target>: Regular attack (one round)")
        sb.append("AA <target>   : Auto-attack (repeated rounds)")

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
    for lvl, name, acronym, desc in moves:
        if player.lvl >= lvl:
            sb.append(f"  {name.upper():15} ({acronym}) (Lv {lvl}): {desc}")

    return "\n".join(sb)


def get_top_ten():
    top_players = Player.objects.order_by('-lvl', '-exp')[:10]
    sb = ["\n=== TOP 10 ADVENTURERS ==="]
    for i, p in enumerate(top_players, 1):
        bot_marker = " (bot)" if p.is_bot else ""
        sb.append(f"{i:2}. {p.user.username}{bot_marker:15} | Lv {p.lvl:2} | EXP: {p.exp:5} | "
                  f"Class: {p.game_class}")
    return "\n".join(sb)


def get_wall_of_death():
    """Display the top players by death count."""
    top_deaths = Player.objects.order_by('-deaths', '-lvl')[:10]
    sb = ["\n=== WALL OF DEATH ==="]
    sb.append("The most fallen souls in the grid:")
    for i, p in enumerate(top_deaths, 1):
        if p.deaths > 0:
            sb.append(f"{i:2}. {p.user.username:15} | {p.deaths:3} deaths | Lv {p.lvl:2} | {p.game_class}")
    if not any(p.deaths > 0 for p in top_deaths):
        sb.append("The wall is empty... for now.")
    return "\n".join(sb)


def get_procedural_desc(obj, viewer=None):
    if isinstance(obj, Player):
        is_self = (viewer and obj.id == viewer.id)
        equipped_items = InventoryItem.objects.filter(player=obj, equipped=True)
        armor = equipped_items.filter(item__item_type='armor').first()
        weapon = equipped_items.filter(item__item_type='weapon').first()
        other_equipped = equipped_items.exclude(item__item_type__in=['armor', 'weapon'])

        rep = get_reputation_title(obj.karma)
        gender_pronoun = obj.gender.lower()
        if gender_pronoun == 'male':
            pronoun_cap = "He"
        elif gender_pronoun == 'female':
            pronoun_cap = "She"
        else:
            pronoun_cap = "They"

        if is_self:
            desc = f"You are a {obj.race} {obj.game_class} known as a {rep}. "
            if armor:
                desc += f"You are wearing {armor.item.name}. "
            else:
                desc += "You are wearing standard-issue synth-rags. "
            if weapon:
                desc += f"You are wielding {weapon.item.name}. "
            if other_equipped.exists():
                names = [ei.item.name for ei in other_equipped]
                desc += f"You also have {', '.join(names)} active. "
        else:
            verb_are = "are" if pronoun_cap == "They" else "is"
            verb_wearing = "are" if pronoun_cap == "They" else "is"
            verb_wielding = "are" if pronoun_cap == "They" else "is"
            verb_has = "have" if pronoun_cap == "They" else "has"
            desc = f"{pronoun_cap} {verb_are} a {obj.race} {obj.game_class} known as a {rep}. "
            if armor:
                desc += f"{pronoun_cap} {verb_wearing} wearing {armor.item.name}. "
            else:
                desc += f"{pronoun_cap} {verb_wearing} wearing standard-issue synth-rags. "
            if weapon:
                desc += f"{pronoun_cap} {verb_wielding} wielding {weapon.item.name}. "
            if other_equipped.exists():
                names = [ei.item.name for ei in other_equipped]
                desc += f"{pronoun_cap} also {verb_has} {', '.join(names)} active. "

        desc += f"{get_combat_desc(obj.attack, obj.defense, is_self=is_self)} "

        pronoun = "you" if is_self else "they"
        subject = "You" if is_self else "They"
        verb = "are" if is_self else "appear"
        seem_verb = "seem" if is_self else "seem"

        desc += (f"Physically, {pronoun} {verb} {get_attribute_desc('str', obj.str_stat)} and "
                 f"{get_attribute_desc('agi', obj.agi_stat)}. {subject} {verb} "
                 f"{get_attribute_desc('hea', obj.hea_stat)}, yet {seem_verb} "
                 f"{get_attribute_desc('int', obj.int_stat)} and "
                 f"{get_attribute_desc('wil', obj.wil_stat)}. "
                 f"Furthermore, {pronoun} {verb} {get_attribute_desc('cha', obj.cha_stat)}. ")

        if is_self:
            if obj.hp < obj.hp_max * 0.3:
                desc += "Your health is critical, systems flickering."
            elif obj.hp < obj.hp_max * 0.7:
                desc += "You show signs of recent combat."
            else:
                desc += "You look ready for action."
        else:
            if obj.hp < obj.hp_max * 0.3:
                desc += "Their health critical, systems flickering."
            elif obj.hp < obj.hp_max * 0.7:
                desc += "They show signs of recent combat."
            else:
                desc += "They look ready for action."
        return desc

    if isinstance(obj, NPC):
        desc = f"{obj.description} This entity appears to be a {get_threat_desc(obj.lvl)}. "
        desc += f"{get_combat_desc(obj.attack, obj.defense, is_self=False)} "
        desc += f"It radiates an energy signature associated with {obj.element.upper()}."

        if obj.hp < obj.hp_max * 0.3:
            desc += " It's badly damaged and near failure."
        elif obj.hp < obj.hp_max * 0.7:
            desc += " It looks somewhat worn down."

        if obj.npc_type == 'boss':
            desc += " It radiates a crushing aura of power. Caution advised."
        elif obj.npc_type == 'dealer':
            desc += " They keep looking over their shoulder."

        if obj.karma_alignment > 50:
            desc += " It seems to represent local law and order."
        elif obj.karma_alignment < -50:
            desc += " It has a distinctly predatory and malevolent presence."

        return desc

    if isinstance(obj, Item):
        desc = obj.description
        desc += f" [Rarity: {get_rarity_desc(obj.rarity)}]"
        if obj.item_type == 'weapon':
            desc += f" It provides a {get_item_bonus_desc(obj.attack_bonus)} boost to offense."
        elif obj.item_type == 'armor':
            desc += f" It provides a {get_item_bonus_desc(obj.defense_bonus)} boost to defense."
        return desc

    return "No detailed data available."


def get_look(player, target_name=None):
    room = player.location
    if not room:
        return "THE VOID."

    if target_name:
        target_name_lower = target_name.lower().strip()
        # Handle common syntax like "look at me"
        if target_name_lower.startswith('at '):
            target_name_lower = target_name_lower[3:].strip()

        if (target_name_lower in ['me', 'sel'] or
                target_name_lower == player.user.username.lower()):
            return f"\n[SCAN: {player.user.username}]\n{get_procedural_desc(player, viewer=player)}"

        # Look at NPC
        npc = NPC.objects.filter(location=room, name__icontains=target_name_lower,
                                 hp__gt=0).first()
        if npc:
            return f"\n[SCAN: {npc.name}]\n{get_procedural_desc(npc)}"

        # Look at Player
        other = Player.objects.filter(location=room, user__username__icontains=target_name_lower,
                                      online=True).exclude(id=player.id).first()
        if other:
            return f"\n[SCAN: {other.user.username}]\n{get_procedural_desc(other, viewer=player)}"

        # Look at Item in room
        item = room.items.filter(name__icontains=target_name_lower).first()
        if item:
            return f"\n[SCAN: {item.name}]\n{get_procedural_desc(item)}"

        # Look at Item in inventory
        ii = InventoryItem.objects.filter(player=player,
                                          item__name__icontains=target_name_lower).first()
        if ii:
            return f"\n[SCAN: {ii.item.name}]\n{get_procedural_desc(ii.item)}"

        return f"Target '{target_name_lower}' not detected in local sector."

    sb = [f"\n[Location] {room.name}"]
    sb.append(f"DATA: {room.description}")

    if room.shop_name:
        sb.append(f"\n[TERMINAL] A commerce node is active here: {room.shop_name}")

    # Advertise Wall of Death in the hub
    if room.zone == 'hub':
        top_deaths = Player.objects.order_by('-deaths', '-lvl')[:3]
        if top_deaths and top_deaths[0].deaths > 0:
            sb.append(f"\n[WALL OF DEATH] Type WALL to see the most fallen. Current leader: {top_deaths[0].user.username} ({top_deaths[0].deaths} deaths)")

    npcs = NPC.objects.filter(location=room, hp__gt=0)
    if npcs.exists():
        sb.append("\nDETECTED ENTITIES:")
        for n in npcs:
            indicator = " [BOSS]" if n.npc_type == 'boss' else ""
            sb.append(f"  > {n.name} ({get_threat_desc(n.lvl)}){indicator}")

    if room.exits:
        sb.append(f"\n[Exits: {', '.join(room.exits.keys()).upper()}]")

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
    if not room.respawn_npcs:
        return ""

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

        npc_names = ["Rogue Drone", "Scavenger", "Corporate Enforcer", "Street Punk",
                     "Glitch-Hulk", "Vigilante", "Paladin-Mech", "Cyber-Assassin"]
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

        NPC.objects.create(
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
            aggressive=(random.random() < 0.3 or is_boss),
            karma_alignment=karma_alignment,
            npc_type=npc_type
        )

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
        # Store old room for broadcast
        old_room = player.location

        # Interrupt rest if player moves
        if player.resting:
            player.resting = False
            player.rest_started_at = None
            player.save()

        player.location = Room.objects.get(id=new_room_id)
        player.save()

        # Broadcast exit to old room
        broadcast_room_event(player, old_room, None, 'exit')

        # Broadcast entry to new room
        broadcast_room_event(player, None, player.location, 'enter')

        # If hidden and moving, re-roll stealth detection for the new room
        stealth_break_msg = ""
        if player.hidden:
            npcs = NPC.objects.filter(location=player.location, hp__gt=0)
            max_npc_lvl = max([n.lvl for n in npcs]) if npcs.exists() else 0
            players_here = Player.objects.filter(location=player.location,
                                                 online=True).exclude(id=player.id)
            max_player_lvl = max([p.lvl for p in players_here]) if players_here.exists() else 0
            threat_lvl = max(max_npc_lvl, max_player_lvl)

            stay_chance = 40 + player.agi_stat // 3
            if threat_lvl > 0:
                lvl_penalty = max(0, (threat_lvl - player.lvl) * 15)
                stay_chance -= lvl_penalty

            if random.randint(1, 100) > stay_chance:
                player.hidden = False
                player.save()
                stealth_break_msg = (
                    f"\n[ALERT] Your cover is blown in the new sector! "
                    f"({stay_chance}% stay hidden)"
                )
            else:
                player.save()
                stealth_break_msg = (
                    f"\n[STEALTH] You remain hidden. ({stay_chance}% stay hidden)"
                )

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
                # Trigger combat start
                player.last_combat_npc = attacker
                player.save()

        return (look_text + stalk_msg + stealth_break_msg + addiction_msg
                + respawn_msg + auto_attack_msg)
    except Room.DoesNotExist:
        return "NAVIGATION ERROR."


def broadcast_room_event(player, old_room, new_room, event_type):
    """Broadcast room entry/exit events to players in the affected rooms."""
    if event_type == 'exit' and old_room:
        players_in_old = Player.objects.filter(location=old_room, online=True).exclude(id=player.id)
        for p in players_in_old:
            p.notification = (p.notification +
                              f"\n[GRID] {player.user.username} leaves the sector.").strip()
            p.save(update_fields=['notification'])

    if event_type == 'enter' and new_room:
        players_in_new = Player.objects.filter(location=new_room, online=True).exclude(id=player.id)
        for p in players_in_new:
            p.notification = (p.notification +
                              f"\n[GRID] {player.user.username} enters the sector.").strip()
            p.save(update_fields=['notification'])


def broadcast_npc_movement(npc, old_room, new_room):
    """Broadcast NPC movement between rooms."""
    if old_room and old_room != new_room:
        players_in_old = Player.objects.filter(location=old_room, online=True)
        for p in players_in_old:
            p.notification = (p.notification +
                              f"\n[GRID] {npc.name} leaves the sector.").strip()
            p.save(update_fields=['notification'])

    if new_room:
        players_in_new = Player.objects.filter(location=new_room, online=True)
        for p in players_in_new:
            p.notification = (p.notification +
                              f"\n[GRID] {npc.name} enters the sector.").strip()
            p.save(update_fields=['notification'])


def calculate_damage(atk, dfn, element='physical', weakness='none',
                     resistance='none', crit_chance=0):
    base_dmg = max(1, atk - dfn // 2)
    dmg = random.randint(max(1, base_dmg - 2), base_dmg + 2)

    # Critical strike check
    is_crit = False
    if crit_chance > 0 and random.randint(1, 100) <= crit_chance:
        is_crit = True
        dmg = int(dmg * 2)  # Critical hits do 2x damage

    strong_against = {'fire': 'air', 'air': 'earth', 'earth': 'water', 'water': 'fire'}

    if element != 'physical':
        if weakness == element or strong_against.get(element) == weakness:
            dmg = int(dmg * 1.5)
        elif resistance == element:
            dmg = int(dmg * 0.5)

    return dmg, is_crit


def handle_player_defeat(player, victor_player=None):
    """Common logic for when a player's HP reaches zero."""
    output = "\n[CRITICAL ERROR] YOU HAVE BEEN NEUTRALIZED. INITIATING SYSTEM RESET."
    stolen = player.money // 4
    player.hp = player.hp_max // 2
    player.money = max(0, player.money - stolen)
    player.location = Room.objects.get(id=1)
    player.last_combat_npc = None
    player.last_combat_player = None
    player.auto_attack = False
    player.save()
    output += f"\nRespawned at The Neon Hub. Lost {stolen} credits."

    if victor_player:
        victor_player.money += stolen
        victor_player.exp += player.lvl * 50
        victor_player.notification = (
            f"\nYou neutralized {player.user.username}! "
            f"+{player.lvl * 50} exp, +{stolen} credits."
        )
        victor_player.save()

    return output


def combat_round(player):
    """Performs one round of combat for the player and their current target."""
    output = ""
    target_npc = player.last_combat_npc
    target_player = player.last_combat_player

    if not target_npc and not target_player:
        player.auto_attack = False
        player.save()
        return ""

    target = target_npc or target_player

    # Check if target is still valid/in room
    if isinstance(target, NPC):
        if target.hp <= 0 or target.location != player.location:
            player.last_combat_npc = None
            player.auto_attack = False
            player.save()
            return f"\n[COMBAT] {target.name} is no longer here."
    else:
        if target.hp <= 0 or target.location != player.location or not target.online:
            player.last_combat_player = None
            player.auto_attack = False
            player.save()
            return f"\n[COMBAT] {target.user.username} is no longer here."
    
    # Get all players in the room for combat broadcasting
    room_players = Player.objects.filter(
        location=player.location, 
        online=True
    ).exclude(id=player.id)
    if target_player:
        room_players = room_players.exclude(id=target_player.id)

    # Player attacks
    equipped_weapon = InventoryItem.objects.filter(
        player=player, equipped=True, item__item_type='weapon'
    ).first()
    speed_bonus = equipped_weapon.item.speed_bonus if equipped_weapon else 0
    agi_attacks = player.agi_stat // 10
    base_attacks = 1 + (speed_bonus // 10) if speed_bonus > 0 else 1
    p_attacks = base_attacks + agi_attacks

    target_name = target.name if target_npc else target.user.username

    # Calculate critical strike chance based on agility (for physical attacks)
    # AGI stat: 1-25+ gives 1-5% crit chance, capping at 10%
    agi_crit_chance = min(10, max(1, player.agi_stat // 5))

    for _ in range(p_attacks):
        if isinstance(target, NPC):
            dmg, is_crit = calculate_damage(
                player.attack, target.defense, element='physical',
                weakness=target.weakness, resistance=target.resistance,
                crit_chance=agi_crit_chance
            )
        else:
            dmg, is_crit = calculate_damage(
                player.attack, target.defense, crit_chance=agi_crit_chance
            )

        target.hp -= dmg
        target.save()
        if is_crit:
            output += f"\n[CRIT] You hit {target_name} for {dmg} damage!"
            # Broadcast crit to room
            broadcast_combat_to_room(player, target_name, f"[CRIT] {player.user.username} hits {target_name} for {dmg} damage!", room_players)
        else:
            output += f"\nYou hit {target_name} for {dmg} damage."
            # Broadcast hit to room
            broadcast_combat_to_room(player, target_name, f"{player.user.username} hits {target_name} for {dmg} damage.", room_players)

        if target.hp <= 0:
            # Win logic
            if target_npc:
                # Bots gain EXP at 50% rate (slower than humans)
                exp_gain = target.exp_drop
                if player.is_bot:
                    exp_gain = int(target.exp_drop * 0.5)
                player.exp += exp_gain
                player.money += target.money_drop
                player.last_combat_npc = None

                if target.karma_alignment < -30:
                    player.karma += 5
                elif target.karma_alignment > 30:
                    player.karma -= 10
                else:
                    player.karma += 1

                player.karma = max(-100, min(100, player.karma))
                player.save()

                output += (f"\nTarget neutralized! +{exp_gain} exp, "
                           f"+{target.money_drop} credits.")
                # Broadcast victory to room
                broadcast_combat_to_room(player, target_name, f"{player.user.username} neutralized {target_name}!", room_players)
                for item in target.drops.all():
                    ii, created = InventoryItem.objects.get_or_create(player=player, item=item)
                    if not created:
                        ii.quantity += 1
                    ii.save()
                    output += f"\nRetrieved: {item.name}"
                output += check_level_up(player)
            else:
                exp_gain = target.lvl * 50
                # Bots gain EXP at 50% rate (slower than humans)
                if player.is_bot:
                    exp_gain = int(target.lvl * 50 * 0.5)
                player.exp += exp_gain
                stolen = target.money // 4
                player.money += stolen
                player.last_combat_player = None
                player.save()

                hub = Room.objects.get(id=1)
                target.hp = target.hp_max // 2
                target.money -= stolen
                target.location = hub
                notif_msg = (f"\nYou were neutralized by {player.user.username}! "
                             f"Lost {stolen} credits.")
                target.notification = notif_msg
                target.save()
                output += (f"\nYou neutralized {target_name}! +{exp_gain} exp, "
                           f"+{stolen} credits.")
                # Broadcast PvP victory to room
                broadcast_combat_to_room(player, target_name, f"{player.user.username} neutralized {target_name}!", room_players)
                output += check_level_up(player)

            player.auto_attack = False
            player.save()
            return output

    # Target counter-attacks
    output += execute_opponent_attack(player, target)
    
    # Broadcast counter-attack to room
    if "hits you" in output:
        counter_msg = f"{target_name} hits {player.user.username}!"
        broadcast_combat_to_room(player, target_name, counter_msg, room_players)
    
    return output


def execute_opponent_attack(player, target):
    """Internal logic for the opponent striking the player."""
    output = ""
    target_npc = isinstance(target, NPC)

    if target_npc:
        target_dmg, _ = calculate_damage(target.attack, player.defense, element=target.element)
        player.hp -= target_dmg
        output += f"\n{target.name} hits you for {target_dmg} damage."
    else:
        # opponent is a Player - can also crit based on their AGI
        t_weapon = InventoryItem.objects.filter(
            player=target, equipped=True, item__item_type='weapon'
        ).first()
        t_speed = t_weapon.item.speed_bonus if t_weapon else 0
        t_agi_attacks = target.agi_stat // 10
        t_base_attacks = 1 + (t_speed // 10) if t_speed > 0 else 1
        t_attacks = t_base_attacks + t_agi_attacks
        t_crit_chance = min(10, max(1, target.agi_stat // 5))

        for _ in range(t_attacks):
            counter_dmg, is_crit = calculate_damage(
                target.attack, player.defense, crit_chance=t_crit_chance
            )
            player.hp -= counter_dmg
            if is_crit:
                output += f"\n[CRIT] {target.user.username} hits you for {counter_dmg} damage!"
            else:
                output += f"\n{target.user.username} hits you for {counter_dmg} damage."
            if player.hp <= 0:
                break

    player.save()

    if player.hp <= 0:
        # Broadcast death to room before handling defeat
        if target_npc:
            death_msg = f"{player.user.username} has been splattered by {target.name}! Blood and circuitry everywhere!"
        else:
            death_msg = f"{player.user.username} has been neutralized by {target.user.username}! A brutal end!"
        room_players = Player.objects.filter(
            location=player.location, online=True
        ).exclude(id=player.id)
        for p in room_players:
            p.notification = (p.notification + f"\n[DEATH] {death_msg}").strip()
            p.save(update_fields=['notification'])
        output += handle_player_defeat(player, victor_player=(None if target_npc else target))

    return output


def broadcast_combat_to_room(attacker, target_name, message, room_players):
    """Broadcast combat message to all other players in the room."""
    for p in room_players:
        p.notification = (p.notification + f"\n[COMBAT] {message}").strip()
        p.save(update_fields=['notification'])


def attack_target(player, target_name, auto=False):
    if not target_name:
        # If already in combat and no target specified, just do a round
        if player.last_combat_npc or player.last_combat_player:
            player.auto_attack = auto
            player.save()
            return combat_round(player)
        return "Specify target."

    if player.location.safe_zone:
        return "Violence is prohibited in this sector."

    # Try to find NPC
    npc = NPC.objects.filter(location=player.location, name__icontains=target_name,
                             hp__gt=0).first()
    # Try to find Player
    other = None
    if not npc:
        other = Player.objects.filter(
            location=player.location, user__username__icontains=target_name,
            online=True
        ).exclude(id=player.id).first()

    if not npc and not other:
        return "Target not found."

    if other:
        if abs(player.lvl - other.lvl) > 3:
            return "Target level too distant. Range: +/- 3 levels."
        player.last_combat_player = other
        player.last_combat_npc = None
        player.karma -= 10
    else:
        player.last_combat_npc = npc
        player.last_combat_player = None

    player.auto_attack = auto
    player.last_combat_tick = timezone.now()
    player.save()

    # Backstab bonus if hidden
    output = ""
    if player.hidden:
        player.hidden = False
        player.save()
        output += "\n[BACKSTAB] Strike from the shadows! They never saw you coming."

    output += combat_round(player)
    return output


def process_combat_tick(player):
    """Called during polling to check if an auto-attack or opponent strike should happen."""
    target = player.last_combat_npc or player.last_combat_player
    if not target:
        return ""

    now = timezone.now()
    if not player.last_combat_tick:
        player.last_combat_tick = now
        player.save()
        return ""

    # Combat tick every 3 seconds
    if (now - player.last_combat_tick).total_seconds() >= 3:
        player.last_combat_tick = now
        player.save()
        if player.auto_attack:
            return combat_round(player)
        else:
            # Player is IDLE in combat, opponent takes advantage
            t_name = target.name if hasattr(target, 'name') else target.user.username
            output = f"\n[COMBAT] You are idle! {t_name} strikes!"
            output += execute_opponent_attack(player, target)
            return output

    return ""


def rest_command(player):
    """Allows player to rest and regenerate HP and Mana over time."""
    # Can't rest if in combat
    if player.last_combat_npc or player.last_combat_player:
        return "Cannot rest while engaged in combat."

    # Can't rest if already at full HP and Mana
    if player.hp >= player.hp_max and player.mana >= player.mana_max:
        return "Already at full health and mana. No need to rest."

    # Can't rest if already resting
    if player.resting:
        return "Already resting."

    # Start resting
    player.resting = True
    player.rest_started_at = timezone.now()
    player.save()

    return "\nYou settle down to rest and recover HP and Mana..."


def process_resting(player):
    """Process HP and Mana regeneration for resting players. Called during polling."""
    if not player.resting:
        return ""

    # Check if rest should be interrupted
    # Interrupted by: combat, movement (handled elsewhere), or full HP and Mana
    if player.hp >= player.hp_max and player.mana >= player.mana_max:
        player.resting = False
        player.rest_started_at = None
        player.save()
        return "\n[REST] You feel fully recovered. Ready to move."

    if player.last_combat_npc or player.last_combat_player:
        player.resting = False
        player.rest_started_at = None
        player.save()
        return "\n[REST] Combat detected! Rest interrupted!"

    # Calculate HP regeneration
    # Base regen: 1 HP per 3 seconds, modified by health stat
    # Higher HEA = faster regen
    hp_regen_rate = max(1, player.hea_stat // 5)  # 1-4 HP per tick depending on HEA
    # Mana regen: 1 Mana per tick, modified by INT stat
    mana_regen_rate = max(1, player.int_stat // 5)  # 1-4 Mana per tick depending on INT
    regen_interval = max(2, 5 - (player.hea_stat // 10))
    # 2-5 seconds between regen

    if not player.rest_started_at:
        player.rest_started_at = timezone.now()
        player.save()
        return ""

    time_resting = (timezone.now() - player.rest_started_at).total_seconds()

    if time_resting >= regen_interval:
        # Regenerate HP
        old_hp = player.hp
        player.hp = min(player.hp_max, player.hp + hp_regen_rate)
        # Regenerate Mana
        old_mana = player.mana
        player.mana = min(player.mana_max, player.mana + mana_regen_rate)
        player.rest_started_at = timezone.now()
        player.save()

        msg_parts = []
        if player.hp != old_hp:
            msg_parts.append(f"Recovered {player.hp - old_hp} HP")
        if player.mana != old_mana:
            msg_parts.append(f"Recovered {player.mana - old_mana} Mana")
        if msg_parts:
            return f"\n[REST] {' and '.join(msg_parts)}. ({player.hp}/{player.hp_max} HP, {player.mana}/{player.mana_max} Mana)"

    return ""


def use_ability(player, ability_name, target_name):
    ability_name = ability_name.lower()
    original_ability_name = ability_name

    # Universal sneak/stealth - works for any class, but success varies
    if ability_name in ('stealth', 'sneak'):
        # ENHANCED: Can only sneak outside combat
        if player.last_combat_npc or player.last_combat_player:
            return "\nCannot hide while engaged in combat. Disengage first."

        # ENHANCED: Can't sneak while resting
        if player.resting:
            player.resting = False
            player.rest_started_at = None
            player.save()
            return "\nYou stop resting and stand up to attempt stealth."

        if player.location.safe_zone:
            return "\nNo need to hide in a safe sector."

        npcs = NPC.objects.filter(location=player.location, hp__gt=0)
        max_npc_lvl = max([n.lvl for n in npcs]) if npcs.exists() else 0
        players_here = Player.objects.filter(location=player.location,
                                             online=True).exclude(id=player.id)
        max_player_lvl = max([p.lvl for p in players_here]) if players_here.exists() else 0
        threat_lvl = max(max_npc_lvl, max_player_lvl)

        # ENHANCED: Sneaking tied to agility stat
        # Base chance heavily influenced by AGI stat
        if player.game_class in ('Thief', 'Trickster') and player.lvl >= 4:
            # Thief/Trickster: AGI is primary stat, get excellent stealth
            base_chance = 50 + (player.agi_stat * 2)  # 70-130 base, capped at 95
        else:
            # Other classes: AGI still matters but less so
            base_chance = 20 + (player.agi_stat * 1.5)  # 35-95 base
            if player.lvl < 4:
                base_chance = max(5, base_chance - 20)

        # Threat level penalty
        if threat_lvl > 0:
            lvl_penalty = max(0, (threat_lvl - player.lvl) * 10)
            base_chance -= lvl_penalty

        # Clamp chance between 5% and 95%
        base_chance = max(5, min(95, base_chance))

        if random.randint(1, 100) <= base_chance:
            player.hidden = True
            player.save()
            agi_bonus = (
                f" (AGI: {player.agi_stat})"
                if player.game_class not in ('Thief', 'Trickster') else ""
            )
            return f"\nYou melt into the shadows. Hidden!{agi_bonus}"
        else:
            player.hidden = False
            player.save()
            return "\nFailed to hide. You remain visible."

    # Check if this command is actually a move for this class
    moves = CLASS_MOVES.get(player.game_class, [])
    req_lvl = 999
    found_name = None
    for lvl, name, acronym, desc in moves:
        # Match by full name or acronym
        if name.lower() == ability_name or acronym.lower() == ability_name:
            req_lvl = lvl
            found_name = name
            break

    if req_lvl == 999:  # Not a move for this class
        return None

    if player.lvl < req_lvl:
        return f"Level required for {ability_name.upper()}."

    npc = None
    target_player = None
    if target_name:
        npc = NPC.objects.filter(location=player.location, name__icontains=target_name,
                                 hp__gt=0).first()
        target_player = Player.objects.filter(location=player.location,
                                               user__username__icontains=target_name,
                                               online=True).exclude(id=player.id).first()

    if target_player:
        if player.lvl < 5:
            return "Neural safety lock engaged. Level 5 required to target users."
        if abs(player.lvl - target_player.lvl) > 3:
            return "Target level too distant. Range: +/- 3 levels."
        if player.location.safe_zone:
            return "Violence is prohibited in this sector."

    target = npc or target_player
    cost = 5 + (req_lvl // 2)
    if player.mana < cost:
        return "INSUFFICIENT BUFFER (MANA)."

    player.mana -= cost
    player.save()

    res = f"You use {ability_name.upper()}."

    # Damage calculation helper
    def deal_dmg(mult, element='physical'):
        nonlocal res
        if not target:
            res += "\nTarget required."
            return

        # Calculate critical strike chance based on INT for spells, AGI for physical
        if element == 'physical':
            crit_chance = min(10, max(1, player.agi_stat // 5))
        else:
            crit_chance = min(10, max(1, player.int_stat // 5))

        # Improved scaling logic
        # Scaling stats based on class primary attributes
        primary_stat = 10
        if player.game_class in ('Street Samurai', 'Heavy'):
            primary_stat = player.str_stat
        elif player.game_class == 'Jade Dragon':
            primary_stat = player.agi_stat
        elif player.game_class in ('Netrunner', 'Techie'):
            primary_stat = player.int_stat
        elif player.game_class in ('Psycher', 'Warlock'):
            primary_stat = player.int_stat
        elif player.game_class in ('Priest',):
            primary_stat = player.wil_stat
        elif player.game_class in ('Thief'):
            primary_stat = player.agi_stat
        elif player.game_class in ('Medie',):
            primary_stat = max(player.int_stat, player.hea_stat)
        elif player.game_class in ('Fixer', 'Trickster'):
            primary_stat = player.cha_stat

        # Base power: primary stat influence + base attack influence
        power_val = (primary_stat * 1.5) + (player.attack * 0.5)

        # Scaling by ability requirement level (more advanced moves are inherently stronger)
        req_mult = 1.0 + (req_lvl / 20.0)

        final_atk = int(power_val * mult * req_mult)

        dmg, is_crit = calculate_damage(
            final_atk, target.defense, element=element, crit_chance=crit_chance
        )
        target.hp -= dmg

        if isinstance(target, Player):
            player.karma -= 2
            player.save()
            target.save()
            if is_crit:
                res += f"\n[CRIT] You hit {target.user.username} for {dmg} {element} damage!"
            else:
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
                res += f"\nYou neutralized {target.user.username}! +{exp_gain} exp, +{stolen} CR."
        else:
            target.save()
            if is_crit:
                res += f"\n[CRIT] You hit {target.name} for {dmg} {element} damage!"
            else:
                res += f"\nYou hit {target.name} for {dmg} {element} damage."
            if target.hp <= 0:
                player.exp += target.exp_drop
                player.money += target.money_drop
                player.save()
                res += (f"\nTarget neutralized! +{target.exp_drop} exp, "
                        f"+{target.money_drop} credits.")
                for item in target.drops.all():
                    ii, created = InventoryItem.objects.get_or_create(player=player, item=item)
                    if not created:
                        ii.quantity += 1
                    ii.save()
                    res += f"\nRetrieved: {item.name}"
                res += check_level_up(player)
        return

    # Abilities Logic - High level mappings
    if ability_name == 'blade':
        deal_dmg(1.2)
    elif ability_name == 'oni_strike':
        deal_dmg(2.5, 'fire')
    elif ability_name == 'zansetsu':
        deal_dmg(3.0)
    elif ability_name == 'mirage':
        buff = 20 + (player.agi_stat // 2)
        player.defense += buff
        player.save()
        res += "\nDefense boosted significantly."
    elif ability_name == 'whirlwind':
        deal_dmg(1.5)
        deal_dmg(1.5)
    elif ability_name == 'dragon_lunge':
        deal_dmg(4.0, 'fire')
    elif ability_name == 'omnislash':
        deal_dmg(2.0)
        deal_dmg(2.0)
        deal_dmg(2.0)
        deal_dmg(2.0)

    elif ability_name == 'hack':
        deal_dmg(2.0, 'water')
    elif ability_name == 'overload':
        deal_dmg(2.5, 'air')
    elif ability_name == 'synapse_burn':
        deal_dmg(3.0, 'fire')
    elif ability_name == 'logic_bomb':
        deal_dmg(3.5, 'air')
    elif ability_name == 'blackout':
        if target:
            debuff = 10 + (player.int_stat // 3)
            target.attack = max(1, target.attack - debuff)
            target.defense = max(1, target.defense - debuff)
            target.save()
            res += "\nTarget systems crippled."
        else:
            res += "\nTarget required."
    elif ability_name == 'databreach':
        if npc:
            stolen = random.randint(10, 50) + (player.int_stat // 2)
            player.money += stolen
            player.save()
            res += f"\nSiphoned {stolen} credits!"
        deal_dmg(3.0, 'water')
    elif ability_name == 'zero_day':
        deal_dmg(10.0, 'water')

    elif ability_name == 'patch':
        heal = 20 + (player.int_stat * 2)
        player.hp = min(player.hp_max, player.hp + heal)
        player.save()
        res += "\nHealed HP."
    elif ability_name == 'detox':
        player.addiction_points = max(
            0, player.addiction_points - 15 - (player.int_stat // 5)
        )
        player.save()
        res += "\nToxins cleared."
    elif ability_name == 'heal':
        heal = 40 + (player.wil_stat * 2)
        player.hp = min(player.hp_max, player.hp + heal)
        player.save()
        res += "\nHealed HP."
    elif ability_name == 'bless':
        buff = 10 + (player.wil_stat // 5)
        player.defense += buff
        player.attack += buff // 2
        player.save()
        res += "\nYou are blessed."

    # Generic keyword-based handlers for other moves
    elif any(x in ability_name for x in [
        'strike', 'slash', 'blade', 'lunge', 'storm', 'whirlwind', 'stab', 'smash',
        'toss', 'bolt', 'burn', 'plasma', 'arc', 'shock', 'flare', 'pulse',
        'assassinate', 'judgment', 'annihilation', 'destruction', 'armageddon'
    ]):
        mult = 2.0 + (req_lvl / 15.0)
        elem = 'physical'
        if any(x in ability_name for x in ['bolt', 'pulse', 'arc', 'tesla']):
            elem = 'air'
        if any(x in ability_name for x in [
            'burn', 'fire', 'flare', 'oni', 'plasma', 'armageddon'
        ]):
            elem = 'fire'
        if any(x in ability_name for x in [
            'seismic', 'earth', 'singularity', 'dart', 'nanobot'
        ]):
            elem = 'earth'
        if any(x in ability_name for x in [
            'hack', 'water', 'ice', 'black', 'zero', 'siphon'
        ]):
            elem = 'water'
        deal_dmg(mult, elem)
    elif any(x in ability_name for x in [
        'boost', 'shield', 'iron', 'protocol', 'vanish', 'smoke', 'mirage', 'image', 'bless'
    ]):
        stat_val = (
            player.int_stat if player.game_class == 'Psycher'
            else (player.wil_stat if player.game_class == 'Priest'
            else (player.agi_stat if player.game_class == 'Thief' else player.hea_stat))
        )
        buff = 10 + req_lvl + (stat_val // 2)
        player.defense += buff
        player.save()
        res += "\nDefense boosted."
    elif any(x in ability_name for x in [
        'heal', 'patch', 'purify', 'restoration', 'resuscitate', 'regeneration'
    ]):
        stat_val = player.wil_stat if player.game_class == 'Priest' else player.int_stat
        heal = 20 + req_lvl * 3 + (stat_val * 2)
        player.hp = min(player.hp_max, player.hp + heal)
        player.save()
        res += "\nHealed HP."
    elif ability_name == 'soul_drain':
        if target:
            soul_stat = player.int_stat if player.game_class == 'Psycher' else player.wil_stat
            dmg, _ = calculate_damage(int(soul_stat * 2.5), target.defense, element='water')
            target.hp -= dmg
            player.hp = min(player.hp_max, player.hp + dmg // 2)
            target.save()
            player.save()
            res += "\nDrained HP!"
        else:
            res += "\nTarget required."
    elif ability_name in ('scheme', 'sleight_of_hand'):
        if npc:
            stolen = random.randint(1, 20) + player.cha_stat
            player.money += stolen
            player.save()
            res += "\nDrained credits."
        else:
            res = "Requires NPC target."
    elif ability_name == 'jackpot':
        if target:
            if random.random() > 0.5:
                dmg = int(player.cha_stat * 6)
                target.hp -= dmg
                target.save()
                res += "\nJACKPOT! Damage dealt!"
            else:
                loot = random.randint(50, 300) + (player.cha_stat * 2)
                player.money += loot
                player.save()
                res += "\nJACKPOT! Credits siphoned!"
        else:
            res += "\nTarget required."
    # Jade Dragon abilities
    elif ability_name == 'palm_strike':
        # Unarmed bonus: +50% damage if no weapon equipped
        unarmed_mult = 1.5 if not InventoryItem.objects.filter(player=player, equipped=True, item__item_type='weapon').exists() else 1.0
        deal_dmg(1.2 * unarmed_mult)
    elif ability_name == 'crane_kick':
        unarmed_mult = 1.5 if not InventoryItem.objects.filter(player=player, equipped=True, item__item_type='weapon').exists() else 1.0
        deal_dmg(2.0 * unarmed_mult, 'air')
    elif ability_name == 'iron_palm':
        buff = 15 + (player.agi_stat // 3)
        player.defense += buff
        player.save()
        res += "\nYour chi hardens your body. Defense boosted."
    elif ability_name == 'tiger_claw':
        unarmed_mult = 1.5 if not InventoryItem.objects.filter(player=player, equipped=True, item__item_type='weapon').exists() else 1.0
        deal_dmg(2.5 * unarmed_mult)
        deal_dmg(2.5 * unarmed_mult)
    elif ability_name == 'dragon_kick':
        unarmed_mult = 1.5 if not InventoryItem.objects.filter(player=player, equipped=True, item__item_type='weapon').exists() else 1.0
        deal_dmg(4.0 * unarmed_mult, 'fire')
    elif ability_name == 'chi_burst':
        deal_dmg(3.5, 'air')
    elif ability_name == 'jade_ascension':
        unarmed_mult = 1.5 if not InventoryItem.objects.filter(player=player, equipped=True, item__item_type='weapon').exists() else 1.0
        deal_dmg(2.5 * unarmed_mult)
        deal_dmg(2.5 * unarmed_mult)
        deal_dmg(2.5 * unarmed_mult)
        deal_dmg(2.5 * unarmed_mult)
    elif ability_name == 'bamboozle':
        if target:
            debuff = 15 + (player.cha_stat // 3)
            target.defense = max(1, target.defense - debuff)
            target.save()
            res += "\nTarget bamboozled!"
        else:
            res += "\nTarget required."
    else:
        # Fallback for anything else in CLASS_MOVES
        deal_dmg(1.5 + (req_lvl / 15.0))

    if npc and npc.hp > 0:
        npc_dmg, _ = calculate_damage(npc.attack, player.defense, element=npc.element)
        player.hp -= npc_dmg
        player.save()
        res += f"\n{npc.name} counters for {npc_dmg} damage!"

    return res


def use_item(player, item_name):
    if not item_name:
        return "Use what?"
    ii = InventoryItem.objects.filter(player=player, item__name__icontains=item_name).first()
    if not ii:
        return "Not in inventory."

    item = ii.item
    output = f"You use {item.name}."

    if item.item_type == 'consumable':
        if item.heal_amount > 0:
            player.hp = min(player.hp_max, player.hp + item.heal_amount)
            output += "\nHealed HP."
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
        return output + (f"\n[TELEPORT] Transferred to {player.location.name}.\n" +
                         get_look(player))

    ii.quantity -= 1
    if ii.quantity <= 0:
        ii.delete()
    else:
        ii.save()
    player.save()
    return output


def train_stat(player, stat):
    if player.stat_points <= 0:
        return "You have no stat points to spend."

    stat = stat.upper()
    if stat == "STR":
        player.str_stat += 1
        player.attack += 2
    elif stat == "INT":
        player.int_stat += 1
        player.mana_max += 5
    elif stat == "WIL":
        player.wil_stat += 1
        player.mana_max += 5
    elif stat == "AGI":
        player.agi_stat += 1
        player.defense += 1
    elif stat == "HEA":
        player.hea_stat += 1
        player.hp_max += 10
    elif stat == "CHA":
        player.cha_stat += 1
    else:
        return "Invalid stat. Choose STR, INT, WIL, AGI, HEA, or CHA."

    player.stat_points -= 1
    player.save()
    return f"You trained {stat}. Points remaining: {player.stat_points}"


def get_map_data(player):
    room = player.location
    if not room:
        return "[]"
    visited = set()
    to_visit = [(room, 0)]
    room_data = []
    while to_visit:
        r, depth = to_visit.pop(0)
        if r.id in visited or depth > 4:
            continue
        visited.add(r.id)
        room_data.append({
            'id': r.id, 'name': r.name,
            'x': r.map_x, 'y': r.map_y,
            'current': (r.id == room.id),
            'players': Player.objects.filter(location=r,
                                             online=True).exclude(id=player.id).exclude(is_bot=True).count(),
            'bots': Player.objects.filter(location=r,
                                          online=True,
                                          is_bot=True).exclude(id=player.id).count(),
            'npcs': NPC.objects.filter(location=r, hp__gt=0).count(),
            'safe': r.safe_zone,
        })
        for rid in r.exits.values():
            try:
                nr = Room.objects.get(id=rid)
                if nr.id not in visited:
                    to_visit.append((nr, depth + 1))
            except Room.DoesNotExist:
                pass
    return json.dumps(room_data)


def get_status_detailed(player):
    sb = [f"\n=== User Profile: {player.user.username} ==="]
    sb.append(f"Level: {player.lvl}")
    sb.append(f"Credits: {player.money} | Stat Points: {player.stat_points} | "
              f"Karma: {player.karma} ({get_reputation_title(player.karma)})")
    sb.append(f"Path (Race): {player.race} | Class: {player.game_class}")
    race_char = RACE_CHARACTERISTICS.get(player.race, '')
    if race_char:
        sb.append(f"Race Trait: {race_char}")
    if player.addiction_points > 0:
        sb.append(f"ADDICTION: {player.addiction_points}%")

    sb.append("\nBiological & Cybernetic Data:")
    sb.append(f"  Strength:  {player.str_stat:2} ({get_attribute_desc('str', player.str_stat)})")
    sb.append(f"  Agility:   {player.agi_stat:2} ({get_attribute_desc('agi', player.agi_stat)})")
    sb.append(f"  Intellect: {player.int_stat:2} ({get_attribute_desc('int', player.int_stat)})")
    sb.append(f"  Willpower: {player.wil_stat:2} ({get_attribute_desc('wil', player.wil_stat)})")
    sb.append(f"  Health:    {player.hea_stat:2} ({get_attribute_desc('hea', player.hea_stat)})")
    sb.append(f"  Charm:     {player.cha_stat:2} ({get_attribute_desc('cha', player.cha_stat)})")

    # Show equipped weapon
    equipped_weapon = InventoryItem.objects.filter(player=player, equipped=True,
                                                   item__item_type='weapon').first()
    if equipped_weapon:
        sb.append(f"\nEquipped Weapon: {equipped_weapon.item.name}")

    sb.append("\nCombat Assessment:")
    sb.append(f"  ATK: {player.attack:2} | DEF: {player.defense:2}")
    sb.append(f"  {get_combat_desc(player.attack, player.defense, is_self=True)}")

    sb.append("\nLearned Moves:")
    moves = CLASS_MOVES.get(player.game_class, [])
    found = False
    for lvl, name, acronym, desc in moves:
        if player.lvl >= lvl:
            sb.append(f"  {name.upper():15} ({acronym}): {desc}")
            found = True
    if not found:
        sb.append("  None")

    sb.append("\nPersonal Narrative Assessment:")
    sb.append(get_procedural_desc(player, viewer=player))

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
        output += "\nGranted 1 stat point. Use TRAIN <stat> to spend it."

        # Notify about new moves
        moves = CLASS_MOVES.get(player.game_class, [])
        for lvl, name, acronym, _ in moves:
            if player.lvl == lvl:
                output += f"\n[SYSTEM] New move unlocked: {name.upper()} ({acronym})!"

        if player.lvl == 5:
            output += "\n[NEW ABILITIES UNLOCKED! Type HELP for details]"
            output += "\n[ALERT] NPC AGGRESSION PROTOCOLS ACTIVATED."
    return output


def handle_say(player, message):
    if not message:
        return "Say what?"
    ChatMessage.objects.create(sender=player, room=player.location, message=message)
    return f"You say: {message}"


def handle_broadcast(player, message):
    if not message:
        return "Broadcast what?"
    ChatMessage.objects.create(sender=player, room=None, message=message)
    return f"You broadcast to the world: {message}"


def get_recent_chat(player):
    cutoff = timezone.now() - timezone.timedelta(seconds=30)
    # Get room messages or world messages
    msgs = ChatMessage.objects.filter(
        Q(room=player.location) | Q(room=None),
        timestamp__gt=cutoff
    ).exclude(sender=player).order_by('timestamp')
    if not msgs:
        return ""

    chat_lines = []
    for m in msgs:
        label = "[Local]" if m.room else "[Global]"
        chat_lines.append(f"{label} {m.sender.user.username}: {m.message}")
    return "\n".join(chat_lines)


def get_inventory(player):
    items = InventoryItem.objects.filter(player=player)
    if not items.exists():
        return "Memory slots empty."
    sb = ["\n=== Hardware Inventory ==="]
    for ii in items:
        eq = " [E]" if ii.equipped else ""
        qty = f" x{ii.quantity}" if ii.quantity > 1 else ""
        sb.append(f"  {ii.item.name}{qty}{eq} ({ii.item.subtype})")
    return "\n".join(sb)


def get_item(player, item_name):
    if not item_name:
        return "Get what?"
    item = player.location.items.filter(name__icontains=item_name).first()
    if not item:
        return "Item not found."
    player.location.items.remove(item)
    ii, created = InventoryItem.objects.get_or_create(player=player, item=item)
    if not created:
        ii.quantity += 1
    ii.save()
    return f"Retrieved {item.name}."


def drop_item(player, item_name):
    if not item_name:
        return "Drop what?"
    ii = InventoryItem.objects.filter(player=player, item__name__icontains=item_name).first()
    if not ii:
        return "You don't have that."
    if ii.equipped:
        return "Unequip first."
    player.location.items.add(ii.item)
    name = ii.item.name
    if ii.quantity > 1:
        ii.quantity -= 1
        ii.save()
    else:
        ii.delete()
    return f"Discarded {name}."


def equip_item(player, item_name):
    if not item_name:
        return "Equip what?"
    ii = InventoryItem.objects.filter(player=player, item__name__icontains=item_name).first()
    if not ii:
        return "Not in inventory."

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

    # Check restrictions
    if ii.item.item_type in ['weapon', 'armor']:
        limits = GEAR_LIMITS.get(player.game_class)
        if limits:
            allowed_subtypes = limits.get(ii.item.item_type, [])
            if allowed_subtypes and ii.item.subtype not in allowed_subtypes:
                allowed_str = ', '.join(allowed_subtypes)
                return (f"Incompatible hardware. {player.game_class} can only equip "
                        f"{allowed_str} {ii.item.item_type}s.")

    if ii.item.item_type == 'weapon':
        old = InventoryItem.objects.filter(player=player, equipped=True,
                                           item__item_type='weapon').first()
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
        old = InventoryItem.objects.filter(player=player, equipped=True,
                                           item__item_type='armor').first()
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
    if not player.location.shop_name:
        return "No terminal shop detected."

    if player.location.shop_inventory.exists():
        items = player.location.shop_inventory.all().order_by('item_type', 'name')
    else:
        # Default shops only sell common and uncommon items
        items = Item.objects.filter(price__gt=0).exclude(
            rarity__in=['rare', 'epic', 'legendary']).order_by('item_type', 'name')

    # Limit to ~12 items to avoid scrolling
    items = items[:12]

    sb = [f"\n=== {player.location.shop_name} Inventory ==="]

    current_type = None
    for item in items:
        if item.item_type != current_type:
            current_type = item.item_type
            sb.append(f"\n[{current_type.upper()}]")
        sb.append(f"  {item.name:25} ({item.subtype:10}) {item.price} CR")
    return "\n".join(sb)


def buy_item(player, item_name):
    if not player.location.shop_name:
        return "No shop here."

    if player.location.shop_inventory.exists():
        item = player.location.shop_inventory.filter(
            name__icontains=item_name, price__gt=0
        ).first()
    else:
        item = Item.objects.filter(name__icontains=item_name, price__gt=0).exclude(
            rarity__in=['rare', 'epic', 'legendary']
        ).first()

    if not item:
        return "Item not in database or unavailable at this terminal."
    if player.money < item.price:
        return "Insufficient credits."
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
        target_npc = NPC.objects.filter(location=player.location, name__icontains=npc_name,
                                         hp__gt=0).first()
        if not target_npc:
            return f"Target '{npc_name}' not found."

    ii = InventoryItem.objects.filter(player=player, item__name__icontains=item_name).first()
    if not ii:
        return "You don't have that."
    if ii.equipped:
        return "Unequip first."

    if target_npc:
        if target_npc.npc_type == 'dealer' and ii.item.item_type == 'drug':
            price = int(ii.item.price * 1.2)  # Dealers pay more for drugs
            player.money += price
            player.karma -= 5  # Selling drugs is significantly bad
            player.save()
            name = ii.item.name
            if ii.quantity > 1:
                ii.quantity -= 1
                ii.save()
            else:
                ii.delete()
            return f"Sold {name} to {target_npc.name} for {price} credits. [Karma -5]"
        return f"{target_npc.name} doesn't want that."

    if not player.location.shop_name:
        return "No shop here to sell to."

    price = ii.item.price // 2
    player.money += price
    player.save()
    name = ii.item.name
    if ii.quantity > 1:
        ii.quantity -= 1
        ii.save()
    else:
        ii.delete()
    # Add sold item to shop inventory
    player.location.shop_inventory.add(ii.item)
    return f"Sold {name} for {price} credits."


def generate_random_weapon(zone):
    """Generate a procedurally spawned weapon with random stat bonuses/penalties."""
    # Weapon name components
    prefixes = ["Glitched", "Corrupted", "Enhanced", "Mutated", "Volatile", "Unstable",
                "Charged", "Infused", "Tainted", "Blessed", "Cursed", "Radiant", "Dark",
                "Quantum", "Neural", "Cyber", "Void", "Chaos", "Harmonic", "Resonant"]

    weapon_types = ["Blade", "Cutter", "Driver", "Piercer", "Crusher", "Striker", "Launcher",
                    "Emitter", "Projector", "Rifle", "Pistol", "Cannon", "Gauntlet", "Claw",
                    "Sword", "Axe", "Mace", "Spear", "Dagger", "Fist"]

    suffixes = ["of Pain", "of Speed", "of Power", "of Shadows", "of Light", "of Chaos",
                "of Order", "of the Grid", "of the Void", "of the Street", "of the Corp",
                "of the Net", "of the Wastes", "of the Neon", "of the Deep"]

    # Generate name with uniqueness guarantee
    max_attempts = 50
    for _ in range(max_attempts):
        if random.random() < 0.6:  # 60% chance for prefix
            name = f"{random.choice(prefixes)} {random.choice(weapon_types)}"
        else:
            name = random.choice(weapon_types)

        if random.random() < 0.4:  # 40% chance for suffix
            name += f" {random.choice(suffixes)}"

        # Check if this name already exists
        if not Item.objects.filter(name=name).exists():
            break
    else:
        # If we couldn't find a unique name, add a random number suffix
        name = f"{name} {random.randint(100, 999)}"

    # Random stats
    attack_bonus = random.randint(5, 25)
    speed_bonus = random.randint(-5, 10)

    # Random stat bonuses (1-3 stats affected)
    stat_bonuses = {}
    num_bonuses = random.randint(1, 3)
    available_stats = [
        'str_bonus', 'int_bonus', 'wil_bonus', 'agi_bonus', 'hea_bonus', 'cha_bonus'
    ]

    for _ in range(num_bonuses):
        stat = random.choice(available_stats)
        available_stats.remove(stat)
        # Can be positive or negative (sagging stats)
        bonus = random.randint(-5, 8)
        stat_bonuses[stat] = bonus

    # Determine rarity based on total power
    total_power = attack_bonus + sum(stat_bonuses.values())
    if total_power > 20:
        rarity = 'rare'
    elif total_power > 12:
        rarity = 'uncommon'
    else:
        rarity = 'common'

    # Price based on power
    price = max(50, total_power * 30)

    # Create description
    desc_parts = [f"A procedurally generated weapon from {zone}."]
    if attack_bonus > 15:
        desc_parts.append("It hums with dangerous energy.")
    elif attack_bonus > 10:
        desc_parts.append("It feels balanced and deadly.")
    else:
        desc_parts.append("It looks serviceable.")

    # Add stat description
    positive_bonuses = [
        k.replace('_bonus', '').upper() for k, v in stat_bonuses.items() if v > 0
    ]
    negative_bonuses = [
        k.replace('_bonus', '').upper() for k, v in stat_bonuses.items() if v < 0
    ]

    if positive_bonuses:
        desc_parts.append(f"Boosts: {', '.join(positive_bonuses)}.")
    if negative_bonuses:
        desc_parts.append(f"Sags: {', '.join(negative_bonuses)}.")

    description = " ".join(desc_parts)

    # Create the item
    item = Item.objects.create(
        name=name,
        description=description,
        item_type='weapon',
        attack_bonus=attack_bonus,
        speed_bonus=speed_bonus,
        rarity=rarity,
        price=price,
        subtype=random.choice(['one-handed', 'two-handed']),
        **stat_bonuses
    )

    return item


def check_procedural_weapon_spawns():
    """Check all zones and spawn new weapons if 30 minutes have passed since last spawn."""
    now = timezone.now()
    zones = [
        'slums', 'industrial', 'corporate', 'undergrid', 'neon', 'wastes', 'nexus', 'undercity'
    ]

    spawned_weapons = []

    for zone in zones:
        # Get the most recent spawn for this zone
        last_spawn = ProceduralWeaponSpawn.objects.filter(zone=zone).order_by('-spawned_at').first()

        # If no spawn exists, or last spawn was more than 30 minutes ago
        if not last_spawn or (now - last_spawn.spawned_at).total_seconds() >= 1800:
            # 30 minutes
            # Get a random room in this zone (not hub, not safe zone)
            zone_rooms = list(Room.objects.filter(zone=zone, safe_zone=False))

            if zone_rooms:
                spawn_room = random.choice(zone_rooms)

                # Generate a new weapon
                weapon = generate_random_weapon(zone)

                # Add it to the room
                spawn_room.items.add(weapon)

                # Record the spawn
                ProceduralWeaponSpawn.objects.create(
                    zone=zone,
                    room=spawn_room,
                    item=weapon
                )

                spawned_weapons.append({
                    'zone': zone,
                    'room': spawn_room.name,
                    'weapon': weapon.name
                })

    return spawned_weapons


def process_bot_ai(bot):
    """Process AI behavior for bot players. Called during polling or by process_bots command."""
    if not bot.is_bot or not bot.online:
        return ""
    
    # Process combat tick for bots in combat (auto-attack continues)
    if bot.last_combat_npc or bot.last_combat_player:
        process_combat_tick(bot)
        return ""
    
    # Skip if bot is resting (they're already "active")
    if bot.resting:
        return ""
    
    # Only act every 10-30 seconds (using persistent database field)
    now = timezone.now()
    if bot.last_bot_action:
        time_since_last = (now - bot.last_bot_action).total_seconds()
        if time_since_last < random.randint(10, 30):
            return ""
    
    # Update last action time
    bot.last_bot_action = now
    bot.save(update_fields=['last_bot_action'])
    
    # AI Decision Making
    room = bot.location
    
    # Check if bot should rest (low HP) - but NOT if in combat
    if bot.hp < bot.hp_max * 0.3 and not bot.last_combat_npc and not bot.last_combat_player:
        rest_command(bot)
        return ""  # Bot is now resting or already resting
    
    # Look for targets in current room
    npcs = NPC.objects.filter(location=room, hp__gt=0)
    players_here = Player.objects.filter(location=room, online=True).exclude(id=bot.id)
    
    # Find a target (only if not in safe zone)
    target_npc = None
    target_player = None
    
    if not room.safe_zone:
        # Attack evil/semi-evil players (any bot can attack players with bad karma)
        # This allows bots to "police" evil players regardless of the bot's own alignment
        if not target_npc and not target_player:
            for p in players_here:
                # Attack players who are evil (karma < -50) or semi-evil (karma < -20)
                if p.karma < -20 and abs(bot.lvl - p.lvl) <= 3:
                    target_player = p
                    break
        
        # Priority 3: Attack nearby NPCs (only aggressive NPCs, and level-appropriate)
        if not target_npc and not target_player:
            if npcs.exists():
                # Only attack NPCs within 5 levels of bot
                valid_npcs = [n for n in npcs if n.aggressive and abs(n.lvl - bot.lvl) <= 5]
                if valid_npcs:
                    target_npc = random.choice(valid_npcs)
    
    # Execute combat (without broadcasting to players - bots fight silently)
    if target_npc or target_player:
        target_name = target_npc.name if target_npc else target_player.user.username
        attack_target(bot, target_name, auto=True)
        return ""
    
    # Party behavior: invite players if social enough
    if bot.bot_social > 60 and not bot.parties.exists() and players_here.exists():
        for p in players_here:
            if abs(bot.lvl - p.lvl) <= 3 and not p.parties.exists():
                # Invite player to party
                invite_to_party(bot, p.user.username)
                break
    
    # Random chat/say to players in room
    if players_here.exists() and random.random() < 0.15:  # 15% chance to say something
        player = random.choice(list(players_here))
        
        # Evil bots talk crap, good bots are friendly
        if bot.karma < -30:
            taunts = [
                "You're gonna die in the gutter, choom.",
                "Pathetic. I'll scrap you for parts.",
                "Your blood will look good on my chrome.",
                "I've killed better players before breakfast.",
                "Run along, meat. This sector's mine.",
                "You smell like weakness.",
                "I'll turn your corpse into street art.",
                "Hope you got your affairs in order, fool.",
                "You're just another corpse waiting to happen.",
                "I'll gut you and sell your organs.",
                "Your screams will echo in the wastes.",
                "I've got a special place in my kill list for you."
            ]
            message = random.choice(taunts)
        else:
            greetings = [
                "Hey there, choom.",
                "Watch your back in this sector.",
                "Looking for a party?",
                "Stay frosty.",
                "The grid's been weird lately.",
                "Heard there's good loot in the wastes.",
                "Beware the corporate enforcers.",
                "Need a heal? I'm a Medie.",
                "Let's wreck some drones.",
                "Karma's a bitch, watch yours."
            ]
            message = random.choice(greetings)
        ChatMessage.objects.create(sender=bot, room=room, message=message)
    
    # Wander to adjacent room
    if room.exits and random.random() < 0.5:  # 50% chance to move
        direction = random.choice(list(room.exits.keys()))
        move_player(bot, direction)
    
    return ""


def get_poll_data(player):
    # Process auto-combat tick
    combat_msg = process_combat_tick(player)

    # Process resting HP regeneration
    rest_msg = process_resting(player)

    # Process bot AI for ALL online bots (not just bots in same room)
    bot_msg = ""
    all_bots = Player.objects.filter(is_bot=True, online=True)
    
    for bot in all_bots:
        bot_result = process_bot_ai(bot)
        if bot_result:
            bot_msg += bot_result

    # Check for procedural weapon spawns (once per poll cycle is fine, it's time-gated)
    if random.random() < 0.1:  # 10% chance each poll to check (roughly every 30 seconds)
        check_procedural_weapon_spawns()
        # Weapons spawn silently - no broadcast messages

    cutoff = timezone.now() - timezone.timedelta(seconds=30)
    # Poll world chat and local chat
    msgs = ChatMessage.objects.filter(
        Q(room=player.location) | Q(room=None),
        timestamp__gt=cutoff
    ).order_by('timestamp')
    chat = [{"player": m.sender.user.username, "message": m.message, "world": (m.room is None)}
            for m in msgs]
    npcs = list(NPC.objects.filter(location=player.location, hp__gt=0).values(
        'id', 'name', 'hp', 'hp_max', 'lvl', 'npc_type'))
    room_items = list(player.location.items.all().values('id', 'name')) if player.location else []
    players_here = list(Player.objects.filter(
        location=player.location, online=True
    ).exclude(id=player.id).values('id', 'user__username', 'lvl', 'game_class'))

    # PvP notification
    notification = player.notification
    if notification:
        player.notification = ''
        player.save(update_fields=['notification'])

    if combat_msg:
        notification = (notification + "\n" + combat_msg).strip()

    if rest_msg:
        notification = (notification + "\n" + rest_msg).strip()

    if bot_msg:
        notification = (notification + "\n" + bot_msg).strip()

    return {
        "chat": chat, "npcs": npcs, "items": room_items, "players": players_here,
        "status": get_status_str(player),
        "location": (player.location.name if player.location else "Unknown"),
        "notification": notification,
    }


# Party System Functions

def create_party(player, party_name=None):
    """Create a new party with the player as leader."""
    # Check if player is already in a party
    if player.parties.exists():
        return "You are already in a party. Leave it first to create a new one."

    # Create the party
    party = Party.objects.create(
        leader=player,
        name=party_name or f"{player.user.username}'s Party"
    )
    # Add leader as a member
    PartyMembership.objects.create(party=party, player=player, invited=False)

    return f"Party '{party.name}' created. You are the leader."


def invite_to_party(leader, target_name):
    """Invite another player to join the party."""
    # Check if leader is in a party
    if not leader.parties.exists():
        return "You are not in a party. Create one with PARTY CREATE first."

    party = Party.objects.get(id=leader.parties.first().id)

    # Check if leader is the party leader
    if party.leader != leader:
        return "Only the party leader can invite members."

    # Check if party is full
    if party.members.count() >= 3:
        return "Party is full (max 3 members). Cannot invite more."

    # Find target player
    target = Player.objects.filter(
        user__username__icontains=target_name,
        online=True
    ).first()

    if not target:
        return "Player not found or not online."

    # Check if target is in the same room
    if target.location != leader.location:
        return "Target must be in the same sector to invite."

    # Check if target is already in a party
    if target.parties.exists():
        return "That player is already in a party."

    # Check if target already has an invite
    if target.party_invite and target.party_invite == party:
        return "That player already has a pending invite from your party."

    # Send invite
    target.party_invite = party
    target.save(update_fields=['party_invite'])

    return f"Invited {target.user.username} to the party. They have 60 seconds to accept."


def accept_party_invite(player):
    """Accept a pending party invitation."""
    if not player.party_invite:
        return "No pending party invitation."

    party = Party.objects.get(id=player.party_invite.id)

    # Check if party is still valid and not full
    if not party.members.exists():
        player.party_invite = None
        player.save(update_fields=['party_invite'])
        return "Party no longer exists."

    if party.members.count() >= 3:
        player.party_invite = None
        player.save(update_fields=['party_invite'])
        return "Party is now full. Cannot join."

    # Add player to party
    PartyMembership.objects.create(party=party, player=player, invited=True)
    player.party_invite = None
    player.save(update_fields=['party_invite'])

    # Notify other party members
    for member in party.members.all():
        if member != player:
            member.notification = (
                f"\n[PARTY] {player.user.username} has joined the party."
            ).strip()
            member.save(update_fields=['notification'])

    return f"You have joined {party.name}."


def leave_party(player):
    """Leave the current party."""
    if not player.parties.exists():
        return "You are not in a party."

    party = player.parties.first()

    # If leader leaves, disband the party
    if party.leader == player:
        # Notify all members
        for member in party.members.all():
            if member != player:
                member.notification = (
                    f"\n[PARTY] {player.user.username} has disbanded the party. "
                    "You are no longer in a party."
                ).strip()
                member.party_invite = None
                member.save(update_fields=['notification', 'party_invite'])

        party.delete()
        return "You have disbanded the party."

    # Remove player from party
    PartyMembership.objects.filter(party=party, player=player).delete()

    # Notify other members
    for member in party.members.all():
        member.notification = (
            f"\n[PARTY] {player.user.username} has left the party."
        ).strip()
        member.save(update_fields=['notification'])

    return "You have left the party."


def get_party_status(player):
    """Get the current party status for a player."""
    if not player.parties.exists():
        return "You are not in a party."

    party = player.parties.first()
    members = list(party.members.all().values_list('user__username', flat=True))
    leader_name = party.leader.user.username

    sb = [f"\n=== Party: {party.name} ==="]
    sb.append(f"Leader: {leader_name}")
    sb.append("Members:")
    for m in members:
        if m == leader_name:
            sb.append(f"  - {m} (Leader)")
        else:
            sb.append(f"  - {m}")
    sb.append(f"Size: {len(members)}/3")

    return "\n".join(sb)


def move_party_leader(player, direction):
    """Move the party leader and all party members together."""
    # Check if player is in a party and is the leader
    if not player.parties.exists():
        return "You are not in a party. Create one with PARTY CREATE first."

    party = player.parties.first()
    if party.leader != player:
        return "Only the party leader can move the party."

    # Store the party id to use after move
    party_id = party.id

    # Move the leader
    result = move_player(player, direction)

    # Refresh party to get updated members
    party = Party.objects.get(id=party_id)

    # Move all party members
    for member in party.members.all():
        if member != player and member.online:
            # Store their old room for broadcast
            old_room = member.location
            # Move them to the same room as the leader
            member.location = player.location
            member.save(update_fields=['location'])

            # Broadcast exit/enter for party members
            if old_room and old_room != member.location:
                broadcast_room_event(member, old_room, None, 'exit')
                broadcast_room_event(member, None, member.location, 'enter')

    return result