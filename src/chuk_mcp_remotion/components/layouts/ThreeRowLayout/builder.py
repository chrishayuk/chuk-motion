# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/ThreeRowLayout/builder.py
"""ThreeRowLayout composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    top: Any | None = None,
    middle: Any | None = None,
    bottom: Any | None = None,
    top_height: float = 25,
    middle_height: float = 50,
    bottom_height: float = 25,
    gap: float = 20,
    padding: float = 40,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add ThreeRowLayout to the composition.

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="ThreeRowLayout",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "top": top,
            "middle": middle,
            "bottom": bottom,
            "top_height": top_height,
            "middle_height": middle_height,
            "bottom_height": bottom_height,
            "gap": gap,
            "padding": padding,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
