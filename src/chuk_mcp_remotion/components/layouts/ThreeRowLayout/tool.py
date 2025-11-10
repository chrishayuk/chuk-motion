# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/ThreeRowLayout/tool.py
"""ThreeRowLayout MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the ThreeRowLayout tool with the MCP server."""

    @mcp.tool
    async def remotion_add_three_row_layout(
        top: str | None = None,
        middle: str | None = None,
        bottom: str | None = None,
        top_height: float = 25,
        middle_height: float = 50,
        bottom_height: float = 25,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add ThreeRowLayout to the composition.

        Header + Main + Footer arrangements with configurable heights

        Args:
            top: JSON component for top row
            middle: JSON component for middle row
            bottom: JSON component for bottom row
            top_height: Top row height (percentage)
            middle_height: Middle row height (percentage)
            bottom_height: Bottom row height (percentage)
            gap: Gap between rows
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
                top_parsed = json.loads(top) if top else None
                middle_parsed = json.loads(middle) if middle else None
                bottom_parsed = json.loads(bottom) if bottom else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                component = ComponentInstance(
                    component_type="ThreeRowLayout",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "top": top_parsed,
                        "middle": middle_parsed,
                        "bottom": bottom_parsed,
                        "top_height": top_height,
                        "middle_height": middle_height,
                        "bottom_height": bottom_height,
                        "gap": gap,
                        "padding": padding,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="ThreeRowLayout",
                    layout=f"{top_height}:{middle_height}:{bottom_height}",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
