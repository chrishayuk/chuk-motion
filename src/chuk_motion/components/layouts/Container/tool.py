# chuk-motion/src/chuk_motion/components/layouts/Container/tool.py
"""Container MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the Container tool with the MCP server."""

    @mcp.tool
    async def remotion_add_container(
        content: str | None = None,
        position: str | None = None,
        width: str | None = None,
        height: str | None = None,
        padding: float = 40,
        duration: float | str = 5.0,
    ) -> str:
        """
        Add Container to the composition.

        Flexible positioning container for components.

        Args:
            content: JSON component to display in container. Format: {"type": "ComponentName", "config": {...}}
                Example with video:
                {
                    "type": "VideoContent",
                    "config": {
                        "src": "https://example.com/video.mp4",
                        "muted": true,
                        "fit": "cover",
                        "loop": true
                    }
                }
            position: Position on screen (center, top-left, etc.)
            width: Container width
            height: Container height
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
                content_parsed = json.loads(content) if content else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid content JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested component to ComponentInstance object
                content_component = parse_nested_component(content_parsed)

                # Get builder and start time
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                # Add component using builder
                builder.add_container(
                    start_time=start_time,
                    position=position,
                    width=width,
                    height=height,
                    padding=padding,
                    content=content_component,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="Container",
                    layout=position or "center",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
