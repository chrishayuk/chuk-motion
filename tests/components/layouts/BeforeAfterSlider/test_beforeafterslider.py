"""Tests for BeforeAfterSlider template generation."""

from tests.components.conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestBeforeAfterSliderBasic:
    """Basic BeforeAfterSlider generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic BeforeAfterSlider generation."""
        tsx = component_builder.build_component("BeforeAfterSlider", {}, theme_name)
        assert tsx is not None
        assert "BeforeAfterSlider" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "BeforeAfterSlider")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestBeforeAfterSliderBuilderMethod:
    """Tests for BeforeAfterSlider builder method."""

    def test_add_to_composition_basic(self):
        """Test add_to_composition creates ComponentInstance."""
        from chuk_motion.components.layouts.BeforeAfterSlider.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        result = add_to_composition(
            builder,
            start_time=0.0,
            duration=5.0,
            before_image="before.jpg",
            after_image="after.jpg"
        )

        assert result is builder
        assert len(builder.components) == 1
        assert builder.components[0].component_type == "BeforeAfterSlider"

    def test_add_to_composition_all_props(self):
        """Test all props are set correctly."""
        from chuk_motion.components.layouts.BeforeAfterSlider.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder()
        add_to_composition(
            builder,
            start_time=1.0,
            duration=10.0,
            before_image="before.jpg",
            after_image="after.jpg",
            before_label="Old",
            after_label="New",
            orientation="vertical",
            slider_position=75.0,
            animate_slider=False,
            slider_start_position=10.0,
            slider_end_position=90.0,
            show_labels=False,
            label_position="bottom",
            handle_style="circle",
            width=1400,
            height=900,
            position="top-left",
            border_radius=20,
        )

        props = builder.components[0].props
        assert props["beforeImage"] == "before.jpg"
        assert props["afterImage"] == "after.jpg"
        assert props["beforeLabel"] == "Old"
        assert props["afterLabel"] == "New"
        assert props["orientation"] == "vertical"
        assert props["sliderPosition"] == 75.0
        assert props["animateSlider"] is False
        assert props["sliderStartPosition"] == 10.0
        assert props["sliderEndPosition"] == 90.0
        assert props["showLabels"] is False
        assert props["labelPosition"] == "bottom"
        assert props["handleStyle"] == "circle"
        assert props["width"] == 1400
        assert props["height"] == 900
        assert props["position"] == "top-left"
        assert props["borderRadius"] == 20

    def test_add_to_composition_timing(self):
        """Test add_to_composition handles timing correctly."""
        from chuk_motion.components.layouts.BeforeAfterSlider.builder import (
            add_to_composition,
        )
        from chuk_motion.generator.composition_builder import CompositionBuilder

        builder = CompositionBuilder(fps=30)
        add_to_composition(
            builder,
            start_time=2.0,
            duration=5.0,
            before_image="before.jpg",
            after_image="after.jpg"
        )

        component = builder.components[0]
        assert component.start_frame == 60  # 2.0 * 30fps
        assert component.duration_frames == 150  # 5.0 * 30fps


class TestBeforeAfterSliderToolRegistration:
    """Tests for BeforeAfterSlider MCP tool registration."""

    def test_register_tool(self):
        """Test tool registration."""
        from unittest.mock import Mock

        from chuk_motion.components.layouts.BeforeAfterSlider.tool import register_tool

        mcp_mock = Mock()
        pm_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        mcp_mock.tool.assert_called_once()

    def test_tool_execution(self):
        """Test tool execution."""
        import asyncio
        from unittest.mock import Mock

        from chuk_motion.components.layouts.BeforeAfterSlider.tool import register_tool

        # Mock ProjectManager and Project
        pm_mock = Mock()
        project_mock = Mock()
        project_mock.add_component_to_track = Mock()
        pm_mock.get_active_project = Mock(return_value=project_mock)

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)

        tool_func = mcp_mock.tool.call_args[0][0]

        # Execute with all parameters
        result = asyncio.run(tool_func(
            startFrame=0,
            durationInFrames=150,
            beforeImage="before.jpg",
            afterImage="after.jpg",
            beforeLabel="Before",
            afterLabel="After",
            orientation="horizontal",
            sliderPosition=50.0,
            animateSlider=True,
            sliderStartPosition=0.0,
            sliderEndPosition=100.0,
            showLabels=True,
            labelPosition="overlay",
            handleStyle="default",
            width=1200,
            height=800,
            position="center",
            borderRadius=12
        ))

        # Parse JSON response
        import json
        response = json.loads(result)

        # Check LayoutComponentResponse structure
        assert response["component"] == "BeforeAfterSlider"
        assert "layout" in response
        assert "start_time" in response
        assert "duration" in response

        # Verify component was added
        project_mock.add_component_to_track.assert_called_once()

    def test_tool_execution_no_project(self):
        """Test tool execution without active project."""
        import asyncio
        import tempfile
        from unittest.mock import Mock

        from chuk_motion.components.layouts.BeforeAfterSlider.tool import register_tool
        from chuk_motion.utils.project_manager import ProjectManager

        with tempfile.TemporaryDirectory() as tmpdir:
            pm = ProjectManager(tmpdir)
            # Don't create or set active project

            mcp_mock = Mock()
            register_tool(mcp_mock, pm)

            tool_func = mcp_mock.tool.call_args[0][0]

            # Should return an error response when no project is set
            result = asyncio.run(tool_func(
                startFrame=0,
                durationInFrames=150,
                beforeImage="before.jpg",
                afterImage="after.jpg"
            ))

            import json
            response = json.loads(result)
            assert "error" in response

    def test_tool_execution_error_handling(self):
        """Test tool handles errors gracefully."""
        import asyncio
        from unittest.mock import Mock

        from chuk_motion.components.layouts.BeforeAfterSlider.tool import register_tool

        # Mock ProjectManager that raises an error
        pm_mock = Mock()
        pm_mock.get_active_project = Mock(side_effect=Exception("Test error"))

        mcp_mock = Mock()
        register_tool(mcp_mock, pm_mock)
        tool_func = mcp_mock.tool.call_args[0][0]

        # The error should propagate
        try:
            result = asyncio.run(tool_func(
                startFrame=0,
                durationInFrames=150,
                beforeImage="before.jpg",
                afterImage="after.jpg"
            ))
            # If we get here, check for error in result
            if result:
                assert "error" in result.lower() or "Test error" in result
        except Exception as e:
            # Error propagated as expected
            assert "Test error" in str(e)
