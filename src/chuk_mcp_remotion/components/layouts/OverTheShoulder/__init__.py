"""OverTheShoulder component."""

from .builder import add_to_composition
from .schema import MCP_SCHEMA, METADATA, OverTheShoulderProps
from .tool import register_tool

__all__ = [
    "METADATA",
    "MCP_SCHEMA",
    "OverTheShoulderProps",
    "register_tool",
    "add_to_composition",
]
