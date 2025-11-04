# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/TitleScene/tool.py
"""TitleScene MCP tool."""

import asyncio

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ErrorResponse, OverlayComponentResponse


def register_tool(mcp, project_manager):
    """Register the TitleScene tool with the MCP server."""

    @mcp.tool
    async def remotion_add_title_scene(
        text: str,
        subtitle: str | None = None,
        variant: str | None = None,
        animation: str | None = None,
        duration_seconds: float = 3.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add TitleScene to the composition.

        Full-screen animated title card for video openings

        Args:
            text: Main title text
            subtitle: Optional subtitle
            variant: Style variant (bold, minimal, etc.)
            animation: Animation style (fade_zoom, slide_up, etc.)
            duration_seconds: Duration in seconds
            track: Track name (default: "main")
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
                    component_type="TitleScene",
                    start_frame=0,  # Will be calculated by timeline
                    duration_frames=0,  # Will be calculated by timeline
                    props={
                        "text": text,
                        "subtitle": subtitle,
                        "variant": variant,
                        "animation": animation,
                    },
                    layer=0,  # Will be set by timeline
                )

                # Add to timeline
                component = project_manager.current_timeline.add_component(
                    component, duration=duration_seconds, track=track, gap_before=gap_before
                )

                return OverlayComponentResponse(
                    component="TitleScene",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration_seconds,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
