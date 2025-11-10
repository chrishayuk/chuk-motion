"""Composition builder method for DeviceFrame component."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    duration: float,
    device: str = "phone",
    content: str = "",
    orientation: str = "portrait",
    scale: float = 1.0,
    glare: bool = True,
    shadow: bool = True,
    position: str = "center",
) -> "CompositionBuilder":
    """Add a DeviceFrame component to the composition.

    Args:
        builder: The composition builder instance
        start_time: Start time in seconds
        duration: Duration in seconds
        device: Type of device frame (phone, tablet, laptop)
        content: Content to display inside the device
        orientation: Device orientation (portrait, landscape)
        scale: Auto-scale factor (0.1 to 2.0)
        glare: Enable realistic screen glare effect
        shadow: Enable device shadow
        position: Position of device on screen

    Returns:
        The builder instance for method chaining
    """
    from chuk_mcp_remotion.generator.composition_builder import ComponentInstance

    # Convert time to frames
    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="DeviceFrame",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "device": device,
            "content": content,
            "orientation": orientation,
            "scale": scale,
            "glare": glare,
            "shadow": shadow,
            "position": position,
            "start_time": start_time,
            "duration": duration,
        },
        layer=5,
    )
    builder.components.append(component)
    return builder
