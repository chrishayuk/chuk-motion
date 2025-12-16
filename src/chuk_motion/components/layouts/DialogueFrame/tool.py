# chuk-motion/src/chuk_motion/components/layouts/DialogueFrame/tool.py
"""DialogueFrame MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.models import ErrorResponse, LayoutComponentResponse


def register_tool(mcp, project_manager):
    """Register the DialogueFrame tool with the MCP server."""

    @mcp.tool
    async def remotion_add_dialogue_frame(
        left_speaker: str | None = None,
        right_speaker: str | None = None,
        center_content: str | None = None,
        speaker_size: float = 40,
        gap: float = 20,
        padding: float = 40,
        duration: float | str = 5.0,
    ) -> str:
        """
        Add DialogueFrame layout to the composition.

        For conversation/dialogue scenes with two speakers

        Args:
            left_speaker: JSON component for left speaker. Format: {"type": "ComponentName", "config": {...}}
                Example:
                {
                    "type": "VideoContent",
                    "config": {
                        "src": "speaker1.mp4",
                        "fit": "cover"
                    }
                }
            right_speaker: JSON component for right speaker. Same format as left_speaker
            center_content: JSON component for center content (captions, etc.). Same format
            speaker_size: Speaker panel size (percentage)
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
                left_parsed = json.loads(left_speaker) if left_speaker else None
                right_parsed = json.loads(right_speaker) if right_speaker else None
                center_parsed = json.loads(center_content) if center_content else None
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid component JSON: {str(e)}").model_dump_json()

            try:
                # Convert nested components to ComponentInstance objects
                left_component = parse_nested_component(left_parsed)
                right_component = parse_nested_component(right_parsed)
                center_component = parse_nested_component(center_parsed)

                # Get builder and start time
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                # Add component using builder
                builder.add_dialogue_frame(
                    start_time=start_time,
                    left_speaker=left_component,
                    right_speaker=right_component,
                    center_content=center_component,
                    speaker_size=speaker_size,
                    gap=gap,
                    padding=padding,
                    duration=duration,
                )

                return LayoutComponentResponse(
                    component="DialogueFrame",
                    layout="dialogue",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
