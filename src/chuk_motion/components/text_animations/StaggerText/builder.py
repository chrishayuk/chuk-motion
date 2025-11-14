"""StaggerText composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    text: str,
    font_size: str = "3xl",
    font_weight: str = "bold",
    text_color: str | None = None,
    stagger_by: str = "char",
    stagger_delay: float = 2.0,
    animation_type: str = "fade",
    position: str = "center",
    align: str = "center",
    duration: float = 3.0,
) -> "CompositionBuilder":
    """
    Add StaggerText to the composition.

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    # Calculate frames if time-based props exist
    start_frame = builder.seconds_to_frames(locals().get("start_time", 0.0))
    duration_frames = builder.seconds_to_frames(
        locals().get("duration_seconds") or locals().get("duration", 3.0)
    )

    props = {
        "text": text,
        "fontSize": font_size,
        "fontWeight": font_weight,
        "staggerBy": stagger_by,
        "staggerDelay": stagger_delay,
        "animationType": animation_type,
        "position": position,
        "align": align,
        "start_time": start_time,
        "duration": duration,
    }

    if text_color is not None:
        props["textColor"] = text_color

    component = ComponentInstance(
        component_type="StaggerText",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props=props,
        layer=0,
    )
    builder.components.append(component)
    return builder
