"""BeforeAfterSlider component schema and metadata."""

from typing import Literal

from pydantic import BaseModel, Field

from chuk_mcp_remotion.components.base import ComponentMetadata


class BeforeAfterSliderProps(BaseModel):
    """Props for BeforeAfterSlider component."""

    startFrame: int = Field(..., description="Frame when component becomes visible")
    durationInFrames: int = Field(..., description="Duration in frames")
    beforeImage: str = Field(..., description="Path to the 'before' image")
    afterImage: str = Field(..., description="Path to the 'after' image")
    beforeLabel: str = Field(default="Before", description="Label for the 'before' state")
    afterLabel: str = Field(default="After", description="Label for the 'after' state")
    orientation: Literal["horizontal", "vertical"] = Field(
        default="horizontal", description="Slider orientation"
    )
    sliderPosition: float = Field(
        default=50.0, description="Initial slider position as percentage (0-100)", ge=0.0, le=100.0
    )
    animateSlider: bool = Field(default=True, description="Animate slider movement")
    sliderStartPosition: float = Field(
        default=0.0, description="Starting position for slider animation (0-100)", ge=0.0, le=100.0
    )
    sliderEndPosition: float = Field(
        default=100.0, description="Ending position for slider animation (0-100)", ge=0.0, le=100.0
    )
    showLabels: bool = Field(default=True, description="Show before/after labels")
    labelPosition: Literal["top", "bottom", "overlay"] = Field(
        default="overlay", description="Position of labels"
    )
    handleStyle: Literal["default", "arrow", "circle", "bar"] = Field(
        default="default", description="Style of the slider handle"
    )
    width: int = Field(default=1200, description="Component width in pixels", ge=400, le=1920)
    height: int = Field(default=800, description="Component height in pixels", ge=300, le=1080)
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
    ] = Field(default="center", description="Position on screen")
    borderRadius: int = Field(default=12, description="Border radius in pixels", ge=0, le=50)


METADATA = ComponentMetadata(
    name="BeforeAfterSlider",
    description="Interactive before/after comparison slider with animated handle, customizable labels, and multiple handle styles",
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
    "beforeImage": {
        "type": "string",
        "description": "Path to the 'before' image",
        "required": True,
    },
    "afterImage": {
        "type": "string",
        "description": "Path to the 'after' image",
        "required": True,
    },
    "beforeLabel": {
        "type": "string",
        "description": "Label for the 'before' state",
        "default": "Before",
    },
    "afterLabel": {
        "type": "string",
        "description": "Label for the 'after' state",
        "default": "After",
    },
    "orientation": {
        "type": "string",
        "description": "Slider orientation: horizontal or vertical",
        "default": "horizontal",
        "enum": ["horizontal", "vertical"],
    },
    "sliderPosition": {
        "type": "number",
        "description": "Initial slider position as percentage (0-100)",
        "default": 50.0,
    },
    "animateSlider": {
        "type": "boolean",
        "description": "Animate slider movement",
        "default": True,
    },
    "sliderStartPosition": {
        "type": "number",
        "description": "Starting position for slider animation (0-100)",
        "default": 0.0,
    },
    "sliderEndPosition": {
        "type": "number",
        "description": "Ending position for slider animation (0-100)",
        "default": 100.0,
    },
    "showLabels": {
        "type": "boolean",
        "description": "Show before/after labels",
        "default": True,
    },
    "labelPosition": {
        "type": "string",
        "description": "Position of labels: top, bottom, overlay",
        "default": "overlay",
        "enum": ["top", "bottom", "overlay"],
    },
    "handleStyle": {
        "type": "string",
        "description": "Style of the slider handle: default, arrow, circle, bar",
        "default": "default",
        "enum": ["default", "arrow", "circle", "bar"],
    },
    "width": {
        "type": "number",
        "description": "Component width in pixels (400-1920)",
        "default": 1200,
    },
    "height": {
        "type": "number",
        "description": "Component height in pixels (300-1080)",
        "default": 800,
    },
    "position": {
        "type": "string",
        "description": "Position on screen",
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
    "borderRadius": {
        "type": "number",
        "description": "Border radius in pixels (0-50)",
        "default": 12,
    },
}
