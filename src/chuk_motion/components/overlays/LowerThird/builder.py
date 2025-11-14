# chuk-motion/src/chuk_motion/components/overlays/LowerThird/builder.py
"""LowerThird composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    name: str,
    start_time: float,
    title: str | None = None,
    variant: str | None = None,
    position: str | None = None,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add LowerThird to the composition.

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
        component_type="LowerThird",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "name": name,
            "title": title,
            "variant": variant,
            "position": position,
            "start_time": start_time,
            "duration": duration,
        },
        layer=10,
    )
    builder.components.append(component)
    return builder
