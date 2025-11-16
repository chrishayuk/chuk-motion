# chuk-motion/src/chuk_motion/components/code/TypingCode/tool.py
"""TypingCode MCP tool."""

import asyncio
import logging

from chuk_motion.generator.composition_builder import ComponentInstance
from chuk_motion.models import CodeComponentResponse, ErrorResponse

logger = logging.getLogger(__name__)


def register_tool(mcp, project_manager):
    """Register the TypingCode tool with the MCP server."""

    @mcp.tool
    async def remotion_add_typing_code(
        code: str,
        language: str | None = None,
        title: str | None = None,
        variant: str | None = None,
        cursor_style: str | None = None,
        typing_speed: str | None = None,
        show_line_numbers: bool = True,
        duration: float | str = 10.0,
        track: str = "main",
        gap_before: float | str | None = None,
        auto_generate: bool = True,
    ) -> str:
        """
        Add TypingCode to the composition.

        Animated typing code effect with cursor

        Args:
            code: Code content to display with typing animation
            language: Programming language for syntax highlighting
            title: Optional title/filename
            variant: Style variant (minimal, terminal, editor, glass)
            cursor_style: Cursor appearance style
            typing_speed: Speed of typing animation
            show_line_numbers: Show line numbers
            duration: Duration in seconds
            track: Track name (default: "main")
            gap_before: Gap before component in seconds (overrides track default)
            auto_generate: Auto-generate composition files after adding component (default: True)

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(
                    error="No active project. Create a project first."
                ).model_dump_json()

            try:
                component = ComponentInstance(
                    component_type="TypingCode",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "code": code,
                        "language": language,
                        "title": title,
                        "variant": variant,
                        "cursor_style": cursor_style,
                        "typing_speed": typing_speed,
                        "show_line_numbers": show_line_numbers,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                # Auto-generate composition files if requested
                if auto_generate:
                    try:
                        project_manager.generate_composition()
                    except Exception as gen_error:
                        # Log but don't fail - component was added successfully
                        logger.warning(f"Auto-generation failed: {gen_error}")

                lines = len(code.split("\n"))
                return CodeComponentResponse(
                    component="TypingCode",
                    language=language or "text",
                    lines=lines,
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
