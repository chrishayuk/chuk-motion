# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/HUDStyle/tool.py
"""HUDStyle MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the HUDStyle tool with the MCP server."""

    @mcp.tool
    async def remotion_add_hud_style(
        main_content: str | None = None,
        top_left: str | None = None,
        top_right: str | None = None,
        bottom_left: str | None = None,
        bottom_right: str | None = None,
        center: str | None = None,
        overlay_size: float = 15,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """Add HUDStyle layout to the composition."""

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                main_parsed = json.loads(main_content) if main_content else None
                tl_parsed = json.loads(top_left) if top_left else None
                tr_parsed = json.loads(top_right) if top_right else None
                bl_parsed = json.loads(bottom_left) if bottom_left else None
                br_parsed = json.loads(bottom_right) if bottom_right else None
                center_parsed = json.loads(center) if center else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid JSON: {str(e)}").model_dump_json()

            try:
                component = ComponentInstance(
                    component_type="HUDStyle",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "main_content": main_parsed,
                        "top_left": tl_parsed,
                        "top_right": tr_parsed,
                        "bottom_left": bl_parsed,
                        "bottom_right": br_parsed,
                        "center": center_parsed,
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
                    component="HUDStyle",
                    layout="hud",
                    start_time=project_manager.current_timeline.frames_to_seconds(component.start_frame),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
