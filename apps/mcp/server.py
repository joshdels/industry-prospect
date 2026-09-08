import os
import django

from mcp.server.fastmcp import FastMCP

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

django.setup()

mcp = FastMCP("Prospect Inspector")


# services from tje inspector, i add ni later josh
@mcp.tool()
def create_prospect(content: str) -> dict:
    """Create a new prospect input"""

    return


if __name__ == "__main__":
    mcp.run()
