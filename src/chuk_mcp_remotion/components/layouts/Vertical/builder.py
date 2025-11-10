# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/Vertical/builder.py
"""Vertical composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    top: Any | None = None,
    bottom: Any | None = None,
    layout_style: str = "top-bottom",
    top_ratio: float = 50,
    gap: float = 20,
    padding: float = 40,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """Add Vertical to the composition."""
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="Vertical",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "top": top,
            "bottom": bottom,
            "layout_style": layout_style,
            "top_ratio": top_ratio,
            "gap": gap,
            "padding": padding,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
