"""Vertical component."""

from .builder import add_to_composition
from .schema import MCP_SCHEMA, METADATA, VerticalProps
from .tool import register_tool

__all__ = [
    "METADATA",
    "MCP_SCHEMA",
    "VerticalProps",
    "register_tool",
    "add_to_composition",
]
