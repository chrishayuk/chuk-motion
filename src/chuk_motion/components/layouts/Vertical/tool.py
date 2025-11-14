# chuk-motion/src/chuk_motion/components/layouts/Vertical/tool.py
"""Vertical MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.generator.composition_builder import ComponentInstance
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
        track: str = "main",
        gap_before: float | str | None = None,
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
                top_parsed = json.loads(top) if top else None
                bottom_parsed = json.loads(bottom) if bottom else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                top_component = parse_nested_component(top_parsed)
                bottom_component = parse_nested_component(bottom_parsed)

                component = ComponentInstance(
                    component_type="Vertical",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "top": top_component,
                        "bottom": bottom_component,
                        "layout_style": layout_style,
                        "top_ratio": top_ratio,
                        "gap": gap,
                        "padding": padding,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="Vertical",
                    layout=layout_style,
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
