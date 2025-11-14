"""PixelTransition composition builder method."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    first_content: Any | None = None,
    second_content: Any | None = None,
    grid_size: int = 10,
    pixel_color: str | None = None,
    transition_start: float = 2.0,
    transition_duration: float = 1.0,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add PixelTransition to the composition.

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    # Calculate frames if time-based props exist
    start_frame = builder.seconds_to_frames(locals().get("start_time", 0.0))
    duration_frames = builder.seconds_to_frames(
        locals().get("duration_seconds") or locals().get("duration", 5.0)
    )

    props = {
        "firstContent": first_content,
        "secondContent": second_content,
        "gridSize": grid_size,
        "transitionStart": int(transition_start * builder.fps),  # Convert to frames
        "transitionDuration": int(transition_duration * builder.fps),  # Convert to frames
        "start_time": start_time,
        "duration": duration,
    }

    if pixel_color is not None:
        props["pixelColor"] = pixel_color

    component = ComponentInstance(
        component_type="PixelTransition",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props=props,
        layer=0,
    )
    builder.components.append(component)
    return builder
