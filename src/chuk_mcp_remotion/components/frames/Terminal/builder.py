"""Composition builder method for Terminal component."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    duration: float,
    commands: str = "[]",
    prompt: str = "bash",
    custom_prompt: str = "$",
    title: str = "Terminal",
    theme: str = "dark",
    width: int = 900,
    height: int = 600,
    position: str = "center",
    show_cursor: bool = True,
    type_speed: float = 0.05,
) -> "CompositionBuilder":
    """Add a Terminal component to the composition.

    Args:
        builder: The composition builder instance
        start_time: Start time in seconds
        duration: Duration in seconds
        commands: JSON string of command blocks
        prompt: Terminal prompt style
        custom_prompt: Custom prompt string
        title: Terminal window title
        theme: Terminal color theme
        width: Terminal window width
        height: Terminal window height
        position: Position of terminal window on screen
        show_cursor: Show blinking cursor
        type_speed: Typing animation speed

    Returns:
        The builder instance for method chaining
    """
    from chuk_mcp_remotion.generator.composition_builder import ComponentInstance

    # Convert time to frames
    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="Terminal",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "commands": commands,
            "prompt": prompt,
            "customPrompt": custom_prompt,
            "title": title,
            "theme": theme,
            "width": width,
            "height": height,
            "position": position,
            "showCursor": show_cursor,
            "typeSpeed": type_speed,
            "start_time": start_time,
            "duration": duration,
        },
        layer=5,
    )
    builder.components.append(component)
    return builder
