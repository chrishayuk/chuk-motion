# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/SplitScreen/tool.py
"""SplitScreen MCP tool."""

import asyncio

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the SplitScreen tool with the MCP server."""

    @mcp.tool
    async def remotion_add_split_screen(
        orientation: str | None = None,
        layout: str | None = None,
        gap: float = 20,
        duration: float = 5.0,
        track: str = "main",
        gap_before: float | None = None,
    ) -> str:
        """
        Add SplitScreen to the composition.

        Layout component for side-by-side content

        Args:
            orientation: Orientation (horizontal, vertical)
            layout: Layout ratio (50-50, 60-40, etc.)
            gap: Gap between sections
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
                component = ComponentInstance(
                    component_type="SplitScreen",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "orientation": orientation,
                        "layout": layout,
                        "gap": gap,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                layout_desc = f"{orientation or 'horizontal'}-{layout or '50-50'}"
                return LayoutComponentResponse(
                    component="SplitScreen",
                    layout=layout_desc,
                    start_time=project_manager.current_timeline.frames_to_seconds(component.start_frame),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
