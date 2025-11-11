# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/AsymmetricLayout/tool.py
"""AsymmetricLayout MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse
from chuk_mcp_remotion.components.component_helpers import parse_nested_component


def register_tool(mcp, project_manager):
    """Register the AsymmetricLayout tool with the MCP server."""

    @mcp.tool
    async def remotion_add_asymmetric_layout(
        main: str | None = None,
        top_side: str | None = None,
        bottom_side: str | None = None,
        layout: str = "main-left",
        main_ratio: float = 66.67,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add AsymmetricLayout to the composition.

        Main feed (2/3) + two demo panels (1/3 stacked) - perfect for tutorials

        Args:
            main: JSON component for main content
            top_side: JSON component for top sidebar
            bottom_side: JSON component for bottom sidebar
            layout: Layout variant (main-left or main-right)
            main_ratio: Main content width (percentage)
            gap: Gap between panels
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
                main_parsed = json.loads(main) if main else None
                top_side_parsed = json.loads(top_side) if top_side else None
                bottom_side_parsed = json.loads(bottom_side) if bottom_side else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                main_component = parse_nested_component(main_parsed)
                top_side_component = parse_nested_component(top_side_parsed)
                bottom_side_component = parse_nested_component(bottom_side_parsed)

                component = ComponentInstance(
                    component_type="AsymmetricLayout",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "main": main_component,
                        "top_side": top_side_component,
                        "bottom_side": bottom_side_component,
                        "layout": layout,
                        "main_ratio": main_ratio,
                        "gap": gap,
                        "padding": padding,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="AsymmetricLayout",
                    layout=layout,
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
