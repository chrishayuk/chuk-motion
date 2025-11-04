# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/LowerThird/tool.py
"""LowerThird MCP tool."""

import asyncio

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, OverlayComponentResponse


def register_tool(mcp, project_manager):
    """Register the LowerThird tool with the MCP server."""

    @mcp.tool
    async def remotion_add_lower_third(
        name: str,
        title: str | None = None,
        variant: str | None = None,
        position: str | None = None,
        duration: float | str = 5.0,
        track: str = "overlay",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add LowerThird to the composition.

        Name plate overlay with title and subtitle (like TV graphics)

        Args:
            name: Person's name to display
            title: Optional title/role to display
            variant: Style variant
            position: Position on screen
            duration: Duration in seconds
            track: Track name (default: "overlay")
            gap_before: Gap before component in seconds (overrides track default)

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
                    component_type="LowerThird",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "name": name,
                        "title": title,
                        "variant": variant,
                        "position": position,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return OverlayComponentResponse(
                    component="LowerThird",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
