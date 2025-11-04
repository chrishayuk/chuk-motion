# chuk-mcp-remotion/src/chuk_mcp_remotion/components/charts/HorizontalBarChart/builder.py
"""HorizontalBarChart composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    data: list,
    title: str | None = None,
    xlabel: str | None = None,
    start_time: float = 0.0,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add an animated horizontalbar chart to the composition.

    Args:
        builder: CompositionBuilder instance
        data: List of objects with label, value, and optional color
        title: Optional chart title
        xlabel: Optional x-axis label
        start_time: When to show (seconds)
        duration: How long to animate (seconds)

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    component = ComponentInstance(
        component_type="HorizontalBarChart",
        start_frame=builder.seconds_to_frames(start_time),
        duration_frames=builder.seconds_to_frames(duration),
        props={
            "data": data,
            "title": title,
            "xlabel": xlabel,
            "start_time": start_time,
            "duration": duration,
        },
        layer=5,
    )
    builder.components.append(component)
    return builder
