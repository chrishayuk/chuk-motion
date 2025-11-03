# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/EndScreen/builder.py
"""EndScreen composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    cta_text: str,
    thumbnail_url: str | None = None,
    variant: str | None = None,
    duration_seconds: float = 10.0,
) -> "CompositionBuilder":
    """
    Add EndScreen to the composition.

    Automatically places end screen after all existing components.

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    # Auto-calculate start time: place after all existing components
    start_time = builder.get_total_duration_seconds()

    # Calculate frames
    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration_seconds)

    component = ComponentInstance(
        component_type="EndScreen",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "cta_text": cta_text,
            "thumbnail_url": thumbnail_url,
            "variant": variant,
            "duration_seconds": duration_seconds,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
