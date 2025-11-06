# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/PiP/builder.py
"""PiP composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    main_content: Any | None = None,
    pip_content: Any | None = None,
    position: str = "bottom-right",
    overlay_size: float = 20,
    margin: float = 40,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add PiP to the composition.

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="PiP",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "main_content": main_content,
            "pip_content": pip_content,
            "position": position,
            "overlay_size": overlay_size,
            "margin": margin,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
