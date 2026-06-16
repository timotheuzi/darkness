import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Player, Room
from . import services


def index(request):
    return render(request, 'game/game.html')


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        race = request.POST.get('race')
        game_class = request.POST.get('gameClass')

        if not name or not password:
            return JsonResponse({'message': 'Name and password required.'}, status=400)
        if User.objects.filter(username=name).exists():
            return JsonResponse({'message': 'Handle already in use.'}, status=400)

        user = User.objects.create_user(username=name, password=password)
        start_room = Room.objects.get_or_create(
            id=1,
            defaults={
                'name': 'The Neon Hub',
                'description': 'Central Hub.',
                'zone': 'hub',
                'theme': 'urban',
            }
        )[0]
        Player.objects.create(
            user=user, race=race, game_class=game_class,
            location=start_room, hp=100, hp_max=100,
            attack=10, defense=5
        )
        return JsonResponse({
            'message': f'Character initialized! Welcome to the grid, {name}.'
        })


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(username=name, password=password)
        if user:
            login(request, user)
            player = user.player
            player.online = True
            player.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'Invalid credentials'})


@csrf_exempt
def command_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Not authenticated'}, status=401)

    player = request.user.player
    cmd_data = json.loads(request.body)
    full_cmd = cmd_data.get('command', '').strip()
    if not full_cmd:
        return JsonResponse({
            'output': '',
            'status': services.get_status_str(player)
        })

    if full_cmd.startswith("'"):
        command = "'"
        args = full_cmd[1:]
    else:
        parts = full_cmd.split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

    output = ""
    if command in ['look', 'l']:
        output = services.get_look(player)
    elif command in ['n', 'north', 's', 'south', 'e', 'east', 'w', 'west']:
        output = services.move_player(player, command)
    elif command == 'who':
        online_players = Player.objects.filter(online=True)
        lines = ["\n=== Nodes Currently Linked ==="]
        for p in online_players:
            lines.append(f"  {p.user.username} (Lvl {p.lvl}) - {p.game_class}")
        output = "\n".join(lines)
    elif command in ['attack', 'a', 'kill', 'k']:
        output = services.attack_npc(player, args)
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
    elif command in ['help', '?']:
        output = services.get_help(player)
    elif command == 'map':
        map_data = services.get_map_data(player)
        output = map_data  # Return JSON for client-side rendering
    elif command == 'use':
        output = services.use_item(player, args)
    else:
        output = "COMMAND ERROR: UNKNOWN INSTRUCTION."

    # Include recent chat messages in every output if any
    chat_output = services.get_recent_chat(player)
    if chat_output:
        output = chat_output + "\n" + output

    return JsonResponse({
        'output': output,
        'status': services.get_status_str(player)
    })


@csrf_exempt
def poll_view(request):
    """Polling endpoint for real-time updates (like chat.js pattern)."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    player = request.user.player
    data = services.get_poll_data(player)
    return JsonResponse(data)


@csrf_exempt
def map_api_view(request):
    """API endpoint for map data."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    player = request.user.player
    map_json = services.get_map_data(player)
    try:
        map_data = json.loads(map_json)
    except (json.JSONDecodeError, TypeError):
        map_data = []
    return JsonResponse({'rooms': map_data})


@csrf_exempt
def player_info_view(request):
    """API endpoint for player info (used by chat.js-style polling)."""
    if not request.user.is_authenticated:
        return JsonResponse({'player_name': 'Unknown'})

    return JsonResponse({
        'player_name': request.user.username,
        'level': request.user.player.lvl,
        'hp': request.user.player.hp,
        'hp_max': request.user.player.hp_max,
    })