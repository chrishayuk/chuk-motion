# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/DialogueFrame/schema.py
"""DialogueFrame component schema and Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class DialogueFrameProps(BaseModel):
    """Properties for DialogueFrame component."""

    left_speaker: Any | None = Field(None, description="Left speaker content")
    right_speaker: Any | None = Field(None, description="Right speaker content")
    center_content: Any | None = Field(None, description="Optional center content (captions, etc.)")
    speaker_size: float | None = Field(40, description="Speaker panel size (percentage, 0-100)")
    gap: float | None = Field(20, description="Gap between panels (pixels)")
    padding: float | None = Field(40, description="Padding around layout (pixels)")
    start_time: float = Field(description="When to show (seconds)")
    duration: float | None = Field(5.0, description="How long to show (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="DialogueFrame",
    description="For conversation/dialogue scenes with two speakers",
    category="layout",
)


# MCP schema
MCP_SCHEMA = {
    "description": "For conversation/dialogue scenes with two speakers",
    "category": "layout",
    "schema": {
        "left_speaker": {"type": "component", "description": "Left speaker content"},
        "right_speaker": {"type": "component", "description": "Right speaker content"},
        "center_content": {"type": "component", "description": "Optional center content (captions, etc.)"},
        "speaker_size": {
            "type": "number",
            "default": 40,
            "description": "Speaker panel size (percentage, 0-100)",
        },
        "gap": {"type": "number", "default": 20, "description": "Gap between panels (pixels)"},
        "padding": {"type": "number", "default": 40, "description": "Padding around layout (pixels)"},
        "start_time": {"type": "float", "required": True, "description": "When to show (seconds)"},
        "duration": {"type": "float", "default": 5.0, "description": "How long to show (seconds)"},
    },
    "example": {
        "left_speaker": {"type": "CodeBlock", "code": "// Speaker 1"},
        "right_speaker": {"type": "CodeBlock", "code": "// Speaker 2"},
        "center_content": {"type": "CodeBlock", "code": "// Captions"},
        "speaker_size": 40,
        "gap": 20,
        "padding": 40,
        "start_time": 0.0,
        "duration": 10.0,
        "use_cases": [
            "Interview videos",
            "Podcast recordings",
            "Debate formats",
            "Conversation scenes",
        ],
    },
}
