import os
import sys

from pathlib import Path

import django

# ============================================================
# DJANGO SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

django.setup()



from mcp.server import MCPServer

from apps.mcp.tools import (
    register_prospect_tools,
)

mcp = MCPServer("Prospect Assistant")

register_prospect_tools(mcp)
