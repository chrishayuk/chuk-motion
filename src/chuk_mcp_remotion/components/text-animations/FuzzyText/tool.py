# chuk-mcp-remotion/src/chuk_mcp_remotion/components/overlays/FuzzyText/tool.py
"""FuzzyText MCP tool."""

import asyncio

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the FuzzyText tool with the MCP server."""

    @mcp.tool
    async def remotion_add_fuzzy_text(
        text: str,
        font_size: str = "3xl",
        font_weight: str = "bold",
        text_color: str | None = None,
        glitch_intensity: float = 5.0,
        scanline_height: float = 2.0,
        animate: bool = True,
        position: str = "center",
        duration: float | str = 3.0,
        track: str = "main",
        gap_before: float | str | None = None,
    ) -> str:
        """
        Add FuzzyText animated text with scanline distortion and glitch effects.

        Creates a fuzzy, VHS-style text effect with horizontal displacement and
        RGB split for a glitchy aesthetic.

        Perfect for: Retro aesthetics, glitch art, VHS effects, cyberpunk themes

        Args:
            text: Text to display with fuzzy effect
            font_size: Font size (xl, 2xl, 3xl, 4xl) - default: 3xl
            font_weight: Font weight (normal, medium, semibold, bold, extrabold, black) - default: bold
            text_color: Text color (uses on_dark color if not specified)
            glitch_intensity: Intensity of glitch displacement (0-20) - default: 5.0
            scanline_height: Height of scanlines in pixels - default: 2.0
            animate: Whether to animate the glitch effect - default: true
            position: Vertical position (center, top, bottom) - default: center
            duration: Total duration in seconds or time string (e.g., "3s", "300ms")
            track: Track name (default: "main")
            gap_before: Gap before component in seconds or time string

        Returns:
            JSON with component info

        Example:
            # Basic fuzzy text with animation
            remotion_add_fuzzy_text(
                text="GLITCH EFFECT",
                font_size="4xl",
                glitch_intensity=8.0
            )

            # Static fuzzy text (no animation)
            remotion_add_fuzzy_text(
                text="VHS Aesthetic",
                animate=False,
                glitch_intensity=3.0,
                scanline_height=1.5
            )

            # High-intensity cyberpunk glitch
            remotion_add_fuzzy_text(
                text="SYSTEM ERROR",
                glitch_intensity=15.0,
                font_weight="extrabold",
                position="top",
                text_color="#FF00FF"
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
                    "glitchIntensity": glitch_intensity,
                    "scanlineHeight": scanline_height,
                    "animate": animate,
                    "position": position,
                }

                if text_color:
                    props["textColor"] = text_color

                component = ComponentInstance(
                    component_type="FuzzyText",
                    start_frame=0,
                    duration_frames=0,
                    props=props,
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return ComponentResponse(
                    component="FuzzyText",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
