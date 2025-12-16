# chuk-motion/src/chuk_motion/components/overlays/TextOverlay/tool.py
"""TextOverlay MCP tool."""

import asyncio

from chuk_motion.models import ErrorResponse, OverlayComponentResponse


def register_tool(mcp, project_manager):
    """Register the TextOverlay tool with the MCP server."""

    @mcp.tool
    async def remotion_add_text_overlay(
        text: str,
        style: str | None = None,
        animation: str | None = None,
        position: str | None = None,
        duration: float = 3.0,
    ) -> str:
        """
        Add TextOverlay to the composition.

        Animated text overlay for emphasis and captions

        Args:
            text: Text content to display
            style: Text style variant
            animation: Animation type
            position: Position on screen
            duration: Duration in seconds (default: 3.0)

        Returns:
            JSON with component info
        """

        def _add():
            builder = project_manager.current_timeline
            if not builder:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                start_time = builder.get_total_duration_seconds()
                builder.add_text_overlay(
                    text=text,
                    start_time=start_time,
                    style=style,
                    animation=animation,
                    duration=duration,
                    position=position,
                )

                return OverlayComponentResponse(
                    component="TextOverlay",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
