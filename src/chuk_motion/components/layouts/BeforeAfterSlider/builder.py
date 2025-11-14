"""Composition builder method for BeforeAfterSlider component."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chuk_motion.generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    duration: float,
    before_image: str,
    after_image: str,
    before_label: str = "Before",
    after_label: str = "After",
    orientation: str = "horizontal",
    slider_position: float = 50.0,
    animate_slider: bool = True,
    slider_start_position: float = 0.0,
    slider_end_position: float = 100.0,
    show_labels: bool = True,
    label_position: str = "overlay",
    handle_style: str = "default",
    width: int = 1200,
    height: int = 800,
    position: str = "center",
    border_radius: int = 12,
) -> "CompositionBuilder":
    """Add a BeforeAfterSlider component to the composition.

    Args:
        builder: The composition builder instance
        start_time: Start time in seconds
        duration: Duration in seconds
        before_image: Path to the 'before' image
        after_image: Path to the 'after' image
        before_label: Label for the 'before' state
        after_label: Label for the 'after' state
        orientation: Slider orientation (horizontal or vertical)
        slider_position: Initial slider position (0-100)
        animate_slider: Animate slider movement
        slider_start_position: Starting position for animation (0-100)
        slider_end_position: Ending position for animation (0-100)
        show_labels: Show before/after labels
        label_position: Position of labels (top, bottom, overlay)
        handle_style: Style of the slider handle
        width: Component width
        height: Component height
        position: Position on screen
        border_radius: Border radius

    Returns:
        The builder instance for method chaining
    """
    from chuk_motion.generator.composition_builder import ComponentInstance

    # Convert time to frames
    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="BeforeAfterSlider",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "beforeImage": before_image,
            "afterImage": after_image,
            "beforeLabel": before_label,
            "afterLabel": after_label,
            "orientation": orientation,
            "sliderPosition": slider_position,
            "animateSlider": animate_slider,
            "sliderStartPosition": slider_start_position,
            "sliderEndPosition": slider_end_position,
            "showLabels": show_labels,
            "labelPosition": label_position,
            "handleStyle": handle_style,
            "width": width,
            "height": height,
            "position": position,
            "borderRadius": border_radius,
            "start_time": start_time,
            "duration": duration,
        },
        layer=5,
    )
    builder.components.append(component)
    return builder
