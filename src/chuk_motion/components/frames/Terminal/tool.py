"""MCP tool registration for Terminal component."""

from chuk_motion.models import ErrorResponse, FrameComponentResponse


def register_tool(mcp, project_manager):
    """Register the Terminal MCP tool."""

    @mcp.tool
    async def remotion_add_terminal(
        duration: float,
        commands: str = "[]",
        prompt: str = "bash",
        custom_prompt: str = "$",
        title: str = "Terminal",
        theme: str = "dark",
        width: int = 900,
        height: int = 600,
        position: str = "center",
        show_cursor: bool = True,
        type_speed: float = 0.05,
    ) -> str:
        """
        Add a Terminal component to the composition.

        Animated terminal/command-line interface with typing effect.

        Args:
            duration: Duration in seconds
            commands: JSON array of command objects with input/output
            prompt: Prompt style (bash, zsh, etc.)
            custom_prompt: Custom prompt string
            title: Terminal window title
            theme: Color theme (dark, light, etc.)
            width: Terminal width in pixels
            height: Terminal height in pixels
            position: Position on screen
            show_cursor: Show blinking cursor
            type_speed: Typing animation speed

        Returns:
            JSON with component info
        """
        if not project_manager.current_timeline:
            return ErrorResponse(
                error="No active project. Create a project first."
            ).model_dump_json()

        try:
            builder = project_manager.current_timeline
            start_time = builder.get_total_duration_seconds()

            builder.add_terminal(
                start_time=start_time,
                duration=duration,
                commands=commands,
                prompt=prompt,
                custom_prompt=custom_prompt,
                title=title,
                theme=theme,
                width=width,
                height=height,
                position=position,
                show_cursor=show_cursor,
                type_speed=type_speed,
            )

            return FrameComponentResponse(
                component="Terminal",
                position=position,
                theme=theme,
                start_time=start_time,
                duration=duration,
            ).model_dump_json()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()
