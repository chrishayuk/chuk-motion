# chuk-motion/src/chuk_motion/components/content/DemoBox/tool.py
"""DemoBox MCP tool."""

import asyncio

from chuk_motion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the DemoBox tool with the MCP server."""

    @mcp.tool
    async def remotion_add_demo_box(
        label: str,
        color: str = "primary",
        duration: float | str = 5.0,
    ) -> str:
        """
        Add DemoBox to the composition.

        Colored box component for demonstrations and placeholders.

        Args:
            label: Text label to display in the box
            color: Color variant (primary, secondary, etc.)
            duration: Duration in seconds or time string (e.g., "2s", "500ms")

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                builder.add_demo_box(
                    label=label,
                    start_time=start_time,
                    color=color,
                    duration=duration,
                )

                return ComponentResponse(
                    component="DemoBox",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
