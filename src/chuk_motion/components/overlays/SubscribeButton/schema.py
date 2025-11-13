# chuk-motion/src/chuk_motion/components/overlays/SubscribeButton/schema.py
"""SubscribeButton component schema and Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class SubscribeButtonProps(BaseModel):
    """Properties for SubscribeButton component."""

    variant: Literal["minimal", "standard", "animated", "3d"] | None = Field(
        "standard", description="Button style"
    )
    animation: Literal["bounce", "glow", "pulse", "slide", "wiggle"] | None = Field(
        "bounce", description="Animation style"
    )
    position: Literal["bottom_right", "bottom_center", "center", "top_right"] | None = Field(
        "bottom_right", description="Screen position"
    )
    start_time: float = Field(description="When to show (seconds)", ge=0.0)
    duration: float | None = Field(3.0, description="How long to show (seconds)", gt=0.0)
    custom_text: str | None = Field("SUBSCRIBE", description="Custom button text", min_length=1)

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="SubscribeButton",
    description="Animated subscribe button overlay (YouTube-specific)",
    category="overlay",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Animated subscribe button overlay (YouTube-specific)",
    "category": "overlay",
    "animations": {
        "bounce": "Bouncy spring animation",
        "glow": "Pulsing glow effect",
        "pulse": "Scale pulse",
        "slide": "Slide in from side",
        "wiggle": "Attention-grabbing wiggle",
    },
    "positions": {
        "bottom_right": "Bottom right (standard)",
        "bottom_center": "Bottom center",
        "center": "Center of screen",
        "top_right": "Top right",
    },
    "schema": {
        "variant": {
            "type": "enum",
            "default": "standard",
            "values": ["minimal", "standard", "animated", "3d"],
            "description": "Button style",
        },
        "animation": {
            "type": "enum",
            "default": "bounce",
            "values": ["bounce", "glow", "pulse", "slide", "wiggle"],
            "description": "Animation style",
        },
        "position": {
            "type": "enum",
            "default": "bottom_right",
            "values": ["bottom_right", "bottom_center", "center", "top_right"],
            "description": "Screen position",
        },
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 3.0, "description": "How long to show (seconds)"},
        "custom_text": {
            "type": "string",
            "default": "SUBSCRIBE",
            "description": "Custom button text",
        },
    },
    "example": {
        "variant": "animated",
        "animation": "bounce",
        "position": "bottom_right",
        "start_time": 10.0,
        "duration": 3.0,
        "custom_text": "SUBSCRIBE",
    },
}
