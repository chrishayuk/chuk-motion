"""PanelCascade - Staggered panel entrance animations for multi-panel layouts."""

from .builder import add_to_composition
from .schema import MCP_SCHEMA, METADATA, PanelCascadeProps
from .tool import register_tool

__all__ = ["METADATA", "MCP_SCHEMA", "PanelCascadeProps", "register_tool", "add_to_composition"]
