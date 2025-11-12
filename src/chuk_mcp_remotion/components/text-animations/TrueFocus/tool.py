# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/TrueFocus/tool.py
"""TrueFocus MCP tool."""

import asyncio

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the TrueFocus tool with the MCP server."""

    @mcp.tool
    async def remotion_add_true_focus(
        text: str,
        font_size: str = "3xl",
        font_weight: str = "black",
        text_color: str | None = None,
        frame_color: str | None = None,
        glow_color: str | None = None,
        blur_amount: float = 5.0,
        word_duration: float = 1.0,
        position: str = "center",
        duration: float | str = 5.0,
        track: str = "overlay",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add TrueFocus animated text overlay to the composition.

        Dramatic text animation that cycles through words, applying blur to inactive words
        while highlighting the focused word with animated corner brackets and glow effect.

        Perfect for: Emphasis text, dramatic reveals, taglines, key messages

        Args:
            text: Text to animate (will be split into words)
            font_size: Size of text (xl, 2xl, 3xl, 4xl) - default: 3xl
            font_weight: Weight of text (bold, extrabold, black) - default: black
            text_color: Text color (uses theme text color if not specified)
            frame_color: Color of corner brackets (uses primary color if not specified)
            glow_color: Glow effect color (uses primary color if not specified)
            blur_amount: Blur intensity for inactive words in pixels - default: 5.0
            word_duration: Duration each word stays focused in seconds - default: 1.0
            position: Vertical position (center, top, bottom) - default: center
            duration: Total duration in seconds or time string (e.g., "5s", "500ms")
            track: Track name (default: "overlay")
            gap_before: Gap before component in seconds or time string

        Returns:
            JSON with component info

        Example:
            # Dramatic tagline reveal
            remotion_add_true_focus(
                text="Innovation Through Excellence",
                font_size="4xl",
                word_duration=1.5,
                position="center"
            )

            # Top-positioned emphasis
            remotion_add_true_focus(
                text="Powered by Advanced Technology",
                font_size="2xl",
                position="top",
                word_duration=1.0
            )
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                # Build props
                props = {
                    "text": text,
                    "fontSize": font_size,
                    "fontWeight": font_weight,
                    "blurAmount": blur_amount,
                    "wordDuration": int(word_duration * 30),  # Convert to frames (30fps)
                    "position": position,
                }

                # Add optional color overrides
                if text_color:
                    props["textColor"] = text_color
                if frame_color:
                    props["frameColor"] = frame_color
                if glow_color:
                    props["glowColor"] = glow_color

                component = ComponentInstance(
                    component_type="TrueFocus",
                    start_frame=0,
                    duration_frames=0,
                    props=props,
                    layer=10,  # Overlay layer
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return ComponentResponse(
                    component="TrueFocus",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
