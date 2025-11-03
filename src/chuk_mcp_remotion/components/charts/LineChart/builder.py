# chuk-mcp-remotion/src/chuk_mcp_remotion/components/charts/LineChart/builder.py
"""LineChart composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    data: list,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    start_time: float = 0.0,
    duration: float = 4.0,
) -> "CompositionBuilder":
    """
    Add an animated line chart to the composition.

    Args:
        builder: CompositionBuilder instance
        data: List of [x, y] data points
        title: Optional chart title
        xlabel: Optional x-axis label
        ylabel: Optional y-axis label
        start_time: When to show (seconds)
        duration: How long to animate (seconds)

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    component = ComponentInstance(
        component_type="LineChart",
        start_frame=builder.seconds_to_frames(start_time),
        duration_frames=builder.seconds_to_frames(duration),
        props={"data": data, "title": title, "xlabel": xlabel, "ylabel": ylabel},
        layer=5,  # Charts render above main content but below overlays
    )
    builder.components.append(component)
    return builder
