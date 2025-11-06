# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/Mosaic/tool.py
"""Mosaic MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the Mosaic tool with the MCP server."""

    @mcp.tool
    async def remotion_add_mosaic(
        clips: str | None = None,
        style: str = "hero-corners",
        gap: float = 10,
        padding: float = 40,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """Add Mosaic layout to the composition."""

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                clips_parsed = json.loads(clips) if clips else []
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid JSON: {str(e)}").model_dump_json()

            try:
                component = ComponentInstance(
                    component_type="Mosaic",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "clips": clips_parsed,
                        "style": style,
                        "gap": gap,
                        "padding": padding,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="Mosaic",
                    layout=style,
                    start_time=project_manager.current_timeline.frames_to_seconds(component.start_frame),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
