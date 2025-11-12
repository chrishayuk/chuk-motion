# chuk-motion/src/chuk_motion/components/layouts/AsymmetricLayout/builder.py
"""AsymmetricLayout composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    main: Any | None = None,
    top_side: Any | None = None,
    bottom_side: Any | None = None,
    layout: str = "main-left",
    main_ratio: float = 66.67,
    gap: float = 20,
    padding: float = 40,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add AsymmetricLayout to the composition.

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="AsymmetricLayout",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "main": main,
            "top_side": top_side,
            "bottom_side": bottom_side,
            "layout": layout,
            "main_ratio": main_ratio,
            "gap": gap,
            "padding": padding,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
