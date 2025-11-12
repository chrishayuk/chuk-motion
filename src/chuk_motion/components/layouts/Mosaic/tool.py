# chuk-motion/src/chuk_motion/components/layouts/Mosaic/tool.py
"""Mosaic MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.generator.composition_builder import ComponentInstance
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the Mosaic tool with the MCP server."""

    @mcp.tool
    async def remotion_add_mosaic(
        clips: str | None = None,
        style: str = "hero-corners",
        gap: float = 10,
        padding: float = 40,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add Mosaic layout to the composition.

        Dynamic collage layout with multiple clips in artistic arrangements.

        Args:
            clips: JSON array of component objects for mosaic cells. Format: [{"type": "ComponentName", "config": {...}}, ...]
            style: Mosaic style (hero-corners, grid, scattered, etc.)
            gap: Gap between clips
            padding: Padding from edges
            duration: Duration in seconds or time string
            track: Track name (default: "main")
            gap_before: Gap before component in seconds or time string

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                clips_parsed = json.loads(clips) if clips else []
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid JSON: {str(e)}").model_dump_json()

            try:
                # Convert array of clip dicts to ComponentInstance objects
                clips_components = []
                if isinstance(clips_parsed, list):
                    for item in clips_parsed:
                        comp = parse_nested_component(item)
                        if comp is not None:
                            clips_components.append(comp)

                component = ComponentInstance(
                    component_type="Mosaic",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "clips": clips_components,
                        "style": style,
                        "gap": gap,
                        "padding": padding,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return LayoutComponentResponse(
                    component="Mosaic",
                    layout=style,
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
