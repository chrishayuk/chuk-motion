# chuk-motion/src/chuk_motion/components/animations/Counter/tool.py
"""Counter MCP tool."""

import asyncio

from chuk_motion.models import CounterComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the Counter tool with the MCP server."""

    @mcp.tool
    async def remotion_add_counter(
        end_value: float,
        start_value: float = 0,
        prefix: str | None = None,
        suffix: str | None = None,
        decimals: int = 0,
        animation: str | None = None,
        duration: float = 2.0,
    ) -> str:
        """
        Add Counter to the composition.

        Animated number counter for statistics and metrics

        Args:
            end_value: Ending number
            start_value: Starting number (default: 0)
            prefix: Text before number (e.g., "$")
            suffix: Text after number (e.g., "%")
            decimals: Number of decimal places (integer, default: 0)
            animation: Animation style
            duration: Duration in seconds (default: 2.0)

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
                builder.add_counter(
                    end_value=end_value,
                    start_time=start_time,
                    start_value=start_value,
                    prefix=prefix,
                    suffix=suffix,
                    decimals=decimals,
                    animation=animation,
                    duration=duration,
                )

                return CounterComponentResponse(
                    component="Counter",
                    start_value=start_value,
                    end_value=end_value,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
