# chuk-motion/src/chuk_motion/components/content/DemoBox/builder.py
"""DemoBox composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    label: str,
    start_time: float,
    color: str = "primary",
    duration: float = 5.0,
) -> "CompositionBuilder":
    """Add DemoBox to the composition."""
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="DemoBox",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "label": label,
            "color": color,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
