# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/ThreeByThreeGrid/tool.py
"""ThreeByThreeGrid MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.components.component_helpers import parse_nested_component
from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the ThreeByThreeGrid tool with the MCP server."""

    @mcp.tool
    async def remotion_add_three_by_three_grid(
        items: str,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add ThreeByThreeGrid to the composition.

        Perfect 3x3 grid layout (9 cells)

        Args:
            items: JSON array of up to 9 grid items. Format: [{"type": "ComponentName", "config": {...}}, ...]
            gap: Gap between grid items
            padding: Padding from edges
            duration: Duration in seconds
            track: Track name (default: "main")
            gap_before: Gap before component in seconds

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                items_parsed = json.loads(items)
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid items JSON: {str(e)}").model_dump_json()

            # Limit to 9 items
            items_parsed = items_parsed[:9]

            try:
                # Convert array of item dicts to ComponentInstance objects
                children_components = []
                if isinstance(items_parsed, list):
                    for item in items_parsed:
                        child = parse_nested_component(item)
                        if child is not None:
                            children_components.append(child)

                component = ComponentInstance(
                    component_type="ThreeByThreeGrid",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "gap": gap,
                        "padding": padding,
                        "children": children_components,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="ThreeByThreeGrid",
                    layout="3x3",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
