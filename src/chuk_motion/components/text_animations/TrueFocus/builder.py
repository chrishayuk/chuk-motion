"""TrueFocus composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    text: str,
    font_size: str = "3xl",
    font_weight: str = "black",
    text_color: str | None = None,
    frame_color: str | None = None,
    glow_color: str | None = None,
    blur_amount: float = 5.0,
    word_duration: float = 1.0,
    position: str = "center",
    duration: float = 3.0,
) -> "CompositionBuilder":
    """
    Add TrueFocus to the composition.

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
        "blurAmount": blur_amount,
        "wordDuration": word_duration,
        "position": position,
        "start_time": start_time,
        "duration": duration,
    }

    if text_color is not None:
        props["textColor"] = text_color

    if frame_color is not None:
        props["frameColor"] = frame_color

    if glow_color is not None:
        props["glowColor"] = glow_color

    component = ComponentInstance(
        component_type="TrueFocus",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props=props,
        layer=0,
    )
    builder.components.append(component)
    return builder
