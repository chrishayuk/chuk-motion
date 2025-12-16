# chuk-motion/src/chuk_motion/components/layouts/Grid/tool.py
"""Grid MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the Grid tool with the MCP server."""

    @mcp.tool
    async def remotion_add_grid(
        items: str,
        layout: str | None = None,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
    ) -> str:
        """
        Add Grid to the composition.

        Grid layout for multiple items.

        Args:
            items: JSON array of grid items. Format: [{"type": "ComponentName", "config": {...}}, ...]
                Example with videos:
                [
                    {
                        "type": "VideoContent",
                        "config": {
                            "src": "https://example.com/video1.mp4",
                            "muted": true,
                            "fit": "cover"
                        }
                    },
                    {
                        "type": "VideoContent",
                        "config": {
                            "src": "https://example.com/video2.mp4",
                            "muted": true
                        }
                    }
                ]
            layout: Grid layout (2x2, 3x3, etc.)
            gap: Gap between grid items
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
                items_parsed = json.loads(items)
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid items JSON: {str(e)}").model_dump_json()

            try:
                # Convert array of item dicts to ComponentInstance objects
                items_components = []
                if isinstance(items_parsed, list):
                    for item in items_parsed:
                        child = parse_nested_component(item)
                        if child is not None:
                            items_components.append(child)

                # Get builder and start time
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                # Add component using builder
                builder.add_grid(
                    start_time=start_time,
                    items=items_components,
                    layout=layout,
                    gap=gap,
                    padding=padding,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="Grid",
                    layout=layout or "2x2",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
