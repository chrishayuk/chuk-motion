# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/ThreeColumnLayout/tool.py
"""ThreeColumnLayout MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse
from chuk_mcp_remotion.components.component_helpers import parse_nested_component


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
        track: str = "main",
        gap_before: float | str | None = None,
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
            track: Track name (default: "main")
            gap_before: Gap before component in seconds

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

                component = ComponentInstance(
                    component_type="ThreeColumnLayout",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "left": left_component,
                        "center": center_component,
                        "right": right_component,
                        "left_width": left_width,
                        "center_width": center_width,
                        "right_width": right_width,
                        "gap": gap,
                        "padding": padding,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="ThreeColumnLayout",
                    layout=f"{left_width}:{center_width}:{right_width}",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
