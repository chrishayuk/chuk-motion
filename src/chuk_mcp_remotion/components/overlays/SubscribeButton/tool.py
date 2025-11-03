# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/SubscribeButton/tool.py
"""SubscribeButton MCP tool."""

import asyncio

from chuk_mcp_remotion.models import ErrorResponse, OverlayComponentResponse


def register_tool(mcp, project_manager):
    """Register the SubscribeButton tool with the MCP server."""

    @mcp.tool
    async def remotion_add_subscribe_button(
        start_time: float,
        variant: str | None = None,
        animation: str | None = None,
        position: str | None = None,
        duration: float = 3.0,
        custom_text: str | None = None,
    ) -> str:
        """
        Add SubscribeButton to the composition.

        Animated subscribe button overlay (YouTube-specific)

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_composition:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                project_manager.current_composition.add_subscribe_button(
                    variant=variant,
                    animation=animation,
                    position=position,
                    start_time=start_time,
                    duration=duration,
                    custom_text=custom_text,
                )

                return OverlayComponentResponse(
                    component="SubscribeButton", start_time=start_time, duration=duration
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
