"""TrueFocus component schema and Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class TrueFocusProps(BaseModel):
    """Properties for TrueFocus component."""

    text: str = Field(description="Text to animate (will be split into words)")
    fontSize: Literal["xl", "2xl", "3xl", "4xl"] = Field(
        default="3xl", description="Font size"
    )
    fontWeight: Literal["bold", "extrabold", "black"] = Field(
        default="black", description="Font weight"
    )
    textColor: str | None = Field(None, description="Text color")
    frameColor: str | None = Field(None, description="Color of corner brackets")
    glowColor: str | None = Field(None, description="Glow effect color")
    blurAmount: float = Field(
        default=5.0, description="Blur intensity for inactive words in pixels", ge=0.0, le=20.0
    )
    wordDuration: float = Field(
        default=1.0, description="Duration each word stays focused in seconds", ge=0.1, le=10.0
    )
    position: Literal["center", "top", "bottom"] = Field(
        default="center", description="Vertical position"
    )
    start_time: float = Field(description="When to show (seconds)")
    duration: float = Field(default=3.0, description="Total duration (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="TrueFocus",
    description="Dramatic text animation with word-by-word focus cycling",
    category="text-animation",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Dramatic text animation with word-by-word focus cycling. Blurs inactive words while highlighting the focused word with animated corner brackets and glow effect",
    "category": "text-animation",
    "tags": ["text", "animation", "focus", "dramatic", "emphasis", "overlay"],
    "schema": {
        "text": {
            "type": "string",
            "required": True,
            "description": "Text to animate (will be split into words)",
        },
        "font_size": {
            "type": "string",
            "default": "3xl",
            "description": "Font size (xl, 2xl, 3xl, 4xl)",
        },
        "font_weight": {
            "type": "string",
            "default": "black",
            "description": "Font weight (bold, extrabold, black)",
        },
        "text_color": {
            "type": "string",
            "optional": True,
            "description": "Text color (uses theme text color if not specified)",
        },
        "frame_color": {
            "type": "string",
            "optional": True,
            "description": "Color of corner brackets (uses primary color if not specified)",
        },
        "glow_color": {
            "type": "string",
            "optional": True,
            "description": "Glow effect color (uses primary color if not specified)",
        },
        "blur_amount": {
            "type": "number",
            "default": 5.0,
            "description": "Blur intensity for inactive words in pixels (0-20)",
        },
        "word_duration": {
            "type": "number",
            "default": 1.0,
            "description": "Duration each word stays focused in seconds (0.1-10)",
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
        "text": "Innovation Through Excellence",
        "font_size": "3xl",
        "word_duration": 1.5,
        "position": "center",
        "start_time": 0.0,
        "duration": 6.0,
    },
    "use_cases": [
        "Dramatic tagline reveals",
        "Key message emphasis",
        "Brand statement animations",
        "Call-to-action highlights",
    ],
    "design_tokens_used": {
        "typography": ["font_sizes['3xl']", "font_weights.black", "primary_font", "letter_spacing.tight", "line_heights.tight"],
        "colors": ["text.on_dark", "primary[0]"],
        "spacing": ["spacing.sm", "spacing.lg", "spacing.xl", "spacing.xs", "spacing['3xl']", "border_width.thick", "border_radius.xs"],
        "motion": ["default_spring.config.damping", "default_spring.config.stiffness", "default_spring.config.mass"],
    },
}
