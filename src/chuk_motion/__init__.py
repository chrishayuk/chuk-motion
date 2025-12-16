"""
chuk-motion - AI-powered video generation with Remotion

A design-system-first approach to creating professional YouTube videos.
"""

__version__ = "0.1.0"

# Export registries and themes
from .registry.components import COMPONENT_REGISTRY
from .themes.youtube_themes import YOUTUBE_THEMES

# Export design tokens
from .tokens.colors import COLOR_TOKENS
from .tokens.motion import MOTION_TOKENS
from .tokens.spacing import SPACING_TOKENS
from .tokens.typography import TYPOGRAPHY_TOKENS

__all__ = [
    "COLOR_TOKENS",
    "TYPOGRAPHY_TOKENS",
    "MOTION_TOKENS",
    "SPACING_TOKENS",
    "COMPONENT_REGISTRY",
    "YOUTUBE_THEMES",
]


def get_mcp():
    """Get the MCP server instance (lazy import to avoid double registration)."""
    from .async_server import mcp

    return mcp


def main():
    """Main entry point for the MCP server."""
    from .server import main as server_main

    return server_main()
