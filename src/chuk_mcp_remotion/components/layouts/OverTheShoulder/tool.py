# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/OverTheShoulder/tool.py
"""OverTheShoulder MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse
from chuk_mcp_remotion.components.component_helpers import parse_nested_component


def register_tool(mcp, project_manager):
    """Register the OverTheShoulder tool with the MCP server."""

    @mcp.tool
    async def remotion_add_over_the_shoulder(
        screen_content: str | None = None,
        shoulder_overlay: str | None = None,
        overlay_position: str = "bottom-left",
        overlay_size: float = 30,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """Add OverTheShoulder layout to the composition."""

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                screen_parsed = json.loads(screen_content) if screen_content else None
                shoulder_parsed = json.loads(shoulder_overlay) if shoulder_overlay else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                screen_component = parse_nested_component(screen_parsed)
                shoulder_component = parse_nested_component(shoulder_parsed)

                component = ComponentInstance(
                    component_type="OverTheShoulder",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "screen_content": screen_component,
                        "shoulder_overlay": shoulder_component,
                        "overlay_position": overlay_position,
                        "overlay_size": overlay_size,
                        "gap": gap,
                        "padding": padding,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="OverTheShoulder",
                    layout=overlay_position,
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
