# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/Grid/tool.py
"""Grid MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the Grid tool with the MCP server."""

    @mcp.tool
    async def remotion_add_grid(
        items: str,
        layout: str | None = None,
        gap: float = 20,
        padding: float = 40,
        duration: float = 5.0,
        track: str = "main",
        gap_before: float | None = None,
    ) -> str:
        """
        Add Grid to the composition.

        Grid layout for multiple items

        Args:
            items: JSON array of grid items
            layout: Grid layout (2x2, 3x3, etc.)
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

            try:
                component = ComponentInstance(
                    component_type="Grid",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "layout": layout,
                        "gap": gap,
                        "padding": padding,
                        "items": items_parsed,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="Grid",
                    layout=layout or "2x2",
                    start_time=project_manager.current_timeline.frames_to_seconds(component.start_frame),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
