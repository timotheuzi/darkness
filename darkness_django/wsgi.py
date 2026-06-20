"""WSGI entry point for PythonAnywhere deployment."""

import sys
import os

# Try multiple possible project locations
possible_paths = [
    '/home/darknesses/darknesses/',
]

for path in possible_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)
        break

# Also try to find the src directory relative to the WSGI file
wsgi_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(wsgi_dir), 'src')
if os.path.exists(src_dir) and src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from app import app as application