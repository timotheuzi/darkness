"""
MUD Telnet Server for Darkness BBS
Provides Telnet connectivity for MUD clients like Mudlet, MUSHclient, etc.
"""
import asyncio
import telnetlib3
import os
import sys
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'darkness_django.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
django.setup()

from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db import OperationalError


class MudClient:
    """Represents a connected MUD client session."""
    
    def __init__(self, reader, writer, ip_address):
        self.reader = reader
        self.writer = writer
        self.ip_address = ip_address
        self.player = None
        self.user = None
        self.authenticated = False
        self.login_stage = 'username'  # username, password, playing
        self.username_input = ""
        self.buffer = ""
        
    async def send(self, data):
        """Send data to the client."""
        try:
            self.writer.write(data)
            await self.writer.drain()
        except Exception as e:
            print(f"Error sending to client: {e}")
    
    async def send_line(self, line=""):
        """Send a line with proper line ending."""
        await self.send(f"{line}\r\n")
    
    async def send_ansi(self, text):
        """Send text with ANSI color codes."""
        # Basic ANSI color support
        # MUD clients typically support ANSI, but we'll keep it simple
        await self.send(text)
    
    def get_status_line(self):
        """Get the status line for the player."""
        if not self.player:
            return ""
        try:
            from game import services
            return services.get_status_str(self.player)
        except:
            return ""
    
    async def display_room(self):
        """Display the current room to the player."""
        if not self.player:
            return
        
        try:
            from game import services
            # Clear screen
            await self.send("\033[2J\033[H")
            
            # Get room description
            look_output = services.get_look(self.player)
            
            # Format and send
            await self.send_ansi(look_output)
            await self.send("\r\n")
            
            # Send status line
            status = self.get_status_line()
            if status:
                await self.send_line(f"\033[1;37m{status}\033[0m")
        except OperationalError:
            await self.send_line("Database error. Please wait...")
        except Exception as e:
            print(f"Error displaying room: {e}")
            await self.send_line("Error displaying room.")
    
    async def process_command(self, command):
        """Process a game command and return output."""
        if not self.player or not self.authenticated:
            return "Not authenticated."
        
        try:
            from game import services
            from game.models import Player

            # Inactivity kick (1 hour of doing NOTHING). Kicked players lose
            # nothing and are returned to the login prompt.
            now = timezone.now()
            last_active = self.player.last_activity or self.player.last_seen
            if last_active and (now - last_active).total_seconds() >= services.AFK_KICK_SECONDS:
                await self.logout()
                return (
                    "\n[SYSTEM] Disconnected: 1 hour of inactivity.\n"
                    "You lost nothing. Please log back in.\n\nHandle: "
                )

            # Update last_seen and record real activity
            self.player.last_seen = now
            self.player.save(update_fields=["last_seen"])
            services.touch_player_activity(self.player)

            parts = command.strip().split(" ", 1)
            cmd = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            output = ""
            
            # Handle EXIT command
            if cmd == "exit":
                await self.logout()
                return "LOGGING OUT..."
            
            # Route commands to services
            if cmd in ["look", "l"]:
                output = services.get_look(self.player, args)
            elif cmd in ["n", "north", "s", "south", "e", "east", "w", "west"]:
                output = services.move_player(self.player, cmd)
            elif cmd == "who":
                from game.models import Player
                online_players = Player.objects.filter(online=True)
                lines = ["\n=== Nodes Currently Linked ==="]
                for p in online_players:
                    bot_marker = " (bot)" if p.is_bot else ""
                    lines.append(f"  {p.user.username}{bot_marker} (Lvl {p.lvl}) - {p.game_class}")
                output = "\n".join(lines)
            elif cmd == "top":
                output = services.get_top_ten()
            elif cmd == "wall":
                output = services.get_wall_of_death()
            elif cmd in ["attack", "a", "kill", "k"]:
                output = services.attack_target(self.player, args, auto=False)
            elif cmd in ["autoattack", "aa"]:
                output = services.attack_target(self.player, args, auto=True)
            elif cmd in ["inventory", "i"]:
                output = services.get_inventory(self.player)
            elif cmd in ["status", "st", "stats"]:
                output = services.get_status_detailed(self.player)
            elif cmd in ["get", "g"]:
                output = services.get_item(self.player, args)
            elif cmd == "drop":
                output = services.drop_item(self.player, args)
            elif cmd == "equip":
                output = services.equip_item(self.player, args)
            elif cmd in ["list", "li"]:
                output = services.list_shop(self.player)
            elif cmd == "buy":
                output = services.buy_item(self.player, args)
            elif cmd == "sell":
                output = services.sell_item(self.player, args)
            elif cmd == "sellall":
                output = services.sell_all_items(self.player)
            elif cmd in ["say", "'"]:
                output = services.handle_say(self.player, args)
            elif cmd in ["broadcast", "bcast"]:
                output = services.handle_broadcast(self.player, args)
            elif cmd in ["help", "?"]:
                output = services.get_help(self.player)
            elif cmd == "guide":
                output = "Opening user guide in browser... (web interface only)"
            elif cmd == "use":
                output = services.use_item(self.player, args)
            elif cmd == "train":
                output = services.train_stat(self.player, args)
            elif cmd == "rest":
                output = services.rest_command(self.player)
            elif cmd == "disengage":
                output = services.disengage_combat(self.player)
            elif cmd == "steal":
                output = services.steal_from_target(self.player, args)
            elif cmd == "party":
                if not args:
                    output = "Party commands: CREATE, INVITE <player>, ACCEPT, LEAVE, STATUS"
                else:
                    parts = args.split(" ", 1)
                    subcmd = parts[0].lower()
                    subargs = parts[1] if len(parts) > 1 else ""
                    if subcmd == "create":
                        output = services.create_party(self.player, subargs)
                    elif subcmd == "invite":
                        output = services.invite_to_party(self.player, subargs)
                    elif subcmd == "accept":
                        output = services.accept_party_invite(self.player)
                    elif subcmd == "leave":
                        output = services.leave_party(self.player)
                    elif subcmd == "status":
                        output = services.get_party_status(self.player)
                    else:
                        output = "Party commands: CREATE, INVITE <player>, ACCEPT, LEAVE, STATUS"
            else:
                # Check for special moves dynamically
                move_output = services.use_ability(self.player, cmd, args)
                if move_output is not None:
                    output = move_output
                else:
                    output = "COMMAND ERROR: UNKNOWN INSTRUCTION."
            
            # Add chat output if any
            chat_output = services.get_recent_chat(self.player)
            if chat_output:
                output = chat_output + "\n" + output
            
            return output
        except OperationalError:
            return "Database error. Reconnecting..."
        except Exception as e:
            print(f"Error processing command: {e}")
            return "Error processing command."
    
    async def logout(self):
        """Log out the player."""
        if self.player:
            self.player.online = False
            self.player.save(update_fields=["online"])
        if self.user:
            logout(None)  # Django logout (no request in Telnet)
        self.authenticated = False
        self.player = None
        self.user = None
        self.login_stage = 'username'
    
    async def handle_login(self, line):
        """Handle login process."""
        if self.login_stage == 'username':
            self.username_input = line.strip()
            await self.send_line("Password: ")
            self.login_stage = 'password'
            
        elif self.login_stage == 'password':
            password = line.strip()
            
            # Authenticate
            user = authenticate(username=self.username_input, password=password)
            if user:
                self.user = user
                self.player = user.player
                self.player.online = True
                now = timezone.now()
                self.player.last_seen = now
                self.player.last_activity = now
                if not self.player.last_move_time:
                    self.player.last_move_time = now
                self.player.save(
                    update_fields=["online", "last_seen", "last_activity", "last_move_time"]
                )
                self.authenticated = True
                self.login_stage = 'playing'
                
                await self.send_line(f"\nWelcome to the grid, {user.username}.")
                await self.display_room()
            else:
                await self.send_line("Invalid credentials.")
                await self.send_line("Handle: ")
                self.login_stage = 'username'
    
    async def handle_register(self, line):
        """Handle registration (simplified for Telnet)."""
        # For Telnet, we'll use a simplified registration
        # In production, you might want to use a web interface for character creation
        await self.send_line("Character creation is done via the web interface.")
        await self.send_line("Please visit the web portal to create your character.")
        await self.send_line("Then return here to log in.")
        await self.send_line("\nHandle: ")
        self.login_stage = 'username'


async def handle_client(reader, writer):
    """Handle a new Telnet client connection."""
    client_ip = writer.get_extra_info('peername')[0]
    client = MudClient(reader, writer, client_ip)
    
    print(f"New connection from {client_ip}")
    
    try:
        # Send welcome banner
        await client.send_line("╔══════════════════════════════════════════════════════════════╗")
        await client.send_line("║                    DARKNESS BBS - MUD PORT                   ║")
        await client.send_line("║              A Cyberpunk Terminal RPG Experience             ║")
        await client.send_line("╚══════════════════════════════════════════════════════════════╝")
        await client.send_line("")
        await client.send_line("Type 'new' to create a new character (web required)")
        await client.send_line("Type your handle to log in")
        await client.send_line("")
        await client.send_line("Handle: ")
        
        # Main loop
        while True:
            try:
                line = await reader.readline()
                if not line:
                    break
                
                # Remove telnet control sequences (basic handling)
                line = line.strip()
                if not line:
                    continue
                
                # Handle registration
                if line.lower() == 'new' and not client.authenticated:
                    await client.handle_register(line)
                    continue
                
                # Handle login
                if not client.authenticated:
                    await client.handle_login(line)
                    continue
                
                # Process game command
                if client.authenticated and line:
                    output = await client.process_command(line)
                    
                    # Display output
                    if output:
                        await client.send_line("")
                        await client.send_ansi(output)
                        await client.send_line("")
                        
                        # Show status line
                        status = client.get_status_line()
                        if status:
                            await client.send_line(f"\033[1;37m{status}\033[0m")
                        
                        # Show prompt (Mudlet-compatible format)
                        await client.send(f"\r\n\033[1;32m>\033[0m ")
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in client loop: {e}")
                break
    
    finally:
        # Cleanup
        await client.logout()
        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass
        print(f"Connection closed: {client_ip}")


async def afk_watchdog():
    """Background task: periodically sweeps idle connections. Handles the
    random 2-minute Hub AFK teleports, stuck-bot rescues, and marks players
    who have been idle 1+ hour as offline so they must log back in."""
    from game import services

    while True:
        await asyncio.sleep(15)
        try:
            services.process_afk_players(force=True)
        except Exception as e:
            print(f"AFK watchdog error: {e}")


async def run_mud_server(host='0.0.0.0', port=4000):
    """Run the MUD Telnet server."""
    print(f"Starting MUD server on {host}:{port}...")
    print(f"Connect using: telnet {host} {port}")
    print("Or configure your MUD client to connect to this address.")
    print("Press Ctrl+C to stop the server.\n")
    
    server = await telnetlib3.create_server(host=host, port=port, client_connected_cb=handle_client)
    watchdog = asyncio.ensure_future(afk_watchdog())
    
    try:
        await server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down MUD server...")
        watchdog.cancel()
        server.close()
        await server.wait_closed()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Darkness BBS MUD Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=4000, help='Port to listen on')
    args = parser.parse_args()
    
    try:
        asyncio.run(run_mud_server(args.host, args.port))
    except KeyboardInterrupt:
        print("\nServer stopped.")