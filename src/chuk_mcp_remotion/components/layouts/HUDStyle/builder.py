# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/HUDStyle/builder.py
"""HUDStyle composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    main_content: Any | None = None,
    top_left: Any | None = None,
    top_right: Any | None = None,
    bottom_left: Any | None = None,
    bottom_right: Any | None = None,
    center: Any | None = None,
    overlay_size: float = 15,
    gap: float = 20,
    padding: float = 40,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """Add HUDStyle to the composition."""
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="HUDStyle",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "main_content": main_content,
            "top_left": top_left,
            "top_right": top_right,
            "bottom_left": bottom_left,
            "bottom_right": bottom_right,
            "center": center,
            "overlay_size": overlay_size,
            "gap": gap,
            "padding": padding,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
