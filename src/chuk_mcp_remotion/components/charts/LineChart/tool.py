# chuk-mcp-remotion/src/chuk_mcp_remotion/components/charts/LineChart/tool.py
"""LineChart MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.models import ChartComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the LineChart tool with the MCP server."""

    @mcp.tool
    async def remotion_add_line_chart(
        data: str,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        start_time: float = 0.0,
        duration: float = 4.0,
    ) -> str:
        """
        Add an animated line chart to the composition.

        Creates a data visualization chart that animates into view. The chart
        displays data points with optional labels and axes.

        Args:
            data: JSON array of data points, either [[x1,y1],[x2,y2],...] or
                  [{"x":x1,"y":y1,"label":"label1"},...]
            title: Optional chart title
            xlabel: Optional x-axis label
            ylabel: Optional y-axis label
            start_time: When to show (seconds from start)
            duration: How long to animate (default: 4.0 seconds)

        Returns:
            JSON with component info

        Example:
            await remotion_add_line_chart(
                data='[[0,10],[1,25],[2,45],[3,70],[4,90]]',
                title="Growth Chart",
                xlabel="Month",
                ylabel="Users (k)",
                start_time=3.0,
                duration=4.0
            )
        """

        def _add():
            if not project_manager.current_composition:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                # Parse the data JSON string
                data_parsed = json.loads(data)
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid data JSON: {str(e)}").model_dump_json()

            try:
                project_manager.current_composition.add_line_chart(
                    data=data_parsed,
                    title=title,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    start_time=start_time,
                    duration=duration,
                )

                return ChartComponentResponse(
                    component="LineChart",
                    data_points=len(data_parsed),
                    title=title,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
