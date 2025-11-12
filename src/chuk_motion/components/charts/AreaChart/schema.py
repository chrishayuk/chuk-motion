# chuk-motion/src/chuk_motion/components/charts/AreaChart/schema.py
"""AreaChart component schema and Pydantic models."""

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class DataPoint(BaseModel):
    """A single data point with x, y coordinates and optional label."""

    x: float
    y: float
    label: str | None = None


class AreaChartProps(BaseModel):
    """Properties for AreaChart component."""

    data: list[list[float] | DataPoint] = Field(
        description="Array of data points as [x, y] or {x, y, label}"
    )
    title: str | None = Field(None, description="Optional chart title")
    xlabel: str | None = Field(None, description="Optional x-axis label")
    ylabel: str | None = Field(None, description="Optional y-axis label")
    start_time: float = Field(0.0, description="When to show (seconds)")
    duration: float = Field(4.0, description="How long to animate (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="AreaChart",
    description="Animated area chart showing trends with filled gradient",
    category="chart",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": METADATA.description,
    "category": METADATA.category,
    "animations": {
        "draw": "Chart draws with animation",
        "fade_in": "Chart fades in",
        "scale_in": "Chart scales from center",
    },
    "schema": {
        "data": {
            "type": "array",
            "required": True,
            "description": "Array of data points as [x, y] or {x, y, label}",
        },
        "title": {"type": "string", "default": "", "description": "Optional chart title"},
        "xlabel": {"type": "string", "default": "", "description": "Optional x-axis label"},
        "ylabel": {"type": "string", "default": "", "description": "Optional y-axis label"},
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {
            "type": "float",
            "required": True,
            "description": "How long to animate (seconds)",
        },
    },
    "example": [[0, 10], [1, 25], [2, 45]],
}
