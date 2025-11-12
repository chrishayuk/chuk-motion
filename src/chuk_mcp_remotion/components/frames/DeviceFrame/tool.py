"""MCP tool registration for DeviceFrame component."""

from chuk_mcp_remotion.models import ErrorResponse, FrameComponentResponse

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
        """
        Add a DeviceFrame component to the composition.

        Realistic device mockup (phone, tablet, laptop) with content inside.

        Args:
            startFrame: Frame to start showing the component
            durationInFrames: How many frames to show the component
            device: Device type (phone, tablet, laptop, desktop)
            content: Content to display inside device
            orientation: Device orientation (portrait, landscape)
            scale: Scale factor for device size
            glare: Show screen glare effect
            shadow: Show device shadow
            position: Position on screen

        Returns:
            JSON with component info
        """
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

        try:
            project = project_manager.get_active_project()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()

        try:
            track_name = "device_frames"
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
                component="DeviceFrame",
                position=position,
                theme=device,
                start_time=start_seconds,
                duration=duration_seconds,
            ).model_dump_json()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()
