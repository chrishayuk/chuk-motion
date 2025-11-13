"""LayoutEntrance composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    content: str | None = None,
    entrance_type: str = "fade_in",
    entrance_delay: float = 0.0,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add LayoutEntrance to the composition.

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    # Calculate frames if time-based props exist
    start_frame = builder.seconds_to_frames(locals().get("start_time", 0.0))
    duration_frames = builder.seconds_to_frames(
        locals().get("duration_seconds") or locals().get("duration", 5.0)
    )

    component = ComponentInstance(
        component_type="LayoutEntrance",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "content": content,
            "entrance_type": entrance_type,
            "entrance_delay": entrance_delay,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
