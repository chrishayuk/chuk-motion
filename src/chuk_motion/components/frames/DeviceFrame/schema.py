"""DeviceFrame component schema and metadata."""

from typing import Literal

from pydantic import BaseModel, Field

from chuk_motion.components.base import ComponentMetadata


class DeviceFrameProps(BaseModel):
    """Props for DeviceFrame component."""

    startFrame: int = Field(..., description="Frame when component becomes visible")
    durationInFrames: int = Field(..., description="Duration in frames")
    device: Literal["phone", "tablet", "laptop"] = Field(
        default="phone", description="Type of device frame to display"
    )
    content: str = Field(
        default="",
        description="Content to display inside the device (can be image path or component)",
    )
    orientation: Literal["portrait", "landscape"] = Field(
        default="portrait", description="Device orientation"
    )
    scale: float = Field(
        default=1.0, description="Auto-scale factor for the device (0.1 to 2.0)", ge=0.1, le=2.0
    )
    glare: bool = Field(default=True, description="Enable realistic screen glare effect")
    shadow: bool = Field(default=True, description="Enable device shadow")
    position: Literal[
        "center",
        "top-left",
        "top-center",
        "top-right",
        "center-left",
        "center-right",
        "bottom-left",
        "bottom-center",
        "bottom-right",
    ] = Field(default="center", description="Position of device on screen")

    class Config:
        extra = "forbid"


METADATA = ComponentMetadata(
    name="DeviceFrame",
    description="Realistic device frame (phone, tablet, laptop) with auto-scaling, glare effects, and content display",
    category="demo_realism",
)

# MCP schema (backward compatible)
MCP_SCHEMA = {
    "startFrame": {
        "type": "number",
        "description": "Frame when component becomes visible",
        "required": True,
    },
    "durationInFrames": {
        "type": "number",
        "description": "Duration in frames",
        "required": True,
    },
    "device": {
        "type": "string",
        "description": "Type of device frame: phone, tablet, or laptop",
        "default": "phone",
        "enum": ["phone", "tablet", "laptop"],
    },
    "content": {
        "type": "string",
        "description": "Content to display inside the device (image path or component)",
        "default": "",
    },
    "orientation": {
        "type": "string",
        "description": "Device orientation: portrait or landscape",
        "default": "portrait",
        "enum": ["portrait", "landscape"],
    },
    "scale": {
        "type": "number",
        "description": "Auto-scale factor for the device (0.1 to 2.0)",
        "default": 1.0,
    },
    "glare": {
        "type": "boolean",
        "description": "Enable realistic screen glare effect",
        "default": True,
    },
    "shadow": {
        "type": "boolean",
        "description": "Enable device shadow",
        "default": True,
    },
    "position": {
        "type": "string",
        "description": "Position of device on screen",
        "default": "center",
        "enum": [
            "center",
            "top-left",
            "top-center",
            "top-right",
            "center-left",
            "center-right",
            "bottom-left",
            "bottom-center",
            "bottom-right",
        ],
    },
}
