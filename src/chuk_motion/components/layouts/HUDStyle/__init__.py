"""HUDStyle component."""

from .builder import add_to_composition
from .schema import MCP_SCHEMA, METADATA, HUDStyleProps
from .tool import register_tool

__all__ = [
    "METADATA",
    "MCP_SCHEMA",
    "HUDStyleProps",
    "register_tool",
    "add_to_composition",
]
