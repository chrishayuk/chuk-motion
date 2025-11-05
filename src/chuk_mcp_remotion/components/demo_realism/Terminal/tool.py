"""MCP tool registration for Terminal component."""

import json
from .schema import TerminalProps, MCP_SCHEMA, METADATA


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
        """Add a Terminal component to the composition."""
        # Parse commands JSON string
        try:
            commands_parsed = json.loads(commands)
        except json.JSONDecodeError:
            commands_parsed = []

        props = TerminalProps(
            startFrame=startFrame,
            durationInFrames=durationInFrames,
            commands=commands_parsed,
            prompt=prompt,
            customPrompt=customPrompt,
            title=title,
            theme=theme,
            width=width,
            height=height,
            position=position,
            showCursor=showCursor,
            typeSpeed=typeSpeed,
        )

        project = project_manager.get_active_project()
        track_name = "terminals"
        project.add_component_to_track(
            track_name=track_name,
            component_type=METADATA.name,
            props=props.model_dump(),
            start_frame=startFrame,
            duration=durationInFrames,
        )

        cmd_count = len(commands)
        return f"Added {METADATA.name} component: {theme} theme with {cmd_count} command(s) at {position}"
