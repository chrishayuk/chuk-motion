# chuk-motion/src/chuk_motion/components/layouts/SplitScreen/tool.py
"""SplitScreen MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the SplitScreen tool with the MCP server."""

    @mcp.tool
    async def remotion_add_split_screen(
        left_content: str | None = None,
        right_content: str | None = None,
        orientation: str | None = None,
        layout: str | None = None,
        gap: float = 20,
        duration: float | str = 5.0,
    ) -> str:
        """
        Add SplitScreen to the composition.

        Layout component for side-by-side or top-bottom content.

        Args:
            left_content: JSON component for left panel. Format: {"type": "ComponentName", "config": {...}}
            right_content: JSON component for right panel. Same format as left_content
            orientation: Orientation (horizontal or vertical)
            layout: Layout style
            gap: Gap between sections
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
                left_parsed = json.loads(left_content) if left_content else None
                right_parsed = json.loads(right_content) if right_content else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                left_component = parse_nested_component(left_parsed)
                right_component = parse_nested_component(right_parsed)

                # Get builder and start time
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                # Add component using builder
                builder.add_split_screen(
                    start_time=start_time,
                    orientation=orientation,
                    layout=layout,
                    gap=gap,
                    left_content=left_component,
                    right_content=right_component,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="SplitScreen",
                    layout=layout or orientation or "horizontal",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
