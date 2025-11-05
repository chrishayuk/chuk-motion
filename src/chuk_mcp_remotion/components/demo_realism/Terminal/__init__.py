"""Terminal component - Realistic terminal with typing animation and command output."""

from .schema import METADATA, TerminalProps
from .tool import register_tool
from .builder import add_to_composition

__all__ = ["METADATA", "TerminalProps", "register_tool", "add_to_composition"]
