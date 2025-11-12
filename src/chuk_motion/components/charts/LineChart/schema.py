# chuk-motion/src/chuk_motion/components/charts/LineChart/schema.py
"""LineChart component schema and Pydantic models."""

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class DataPoint(BaseModel):
    """A single data point with x, y coordinates and optional label."""

    x: float
    y: float
    label: str | None = None


class LineChartProps(BaseModel):
    """Properties for LineChart component."""

    data: list[list[float] | DataPoint] = Field(
        description="Array of data points as [x, y] or {x, y, label}"
    )
    title: str | None = Field(None, description="Chart title")
    xlabel: str | None = Field(None, description="X-axis label")
    ylabel: str | None = Field(None, description="Y-axis label")
    start_time: float = Field(0.0, description="When to show (seconds)")
    duration: float = Field(4.0, description="How long to animate (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="LineChart",
    description="Animated line chart for data visualization with smooth drawing animation",
    category="chart",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": METADATA.description,
    "category": METADATA.category,
    "animations": {
        "draw": "Line draws from left to right",
        "fade_in": "Chart fades in",
        "scale_in": "Chart scales from center",
        "points_sequence": "Points appear sequentially",
    },
    "schema": {
        "data": {
            "type": "array",
            "required": True,
            "description": "Array of data points [x, y] or {x, y, label}",
        },
        "title": {"type": "string", "default": "", "description": "Chart title"},
        "xlabel": {"type": "string", "default": "", "description": "X-axis label"},
        "ylabel": {"type": "string", "default": "", "description": "Y-axis label"},
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {
            "type": "float",
            "default": 4.0,
            "description": "How long to animate (seconds)",
        },
    },
    "example": {
        "data": [[0, 10], [1, 25], [2, 45], [3, 70], [4, 90]],
        "title": "User Growth",
        "xlabel": "Month",
        "ylabel": "Users (thousands)",
        "start_time": 8.0,
        "duration": 4.0,
    },
}
