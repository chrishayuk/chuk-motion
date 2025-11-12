# chuk-mcp-remotion/src/chuk_mcp_remotion/components/charts/LineChart/tool.py
"""LineChart MCP tool."""

import asyncio
import json

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ChartComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the LineChart tool with the MCP server."""

    @mcp.tool
    async def remotion_add_line_chart(
        data: str,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        duration: float | str = 4.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add an animated line chart to the composition.

        Animated line chart for showing trends over time.

        IMPORTANT: Data format is [x, y] or {x, y, label}. NOT {label, value}!

        Valid props: data, title, xlabel, ylabel, duration, track, gap_before
        Invalid props: variant, style, color, theme (these don't exist)

        Args:
            data: JSON array of [x, y] pairs or {x, y, label} objects.
                Format: [[0, 10], [1, 25], [2, 45]] or
                        [{"x": 0, "y": 10, "label": "Jan"}, {"x": 1, "y": 25, "label": "Feb"}]
            title: Optional chart title
            xlabel: Optional x-axis label
            ylabel: Optional y-axis label
            duration: How long to animate (seconds) or time string
            track: Track name (default: "main")
            gap_before: Gap before component in seconds or time string

        Returns:
            JSON with component info

        Example:
            await remotion_add_line_chart(
                data='[[0, 10], [1, 25], [2, 45], [3, 70]]',
                title="User Growth",
                xlabel="Month",
                ylabel="Users",
                duration=4.0
            )
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                data_parsed = json.loads(data)
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid data JSON: {str(e)}").model_dump_json()

            try:
                component = ComponentInstance(
                    component_type="LineChart",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "data": data_parsed,
                        "title": title,
                        "xlabel": xlabel,
                        "ylabel": ylabel,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return ChartComponentResponse(
                    component="LineChart",
                    data_points=len(data_parsed),
                    title=title,
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
