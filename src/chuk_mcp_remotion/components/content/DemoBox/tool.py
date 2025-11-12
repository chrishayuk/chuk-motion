# chuk-mcp-remotion/src/chuk_mcp_remotion/components/content/DemoBox/tool.py
"""DemoBox MCP tool."""

import asyncio

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the DemoBox tool with the MCP server."""

    @mcp.tool
    async def remotion_add_demo_box(
        label: str,
        color: str = "primary",
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add DemoBox to the composition.

        Colored box component for demonstrations and placeholders.

        Args:
            label: Text label to display in the box
            color: Color variant (primary, secondary, etc.)
            duration: Duration in seconds or time string (e.g., "2s", "500ms")
            track: Track name (default: "main")
            gap_before: Gap before component in seconds or time string

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                component = ComponentInstance(
                    component_type="DemoBox",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "label": label,
                        "color": color,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return ComponentResponse(
                    component="DemoBox",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
