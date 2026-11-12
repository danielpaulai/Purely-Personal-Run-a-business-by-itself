"""Vercel entrypoint: exposes the ASGI app. All routes are rewritten here (see vercel.json)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pp_mcp.server import app  # noqa: E402,F401
