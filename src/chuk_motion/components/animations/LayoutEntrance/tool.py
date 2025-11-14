"""LayoutEntrance MCP tool."""

import asyncio
import json

from chuk_motion.components.component_helpers import parse_nested_component
from chuk_motion.generator.composition_builder import ComponentInstance
from chuk_motion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the LayoutEntrance tool with the MCP server."""

    @mcp.tool
    async def remotion_add_layout_entrance(
        content: str,
        entrance_type: str = "fade_in",
        entrance_delay: float = 0.0,
        duration: float | str = 5.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add LayoutEntrance wrapper to animate any layout or component in.

        Universal entrance animation that works with any layout or component.
        Uses motion tokens for consistent timing and easing across all entrance types.

        Perfect for: Adding polish to any layout, consistent entrance patterns, zero-config animation

        Example entrance_type values and their effects:
        - fade_in: Simple fade (subtle, professional)
        - fade_slide_up: Fade + slide up (modern, polished)
        - scale_in_soft: Subtle scale 0.95→1.0 (elegant, refined)
        - scale_in_pop: Pop with bounce (playful, energetic)
        - slide_in_left: Slide from left (spatial, directional)
        - slide_in_right: Slide from right (spatial, alternative)
        - blur_in: Fade from blur (dramatic, cinematic)
        - zoom_in: Zoom 0→100% (explosive, hero entrance)

        Example content Grid layout:
        {
            "type": "Grid",
            "config": {
                "layout": "3x3",
                "items": [
                    {"type": "CodeBlock", "config": {"code": "Item 1"}},
                    {"type": "CodeBlock", "config": {"code": "Item 2"}},
                    {"type": "CodeBlock", "config": {"code": "Item 3"}}
                ]
            }
        }

        Example content Container:
        {
            "type": "Container",
            "config": {
                "position": "center",
                "content": {"type": "TitleScene", "config": {"text": "Hello"}}
            }
        }

        Args:
            content: JSON component to animate (format: {"type": "ComponentName", "config": {...}})
            entrance_type: Animation style - one of: none, fade_in, fade_slide_up, scale_in_soft, scale_in_pop, slide_in_left, slide_in_right, blur_in, zoom_in (default: "fade_in")
                - "none": No animation (instant)
                - "fade_in": Simple fade in (subtle, professional)
                - "fade_slide_up": Fade + slide up (content blocks, cards)
                - "scale_in_soft": Subtle scale 0.95 → 1.0 (elegant)
                - "scale_in_pop": Pop scale 0.9 → 1.05 → 1.0 (playful)
                - "slide_in_left": Slide from left (side panels)
                - "slide_in_right": Slide from right (side panels)
                - "blur_in": Fade from blur (dramatic)
                - "zoom_in": Zoom from 0 to 100% (hero elements)
            entrance_delay: Delay before entrance animation starts (seconds)
            duration: Total duration in seconds or time string (e.g., "5s", "500ms")
            track: Track name (default: "main")
            gap_before: Gap before component in seconds or time string

        Returns:
            JSON with component info

        Example:
            # Add fade-slide entrance to Grid layout
            remotion_add_layout_entrance(
                content='{"type":"Grid","config":{"layout":"3x3","items":[...]}}',
                entrance_type="fade_slide_up",
                entrance_delay=0.2,
                duration=10.0
            )

            # Add pop entrance to Container
            remotion_add_layout_entrance(
                content='{"type":"Container","config":{"content":{...}}}',
                entrance_type="scale_in_pop",
                duration=5.0
            )

            # Add dramatic blur entrance to Timeline
            remotion_add_layout_entrance(
                content='{"type":"Timeline","config":{...}}',
                entrance_type="blur_in",
                entrance_delay=0.5
            )
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                # Parse nested content
                content_parsed = json.loads(content)
                content_component = parse_nested_component(content_parsed)

                # Validate that we got a ComponentInstance
                if not isinstance(content_component, ComponentInstance):
                    return ErrorResponse(
                        error="Invalid content format. Use format: {'type': 'ComponentName', 'config': {...}}"
                    ).model_dump_json()

                # Validate entrance type
                valid_types = [
                    "none",
                    "fade_in",
                    "fade_slide_up",
                    "scale_in_soft",
                    "scale_in_pop",
                    "slide_in_left",
                    "slide_in_right",
                    "blur_in",
                    "zoom_in",
                ]
                if entrance_type not in valid_types:
                    return ErrorResponse(
                        error=f"Invalid entrance_type. Must be one of: {', '.join(valid_types)}"
                    ).model_dump_json()

                # Build props
                props = {
                    "content": content_component,
                    "entranceType": entrance_type,
                    "entranceDelay": entrance_delay,
                }

                component = ComponentInstance(
                    component_type="LayoutEntrance",
                    start_frame=0,
                    duration_frames=0,
                    props=props,
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return ComponentResponse(
                    component="LayoutEntrance",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except json.JSONDecodeError as e:
                return ErrorResponse(error=f"Invalid JSON: {str(e)}").model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
