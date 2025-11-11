# chuk-mcp-remotion/src/chuk_mcp_remotion/components/layouts/SplitScreen/tool.py
"""SplitScreen MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, LayoutComponentResponse
from chuk_mcp_remotion.components.component_helpers import parse_nested_component


def register_tool(mcp, project_manager):
    """Register the SplitScreen tool with the MCP server."""

    @mcp.tool
    async def remotion_add_split_screen(
        left: str | None = None,
        right: str | None = None,
        top: str | None = None,
        bottom: str | None = None,
        orientation: str = "horizontal",
        ratio: float = 0.5,
        gap: float = 20,
        padding: float = 40,
        divider_width: float | None = None,
        divider_color: str | None = None,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add SplitScreen to the composition.

        Layout component for side-by-side or top-bottom content.

        For video content in panels, use VideoContent component:
        Example left panel with video:
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
            left: JSON component for left panel (format: {"type": "ComponentName", "config": {...}})
            right: JSON component for right panel (format: {"type": "ComponentName", "config": {...}})
            top: JSON component for top panel (format: {"type": "ComponentName", "config": {...}})
            bottom: JSON component for bottom panel (format: {"type": "ComponentName", "config": {...}})
            orientation: Orientation (horizontal or vertical, default: horizontal)
            ratio: Split ratio 0.0-1.0 (default: 0.5 for 50/50)
            gap: Gap between sections
            padding: Padding from edges
            divider_width: Width of divider line between panels
            divider_color: Color of divider line
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
                right_parsed = json.loads(right) if right else None
                top_parsed = json.loads(top) if top else None
                bottom_parsed = json.loads(bottom) if bottom else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                left_component = parse_nested_component(left_parsed)
                right_component = parse_nested_component(right_parsed)
                top_component = parse_nested_component(top_parsed)
                bottom_component = parse_nested_component(bottom_parsed)

                component = ComponentInstance(
                    component_type="SplitScreen",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "orientation": orientation,
                        "ratio": ratio,
                        "gap": gap,
                        "padding": padding,
                        "divider_width": divider_width,
                        "divider_color": divider_color,
                        "left": left_component,
                        "right": right_component,
                        "top": top_component,
                        "bottom": bottom_component,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                ratio_pct = f"{int(ratio*100)}-{int((1-ratio)*100)}"
                layout_desc = f"{orientation}-{ratio_pct}"
                return LayoutComponentResponse(
                    component="SplitScreen",
                    layout=layout_desc,
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
