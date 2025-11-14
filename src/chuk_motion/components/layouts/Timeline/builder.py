# chuk-motion/src/chuk_motion/components/layouts/Timeline/builder.py
"""Timeline composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    main_content: Any | None = None,
    milestones: list[dict] | None = None,
    current_time: float = 0,
    total_duration: float = 10,
    position: str = "bottom",
    height: float = 100,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """Add Timeline to the composition."""
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="Timeline",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "main_content": main_content,
            "milestones": milestones or [],
            "current_time": current_time,
            "total_duration": total_duration,
            "position": position,
            "height": height,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
