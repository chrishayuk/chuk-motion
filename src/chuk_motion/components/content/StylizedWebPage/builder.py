# chuk-motion/src/chuk_motion/components/content/StylizedWebPage/builder.py
"""StylizedWebPage composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    title: str,
    subtitle: str,
    start_time: float,
    show_header: bool = True,
    show_sidebar: bool = False,
    show_footer: bool = False,
    header_text: str = "Navigation",
    sidebar_items: list[str] | None = None,
    content_lines: list[str] | None = None,
    footer_text: str = "© 2024 Company",
    theme: str = "light",
    accent_color: str = "primary",
    duration: float = 5.0,
) -> "CompositionBuilder":
    """Add StylizedWebPage to the composition."""
    from ....generator.composition_builder import ComponentInstance

    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    # Default values for lists
    if sidebar_items is None:
        sidebar_items = ["Dashboard", "Analytics", "Settings"]
    if content_lines is None:
        content_lines = ["Welcome to our site", "Explore our features", "Get started today"]

    component = ComponentInstance(
        component_type="StylizedWebPage",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "title": title,
            "subtitle": subtitle,
            "showHeader": show_header,
            "showSidebar": show_sidebar,
            "showFooter": show_footer,
            "headerText": header_text,
            "sidebarItems": sidebar_items,
            "contentLines": content_lines,
            "footerText": footer_text,
            "theme": theme,
            "accentColor": accent_color,
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
