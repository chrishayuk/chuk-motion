"""PixelTransition component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class PixelTransitionProps(BaseModel):
    """Properties for PixelTransition component."""

    firstContent: Any = Field(description="First content component")
    secondContent: Any = Field(description="Second content component")
    gridSize: int = Field(
        default=10, description="Number of pixels per row/column", ge=3, le=30
    )
    pixelColor: str | None = Field(None, description="Color of transition pixels")
    transitionStart: int = Field(default=60, description="When transition starts (frames)", ge=0)
    transitionDuration: int = Field(default=30, description="Transition duration (frames)", ge=1)
    start_time: float = Field(description="When to show (seconds)")
    duration: float = Field(default=5.0, description="Total duration (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="PixelTransition",
    description="Pixelated dissolve transition effect between two pieces of content",
    category="transition",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Pixelated dissolve transition effect between two pieces of content. Pixels animate in with random stagger to cover first content, then animate out to reveal second content",
    "category": "transition",
    "tags": ["transition", "pixel", "dissolve", "reveal", "animation", "effect"],
    "schema": {
        "first_content": {
            "type": "component",
            "required": True,
            "description": "First content component (shown initially)",
        },
        "second_content": {
            "type": "component",
            "required": True,
            "description": "Second content component (revealed after transition)",
        },
        "grid_size": {
            "type": "number",
            "default": 10,
            "description": "Number of pixels per row/column (10 = 10x10 = 100 pixels)",
        },
        "pixel_color": {
            "type": "string",
            "optional": True,
            "description": "Color of transition pixels (uses primary color if not specified)",
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
        "first_content": {"type": "TitleScene", "config": {"text": "Before", "variant": "bold"}},
        "second_content": {"type": "TitleScene", "config": {"text": "After", "variant": "glass"}},
        "grid_size": 12,
        "transition_start": 2.0,
        "transition_duration": 1.0,
        "start_time": 0.0,
        "duration": 5.0,
    },
    "use_cases": [
        "Scene transitions",
        "Content reveals",
        "Before/after showcases",
        "Dramatic content switches",
        "Retro-style transitions",
    ],
    "design_tokens_used": {
        "colors": ["primary[0]"],
    },
}
