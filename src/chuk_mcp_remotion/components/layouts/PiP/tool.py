# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/PiP/tool.py
"""PiP MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.components.component_helpers import parse_nested_component
from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the PiP tool with the MCP server."""

    @mcp.tool
    async def remotion_add_pip(
        main_content: str | None = None,
        pip_content: str | None = None,
        position: str = "bottom-right",
        overlay_size: float = 20,
        margin: float = 40,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add PiP (Picture-in-Picture) to the composition.

        Picture-in-Picture webcam overlay with customizable positions

        Args:
            main_content: JSON component for main background. Format: {"type": "ComponentName", "config": {...}}
            pip_content: JSON component for PiP overlay. Same format as main_content
            position: Overlay position (bottom-right, bottom-left, top-right, top-left)
            overlay_size: Overlay size (percentage of screen)
            margin: Margin from edges
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
                pip_parsed = json.loads(pip_content) if pip_content else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                main_component = parse_nested_component(main_parsed)
                pip_component = parse_nested_component(pip_parsed)

                component = ComponentInstance(
                    component_type="PiP",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "mainContent": main_component,
                        "pipContent": pip_component,
                        "position": position,
                        "overlay_size": overlay_size,
                        "margin": margin,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="PiP",
                    layout=position,
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
