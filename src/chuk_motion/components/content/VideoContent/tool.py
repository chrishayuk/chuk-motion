"""VideoContent MCP tool definition."""

from pydantic import BaseModel, Field


class VideoContentConfig(BaseModel):
    """Configuration for VideoContent component."""

    src: str = Field(description="Video source URL or path to static file (e.g. 'video.mp4')")
    volume: float | None = Field(
        default=1.0, description="Video volume (0.0 to 1.0)", ge=0.0, le=1.0
    )
    playback_rate: float | None = Field(
        default=1.0,
        description="Video playback speed (0.5 = half speed, 2.0 = double speed)",
        gt=0.0,
    )
    fit: str | None = Field(
        default="cover", description="How video fits in container: 'contain', 'cover', or 'fill'"
    )
    muted: bool | None = Field(default=False, description="Whether video should be muted")
    start_from: int | None = Field(
        default=0, description="Frame offset to start video playback from"
    )
    loop: bool | None = Field(default=False, description="Whether to loop the video continuously")


TOOL_DEFINITION = {
    "name": "create_video_content",
    "description": "Create a video player component that plays a video file. Supports local files (via staticFile) and remote URLs. Use this for adding video content to layouts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "component_type": {
                "type": "string",
                "const": "VideoContent",
                "description": "Component type identifier",
            },
            "start_frame": {
                "type": "integer",
                "description": "Frame to start showing the component",
                "default": 0,
            },
            "duration_frames": {
                "type": "integer",
                "description": "How many frames to show the component",
                "default": 150,
            },
            "props": {
                "type": "object",
                "properties": {
                    "src": {
                        "type": "string",
                        "description": "Video source URL or path (e.g. 'video.mp4' for static file, or full URL)",
                    },
                    "volume": {
                        "type": "number",
                        "description": "Video volume (0.0 to 1.0)",
                        "minimum": 0.0,
                        "maximum": 1.0,
                        "default": 1.0,
                    },
                    "playback_rate": {
                        "type": "number",
                        "description": "Playback speed multiplier",
                        "minimum": 0.1,
                        "maximum": 4.0,
                        "default": 1.0,
                    },
                    "fit": {
                        "type": "string",
                        "enum": ["contain", "cover", "fill"],
                        "description": "How video fits in container",
                        "default": "cover",
                    },
                    "muted": {
                        "type": "boolean",
                        "description": "Whether video should be muted",
                        "default": False,
                    },
                    "start_from": {
                        "type": "integer",
                        "description": "Frame offset to start video from",
                        "default": 0,
                    },
                    "loop": {
                        "type": "boolean",
                        "description": "Whether to loop the video continuously",
                        "default": False,
                    },
                },
                "required": ["src"],
            },
            "layer": {
                "type": "integer",
                "description": "Z-index layer for component stacking",
                "default": 0,
            },
        },
        "required": ["component_type", "props"],
    },
}
