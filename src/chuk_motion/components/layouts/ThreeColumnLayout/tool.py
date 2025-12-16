# chuk-motion/src/chuk_motion/components/layouts/ThreeColumnLayout/tool.py
"""ThreeColumnLayout MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the ThreeColumnLayout tool with the MCP server."""

    @mcp.tool
    async def remotion_add_three_column_layout(
        left: str | None = None,
        center: str | None = None,
        right: str | None = None,
        left_width: float = 25,
        center_width: float = 50,
        right_width: float = 25,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
    ) -> str:
        """
        Add ThreeColumnLayout to the composition.

        Sidebar + Main + Sidebar arrangements with configurable widths.

        For video content in columns, use VideoContent component:
        Example left column with video:
        {
            "type": "VideoContent",
            "config": {
                "src": "https://example.com/video.mp4",
                "muted": true,
                "fit": "cover",
                "loop": true
            }
        }

        Args:
            left: JSON component for left column (format: {"type": "ComponentName", "config": {...}})
            center: JSON component for center column (format: {"type": "ComponentName", "config": {...}})
            right: JSON component for right column (format: {"type": "ComponentName", "config": {...}})
            left_width: Left column width (percentage)
            center_width: Center column width (percentage)
            right_width: Right column width (percentage)
            gap: Gap between columns
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
                left_parsed = json.loads(left) if left else None
                center_parsed = json.loads(center) if center else None
                right_parsed = json.loads(right) if right else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                left_component = parse_nested_component(left_parsed)
                center_component = parse_nested_component(center_parsed)
                right_component = parse_nested_component(right_parsed)

                # Get builder and start time
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                # Add component using builder
                builder.add_three_column_layout(
                    start_time=start_time,
                    left=left_component,
                    center=center_component,
                    right=right_component,
                    left_width=left_width,
                    center_width=center_width,
                    right_width=right_width,
                    gap=gap,
                    padding=padding,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="ThreeColumnLayout",
                    layout=f"{left_width}:{center_width}:{right_width}",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
