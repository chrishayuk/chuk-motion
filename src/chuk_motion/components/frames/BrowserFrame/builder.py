"""Composition builder method for BrowserFrame component."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chuk_motion.generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    duration: float,
    url: str = "https://example.com",
    theme: str = "chrome",
    tabs: str | None = None,
    show_status: bool = False,
    status_text: str = "",
    content: str = "",
    width: int = 1200,
    height: int = 800,
    position: str = "center",
    shadow: bool = True,
) -> "CompositionBuilder":
    """Add a BrowserFrame component to the composition.

    Args:
        builder: The composition builder instance
        start_time: Start time in seconds
        duration: Duration in seconds
        url: URL to display in the address bar
        theme: Browser theme (light, dark, chrome, firefox, safari, arc)
        tabs: JSON string of tabs to display
        show_status: Show status bar at bottom
        status_text: Status bar text
        content: Content to display in browser window
        width: Browser window width
        height: Browser window height
        position: Position of browser window on screen
        shadow: Enable window shadow

    Returns:
        The builder instance for method chaining
    """
    from chuk_motion.generator.composition_builder import ComponentInstance

    # Convert time to frames
    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="BrowserFrame",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "url": url,
            "theme": theme,
            "tabs": tabs,
            "showStatus": show_status,
            "statusText": status_text,
            "content": content,
            "width": width,
            "height": height,
            "position": position,
            "shadow": shadow,
            "start_time": start_time,
            "duration": duration,
        },
        layer=5,
    )
    builder.components.append(component)
    return builder
