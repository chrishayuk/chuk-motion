# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/ThreeByThreeGrid/builder.py
"""ThreeByThreeGrid composition builder method."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.composition_builder import CompositionBuilder


def add_to_composition(
    builder: "CompositionBuilder",
    items: list,
    start_time: float,
    gap: float = 20,
    padding: float = 40,
    duration: float = 5.0,
) -> "CompositionBuilder":
    """
    Add ThreeByThreeGrid to the composition.

    Returns:
        CompositionBuilder instance for chaining
    """
    from ....generator.composition_builder import ComponentInstance

    # Calculate frames if time-based props exist
    start_frame = builder.seconds_to_frames(locals().get("start_time", 0.0))
    duration_frames = builder.seconds_to_frames(
        locals().get("duration_seconds") or locals().get("duration", 3.0)
    )

    component = ComponentInstance(
        component_type="ThreeByThreeGrid",
        start_frame=start_frame,
        duration_frames=duration_frames,
        props={
            "gap": gap,
            "padding": padding,
            "items": items[:9],  # Limit to 9 items
            "start_time": start_time,
            "duration": duration,
        },
        layer=0,
    )
    builder.components.append(component)
    return builder
