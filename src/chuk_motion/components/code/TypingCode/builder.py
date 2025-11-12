# chuk-motion/src/chuk_motion/components/code/TypingCode/builder.py
"""TypingCode composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    code: str,
    start_time: float,
    language: str | None = None,
    title: str | None = None,
    variant: str | None = None,
    cursor_style: str | None = None,
    typing_speed: str | None = None,
    show_line_numbers: bool = True,
    duration: float = 10.0,
) -> "CompositionBuilder":
    """
    Add TypingCode to the composition.

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
        component_type="TypingCode",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "code": code,
            "language": language,
            "title": title,
            "variant": variant,
            "cursor_style": cursor_style,
            "typing_speed": typing_speed,
            "show_line_numbers": show_line_numbers,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
