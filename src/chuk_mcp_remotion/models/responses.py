"""Pydantic response models for MCP tool responses."""

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error message")


class ComponentResponse(BaseModel):
    """Base response model for all component additions."""

    component: str = Field(..., description="Component type added")
    start_time: float = Field(..., description="Start time in seconds")
    duration: float = Field(..., description="Duration in seconds")


class ChartComponentResponse(ComponentResponse):
    """Response model for chart components."""

    data_points: int = Field(..., description="Number of data points")
    title: str | None = Field(None, description="Chart title")


class CodeComponentResponse(ComponentResponse):
    """Response model for code components."""

    language: str = Field(..., description="Programming language")
    lines: int = Field(..., description="Number of lines of code")


class CounterComponentResponse(ComponentResponse):
    """Response model for counter component."""

    start_value: float = Field(..., description="Starting value")
    end_value: float = Field(..., description="Ending value")


class LayoutComponentResponse(ComponentResponse):
    """Response model for layout components."""

    layout: str = Field(..., description="Layout type or configuration")


class OverlayComponentResponse(ComponentResponse):
    """Response model for overlay components."""

    # Flexible model for various overlay props
    pass
