import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import OperationalError
from .models import Player, Room
from . import services


def index(request):
    try:
        return render(request, 'game/game.html')
    except OperationalError:
        return JsonResponse({'error': 'Database is being initialized. Please refresh in a moment.'}, status=503)


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        race = request.POST.get('race', 'Human')
        game_class = request.POST.get('gameClass', 'Street Samurai')
        
        # User customized stats
        custom_stats_json = request.POST.get('stats')
        custom_stats = {}
        if custom_stats_json:
            try:
                custom_stats = json.loads(custom_stats_json)
            except json.JSONDecodeError:
                pass

        if not name or not password:
            return JsonResponse({'message': 'Name and password required.'}, status=400)
        
        try:
            if User.objects.filter(username=name).exists():
                return JsonResponse({'message': 'Handle already in use.'}, status=400)

            user = User.objects.create_user(username=name, password=password)
            start_room = Room.objects.get_or_create(
                id=1,
                defaults={
                    'name': 'The Neon Hub',
                    'description': 'A bustling intersection of neon lights and rainy streets. The center of the grid.',
                    'zone': 'hub',
                    'theme': 'urban',
                    'safe_zone': True
                }
            )[0]
            
            # Starting Stats based on Race
            stats = {
                'str_stat': 10, 'int_stat': 10, 'wil_stat': 10,
                'agi_stat': 10, 'hea_stat': 10, 'cha_stat': 10,
            }

            race_base_stats = {
                'Cyborg': {'str_stat': 15, 'hea_stat': 12, 'agi_stat': 8, 'int_stat': 12, 'cha_stat': 5, 'wil_stat': 8},
                'Bio-hacked': {'hea_stat': 15, 'str_stat': 12, 'cha_stat': 8, 'agi_stat': 12, 'int_stat': 8, 'wil_stat': 5},
                'Android': {'int_stat': 17, 'wil_stat': 12, 'cha_stat': 5, 'hea_stat': 8, 'str_stat': 10, 'agi_stat': 8},
                'Mutant': {'str_stat': 13, 'hea_stat': 18, 'wil_stat': 7, 'cha_stat': 6, 'agi_stat': 11, 'int_stat': 5},
                'Human': {'cha_stat': 15, 'wil_stat': 13, 'str_stat': 7, 'hea_stat': 7, 'agi_stat': 10, 'int_stat': 8},
                'Void-Walker': {'wil_stat': 20, 'agi_stat': 12, 'str_stat': 5, 'hea_stat': 8, 'int_stat': 10, 'cha_stat': 5},
                'Synth-Soul': {'int_stat': 22, 'cha_stat': 5, 'wil_stat': 15, 'str_stat': 5, 'hea_stat': 5, 'agi_stat': 8},
                'Chrome-Crawler': {'str_stat': 18, 'agi_stat': 18, 'int_stat': 5, 'cha_stat': 5, 'hea_stat': 10, 'wil_stat': 4},
                'Elf': {'agi_stat': 14, 'wil_stat': 10, 'hea_stat': 7, 'cha_stat': 12, 'str_stat': 8, 'int_stat': 9},
                'Goblin': {'cha_stat': 15, 'agi_stat': 13, 'str_stat': 5, 'int_stat': 12, 'hea_stat': 8, 'wil_stat': 7},
            }
            
            if race in race_base_stats:
                stats.update(race_base_stats[race])
            
            # Apply user customized distribution (bonus points added to racial base)
            # The frontend starts with 60 base points (10 per stat) and 20 bonus pool (Total 80).
            if custom_stats:
                total_sum = 0
                for s_key in ['str', 'int', 'wil', 'agi', 'hea', 'cha']:
                    val = int(custom_stats.get(s_key, 10))
                    total_sum += val
                    # Apply the user's deviation from the standard base (10) to the racial base
                    delta = val - 10
                    stats[f'{s_key}_stat'] += delta
                
                if total_sum > 80:
                    return JsonResponse({'message': f'Stat point allocation error. Max total points is 80 (You assigned {total_sum}).'}, status=400)
            
            # Class Modifiers
            class_mods = {
                'Street Samurai': {'attack': 5, 'str_stat': 3, 'agi_stat': 2},
                'Netrunner': {'int_stat': 5, 'mana_max': 20},
                'Techie': {'int_stat': 3, 'wil_stat': 2, 'defense': 3},
                'Medie': {'hea_stat': 3, 'hp_max': 20},
                'Fixer': {'cha_stat': 5, 'money': 50},
                'Thief': {'agi_stat': 6, 'attack': 2},
                'Heavy': {'str_stat': 5, 'hea_stat': 5, 'defense': 5, 'hp_max': 30},
                'Psycher': {'wil_stat': 8, 'mana_max': 40},
                'Warlock': {'int_stat': 5, 'wil_stat': 5, 'mana_max': 30},
                'Priest': {'wil_stat': 6, 'hea_stat': 4, 'hp_max': 25},
                'Trickster': {'cha_stat': 15, 'agi_stat': 5},
            }
            
            c_mods = class_mods.get(game_class, {})
            for k, v in c_mods.items():
                if k in stats: stats[k] += v
                
            # Initialize derived stats
            stats['attack'] = 10 + (stats['str_stat'] // 2) + c_mods.get('attack', 0)
            stats['defense'] = 5 + (stats['agi_stat'] // 2) + c_mods.get('defense', 0)
            stats['hp_max'] = 100 + (stats['hea_stat'] * 2) + c_mods.get('hp_max', 0)
            stats['hp'] = stats['hp_max']
            stats['mana_max'] = 20 + (stats['wil_stat'] * 2) + c_mods.get('mana_max', 0)
            stats['mana'] = stats['mana_max']
            
            initial_money = 25 + c_mods.get('money', 0)

            Player.objects.create(
                user=user, race=race, game_class=game_class,
                location=start_room, money=initial_money, **stats
            )
            return JsonResponse({
                'message': f'Character initialized! Welcome to the grid, {name}.'
            })
        except OperationalError:
            return JsonResponse({'message': 'System initializing. Try again in 10 seconds.'}, status=503)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        try:
            user = authenticate(username=name, password=password)
            if user:
                login(request, user)
                player = user.player
                player.online = True
                player.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        except OperationalError:
            return JsonResponse({'success': False, 'message': 'Database not ready.'})


@csrf_exempt
def command_view(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'Not authenticated'}, status=401)

        player = request.user.player
        try:
            cmd_data = json.loads(request.body)
            full_cmd = cmd_data.get('command', '').strip()
        except (json.JSONDecodeError, AttributeError):
            full_cmd = ""

        if not full_cmd:
            return JsonResponse({
                'output': '',
                'status': services.get_status_str(player)
            })

        parts = full_cmd.split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        output = ""
        # Handle EXIT command
        if command == 'exit':
            player.online = False
            player.save()
            logout(request)
            return JsonResponse({
                'output': 'LOGGING OUT...',
                'status': 'OFFLINE',
                'action': 'exit'
            })

        if command in ['look', 'l']:
            output = services.get_look(player, args)
        elif command in ['n', 'north', 's', 'south', 'e', 'east', 'w', 'west']:
            output = services.move_player(player, command)
        elif command == 'who':
            online_players = Player.objects.filter(online=True)
            lines = ["\n=== Nodes Currently Linked ==="]
            for p in online_players:
                lines.append(f"  {p.user.username} (Lvl {p.lvl}) - {p.game_class}")
            output = "\n".join(lines)
        elif command == 'top':
            output = services.get_top_ten()
        elif command in ['attack', 'a', 'kill', 'k']:
            output = services.attack_target(player, args)
        elif command in ['inventory', 'i']:
            output = services.get_inventory(player)
        elif command in ['status', 'st']:
            output = services.get_status_detailed(player)
        elif command in ['get', 'g']:
            output = services.get_item(player, args)
        elif command == 'drop':
            output = services.drop_item(player, args)
        elif command == 'equip':
            output = services.equip_item(player, args)
        elif command in ['list', 'li']:
            output = services.list_shop(player)
        elif command == 'buy':
            output = services.buy_item(player, args)
        elif command == 'sell':
            output = services.sell_item(player, args)
        elif command in ['say', "'"]:
            output = services.handle_say(player, args)
        elif command in ['broadcast', 'bcast']:
            output = services.handle_broadcast(player, args)
        elif command in ['help', '?']:
            output = services.get_help(player)
        elif command == 'use':
            output = services.use_item(player, args)
        elif command == 'train':
            output = services.train_stat(player, args)
        elif command in ['blade', 'oni_strike', 'hack', 'overload', 'patch', 'detox', 'scheme', 'calibrate', 'turret', 'call_in', 
                        'stealth', 'backstab', 'sneak', 'smash', 'taunt', 'mind_bolt', 'soul_drain', 'curse', 'chaos_bolt', 'heal', 'bless', 'bamboozle', 'jackpot']:
            output = services.use_ability(player, command, args)
        else:
            output = "COMMAND ERROR: UNKNOWN INSTRUCTION."

        chat_output = services.get_recent_chat(player)
        if chat_output:
            output = chat_output + "\n" + output

        return JsonResponse({
            'output': output,
            'status': services.get_status_str(player)
        })
    except OperationalError:
        return JsonResponse({'output': 'Database error. Reconnecting...', 'status': 'OFFLINE'})


@csrf_exempt
def poll_view(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'idle', 'authenticated': False})
        player = request.user.player
        return JsonResponse(services.get_poll_data(player))
    except (OperationalError, Exception):
        return JsonResponse({'status': 'db_not_ready', 'authenticated': False})


@csrf_exempt
def map_api_view(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'rooms': [], 'authenticated': False})
        player = request.user.player
        map_json = services.get_map_data(player)
        return JsonResponse({'rooms': json.loads(map_json)})
    except (OperationalError, Exception):
        return JsonResponse({'rooms': [], 'authenticated': False})


@csrf_exempt
def player_info_view(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'player_name': 'Unknown', 'authenticated': False})

        player = request.user.player
        return JsonResponse({
            'player_name': request.user.username,
            'level': player.lvl,
            'hp': player.hp,
            'hp_max': player.hp_max,
        })
    except (OperationalError, Exception):
        return JsonResponse({'player_name': 'Unknown', 'authenticated': False})
