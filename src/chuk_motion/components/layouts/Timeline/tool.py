# chuk-motion/src/chuk_motion/components/layouts/Timeline/tool.py
"""Timeline MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.generator.composition_builder import ComponentInstance
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the Timeline tool with the MCP server."""

    @mcp.tool
    async def remotion_add_timeline(
        main_content: str | None = None,
        milestones: str | None = None,
        current_time: float = 0,
        total_duration: float = 10,
        position: str = "bottom",
        height: float = 100,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add Timeline layout to the composition.

        Timeline visualization with main content and milestone markers.

        Args:
            main_content: JSON component for main content area. Format: {"type": "ComponentName", "config": {...}}
            milestones: JSON array of milestone component objects. Format: [{"type": "...", "config": {...}}, ...]
            current_time: Current time position on timeline
            total_duration: Total timeline duration
            position: Timeline position (top, bottom)
            height: Timeline bar height in pixels
            duration: Duration in seconds or time string (e.g., "5s", "1000ms")
            track: Track name (default: "main")
            gap_before: Gap before component in seconds or time string

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                main_parsed = json.loads(main_content) if main_content else None
                milestones_parsed = json.loads(milestones) if milestones else []
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                main_component = parse_nested_component(main_parsed)

                # Parse array of milestones
                milestones_components = []
                if isinstance(milestones_parsed, list):
                    for item in milestones_parsed:
                        comp = parse_nested_component(item)
                        if comp is not None:
                            milestones_components.append(comp)

                component = ComponentInstance(
                    component_type="Timeline",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "main_content": main_component,
                        "milestones": milestones_components,
                        "current_time": current_time,
                        "total_duration": total_duration,
                        "position": position,
                        "height": height,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="Timeline",
                    layout=position,
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
