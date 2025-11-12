# chuk-motion/src/chuk_motion/components/animations/Counter/builder.py
"""Counter composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    end_value: float,
    start_time: float,
    start_value: float = 0,
    prefix: str | None = None,
    suffix: str | None = None,
    decimals: int = 0,
    animation: str | None = None,
    duration: float = 2.0,
) -> "CompositionBuilder":
    """
    Add Counter to the composition.

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
        component_type="Counter",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "start_value": start_value,
            "end_value": end_value,
            "prefix": prefix,
            "suffix": suffix,
            "decimals": decimals,
            "animation": animation,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
