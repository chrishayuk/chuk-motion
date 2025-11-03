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
