"""VideoContent component schema and Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field

from ...base import ComponentMetadata


class VideoContentProps(BaseModel):
    """Properties for VideoContent component."""

    src: str = Field(description="Video source URL or path to static file (e.g. 'video.mp4')")
    volume: float = Field(
        default=1.0, description="Video volume (0.0 to 1.0)", ge=0.0, le=1.0
    )
    playbackRate: float = Field(
        default=1.0, description="Video playback speed multiplier", gt=0.0, le=4.0
    )
    fit: Literal["contain", "cover", "fill"] = Field(
        default="cover", description="How video fits in container"
    )
    muted: bool = Field(default=False, description="Whether video should be muted")
    startFrom: int = Field(
        default=0, description="Frame offset to start video playback from", ge=0
    )
    loop: bool = Field(default=False, description="Whether to loop the video continuously")
    start_time: float = Field(description="When to show (seconds)")
    duration: float = Field(default=5.0, description="Total duration (seconds)")

    class Config:
        extra = "forbid"


# Component metadata
METADATA = ComponentMetadata(
    name="VideoContent",
    description="Video player component for playing video files",
    category="content",
)


# MCP schema (for backward compatibility with MCP tools list)
MCP_SCHEMA = {
    "description": "Video player component that plays video files. Supports local files (via staticFile) and remote URLs. Perfect for adding video content to layouts.",
    "category": "content",
    "tags": ["video", "player", "media", "content", "playback"],
    "schema": {
        "src": {
            "type": "string",
            "required": True,
            "description": "Video source URL or path to static file (e.g. 'video.mp4')",
        },
        "volume": {
            "type": "number",
            "default": 1.0,
            "description": "Video volume (0.0 to 1.0)",
        },
        "playback_rate": {
            "type": "number",
            "default": 1.0,
            "description": "Video playback speed (0.5 = half speed, 2.0 = double speed)",
        },
        "fit": {
            "type": "string",
            "default": "cover",
            "values": ["contain", "cover", "fill"],
            "description": "How video fits in container",
        },
        "muted": {
            "type": "boolean",
            "default": False,
            "description": "Whether video should be muted",
        },
        "start_from": {
            "type": "integer",
            "default": 0,
            "description": "Frame offset to start video from",
        },
        "loop": {
            "type": "boolean",
            "default": False,
            "description": "Whether to loop the video continuously",
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
        "src": "video.mp4",
        "volume": 1.0,
        "playback_rate": 1.0,
        "fit": "cover",
        "muted": False,
        "loop": False,
        "start_time": 0.0,
        "duration": 5.0,
    },
    "use_cases": [
        "Video backgrounds for layouts",
        "Product demonstration videos",
        "Tutorial content",
        "Marketing video content",
        "Presentation video clips",
    ],
    "design_tokens_used": {
        "colors": ["background.dark"],
    },
}
