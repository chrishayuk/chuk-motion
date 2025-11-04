"""LineChart component."""

from .builder import add_to_composition
from .schema import MCP_SCHEMA, METADATA, DataPoint, LineChartProps
from .tool import register_tool

__all__ = [
    "METADATA",
    "MCP_SCHEMA",
    "LineChartProps",
    "DataPoint",
    "register_tool",
    "add_to_composition",
]
