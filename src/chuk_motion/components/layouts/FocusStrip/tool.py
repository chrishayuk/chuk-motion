# chuk-motion/src/chuk_motion/components/layouts/FocusStrip/tool.py
"""FocusStrip MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


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
    ) -> str:
        """
        Add FocusStrip layout to the composition.

        Focused strip/banner layout for highlighting key content

        Args:
            main_content: JSON component for background. Format: {"type": "ComponentName", "config": {...}}
            focus_content: JSON component for focused strip. Same format as main_content
            position: Strip position (top, center, bottom)
            strip_height: Strip height (percentage)
            gap: Gap
            padding: Padding from edges
            duration: Duration in seconds

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

                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                builder.add_focus_strip(
                    start_time=start_time,
                    main_content=main_component,
                    focus_content=focus_component,
                    position=position,
                    strip_height=strip_height,
                    gap=gap,
                    padding=padding,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="FocusStrip",
                    layout=position,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
