# chuk-mcp-remotion/src/chuk_mcp_remotion/components/charts/DonutChart/builder.py
"""DonutChart composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    data: list,
    title: str | None = None,
    center_text: str | None = None,
    start_time: float = 0.0,
    duration: float = 4.0,
) -> "CompositionBuilder":
    """
    Add an animated donut chart to the composition.

    Args:
        builder: CompositionBuilder instance
        data: List of objects with label, value, and optional color
        title: Optional chart title
        center_text: Text to display in center
        start_time: When to show (seconds)
        duration: How long to animate (seconds)

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    component = ComponentInstance(
        component_type="DonutChart",
        start_frame=builder.seconds_to_frames(start_time),
        duration_frames=builder.seconds_to_frames(duration),
        props={
            "data": data,
            "title": title,
            "centerText": center_text,
            "start_time": start_time,
            "duration": duration,
        },
        layer=5,
    )
    builder.components.append(component)
    return builder
