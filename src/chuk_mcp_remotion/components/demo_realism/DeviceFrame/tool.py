"""MCP tool registration for DeviceFrame component."""

from .schema import METADATA, DeviceFrameProps


def register_tool(mcp, project_manager):
    """Register the DeviceFrame MCP tool."""

    @mcp.tool
    async def remotion_add_device_frame(
        startFrame: int,
        durationInFrames: int,
        device: str = "phone",
        content: str = "",
        orientation: str = "portrait",
        scale: float = 1.0,
        glare: bool = True,
        shadow: bool = True,
        position: str = "center",
    ) -> str:
        """Add a DeviceFrame component to the composition."""
        props = DeviceFrameProps(
            startFrame=startFrame,
            durationInFrames=durationInFrames,
            device=device,  # type: ignore[arg-type]
            content=content,
            orientation=orientation,  # type: ignore[arg-type]
            scale=scale,
            glare=glare,
            shadow=shadow,
            position=position,  # type: ignore[arg-type]
        )

        project = project_manager.get_active_project()
        track_name = "device_frames"
        project.add_component_to_track(
            track_name=track_name,
            component_type=METADATA.name,
            props=props.model_dump(),
            start_frame=startFrame,
            duration=durationInFrames,
        )

        return f"Added {METADATA.name} component: {device} device in {orientation} orientation at {position}"
