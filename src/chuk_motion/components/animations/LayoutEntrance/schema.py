"""LayoutEntrance component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class LayoutEntranceProps(BaseModel):
    """Properties for LayoutEntrance component."""

    content: Any = Field(description="Layout or component to animate in")
    entrance_type: str | None = Field("fade_in", description="Entrance animation style")
    entrance_delay: float | None = Field(0.0, description="Delay before entrance (seconds)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="LayoutEntrance",
    description="Universal entrance animation wrapper for any layout",
    category="animation",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Universal entrance animation wrapper for any layout",
    "category": "animation",
    "entrance_types": {
        "none": "No animation (instant)",
        "fade_in": "Simple fade in (subtle, professional)",
        "fade_slide_up": "Fade + slide up (content blocks, cards)",
        "scale_in_soft": "Subtle scale 0.95 → 1.0 (elegant)",
        "scale_in_pop": "Pop scale 0.9 → 1.05 → 1.0 (playful)",
        "slide_in_left": "Slide from left (side panels)",
        "slide_in_right": "Slide from right (side panels)",
        "blur_in": "Fade from blur (dramatic)",
        "zoom_in": "Zoom from 0 to 100% (hero elements)",
    },
    "schema": {
        "content": {
            "type": "component",
            "required": True,
            "description": "Layout or component to animate in",
        },
        "entrance_type": {
            "type": "enum",
            "default": "fade_in",
            "values": [
                "none",
                "fade_in",
                "fade_slide_up",
                "scale_in_soft",
                "scale_in_pop",
                "slide_in_left",
                "slide_in_right",
                "blur_in",
                "zoom_in",
            ],
            "description": "Entrance animation style",
        },
        "entrance_delay": {
            "type": "float",
            "default": 0.0,
            "description": "Delay before entrance (seconds)",
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
        "entrance_type": "fade_slide_up",
        "entrance_delay": 0.2,
        "content": {"type": "Grid", "config": {"layout": "3x3", "items": [...]}},
        "start_time": 0.0,
        "duration": 10.0,
    },
}
