# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/ThreeColumnLayout/builder.py
"""ThreeColumnLayout composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    left: Any | None = None,
    center: Any | None = None,
    right: Any | None = None,
    left_width: float = 25,
    center_width: float = 50,
    right_width: float = 25,
    gap: float = 20,
    padding: float = 40,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add ThreeColumnLayout to the composition.

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    # Calculate frames if time-based props exist
    start_frame = builder.seconds_to_frames(locals().get("start_time", 0.0))
    duration_frames = builder.seconds_to_frames(
        locals().get("duration_seconds") or locals().get("duration", 3.0)
    )

    component = ComponentInstance(
        component_type="ThreeColumnLayout",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "left": left,
            "center": center,
            "right": right,
            "left_width": left_width,
            "center_width": center_width,
            "right_width": right_width,
            "gap": gap,
            "padding": padding,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
