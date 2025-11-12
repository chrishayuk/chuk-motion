# chuk-motion/src/chuk_motion/components/layouts/StackedReaction/builder.py
"""StackedReaction composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    original_content: Any | None = None,
    reaction_content: Any | None = None,
    layout: str = "vertical",
    reaction_size: float = 40,
    gap: float = 20,
    padding: float = 40,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """Add StackedReaction to the composition."""
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="StackedReaction",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "original_content": original_content,
            "reaction_content": reaction_content,
            "layout": layout,
            "reaction_size": reaction_size,
            "gap": gap,
            "padding": padding,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
