"""BrowserFrame component - Realistic browser window with swappable themes."""

from .schema import METADATA, BrowserFrameProps
from .tool import register_tool
from .builder import add_to_composition

__all__ = ["METADATA", "BrowserFrameProps", "register_tool", "add_to_composition"]
