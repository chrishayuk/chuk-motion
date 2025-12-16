# chuk-motion/src/chuk_motion/components/layouts/Vertical/tool.py
"""Vertical MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the Vertical tool with the MCP server."""

    @mcp.tool
    async def remotion_add_vertical(
        top: str | None = None,
        bottom: str | None = None,
        layout_style: str = "top-bottom",
        top_ratio: float = 50,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
    ) -> str:
        """
        Add Vertical layout to the composition.

        9:16 optimized for Shorts/TikTok/Reels with multiple layout styles

        Args:
            top: JSON component for top section. Format: {"type": "ComponentName", "config": {...}}
                Example:
                {
                    "type": "VideoContent",
                    "config": {
                        "src": "video.mp4",
                        "muted": true
                    }
                }
            bottom: JSON component for bottom section. Same format as top
            layout_style: Layout style (top-bottom, caption-content, content-caption, split-vertical)
            top_ratio: Top section ratio (percentage)
            gap: Gap between sections
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
                bottom_parsed = json.loads(bottom) if bottom else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                top_component = parse_nested_component(top_parsed)
                bottom_component = parse_nested_component(bottom_parsed)

                # Get builder and start time
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                # Add component using builder
                builder.add_vertical(
                    start_time=start_time,
                    top=top_component,
                    bottom=bottom_component,
                    layout_style=layout_style,
                    top_ratio=top_ratio,
                    gap=gap,
                    padding=padding,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="Vertical",
                    layout=layout_style,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
