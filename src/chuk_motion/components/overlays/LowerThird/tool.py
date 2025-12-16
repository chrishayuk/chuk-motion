# chuk-motion/src/chuk_motion/components/overlays/LowerThird/tool.py
"""LowerThird MCP tool."""

import asyncio

from chuk_motion.models import ErrorResponse, OverlayComponentResponse


def register_tool(mcp, project_manager):
    """Register the LowerThird tool with the MCP server."""

    @mcp.tool
    async def remotion_add_lower_third(
        name: str,
        title: str | None = None,
        variant: str | None = None,
        position: str | None = None,
        duration: float = 5.0,
    ) -> str:
        """
        Add LowerThird to the composition.

        Name plate overlay with title and subtitle (like TV graphics)

        Args:
            name: Person's name to display
            title: Optional title/role to display
            variant: Style variant
            position: Position on screen
            duration: Duration in seconds (default: 5.0)

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
                builder.add_lower_third(
                    name=name,
                    start_time=start_time,
                    title=title,
                    variant=variant,
                    position=position,
                    duration=duration,
                )

                return OverlayComponentResponse(
                    component="LowerThird",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
