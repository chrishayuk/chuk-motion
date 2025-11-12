# chuk-mcp-remotion/src/chuk_mcp_remotion/components/content/WebPage/builder.py
"""WebPage composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    html: str,
    start_time: float,
    css: str = "",
    base_styles: bool = True,
    scale: float = 1.0,
    scroll_y: float = 0,
    animate_scroll: bool = False,
    scroll_duration: float = 60,
    theme: str = "light",
    duration: float = 5.0,
) -> "CompositionBuilder":
    """Add WebPage to the composition."""
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="WebPage",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "html": html,
            "css": css,
            "baseStyles": base_styles,
            "scale": scale,
            "scrollY": scroll_y,
            "animateScroll": animate_scroll,
            "scrollDuration": scroll_duration,
            "theme": theme,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
