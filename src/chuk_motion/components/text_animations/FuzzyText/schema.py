"""FuzzyText component schema and Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class FuzzyTextProps(BaseModel):
    """Properties for FuzzyText component."""

    text: str = Field(description="Text to display with fuzzy effect")
    fontSize: Literal["xl", "2xl", "3xl", "4xl"] = Field(default="3xl", description="Font size")
    fontWeight: Literal["normal", "medium", "semibold", "bold", "extrabold", "black"] = Field(
        default="bold", description="Font weight"
    )
    textColor: str | None = Field(None, description="Text color")
    glitchIntensity: float = Field(
        default=5.0, description="Intensity of glitch displacement", ge=0.0, le=20.0
    )
    scanlineHeight: float = Field(
        default=2.0, description="Height of scanlines in pixels", ge=0.5, le=10.0
    )
    animate: bool = Field(default=True, description="Whether to animate the glitch effect")
    position: Literal["center", "top", "bottom"] = Field(
        default="center", description="Vertical position"
    )
    start_time: float = Field(description="When to show (seconds)")
    duration: float = Field(default=3.0, description="Total duration (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="FuzzyText",
    description="Animated text with scanline distortion and glitch effects",
    category="text-animation",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Animated text with scanline distortion and glitch effects. Creates a fuzzy, VHS-style aesthetic with horizontal displacement and RGB split",
    "category": "text-animation",
    "tags": ["text", "glitch", "VHS", "scanline", "retro", "cyberpunk", "distortion"],
    "schema": {
        "text": {
            "type": "string",
            "required": True,
            "description": "Text to display with fuzzy effect",
        },
        "font_size": {
            "type": "string",
            "default": "3xl",
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
        "glitch_intensity": {
            "type": "number",
            "default": 5.0,
            "description": "Intensity of glitch displacement (0-20)",
        },
        "scanline_height": {
            "type": "number",
            "default": 2.0,
            "description": "Height of scanlines in pixels",
        },
        "animate": {
            "type": "boolean",
            "default": True,
            "description": "Whether to animate the glitch effect",
        },
        "position": {
            "type": "string",
            "default": "center",
            "values": ["center", "top", "bottom"],
            "description": "Vertical position",
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
        "text": "GLITCH EFFECT",
        "font_size": "3xl",
        "glitch_intensity": 5.0,
        "animate": True,
        "start_time": 0.0,
        "duration": 3.0,
    },
    "use_cases": [
        "Retro VHS aesthetics",
        "Glitch art effects",
        "Cyberpunk themes",
        "System error messages",
        "80s/90s retro titles",
    ],
    "design_tokens_used": {
        "typography": [
            "font_sizes['3xl']",
            "font_weights.bold",
            "primary_font",
            "letter_spacing.wide",
        ],
        "colors": ["text.on_dark"],
        "spacing": ["spacing.xl", "spacing['4xl']"],
    },
}
