"""PanelCascade component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class PanelCascadeProps(BaseModel):
    """Properties for PanelCascade component."""

    items: list[Any] = Field(description="Array of panel components to animate")
    cascade_type: str | None = Field(
        "from_edges", description="Cascade animation style"
    )
    stagger_delay: float | None = Field(
        0.08, description="Delay between each panel (seconds)"
    )
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="PanelCascade",
    description="Staggered panel entrance animations for multi-panel layouts",
    category="animation",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Staggered panel entrance animations for multi-panel layouts",
    "category": "animation",
    "cascade_types": {
        "from_edges": "Panels slide in from nearest screen edge (spatial)",
        "from_center": "Panels scale out from center (radial)",
        "bounce_in": "Panels bounce in with slight overshoot (playful)",
        "sequential_left": "Left to right sequence (reading order)",
        "sequential_right": "Right to left sequence (reverse)",
        "sequential_top": "Top to bottom sequence (vertical)",
        "wave": "Wave pattern across panels (dynamic)",
    },
    "schema": {
        "items": {
            "type": "array",
            "required": True,
            "description": "Array of panel components to animate",
        },
        "cascade_type": {
            "type": "enum",
            "default": "from_edges",
            "values": [
                "from_edges",
                "from_center",
                "bounce_in",
                "sequential_left",
                "sequential_right",
                "sequential_top",
                "wave",
            ],
            "description": "Cascade animation style",
        },
        "stagger_delay": {
            "type": "float",
            "default": 0.08,
            "description": "Delay between each panel (seconds)",
        },
        "start_time": {
            "type": "float",
            "required": True,
            "description": "When to show (seconds)",
        },
        "duration": {
            "type": "float",
            "default": 5.0,
            "description": "How long to show (seconds)",
        },
    },
    "example": {
        "cascade_type": "from_edges",
        "stagger_delay": 0.08,
        "items": [
            {"type": "CodeBlock", "code": "Panel 1"},
            {"type": "CodeBlock", "code": "Panel 2"},
            {"type": "CodeBlock", "code": "Panel 3"},
            {"type": "CodeBlock", "code": "Panel 4"},
        ],
        "start_time": 0.0,
        "duration": 10.0,
    },
}
