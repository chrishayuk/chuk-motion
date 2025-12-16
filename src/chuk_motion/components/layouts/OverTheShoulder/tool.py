# chuk-motion/src/chuk_motion/components/layouts/OverTheShoulder/tool.py
"""OverTheShoulder MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


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
    ) -> str:
        """
        Add OverTheShoulder layout to the composition.

        Screen recording with presenter overlay in corner (tutorial style).

        Args:
            screen_content: JSON component for main screen content. Format: {"type": "ComponentName", "config": {...}}
            shoulder_overlay: JSON component for presenter overlay. Same format as screen_content
            overlay_position: Presenter position (bottom-left, bottom-right, etc.)
            overlay_size: Presenter overlay size (percentage)
            gap: Gap between elements
            padding: Padding from edges
            duration: Duration in seconds or time string

        Returns:
            JSON with component info
        """

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

                # Get builder and start time
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                # Add component using builder
                builder.add_over_the_shoulder(
                    start_time=start_time,
                    screen_content=screen_component,
                    shoulder_overlay=shoulder_component,
                    overlay_position=overlay_position,
                    overlay_size=overlay_size,
                    gap=gap,
                    padding=padding,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="OverTheShoulder",
                    layout=overlay_position,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
