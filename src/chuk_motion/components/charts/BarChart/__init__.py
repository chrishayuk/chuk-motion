"""BarChart component."""

from .builder import add_to_composition
from .schema import MCP_SCHEMA, METADATA, BarChartProps, BarDataPoint
from .tool import register_tool

__all__ = [
    "METADATA",
    "MCP_SCHEMA",
    "BarChartProps",
    "BarDataPoint",
    "register_tool",
    "add_to_composition",
]
