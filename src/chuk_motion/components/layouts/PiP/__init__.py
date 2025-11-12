"""PiP component."""

from .builder import add_to_composition
from .schema import MCP_SCHEMA, METADATA, PiPProps
from .tool import register_tool

__all__ = [
    "METADATA",
    "MCP_SCHEMA",
    "PiPProps",
    "register_tool",
    "add_to_composition",
]
