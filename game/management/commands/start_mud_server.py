"""
Django management command to start the MUD Telnet server.
"""
import os
import sys
import django
import asyncio
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start the MUD Telnet server for MUD client connections'

    def add_arguments(self, parser):
        parser.add_argument(
            '--host',
            default='0.0.0.0',
            help='Host to bind the server to (default: 0.0.0.0)'
        )
        parser.add_argument(
            '--port',
            type=int,
            default=4000,
            help='Port to listen on (default: 4000)'
        )

    def handle(self, *args, **options):
        host = options['host']
        port = options['port']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting MUD server on {host}:{port}...')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Connect using: telnet {host} {port}')
        )
        self.stdout.write(
            self.style.WARNING('Press Ctrl+C to stop the server.\n')
        )
        
        # Import and run the MUD server
        from game.mud_server import run_mud_server
        
        try:
            asyncio.run(run_mud_server(host, port))
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.SUCCESS('\nMUD server stopped.')
            )