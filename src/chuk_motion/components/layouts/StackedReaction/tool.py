# chuk-motion/src/chuk_motion/components/layouts/StackedReaction/tool.py
"""StackedReaction MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the StackedReaction tool with the MCP server."""

    @mcp.tool
    async def remotion_add_stacked_reaction(
        original_content: str | None = None,
        reaction_content: str | None = None,
        layout: str = "vertical",
        reaction_size: float = 40,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
    ) -> str:
        """
        Add StackedReaction layout to the composition.

        Reaction video style with stacked feeds

        Args:
            original_content: JSON component for original video. Format: {"type": "ComponentName", "config": {...}}
            reaction_content: JSON component for reaction video. Same format as original_content
            layout: Layout style (vertical, horizontal, pip)
            reaction_size: Reaction panel size (percentage)
            gap: Gap between panels
            padding: Padding from edges
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
                original_parsed = json.loads(original_content) if original_content else None
                reaction_parsed = json.loads(reaction_content) if reaction_content else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                original_component = parse_nested_component(original_parsed)
                reaction_component = parse_nested_component(reaction_parsed)

                # Get builder and start time
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                # Add component using builder
                builder.add_stacked_reaction(
                    start_time=start_time,
                    original_content=original_component,
                    reaction_content=reaction_component,
                    layout=layout,
                    reaction_size=reaction_size,
                    gap=gap,
                    padding=padding,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="StackedReaction",
                    layout=layout,
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
