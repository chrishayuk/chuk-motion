# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/Container/tool.py
"""Container MCP tool."""

import asyncio

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the Container tool with the MCP server."""

    @mcp.tool
    async def remotion_add_container(
        position: str | None = None,
        width: str | None = None,
        height: str | None = None,
        padding: float = 40,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add Container to the composition.

        Flexible positioning container for components

        Args:
            position: Position on screen (center, top-left, etc.)
            width: Container width
            height: Container height
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
                component = ComponentInstance(
                    component_type="Container",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "position": position,
                        "width": width,
                        "height": height,
                        "padding": padding,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="Container",
                    layout=position or "center",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
