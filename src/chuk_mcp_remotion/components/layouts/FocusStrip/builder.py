# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/FocusStrip/builder.py
"""FocusStrip composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    main_content: Any | None = None,
    focus_content: Any | None = None,
    position: str = "center",
    strip_height: float = 30,
    gap: float = 20,
    padding: float = 40,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """Add FocusStrip to the composition."""
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="FocusStrip",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "main_content": main_content,
            "focus_content": focus_content,
            "position": position,
            "strip_height": strip_height,
            "gap": gap,
            "padding": padding,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
