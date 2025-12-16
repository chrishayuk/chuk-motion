"""MCP tool registration for DeviceFrame component."""

from chuk_motion.models import ErrorResponse, FrameComponentResponse


def register_tool(mcp, project_manager):
    """Register the DeviceFrame MCP tool."""

    @mcp.tool
    async def remotion_add_device_frame(
        duration: float,
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
            duration: Duration in seconds
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
        if not project_manager.current_timeline:
            return ErrorResponse(
                error="No active project. Create a project first."
            ).model_dump_json()

        try:
            builder = project_manager.current_timeline
            start_time = builder.get_total_duration_seconds()

            builder.add_device_frame(
                start_time=start_time,
                duration=duration,
                device=device,
                content=content,
                orientation=orientation,
                scale=scale,
                glare=glare,
                shadow=shadow,
                position=position,
            )

            return FrameComponentResponse(
                component="DeviceFrame",
                position=position,
                theme=device,
                start_time=start_time,
                duration=duration,
            ).model_dump_json()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()
