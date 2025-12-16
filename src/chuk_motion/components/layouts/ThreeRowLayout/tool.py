# chuk-motion/src/chuk_motion/components/layouts/ThreeRowLayout/tool.py
"""ThreeRowLayout MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the ThreeRowLayout tool with the MCP server."""

    @mcp.tool
    async def remotion_add_three_row_layout(
        top: str | None = None,
        middle: str | None = None,
        bottom: str | None = None,
        top_height: float = 25,
        middle_height: float = 50,
        bottom_height: float = 25,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
    ) -> str:
        """
        Add ThreeRowLayout to the composition.

        Header + Main + Footer arrangements with configurable heights.

        Args:
            top: JSON component for top row. Format: {"type": "ComponentName", "config": {...}}
                Example with video:
                {
                    "type": "VideoContent",
                    "config": {
                        "src": "https://example.com/video.mp4",
                        "muted": true,
                        "fit": "cover"
                    }
                }
            middle: JSON component for middle row. Same format as top
            bottom: JSON component for bottom row. Same format as top
            top_height: Top row height (percentage)
            middle_height: Middle row height (percentage)
            bottom_height: Bottom row height (percentage)
            gap: Gap between rows
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
                top_parsed = json.loads(top) if top else None
                middle_parsed = json.loads(middle) if middle else None
                bottom_parsed = json.loads(bottom) if bottom else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                top_component = parse_nested_component(top_parsed)
                middle_component = parse_nested_component(middle_parsed)
                bottom_component = parse_nested_component(bottom_parsed)

                # Get builder and start time
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                # Add component using builder
                builder.add_three_row_layout(
                    start_time=start_time,
                    top=top_component,
                    middle=middle_component,
                    bottom=bottom_component,
                    top_height=top_height,
                    middle_height=middle_height,
                    bottom_height=bottom_height,
                    gap=gap,
                    padding=padding,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="ThreeRowLayout",
                    layout=f"{top_height}:{middle_height}:{bottom_height}",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
