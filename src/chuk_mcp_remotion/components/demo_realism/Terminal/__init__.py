"""Terminal component - Realistic terminal with typing animation and command output."""

from .builder import add_to_composition
from .schema import METADATA, TerminalProps
from .tool import register_tool

__all__ = ["METADATA", "TerminalProps", "register_tool", "add_to_composition"]
