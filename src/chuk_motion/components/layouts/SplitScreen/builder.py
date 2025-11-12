# chuk-motion/src/chuk_motion/components/layouts/SplitScreen/builder.py
"""SplitScreen composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    orientation: str | None = None,
    layout: str | None = None,
    gap: float = 20,
    left_content: str | None = None,
    right_content: str | None = None,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add SplitScreen to the composition.

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
        component_type="SplitScreen",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "orientation": orientation,
            "layout": layout,
            "gap": gap,
            "left_content": left_content,
            "right_content": right_content,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
