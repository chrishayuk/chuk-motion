# chuk-mcp-remotion/src/chuk_mcp_remotion/components/animations/Counter/tool.py
"""Counter MCP tool."""

import asyncio

from chuk_mcp_remotion.models import CounterComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the Counter tool with the MCP server."""

    @mcp.tool
    async def remotion_add_counter(
        end_value: float,
        start_time: float,
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

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_composition:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                project_manager.current_composition.add_counter(
                    start_value=start_value,
                    end_value=end_value,
                    prefix=prefix,
                    suffix=suffix,
                    decimals=decimals,
                    animation=animation,
                    start_time=start_time,
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
