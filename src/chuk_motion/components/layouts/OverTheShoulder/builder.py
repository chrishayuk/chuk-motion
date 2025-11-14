# chuk-motion/src/chuk_motion/components/layouts/OverTheShoulder/builder.py
"""OverTheShoulder composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    screen_content: Any | None = None,
    shoulder_overlay: Any | None = None,
    overlay_position: str = "bottom-left",
    overlay_size: float = 30,
    gap: float = 20,
    padding: float = 40,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """Add OverTheShoulder to the composition."""
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="OverTheShoulder",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "screen_content": screen_content,
            "shoulder_overlay": shoulder_overlay,
            "overlay_position": overlay_position,
            "overlay_size": overlay_size,
            "gap": gap,
            "padding": padding,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
