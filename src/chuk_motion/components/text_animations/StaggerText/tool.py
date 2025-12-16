# chuk-motion/src/chuk_motion/components/text-animations/StaggerText/tool.py
"""StaggerText MCP tool."""

import asyncio

from chuk_motion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the StaggerText tool with the MCP server."""

    @mcp.tool
    async def remotion_add_stagger_text(
        text: str,
        font_size: str = "3xl",
        font_weight: str = "bold",
        text_color: str | None = None,
        stagger_by: str = "char",
        stagger_delay: float = 2.0,
        animation_type: str = "fade",
        position: str = "center",
        align: str = "center",
        duration: float = 3.0,
    ) -> str:
        """
        Add StaggerText staggered reveal animation with spring physics.

        Creates a professional staggered reveal where characters or words appear
        one-by-one with smooth spring animation.

        Perfect for: Titles, bullet points, reveals, professional presentations

        Args:
            text: Text to animate
            font_size: Font size (xl, 2xl, 3xl, 4xl) - default: 3xl
            font_weight: Font weight (normal, medium, semibold, bold, extrabold, black) - default: bold
            text_color: Text color (uses on_dark color if not specified)
            stagger_by: Stagger by character or word (char, word) - default: char
            stagger_delay: Delay in frames between units (default: 2.0)
            animation_type: Animation style (fade, slide-up, slide-down, scale) - default: fade
            position: Vertical position (center, top, bottom) - default: center
            align: Text alignment (left, center, right) - default: center
            duration: Total duration in seconds (default: 3.0)

        Returns:
            JSON with component info

        Example:
            # Basic character stagger
            remotion_add_stagger_text(
                text="Welcome",
                stagger_by="char",
                animation_type="slide-up"
            )

            # Word-by-word reveal
            remotion_add_stagger_text(
                text="Key Points To Remember",
                stagger_by="word",
                stagger_delay=3.0,
                animation_type="fade"
            )

            # Scaling entrance
            remotion_add_stagger_text(
                text="IMPACT",
                font_size="4xl",
                animation_type="scale",
                stagger_delay=1.5
            )
        """

        def _add():
            builder = project_manager.current_timeline
            if not builder:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                start_time = builder.get_total_duration_seconds()
                builder.add_stagger_text(
                    text=text,
                    font_size=font_size,
                    font_weight=font_weight,
                    text_color=text_color,
                    stagger_by=stagger_by,
                    stagger_delay=stagger_delay,
                    animation_type=animation_type,
                    position=position,
                    align=align,
                    start_time=start_time,
                    duration=duration,
                )

                return ComponentResponse(
                    component="StaggerText",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
