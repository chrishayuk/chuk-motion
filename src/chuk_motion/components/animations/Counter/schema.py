# chuk-motion/src/chuk_motion/components/animations/Counter/schema.py
"""Counter component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class CounterProps(BaseModel):
    """Properties for Counter component."""

    start_value: float | None = Field(0, description="Starting number")
    end_value: float = Field(description="Ending number")
    prefix: str | None = Field(None, description="Text before number (e.g., '$')")
    suffix: str | None = Field(None, description="Text after number (e.g., 'M', '%')")
    decimals: int | None = Field(0, description="Number of decimal places")
    animation: Any | None = Field("count_up", description="Animation style")
    start_time: float = Field(description="When to start (seconds)")
    duration: float | None = Field(2.0, description="Animation duration (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="Counter",
    description="Animated number counter for statistics and metrics",
    category="animation",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Animated number counter for statistics and metrics",
    "category": "animation",
    "animations": {
        "count_up": "Count from start to end value",
        "flip": "Digit flip animation",
        "slot_machine": "Slot machine roll effect",
        "digital": "Digital display style",
    },
    "schema": {
        "start_value": {"type": "number", "default": 0, "description": "Starting number"},
        "end_value": {"type": "number", "required": True, "description": "Ending number"},
        "prefix": {
            "type": "string",
            "default": "",
            "description": "Text before number (e.g., '$')",
        },
        "suffix": {
            "type": "string",
            "default": "",
            "description": "Text after number (e.g., 'M', '%')",
        },
        "decimals": {"type": "integer", "default": 0, "description": "Number of decimal places"},
        "animation": {
            "type": "enum",
            "default": "count_up",
            "values": ["count_up", "flip", "slot_machine", "digital"],
            "description": "Animation style",
        },
        "start_time": {"type": "float", "required": True, "description": "When to start (seconds)"},
        "duration": {
            "type": "float",
            "default": 2.0,
            "description": "Animation duration (seconds)",
        },
    },
    "example": {
        "start_value": 0,
        "end_value": 1000000,
        "prefix": "",
        "suffix": "+ users",
        "decimals": 0,
        "animation": "count_up",
        "start_time": 5.0,
        "duration": 2.0,
    },
}
