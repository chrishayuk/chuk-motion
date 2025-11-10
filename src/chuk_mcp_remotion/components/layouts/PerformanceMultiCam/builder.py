# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/PerformanceMultiCam/builder.py
"""PerformanceMultiCam composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    primary_cam: Any | None = None,
    secondary_cams: list[Any] | None = None,
    layout: str = "primary-main",
    gap: float = 20,
    padding: float = 40,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """Add PerformanceMultiCam to the composition."""
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="PerformanceMultiCam",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "primary_cam": primary_cam,
            "secondary_cams": secondary_cams or [],
            "layout": layout,
            "gap": gap,
            "padding": padding,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
