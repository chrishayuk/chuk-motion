"""DonutChart component."""

from .builder import add_to_composition
from .schema import MCP_SCHEMA, METADATA, DonutChartProps, DonutDataPoint
from .tool import register_tool

__all__ = [
    "METADATA",
    "MCP_SCHEMA",
    "DonutChartProps",
    "DonutDataPoint",
    "register_tool",
    "add_to_composition",
]
