"""DecryptedText component schema and Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class DecryptedTextProps(BaseModel):
    """Properties for DecryptedText component."""

    text: str = Field(description="Text to animate")
    fontSize: Literal["xl", "2xl", "3xl", "4xl"] = Field(
        default="3xl", description="Font size"
    )
    fontWeight: Literal["normal", "medium", "semibold", "bold", "extrabold", "black"] = Field(
        default="bold", description="Font weight"
    )
    textColor: str | None = Field(None, description="Text color")
    revealDirection: Literal["start", "end", "center"] = Field(
        default="start", description="Direction of reveal"
    )
    scrambleSpeed: float = Field(
        default=3.0, description="Speed of character scrambling", ge=0.5, le=10.0
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
    name="DecryptedText",
    description="Animated text reveal with character scrambling effect",
    category="text-animation",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Animated text reveal with character scrambling effect. Characters progressively decrypt from random characters to the final text",
    "category": "text-animation",
    "tags": ["text", "animation", "reveal", "scramble", "decrypt", "hacker", "glitch"],
    "schema": {
        "text": {
            "type": "string",
            "required": True,
            "description": "Text to animate (characters will scramble then reveal)",
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
        "reveal_direction": {
            "type": "string",
            "default": "start",
            "values": ["start", "end", "center"],
            "description": "Direction of reveal",
        },
        "scramble_speed": {
            "type": "number",
            "default": 3.0,
            "description": "Speed of character scrambling (higher = faster)",
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
        "text": "Access Granted",
        "font_size": "3xl",
        "reveal_direction": "start",
        "scramble_speed": 3.0,
        "start_time": 0.0,
        "duration": 3.0,
    },
    "use_cases": [
        "Dramatic text reveals",
        "Code/hacker aesthetics",
        "Mystery unveilings",
        "System messages",
        "Access granted screens",
    ],
    "design_tokens_used": {
        "typography": ["font_sizes['3xl']", "font_weights.bold", "primary_font", "letter_spacing.wide"],
        "colors": ["text.on_dark"],
        "spacing": ["spacing.xl", "spacing['4xl']"],
    },
}
