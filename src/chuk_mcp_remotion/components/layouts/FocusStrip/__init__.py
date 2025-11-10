"""FocusStrip component."""

from .builder import add_to_composition
from .schema import MCP_SCHEMA, METADATA, FocusStripProps
from .tool import register_tool

__all__ = [
    "METADATA",
    "MCP_SCHEMA",
    "FocusStripProps",
    "register_tool",
    "add_to_composition",
]
