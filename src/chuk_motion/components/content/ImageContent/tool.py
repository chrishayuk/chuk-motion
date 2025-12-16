"""ImageContent MCP tool definition."""

from pydantic import BaseModel, Field

from .schema import METADATA


class ImageContentConfig(BaseModel):
    """Configuration for ImageContent component."""

    src: str = Field(description="Image source URL or path to static file (e.g. 'image.png')")
    fit: str = Field(
        default="cover", description="How image fits in container: 'contain', 'cover', or 'fill'"
    )
    opacity: float = Field(default=1.0, description="Image opacity (0.0 to 1.0)", ge=0.0, le=1.0)
    border_radius: int = Field(default=0, description="Border radius in pixels", ge=0)


TOOL_DEFINITION = {
    "name": "create_image_content",
    "description": "Create an image display component. Supports local files (via staticFile) and remote URLs. Use this for adding image content to layouts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "component_type": {
                "type": "string",
                "const": METADATA.name,
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
                        "description": "Image source URL or path (e.g. 'image.png' for static file, or full URL)",
                    },
                    "fit": {
                        "type": "string",
                        "enum": ["contain", "cover", "fill"],
                        "description": "How image fits in container",
                        "default": "cover",
                    },
                    "opacity": {
                        "type": "number",
                        "description": "Image opacity (0.0 to 1.0)",
                        "minimum": 0.0,
                        "maximum": 1.0,
                        "default": 1.0,
                    },
                    "border_radius": {
                        "type": "integer",
                        "description": "Border radius in pixels",
                        "minimum": 0,
                        "default": 0,
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
