"""Composition builder method for CodeDiff component."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chuk_motion.generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    start_time: float,
    duration: float,
    lines: str = "[]",
    mode: str = "unified",
    language: str = "typescript",
    show_line_numbers: bool = True,
    show_heatmap: bool = False,
    title: str = "Code Comparison",
    left_label: str = "Before",
    right_label: str = "After",
    theme: str = "dark",
    width: int = 1400,
    height: int = 800,
    position: str = "center",
    animate_lines: bool = True,
) -> "CompositionBuilder":
    """Add a CodeDiff component to the composition.

    Args:
        builder: The composition builder instance
        start_time: Start time in seconds
        duration: Duration in seconds
        lines: JSON string of diff lines
        mode: Diff display mode (unified or split)
        language: Programming language for syntax highlighting
        show_line_numbers: Show line numbers
        show_heatmap: Show heatmap visualization
        title: Title for the diff viewer
        left_label: Label for left side (split mode)
        right_label: Label for right side (split mode)
        theme: Color theme
        width: Diff viewer width
        height: Diff viewer height
        position: Position of diff viewer on screen
        animate_lines: Animate lines appearing

    Returns:
        The builder instance for method chaining
    """
    from chuk_motion.generator.composition_builder import ComponentInstance

    # Convert time to frames
    start_frame = builder.seconds_to_frames(start_time)
    duration_frames = builder.seconds_to_frames(duration)

    component = ComponentInstance(
        component_type="CodeDiff",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "lines": lines,
            "mode": mode,
            "language": language,
            "showLineNumbers": show_line_numbers,
            "showHeatmap": show_heatmap,
            "title": title,
            "leftLabel": left_label,
            "rightLabel": right_label,
            "theme": theme,
            "width": width,
            "height": height,
            "position": position,
            "animateLines": animate_lines,
            "start_time": start_time,
            "duration": duration,
        },
        layer=5,
    )
    builder.components.append(component)
    return builder
