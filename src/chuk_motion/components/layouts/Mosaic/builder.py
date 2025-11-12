# chuk-motion/src/chuk_motion/components/layouts/Mosaic/builder.py
"""Mosaic composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    clips: list[dict] | None = None,
    style: str = "hero-corners",
    gap: float = 10,
    padding: float = 40,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """Add Mosaic to the composition."""
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="Mosaic",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "clips": clips or [],
            "style": style,
            "gap": gap,
            "padding": padding,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
