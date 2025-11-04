"""
chuk-mcp-remotion - AI-powered video generation with Remotion

A design-system-first approach to creating professional YouTube videos.
"""

__version__ = "0.1.0"

# Export main server
# Export registries and themes
from .registry.components import COMPONENT_REGISTRY
from .server import main, mcp
from .themes.youtube_themes import YOUTUBE_THEMES

# Export design tokens
from .tokens.colors import COLOR_TOKENS
from .tokens.motion import MOTION_TOKENS
from .tokens.spacing import SPACING_TOKENS
from .tokens.typography import TYPOGRAPHY_TOKENS

__all__ = [
    "mcp",
    "main",
    "COLOR_TOKENS",
    "TYPOGRAPHY_TOKENS",
    "MOTION_TOKENS",
    "SPACING_TOKENS",
    "COMPONENT_REGISTRY",
    "YOUTUBE_THEMES",
]
