# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/TextOverlay/tool.py
"""TextOverlay MCP tool."""

import asyncio

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, OverlayComponentResponse


def register_tool(mcp, project_manager):
    """Register the TextOverlay tool with the MCP server."""

    @mcp.tool
    async def remotion_add_text_overlay(
        text: str,
        style: str | None = None,
        animation: str | None = None,
        position: str | None = None,
        duration: float = 3.0,
        track: str = "overlay",
        gap_before: float | None = None,
    ) -> str:
        """
        Add TextOverlay to the composition.

        Animated text overlay for emphasis and captions

        Args:
            text: Text content to display
            style: Text style variant
            animation: Animation type
            position: Position on screen
            duration: Duration in seconds
            track: Track name (default: "overlay")
            gap_before: Gap before component in seconds (overrides track default)

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                component = ComponentInstance(
                    component_type="TextOverlay",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "text": text,
                        "style": style,
                        "animation": animation,
                        "position": position,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return OverlayComponentResponse(
                    component="TextOverlay",
                    start_time=project_manager.current_timeline.frames_to_seconds(component.start_frame),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
