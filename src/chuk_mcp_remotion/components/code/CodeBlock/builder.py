# chuk-mcp-remotion/src/chuk_mcp_remotion/components/code/CodeBlock/builder.py
"""CodeBlock composition builder method."""

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
    animation: str | None = None,
    show_line_numbers: bool = True,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add CodeBlock to the composition.

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
        component_type="CodeBlock",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "code": code,
            "language": language,
            "title": title,
            "variant": variant,
            "animation": animation,
            "show_line_numbers": show_line_numbers,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
