# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/FocusStrip/tool.py
"""FocusStrip MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse
from chuk_mcp_remotion.components.component_helpers import parse_nested_component


def register_tool(mcp, project_manager):
    """Register the FocusStrip tool with the MCP server."""

    @mcp.tool
    async def remotion_add_focus_strip(
        main_content: str | None = None,
        focus_content: str | None = None,
        position: str = "center",
        strip_height: float = 30,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add FocusStrip layout to the composition.

        Focused strip/banner layout for highlighting key content

        Args:
            main_content: JSON component for background
            focus_content: JSON component for focused strip
            position: Strip position (top, center, bottom)
            strip_height: Strip height (percentage)
            gap: Gap
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
                main_parsed = json.loads(main_content) if main_content else None
                focus_parsed = json.loads(focus_content) if focus_content else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                main_component = parse_nested_component(main_parsed)
                focus_component = parse_nested_component(focus_parsed)

                component = ComponentInstance(
                    component_type="FocusStrip",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "main_content": main_component,
                        "focus_content": focus_component,
                        "position": position,
                        "strip_height": strip_height,
                        "gap": gap,
                        "padding": padding,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="FocusStrip",
                    layout=position,
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
