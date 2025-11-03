# chuk-mcp-remotion/src/chuk_mcp_remotion/components/charts/HorizontalBarChart/tool.py
"""HorizontalBarChart MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.models import ChartComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the HorizontalBarChart tool with the MCP server."""

    @mcp.tool
    async def remotion_add_horizontal_bar_chart(
        data: str,
        title: str | None = None,
        xlabel: str | None = None,
        start_time: float = 0.0,
        duration: float = 5.0,
    ) -> str:
        """
        Add an animated horizontalbar chart to the composition.

        Animated horizontal bar chart perfect for rankings with rank badges.

        Args:
            data: JSON array of data points
            title: Optional chart title
            xlabel: Optional x-axis label
            start_time: When to show (seconds)
            duration: How long to animate (seconds)

        Returns:
            JSON with component info

        Example:
            await remotion_add_horizontal_bar_chart(
                data='[{"label": "Comt\u00e9", "value": 95}, {"label": "Roquefort", "value": 90}]',
                title="Example Chart",
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
                data_parsed = json.loads(data)
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid data JSON: {str(e)}").model_dump_json()

            try:
                project_manager.current_composition.add_horizontal_bar_chart(
                    data=data_parsed,
                    title=title,
                    xlabel=xlabel,
                    start_time=start_time,
                    duration=duration,
                )

                return ChartComponentResponse(
                    component="HorizontalBarChart",
                    data_points=len(data_parsed),
                    title=title,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
