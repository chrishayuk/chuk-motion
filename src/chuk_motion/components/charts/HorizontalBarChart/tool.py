# chuk-motion/src/chuk_motion/components/charts/HorizontalBarChart/tool.py
"""HorizontalBarChart MCP tool."""

import asyncio
import json

from chuk_motion.models import ChartComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the HorizontalBarChart tool with the MCP server."""

    @mcp.tool
    async def remotion_add_horizontal_bar_chart(
        data: str,
        title: str | None = None,
        xlabel: str | None = None,
        duration: float = 4.0,
    ) -> str:
        """
        Add an animated horizontal bar chart to the composition.

        Animated horizontal bar chart for comparing categories.

        Args:
            data: JSON array of {label, value} objects. Optionally include "color" per bar.
                Format: [{"label": "Product A", "value": 85}, {"label": "Product B", "value": 60}]
            title: Optional chart title
            xlabel: Optional x-axis label
            duration: How long to animate in seconds (default: 4.0)

        Returns:
            JSON with component info

        Example:
            await remotion_add_horizontal_bar_chart(
                data='[{"label": "Product X", "value": 85}, {"label": "Product Y", "value": 60}]',
                title="Product Comparison",
                duration=4.0
            )
        """

        def _add():
            builder = project_manager.current_timeline
            if not builder:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                data_parsed = json.loads(data)
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid data JSON: {str(e)}").model_dump_json()

            try:
                start_time = builder.get_total_duration_seconds()
                builder.add_horizontal_bar_chart(
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
