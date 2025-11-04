"""PieChart component."""

from .builder import add_to_composition
from .schema import MCP_SCHEMA, METADATA, PieChartProps, PieDataPoint
from .tool import register_tool

__all__ = [
    "METADATA",
    "MCP_SCHEMA",
    "PieChartProps",
    "PieDataPoint",
    "register_tool",
    "add_to_composition",
]
