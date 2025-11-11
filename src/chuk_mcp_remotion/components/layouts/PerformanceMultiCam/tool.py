# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/PerformanceMultiCam/tool.py
"""PerformanceMultiCam MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse
from chuk_mcp_remotion.components.component_helpers import parse_nested_component


def register_tool(mcp, project_manager):
    """Register the PerformanceMultiCam tool with the MCP server."""

    @mcp.tool
    async def remotion_add_performance_multi_cam(
        primary_cam: str | None = None,
        secondary_cams: str | None = None,
        layout: str = "primary-main",
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """Add PerformanceMultiCam layout to the composition."""

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                primary_parsed = json.loads(primary_cam) if primary_cam else None
                secondary_parsed = json.loads(secondary_cams) if secondary_cams else []
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid JSON: {str(e)}").model_dump_json()

            # Limit to 4 secondary cameras
            if isinstance(secondary_parsed, list):
                secondary_parsed = secondary_parsed[:4]

            try:
                # Convert nested components to ComponentInstance objects
                primary_component = parse_nested_component(primary_parsed)

                # Parse array of secondary cameras
                secondary_components = []
                if isinstance(secondary_parsed, list):
                    for item in secondary_parsed:
                        comp = parse_nested_component(item)
                        if comp is not None:
                            secondary_components.append(comp)

                component = ComponentInstance(
                    component_type="PerformanceMultiCam",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "primary_cam": primary_component,
                        "secondary_cams": secondary_components,
                        "layout": layout,
                        "gap": gap,
                        "padding": padding,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="PerformanceMultiCam",
                    layout=layout,
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
