# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/TextOverlay/tool.py
"""TextOverlay MCP tool."""

import asyncio

from chuk_mcp_remotion.models import ErrorResponse, OverlayComponentResponse


def register_tool(mcp, project_manager):
    """Register the TextOverlay tool with the MCP server."""

    @mcp.tool
    async def remotion_add_text_overlay(
        text: str,
        start_time: float,
        style: str | None = None,
        animation: str | None = None,
        duration: float = 3.0,
        position: str | None = None,
    ) -> str:
        """
        Add TextOverlay to the composition.

        Animated text overlay for emphasis and captions

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_composition:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                project_manager.current_composition.add_text_overlay(
                    text=text,
                    style=style,
                    animation=animation,
                    start_time=start_time,
                    duration=duration,
                    position=position,
                )

                return OverlayComponentResponse(
                    component="TextOverlay", start_time=start_time, duration=duration
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
