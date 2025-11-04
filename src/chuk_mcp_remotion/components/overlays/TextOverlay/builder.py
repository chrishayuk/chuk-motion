# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/TextOverlay/builder.py
"""TextOverlay composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    text: str,
    start_time: float,
    style: str | None = None,
    animation: str | None = None,
    duration: float = 3.0,
    position: str | None = None,
) -> "CompositionBuilder":
    """
    Add TextOverlay to the composition.

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
        component_type="TextOverlay",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "text": text,
            "style": style,
            "animation": animation,
            "start_time": start_time,
            "duration": duration,
            "position": position,
        },
        layer=10,
    )
    builder.components.append(component)
    return builder
