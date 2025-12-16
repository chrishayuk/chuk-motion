# chuk-motion/src/chuk_motion/components/charts/BarChart/tool.py
"""BarChart MCP tool."""

import asyncio
import json

from chuk_motion.models import ChartComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the BarChart tool with the MCP server."""

    @mcp.tool
    async def remotion_add_bar_chart(
        data: str,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        duration: float = 4.0,
    ) -> str:
        """
        Add an animated bar chart to the composition.

        Animated vertical bar chart for comparing categories.

        Args:
            data: JSON array of {label, value} objects. Optionally include "color" per bar.
                Format: [{"label": "Q1", "value": 45}, {"label": "Q2", "value": 67}]
                With colors: [{"label": "Q1", "value": 45, "color": "#FF0000"}]
            title: Optional chart title
            xlabel: Optional x-axis label
            ylabel: Optional y-axis label
            duration: How long to animate in seconds (default: 4.0)

        Returns:
            JSON with component info

        Example:
            await remotion_add_bar_chart(
                data='[{"label": "Q1", "value": 45}, {"label": "Q2", "value": 67}, {"label": "Q3", "value": 89}]',
                title="Quarterly Sales",
                ylabel="Revenue ($K)",
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
                # Get current end time as start time for new component
                start_time = builder.get_total_duration_seconds()

                # Use the builder method registered by register_all_builders
                builder.add_bar_chart(
                    data=data_parsed,
                    title=title,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    start_time=start_time,
                    duration=duration,
                )

                return ChartComponentResponse(
                    component="BarChart",
                    data_points=len(data_parsed),
                    title=title,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
