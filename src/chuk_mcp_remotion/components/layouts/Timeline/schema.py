# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/Timeline/schema.py
"""Timeline component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class TimelineProps(BaseModel):
    """Properties for Timeline component."""

    main_content: Any | None = Field(None, description="Background content")
    milestones: list[dict] | None = Field(
        None, description="List of milestone objects with {time, label, icon}"
    )
    current_time: float | None = Field(0, description="Current progress time")
    total_duration: float | None = Field(10, description="Total timeline duration")
    position: str | None = Field("bottom", description="Position: top, bottom")
    height: float | None = Field(100, description="Timeline bar height (pixels)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


METADATA = ComponentMetadata(
    name="Timeline",
    description="Progress/timeline overlay with milestones and progress indicators",
    category="layout",
)

MCP_SCHEMA = {
    "description": "Progress/timeline overlay with milestones and progress indicators",
    "category": "layout",
    "schema": {
        "main_content": {"type": "component", "description": "Background content"},
        "milestones": {"type": "array", "description": "Milestone objects"},
        "current_time": {"type": "number", "default": 0, "description": "Current progress time"},
        "total_duration": {"type": "number", "default": 10, "description": "Total duration"},
        "position": {"type": "enum", "default": "bottom", "values": ["top", "bottom"], "description": "Position"},
        "height": {"type": "number", "default": 100, "description": "Timeline height (pixels)"},
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
}
