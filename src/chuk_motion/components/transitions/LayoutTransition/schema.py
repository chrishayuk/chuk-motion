"""LayoutTransition component schema and Pydantic models."""

from typing import Any, Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class LayoutTransitionProps(BaseModel):
    """Properties for LayoutTransition component."""

    firstContent: Any = Field(description="First scene content")
    secondContent: Any = Field(description="Second scene content")
    transitionType: Literal[
        "crossfade", "slide_horizontal", "slide_vertical", "cube_rotate", "parallax_push"
    ] = Field(default="crossfade", description="Transition animation style")
    transitionStart: int = Field(default=60, description="When transition starts (frames)", ge=0)
    transitionDuration: int = Field(default=30, description="Transition duration (frames)", ge=1)
    start_time: float = Field(description="When to show (seconds)")
    duration: float = Field(default=5.0, description="Total duration (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="LayoutTransition",
    description="Animated scene-to-scene layout transitions with motion token integration",
    category="transition",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Animated scene-to-scene layout transitions with motion token integration",
    "category": "transition",
    "transition_types": {
        "crossfade": "Smooth opacity blend between layouts",
        "slide_horizontal": "Slide left/right with ease-out-expo",
        "slide_vertical": "Slide up/down with ease-out-expo",
        "cube_rotate": "3D cube rotation effect with perspective",
        "parallax_push": "Parallax depth effect with scale and offset",
    },
    "motion_tokens": {
        "duration": ["medium", "slow"],
        "easing": ["ease_out_expo", "ease_in_out_quart", "ease_out_quint"],
        "used_for": "Scene transitions, layout switches, content reveals",
    },
    "schema": {
        "first_content": {
            "type": "component",
            "required": True,
            "description": "First scene content (any layout or component)",
        },
        "second_content": {
            "type": "component",
            "required": True,
            "description": "Second scene content (any layout or component)",
        },
        "transition_type": {
            "type": "enum",
            "default": "crossfade",
            "values": [
                "crossfade",
                "slide_horizontal",
                "slide_vertical",
                "cube_rotate",
                "parallax_push",
            ],
            "description": "Transition animation style",
        },
        "transition_start": {
            "type": "float",
            "default": 2.0,
            "description": "When to start transition (seconds into duration)",
        },
        "transition_duration": {
            "type": "float",
            "default": 1.0,
            "description": "Duration of transition animation (seconds)",
        },
        "start_time": {
            "type": "float",
            "required": True,
            "description": "When to show (seconds)",
        },
        "duration": {
            "type": "float",
            "default": 5.0,
            "description": "Total duration (seconds)",
        },
    },
    "example": {
        "first_content": {"type": "Grid", "config": {"layout": "3x3", "items": [...]}},
        "second_content": {"type": "Container", "config": {"content": {...}}},
        "transition_type": "crossfade",
        "transition_start": 2.0,
        "transition_duration": 1.0,
        "start_time": 0.0,
        "duration": 5.0,
    },
    "use_cases": [
        "Scene changes in narratives",
        "Layout switches (Grid → Container → Timeline)",
        "Before/after showcases",
        "Chapter transitions",
        "Multi-part content flow",
    ],
    "best_practices": [
        "Use crossfade for subtle, professional transitions",
        "Use slide_horizontal for sequential content (chapters, slides)",
        "Use cube_rotate for dramatic, 3D transitions",
        "Use parallax_push for depth and layering effects",
        "Keep transition_duration between 0.5s-1.5s for optimal viewing",
    ],
}
