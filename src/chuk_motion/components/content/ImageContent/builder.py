"""ImageContent composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    src: str,
    fit: str = "cover",
    opacity: float = 1.0,
    border_radius: int = 0,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add ImageContent to the composition.

    Args:
        builder: CompositionBuilder instance
        start_time: When to show the image (seconds)
        src: Image source URL or path to static file (e.g. 'image.png')
        fit: How image fits in container ("contain", "cover", or "fill")
        opacity: Image opacity (0.0 to 1.0)
        border_radius: Border radius in pixels
        duration: Total duration (seconds)

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    # Calculate frames
    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    props = {
        "src": src,
        "fit": fit,
        "opacity": opacity,
        "borderRadius": border_radius,
        "start_time": start_time,
        "duration": duration,
    }

    from .schema import METADATA

    component = ComponentInstance(
        component_type=METADATA.name,
        start_frame=start_frame,
        duration_frames=duration_frames,
        props=props,
        layer=0,
    )
    builder.components.append(component)
    return builder
