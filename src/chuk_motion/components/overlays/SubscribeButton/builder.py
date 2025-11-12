# chuk-motion/src/chuk_motion/components/overlays/SubscribeButton/builder.py
"""SubscribeButton composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    variant: str | None = None,
    animation: str | None = None,
    position: str | None = None,
    duration: float = 3.0,
    custom_text: str | None = None,
) -> "CompositionBuilder":
    """
    Add SubscribeButton to the composition.

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
        component_type="SubscribeButton",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "variant": variant,
            "animation": animation,
            "position": position,
            "start_time": start_time,
            "duration": duration,
            "custom_text": custom_text,
        },
        layer=10,
    )
    builder.components.append(component)
    return builder
