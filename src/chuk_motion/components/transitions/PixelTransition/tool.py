# chuk-motion/src/chuk_motion/components/transitions/PixelTransition/tool.py
"""PixelTransition MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the PixelTransition tool with the MCP server."""

    @mcp.tool
    async def remotion_add_pixel_transition(
        first_content: str,
        second_content: str,
        grid_size: int = 10,
        pixel_color: str | None = None,
        transition_start: float = 2.0,
        transition_duration: float = 1.0,
        duration: float | str = 5.0,
    ) -> str:
        """
        Add PixelTransition animated transition effect to the composition.

        Creates a pixelated dissolve transition between two pieces of content. Pixels
        animate in with random stagger to cover the first content, then animate out
        to reveal the second content.

        Perfect for: Scene transitions, content reveals, before/after showcases

        Args:
            first_content: JSON string of first content component (format: {"type": "ComponentName", "config": {...}})
            second_content: JSON string of second content component (format: {"type": "ComponentName", "config": {...}})
            grid_size: Number of pixels per row/column (default: 10 = 10x10 = 100 pixels)
            pixel_color: Color of transition pixels (uses primary color if not specified)
            transition_start: When to start transition in seconds (default: 2.0)
            transition_duration: Duration of transition animation in seconds (default: 1.0)
            duration: Total duration in seconds or time string (e.g., "5s", "500ms")

        Returns:
            JSON with component info

        Example:
            # Transition between two title cards
            remotion_add_pixel_transition(
                first_content='{"type":"TitleScene","config":{"text":"Before","variant":"bold"}}',
                second_content='{"type":"TitleScene","config":{"text":"After","variant":"glass"}}',
                grid_size=12,
                transition_start=2.0,
                transition_duration=1.0,
                duration=5.0
            )

            # Transition between chart and text
            remotion_add_pixel_transition(
                first_content='{"type":"BarChart","config":{"data":[...],"title":"Sales Data"}}',
                second_content='{"type":"TextOverlay","config":{"text":"Record Growth","size":"large"}}',
                grid_size=15,
                pixel_color="#00D9FF"
            )
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                # Parse nested content
                first_parsed = json.loads(first_content)
                second_parsed = json.loads(second_content)

                first_component = parse_nested_component(first_parsed)
                second_component = parse_nested_component(second_parsed)

                if first_component is None or second_component is None:
                    return ErrorResponse(
                        error="Invalid content format. Use format: {'type': 'ComponentName', 'config': {...}}"
                    ).model_dump_json()

                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                builder.add_pixel_transition(
                    start_time=start_time,
                    first_content=first_component,
                    second_content=second_component,
                    grid_size=grid_size,
                    pixel_color=pixel_color,
                    transition_start=transition_start,
                    transition_duration=transition_duration,
                    duration=duration,
                )

                return ComponentResponse(
                    component="PixelTransition",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid JSON: {str(e)}").model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
