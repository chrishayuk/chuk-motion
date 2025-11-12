"""MCP tool registration for Terminal component."""

import json

from chuk_motion.models import ErrorResponse, FrameComponentResponse

from .schema import METADATA, TerminalProps


def register_tool(mcp, project_manager):
    """Register the Terminal MCP tool."""

    @mcp.tool
    async def remotion_add_terminal(
        startFrame: int,
        durationInFrames: int,
        commands: str = "[]",
        prompt: str = "bash",
        customPrompt: str = "$",
        title: str = "Terminal",
        theme: str = "dark",
        width: int = 900,
        height: int = 600,
        position: str = "center",
        showCursor: bool = True,
        typeSpeed: float = 0.05,
    ) -> str:
        """
        Add a Terminal component to the composition.

        Animated terminal/command-line interface with typing effect.

        Args:
            startFrame: Frame to start showing the component
            durationInFrames: How many frames to show the component
            commands: JSON array of command objects with input/output
            prompt: Prompt style (bash, zsh, etc.)
            customPrompt: Custom prompt string
            title: Terminal window title
            theme: Color theme (dark, light, etc.)
            width: Terminal width in pixels
            height: Terminal height in pixels
            position: Position on screen
            showCursor: Show blinking cursor
            typeSpeed: Typing animation speed

        Returns:
            JSON with component info
        """
        # Parse commands JSON string
        try:
            commands_parsed = json.loads(commands)
        except json.JSONDecodeError:
            commands_parsed = []

        props = TerminalProps(
            startFrame=startFrame,
            durationInFrames=durationInFrames,
            commands=commands_parsed,
            prompt=prompt,  # type: ignore[arg-type]
            customPrompt=customPrompt,
            title=title,
            theme=theme,  # type: ignore[arg-type]
            width=width,
            height=height,
            position=position,  # type: ignore[arg-type]
            showCursor=showCursor,
            typeSpeed=typeSpeed,
        )

        try:
            project = project_manager.get_active_project()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()

        try:
            track_name = "terminals"
            project.add_component_to_track(
                track_name=track_name,
                component_type=METADATA.name,
                props=props.model_dump(),
                start_frame=startFrame,
                duration=durationInFrames,
            )

            # Calculate duration in seconds (assuming 30fps)
            duration_seconds = durationInFrames / 30.0
            start_seconds = startFrame / 30.0

            return FrameComponentResponse(
                component="Terminal",
                position=position,
                theme=theme,
                start_time=start_seconds,
                duration=duration_seconds,
            ).model_dump_json()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()
