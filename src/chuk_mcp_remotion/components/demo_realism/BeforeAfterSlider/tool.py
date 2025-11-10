"""MCP tool registration for BeforeAfterSlider component."""

from .schema import METADATA, BeforeAfterSliderProps


def register_tool(mcp, project_manager):
    """Register the BeforeAfterSlider MCP tool."""

    @mcp.tool
    async def remotion_add_before_after_slider(
        startFrame: int,
        durationInFrames: int,
        beforeImage: str,
        afterImage: str,
        beforeLabel: str = "Before",
        afterLabel: str = "After",
        orientation: str = "horizontal",
        sliderPosition: float = 50.0,
        animateSlider: bool = True,
        sliderStartPosition: float = 0.0,
        sliderEndPosition: float = 100.0,
        showLabels: bool = True,
        labelPosition: str = "overlay",
        handleStyle: str = "default",
        width: int = 1200,
        height: int = 800,
        position: str = "center",
        borderRadius: int = 12,
    ) -> str:
        """Add a BeforeAfterSlider component to the composition."""
        props = BeforeAfterSliderProps(
            startFrame=startFrame,
            durationInFrames=durationInFrames,
            beforeImage=beforeImage,
            afterImage=afterImage,
            beforeLabel=beforeLabel,
            afterLabel=afterLabel,
            orientation=orientation,  # type: ignore[arg-type]
            sliderPosition=sliderPosition,
            animateSlider=animateSlider,
            sliderStartPosition=sliderStartPosition,
            sliderEndPosition=sliderEndPosition,
            showLabels=showLabels,
            labelPosition=labelPosition,  # type: ignore[arg-type]
            handleStyle=handleStyle,  # type: ignore[arg-type]
            width=width,
            height=height,
            position=position,  # type: ignore[arg-type]
            borderRadius=borderRadius,
        )

        project = project_manager.get_active_project()
        track_name = "comparisons"
        project.add_component_to_track(
            track_name=track_name,
            component_type=METADATA.name,
            props=props.model_dump(),
            start_frame=startFrame,
            duration=durationInFrames,
        )

        return f"Added {METADATA.name} component: {orientation} slider at {position}"
