# chuk-motion/src/chuk_motion/components/overlays/SubscribeButton/tool.py
"""SubscribeButton MCP tool."""

import asyncio

from chuk_motion.models import ErrorResponse, OverlayComponentResponse


def register_tool(mcp, project_manager):
    """Register the SubscribeButton tool with the MCP server."""

    @mcp.tool
    async def remotion_add_subscribe_button(
        variant: str | None = None,
        animation: str | None = None,
        position: str | None = None,
        custom_text: str | None = None,
        duration: float = 3.0,
    ) -> str:
        """
        Add SubscribeButton to the composition.

        Animated subscribe button overlay (YouTube-specific)

        Args:
            variant: Style variant
            animation: Animation type
            position: Position on screen
            custom_text: Optional custom button text
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
                builder.add_subscribe_button(
                    start_time=start_time,
                    variant=variant,
                    animation=animation,
                    position=position,
                    duration=duration,
                    custom_text=custom_text,
                )

                return OverlayComponentResponse(
                    component="SubscribeButton",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
