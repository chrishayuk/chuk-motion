# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/Container/builder.py
"""Container composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    position: str | None = None,
    width: str | None = None,
    height: str | None = None,
    padding: float = 40,
    content: str | None = None,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add Container to the composition.

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
        component_type="Container",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "position": position,
            "width": width,
            "height": height,
            "padding": padding,
            "content": content,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
