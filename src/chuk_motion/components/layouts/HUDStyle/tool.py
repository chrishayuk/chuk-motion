# chuk-motion/src/chuk_motion/components/layouts/HUDStyle/tool.py
"""HUDStyle MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


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
    ) -> str:
        """
        Add HUDStyle layout to the composition.

        Gaming/sports HUD with main content and corner overlays.

        Args:
            main_content: JSON component for main background content. Format: {"type": "ComponentName", "config": {...}}
            top_left: JSON component for top-left overlay. Same format as main_content
            top_right: JSON component for top-right overlay. Same format
            bottom_left: JSON component for bottom-left overlay. Same format
            bottom_right: JSON component for bottom-right overlay. Same format
            center: JSON component for center overlay. Same format
            overlay_size: Overlay panel size (percentage)
            gap: Gap between panels
            padding: Padding from edges
            duration: Duration in seconds or time string

        Returns:
            JSON with component info
        """

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
                # Convert nested components to ComponentInstance objects
                main_component = parse_nested_component(main_parsed)
                tl_component = parse_nested_component(tl_parsed)
                tr_component = parse_nested_component(tr_parsed)
                bl_component = parse_nested_component(bl_parsed)
                br_component = parse_nested_component(br_parsed)
                center_component = parse_nested_component(center_parsed)

                # Get builder and start time
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                # Add component using builder
                builder.add_hud_style(
                    start_time=start_time,
                    main_content=main_component,
                    top_left=tl_component,
                    top_right=tr_component,
                    bottom_left=bl_component,
                    bottom_right=br_component,
                    center=center_component,
                    overlay_size=overlay_size,
                    gap=gap,
                    padding=padding,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="HUDStyle",
                    layout="hud",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
