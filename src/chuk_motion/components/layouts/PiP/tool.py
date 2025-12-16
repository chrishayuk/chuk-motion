# chuk-motion/src/chuk_motion/components/layouts/PiP/tool.py
"""PiP MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the PiP tool with the MCP server."""

    @mcp.tool
    async def remotion_add_pip(
        main_content: str | None = None,
        pip_content: str | None = None,
        position: str = "bottom-right",
        overlay_size: float = 20,
        margin: float = 40,
        duration: float | str = 5.0,
    ) -> str:
        """
        Add PiP (Picture-in-Picture) to the composition.

        Picture-in-Picture webcam overlay with customizable positions

        Args:
            main_content: JSON component for main background. Format: {"type": "ComponentName", "config": {...}}
            pip_content: JSON component for PiP overlay. Same format as main_content
            position: Overlay position (bottom-right, bottom-left, top-right, top-left)
            overlay_size: Overlay size (percentage of screen)
            margin: Margin from edges
            duration: Duration in seconds

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                main_parsed = json.loads(main_content) if main_content else None
                pip_parsed = json.loads(pip_content) if pip_content else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                main_component = parse_nested_component(main_parsed)
                pip_component = parse_nested_component(pip_parsed)

                # Get builder and start time
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                # Add component using builder
                builder.add_pi_p(
                    start_time=start_time,
                    main_content=main_component,
                    pip_content=pip_component,
                    position=position,
                    overlay_size=overlay_size,
                    margin=margin,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="PiP",
                    layout=position,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
