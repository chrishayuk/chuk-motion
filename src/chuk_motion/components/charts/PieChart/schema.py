# chuk-motion/src/chuk_motion/components/charts/PieChart/schema.py
"""PieChart component schema and Pydantic models."""

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class PieDataPoint(BaseModel):
    """A single data point with label and value."""

    label: str = Field(min_length=1, description="Label for the data point")
    value: float = Field(ge=0.0, description="Value for the data point (must be non-negative)")
    color: str | None = Field(None, min_length=1, description="Optional color for the segment")


class PieChartProps(BaseModel):
    """Properties for PieChart component."""

    data: list[PieDataPoint] = Field(
        min_length=1,
        description="List of objects with label, value, and optional color"
    )
    title: str | None = Field(None, min_length=1, description="Optional chart title")
    start_time: float = Field(0.0, ge=0.0, description="When to show (seconds)")
    duration: float = Field(4.0, gt=0.0, description="How long to animate (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="PieChart",
    description="Animated pie chart for showing proportions and percentages",
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
            "description": "List of objects with label, value, and optional color",
        },
        "title": {"type": "string", "default": "", "description": "Optional chart title"},
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {
            "type": "float",
            "required": True,
            "description": "How long to animate (seconds)",
        },
    },
    "example": [{"label": "Desktop", "value": 45}, {"label": "Mobile", "value": 35}],
}
