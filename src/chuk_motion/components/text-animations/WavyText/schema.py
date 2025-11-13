"""WavyText component schema and Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class WavyTextProps(BaseModel):
    """Properties for WavyText component."""

    text: str = Field(description="Text to animate with wave")
    fontSize: Literal["xl", "2xl", "3xl", "4xl"] = Field(
        default="4xl", description="Font size"
    )
    fontWeight: Literal["normal", "medium", "semibold", "bold", "extrabold", "black"] = Field(
        default="bold", description="Font weight"
    )
    textColor: str | None = Field(None, description="Text color")
    waveAmplitude: float = Field(
        default=20.0, description="Height of wave oscillation in pixels", ge=5.0, le=50.0
    )
    waveSpeed: float = Field(
        default=1.0, description="Speed of wave motion", ge=0.1, le=5.0
    )
    waveFrequency: float = Field(
        default=0.3, description="Frequency of wave (spacing between peaks)", ge=0.1, le=2.0
    )
    position: Literal["center", "top", "bottom"] = Field(
        default="center", description="Vertical position"
    )
    align: Literal["left", "center", "right"] = Field(
        default="center", description="Text alignment"
    )
    start_time: float = Field(description="When to show (seconds)")
    duration: float = Field(default=3.0, description="Total duration (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="WavyText",
    description="Continuous wave motion animation on characters",
    category="text-animation",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Continuous wave motion animation on characters. Each character oscillates vertically with a phase offset to create a wave effect",
    "category": "text-animation",
    "tags": ["text", "wave", "motion", "animation", "playful", "fun"],
    "schema": {
        "text": {
            "type": "string",
            "required": True,
            "description": "Text to animate with wave",
        },
        "font_size": {
            "type": "string",
            "default": "4xl",
            "description": "Font size (xl, 2xl, 3xl, 4xl)",
        },
        "font_weight": {
            "type": "string",
            "default": "bold",
            "description": "Font weight (normal, medium, semibold, bold, extrabold, black)",
        },
        "text_color": {
            "type": "string",
            "optional": True,
            "description": "Text color (uses on_dark color if not specified)",
        },
        "wave_amplitude": {
            "type": "number",
            "default": 20.0,
            "description": "Height of wave oscillation in pixels (5-50)",
        },
        "wave_speed": {
            "type": "number",
            "default": 1.0,
            "description": "Speed of wave motion (0.1-5.0)",
        },
        "wave_frequency": {
            "type": "number",
            "default": 0.3,
            "description": "Frequency of wave (spacing between peaks, 0.1-2.0)",
        },
        "position": {
            "type": "string",
            "default": "center",
            "values": ["center", "top", "bottom"],
            "description": "Vertical position",
        },
        "align": {
            "type": "string",
            "default": "center",
            "values": ["left", "center", "right"],
            "description": "Text alignment",
        },
        "start_time": {
            "type": "float",
            "required": True,
            "description": "When to show (seconds)",
        },
        "duration": {
            "type": "float",
            "default": 3.0,
            "description": "Total duration (seconds)",
        },
    },
    "example": {
        "text": "WAVE",
        "font_size": "4xl",
        "wave_amplitude": 20.0,
        "wave_speed": 1.0,
        "wave_frequency": 0.3,
        "start_time": 0.0,
        "duration": 3.0,
    },
    "use_cases": [
        "Fun titles",
        "Music videos",
        "Creative content",
        "Playful effects",
        "Party/celebration themes",
    ],
    "design_tokens_used": {
        "typography": ["font_sizes['4xl']", "font_weights.bold", "primary_font", "letter_spacing.wide"],
        "colors": ["text.on_dark"],
        "spacing": ["spacing.xl", "spacing['4xl']"],
    },
}
