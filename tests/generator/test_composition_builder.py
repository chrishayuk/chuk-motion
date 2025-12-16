"""Tests for CompositionBuilder."""

from chuk_motion.generator.composition_builder import (
    ComponentInstance,
    CompositionBuilder,
    snake_to_camel,
)


class TestSnakeToCamel:
    """Test snake_to_camel utility function."""

    def test_single_word(self):
        """Test single word conversion."""
        assert snake_to_camel("hello") == "hello"

    def test_two_words(self):
        """Test two word conversion."""
        assert snake_to_camel("hello_world") == "helloWorld"

    def test_multiple_words(self):
        """Test multiple word conversion."""
        assert snake_to_camel("some_long_name") == "someLongName"

    def test_already_camel_case(self):
        """Test already camelCase string."""
        assert snake_to_camel("helloWorld") == "helloWorld"


class TestComponentInstance:
    """Test ComponentInstance dataclass."""

    def test_component_instance_creation(self):
        """Test creating ComponentInstance."""
        comp = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=90,
            props={"text": "Hello"},
            layer=0,
        )

        assert comp.component_type == "TitleScene"
        assert comp.start_frame == 0
        assert comp.duration_frames == 90
        assert comp.props == {"text": "Hello"}
        assert comp.layer == 0

    def test_component_instance_defaults(self):
        """Test ComponentInstance default values."""
        comp = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=90,
        )

        assert comp.props == {}
        assert comp.layer == 0


class TestCompositionBuilderInitialization:
    """Test CompositionBuilder initialization."""

    def test_default_initialization(self):
        """Test default initialization values."""
        builder = CompositionBuilder()

        assert builder.fps == 30
        assert builder.width == 1920
        assert builder.height == 1080
        assert builder.transparent is False
        assert builder.theme == "tech"
        assert builder.components == []

    def test_custom_initialization(self):
        """Test custom initialization values."""
        builder = CompositionBuilder(fps=60, width=1280, height=720, transparent=True)

        assert builder.fps == 60
        assert builder.width == 1280
        assert builder.height == 720
        assert builder.transparent is True


class TestCompositionBuilderTimeConversion:
    """Test time conversion methods."""

    def test_seconds_to_frames(self):
        """Test converting seconds to frames."""
        builder = CompositionBuilder(fps=30)

        assert builder.seconds_to_frames(1.0) == 30
        assert builder.seconds_to_frames(2.5) == 75
        assert builder.seconds_to_frames(0.0) == 0

    def test_frames_to_seconds(self):
        """Test converting frames to seconds."""
        builder = CompositionBuilder(fps=30)

        assert builder.frames_to_seconds(30) == 1.0
        assert builder.frames_to_seconds(75) == 2.5
        assert builder.frames_to_seconds(0) == 0.0


class TestCompositionBuilderDuration:
    """Test duration calculation methods."""

    def test_get_total_duration_empty(self):
        """Test duration of empty composition."""
        builder = CompositionBuilder()

        assert builder.get_total_duration_frames() == 0
        assert builder.get_total_duration_seconds() == 0.0

    def test_get_total_duration_single_component(self):
        """Test duration with single component."""
        builder = CompositionBuilder(fps=30)
        builder.components.append(
            ComponentInstance(
                component_type="TitleScene",
                start_frame=0,
                duration_frames=90,
            )
        )

        assert builder.get_total_duration_frames() == 90
        assert builder.get_total_duration_seconds() == 3.0

    def test_get_total_duration_multiple_components(self):
        """Test duration with multiple components."""
        builder = CompositionBuilder(fps=30)
        builder.components.extend(
            [
                ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90),
                ComponentInstance(component_type="TitleScene", start_frame=90, duration_frames=60),
            ]
        )

        assert builder.get_total_duration_frames() == 150
        assert builder.get_total_duration_seconds() == 5.0

    def test_get_total_duration_overlapping_components(self):
        """Test duration with overlapping components."""
        builder = CompositionBuilder(fps=30)
        builder.components.extend(
            [
                ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90),
                ComponentInstance(
                    component_type="TextOverlay", start_frame=30, duration_frames=90, layer=10
                ),
            ]
        )

        # Total is max(0+90, 30+90) = 120 frames
        assert builder.get_total_duration_frames() == 120


class TestCompositionBuilderNextStartFrame:
    """Test _get_next_start_frame method."""

    def test_next_start_frame_empty(self):
        """Test next start frame for empty composition."""
        builder = CompositionBuilder()

        assert builder._get_next_start_frame() == 0

    def test_next_start_frame_with_components(self):
        """Test next start frame with existing components."""
        builder = CompositionBuilder(fps=30)
        builder.components.append(
            ComponentInstance(
                component_type="TitleScene",
                start_frame=0,
                duration_frames=90,
                layer=0,
            )
        )

        assert builder._get_next_start_frame() == 90

    def test_next_start_frame_ignores_non_layer_zero(self):
        """Test next start frame ignores overlay components."""
        builder = CompositionBuilder(fps=30)
        builder.components.extend(
            [
                ComponentInstance(
                    component_type="TitleScene", start_frame=0, duration_frames=90, layer=0
                ),
                ComponentInstance(
                    component_type="TextOverlay", start_frame=0, duration_frames=180, layer=10
                ),
            ]
        )

        # Should only consider layer 0 components
        assert builder._get_next_start_frame() == 90

    def test_next_start_frame_no_layer_zero_components(self):
        """Test next start frame when no layer 0 components exist."""
        builder = CompositionBuilder(fps=30)
        builder.components.append(
            ComponentInstance(
                component_type="TextOverlay",
                start_frame=0,
                duration_frames=90,
                layer=10,
            )
        )

        assert builder._get_next_start_frame() == 0


class TestCompositionBuilderFindComponentTypes:
    """Test _find_all_component_types method."""

    def test_find_types_simple(self):
        """Test finding component types in simple components."""
        builder = CompositionBuilder()
        components = [
            ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90),
            ComponentInstance(component_type="LineChart", start_frame=90, duration_frames=60),
        ]

        types = builder._find_all_component_types(components)

        assert "TitleScene" in types
        assert "LineChart" in types
        assert len(types) == 2

    def test_find_types_with_nested_children(self):
        """Test finding component types including nested children."""
        builder = CompositionBuilder()

        child = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        container = ComponentInstance(
            component_type="Container",
            start_frame=0,
            duration_frames=90,
            props={"children": child},
        )

        types = builder._find_all_component_types([container])

        assert "Container" in types
        assert "CodeBlock" in types

    def test_find_types_with_children_array(self):
        """Test finding types with children array."""
        builder = CompositionBuilder()

        children = [
            ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90),
            ComponentInstance(component_type="LineChart", start_frame=0, duration_frames=90),
        ]
        grid = ComponentInstance(
            component_type="Grid",
            start_frame=0,
            duration_frames=90,
            props={"children": children},
        )

        types = builder._find_all_component_types([grid])

        assert "Grid" in types
        assert "TitleScene" in types
        assert "LineChart" in types


class TestCompositionBuilderFindNestedChildren:
    """Test _find_nested_children method."""

    def test_find_nested_children_simple(self):
        """Test finding nested children in simple layout."""
        builder = CompositionBuilder()

        child = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        container = ComponentInstance(
            component_type="Container",
            start_frame=0,
            duration_frames=90,
            props={"children": child},
        )

        nested = builder._find_nested_children([container])

        assert id(child) in nested

    def test_find_nested_children_array(self):
        """Test finding nested children in array."""
        builder = CompositionBuilder()

        child1 = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        child2 = ComponentInstance(component_type="LineChart", start_frame=0, duration_frames=90)
        grid = ComponentInstance(
            component_type="Grid",
            start_frame=0,
            duration_frames=90,
            props={"children": [child1, child2]},
        )

        nested = builder._find_nested_children([grid])

        assert id(child1) in nested
        assert id(child2) in nested


class TestCompositionBuilderFormatPropValue:
    """Test _format_prop_value method."""

    def test_format_string(self):
        """Test formatting string values."""
        builder = CompositionBuilder()

        result = builder._format_prop_value("hello")
        assert result == "{`hello`}"

    def test_format_string_with_special_chars(self):
        """Test formatting string with special characters."""
        builder = CompositionBuilder()

        result = builder._format_prop_value("hello`world")
        assert result == "{`hello\\`world`}"

    def test_format_boolean(self):
        """Test formatting boolean values."""
        builder = CompositionBuilder()

        assert builder._format_prop_value(True) == "{true}"
        assert builder._format_prop_value(False) == "{false}"

    def test_format_integer(self):
        """Test formatting integer values."""
        builder = CompositionBuilder()

        assert builder._format_prop_value(42) == "{42}"

    def test_format_float(self):
        """Test formatting float values."""
        builder = CompositionBuilder()

        assert builder._format_prop_value(3.14) == "{3.14}"

    def test_format_dict(self):
        """Test formatting dict values."""
        builder = CompositionBuilder()

        result = builder._format_prop_value({"key": "value"})
        # Result is wrapped in {} for JSX
        assert result == '{{"key": "value"}}'

    def test_format_list(self):
        """Test formatting list values."""
        builder = CompositionBuilder()

        result = builder._format_prop_value([1, 2, 3])
        assert result == "{[1, 2, 3]}"


class TestCompositionBuilderSerializeValue:
    """Test _serialize_value method."""

    def test_serialize_primitive_types(self):
        """Test serializing primitive types."""
        builder = CompositionBuilder()

        assert builder._serialize_value(42) == 42
        assert builder._serialize_value("hello") == "hello"
        assert builder._serialize_value(True) is True
        assert builder._serialize_value(3.14) == 3.14

    def test_serialize_dict(self):
        """Test serializing dict."""
        builder = CompositionBuilder()

        result = builder._serialize_value({"key": "value"})
        assert result == {"key": "value"}

    def test_serialize_list(self):
        """Test serializing list."""
        builder = CompositionBuilder()

        result = builder._serialize_value([1, 2, 3])
        assert result == [1, 2, 3]

    def test_serialize_tuple(self):
        """Test serializing tuple to list."""
        builder = CompositionBuilder()

        result = builder._serialize_value((1, 2, 3))
        assert result == [1, 2, 3]


class TestCompositionBuilderRenderSimpleComponent:
    """Test _render_simple_component method."""

    def test_render_simple_component_no_props(self):
        """Test rendering simple component without props."""
        builder = CompositionBuilder()
        comp = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=90,
        )

        jsx = builder._render_simple_component(comp, indent=0)

        assert "<TitleScene" in jsx
        assert "startFrame={0}" in jsx
        assert "durationInFrames={90}" in jsx

    def test_render_simple_component_with_props(self):
        """Test rendering simple component with props."""
        builder = CompositionBuilder()
        comp = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=90,
            props={"text": "Hello", "font_size": 48},
        )

        jsx = builder._render_simple_component(comp, indent=0)

        assert "<TitleScene" in jsx
        assert "text={`Hello`}" in jsx
        # snake_case should be converted to camelCase
        assert "fontSize={48}" in jsx


class TestCompositionBuilderRenderLayoutComponent:
    """Test _render_layout_component method."""

    def test_render_grid_component(self):
        """Test rendering Grid component with children."""
        builder = CompositionBuilder()
        children = [
            ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90),
            ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90),
        ]
        grid = ComponentInstance(
            component_type="Grid",
            start_frame=0,
            duration_frames=90,
            props={"children": children, "columns": 2},
        )

        jsx = builder._render_layout_component(grid, indent=0)

        assert "<Grid" in jsx
        assert "</Grid>" in jsx
        assert "TitleScene" in jsx
        assert "CodeBlock" in jsx

    def test_render_container_component(self):
        """Test rendering Container component with single child."""
        builder = CompositionBuilder()
        child = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        container = ComponentInstance(
            component_type="Container",
            start_frame=0,
            duration_frames=90,
            props={"children": child},
        )

        jsx = builder._render_layout_component(container, indent=0)

        assert "<Container" in jsx
        assert "</Container>" in jsx
        assert "CodeBlock" in jsx

    def test_render_split_screen_horizontal(self):
        """Test rendering horizontal SplitScreen."""
        builder = CompositionBuilder()
        left = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        right = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        split = ComponentInstance(
            component_type="SplitScreen",
            start_frame=0,
            duration_frames=90,
            props={"left": left, "right": right, "orientation": "horizontal"},
        )

        jsx = builder._render_layout_component(split, indent=0)

        assert "<SplitScreen" in jsx
        assert "left={" in jsx
        assert "right={" in jsx
        assert "CodeBlock" in jsx
        assert "TitleScene" in jsx

    def test_render_split_screen_vertical(self):
        """Test rendering vertical SplitScreen."""
        builder = CompositionBuilder()
        top = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        bottom = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        split = ComponentInstance(
            component_type="SplitScreen",
            start_frame=0,
            duration_frames=90,
            props={"top": top, "bottom": bottom, "orientation": "vertical"},
        )

        jsx = builder._render_layout_component(split, indent=0)

        assert "<SplitScreen" in jsx
        assert "top={" in jsx
        assert "bottom={" in jsx


class TestCompositionBuilderGenerateTsx:
    """Test generate_composition_tsx method."""

    def test_generate_tsx_empty(self):
        """Test generating TSX for empty composition."""
        builder = CompositionBuilder()
        tsx = builder.generate_composition_tsx()

        assert "import React from 'react'" in tsx
        assert "import { AbsoluteFill } from 'remotion'" in tsx
        assert "VideoComposition" in tsx
        assert "theme: string" in tsx

    def test_generate_tsx_with_transparent_background(self):
        """Test generating TSX with transparent background."""
        builder = CompositionBuilder(transparent=True)
        tsx = builder.generate_composition_tsx()

        assert "transparent" in tsx

    def test_generate_tsx_with_black_background(self):
        """Test generating TSX with black background."""
        builder = CompositionBuilder(transparent=False)
        tsx = builder.generate_composition_tsx()

        assert "#000" in tsx

    def test_generate_tsx_with_components(self):
        """Test generating TSX with components."""
        builder = CompositionBuilder()
        builder.components.append(
            ComponentInstance(
                component_type="TitleScene",
                start_frame=0,
                duration_frames=90,
                props={"text": "Hello"},
            )
        )

        tsx = builder.generate_composition_tsx()

        assert "import { TitleScene }" in tsx
        assert "<TitleScene" in tsx
        assert "Hello" in tsx


class TestCompositionBuilderToDict:
    """Test to_dict method."""

    def test_to_dict_empty(self):
        """Test serializing empty composition."""
        builder = CompositionBuilder(fps=30, width=1920, height=1080)
        builder.theme = "finance"

        result = builder.to_dict()

        assert result["fps"] == 30
        assert result["width"] == 1920
        assert result["height"] == 1080
        assert result["theme"] == "finance"
        assert result["duration_frames"] == 0
        assert result["duration_seconds"] == 0.0
        assert result["components"] == []

    def test_to_dict_with_components(self):
        """Test serializing composition with components."""
        builder = CompositionBuilder(fps=30)
        builder.components.append(
            ComponentInstance(
                component_type="TitleScene",
                start_frame=0,
                duration_frames=90,
                props={"text": "Hello"},
            )
        )

        result = builder.to_dict()

        assert len(result["components"]) == 1
        assert result["components"][0]["type"] == "TitleScene"
        assert result["components"][0]["start_frame"] == 0
        assert result["components"][0]["duration_frames"] == 90
        assert result["components"][0]["props"]["text"] == "Hello"


class TestCompositionBuilderCustomRenderer:
    """Test custom renderer functionality."""

    def test_try_custom_renderer_none_registered(self):
        """Test custom renderer when none registered."""
        builder = CompositionBuilder()
        comp = ComponentInstance(
            component_type="TitleScene",
            start_frame=0,
            duration_frames=90,
        )

        result = builder._try_custom_renderer(comp, indent=0)

        assert result is None

    def test_try_custom_renderer_registered(self):
        """Test custom renderer when registered."""
        builder = CompositionBuilder()

        def custom_renderer(comp, render_fn, indent, snake_to_camel_fn, format_prop_fn):
            return "<CustomRendered />"

        # Register custom renderer
        CompositionBuilder._component_renderers["TitleScene"] = custom_renderer

        try:
            comp = ComponentInstance(
                component_type="TitleScene",
                start_frame=0,
                duration_frames=90,
            )

            result = builder._try_custom_renderer(comp, indent=0)

            assert result == "<CustomRendered />"
        finally:
            # Clean up
            del CompositionBuilder._component_renderers["TitleScene"]


class TestCompositionBuilderMoreLayouts:
    """Test rendering more layout component types."""

    def test_render_three_column_layout(self):
        """Test rendering ThreeColumnLayout."""
        builder = CompositionBuilder()
        left = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        center = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        right = ComponentInstance(component_type="LineChart", start_frame=0, duration_frames=90)
        layout = ComponentInstance(
            component_type="ThreeColumnLayout",
            start_frame=0,
            duration_frames=90,
            props={"left": left, "center": center, "right": right},
        )

        jsx = builder._render_layout_component(layout, indent=0)

        assert "<ThreeColumnLayout" in jsx
        assert "CodeBlock" in jsx
        assert "TitleScene" in jsx
        assert "LineChart" in jsx

    def test_render_three_row_layout(self):
        """Test rendering ThreeRowLayout."""
        builder = CompositionBuilder()
        top = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        middle = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        bottom = ComponentInstance(component_type="LineChart", start_frame=0, duration_frames=90)
        layout = ComponentInstance(
            component_type="ThreeRowLayout",
            start_frame=0,
            duration_frames=90,
            props={"top": top, "middle": middle, "bottom": bottom},
        )

        jsx = builder._render_layout_component(layout, indent=0)

        assert "<ThreeRowLayout" in jsx
        assert "CodeBlock" in jsx
        assert "TitleScene" in jsx
        assert "LineChart" in jsx

    def test_render_browser_frame_with_content(self):
        """Test rendering BrowserFrame with content."""
        builder = CompositionBuilder()
        content = ComponentInstance(component_type="WebPage", start_frame=0, duration_frames=90)
        frame = ComponentInstance(
            component_type="BrowserFrame",
            start_frame=0,
            duration_frames=90,
            props={"content": content, "url": "https://example.com"},
        )

        jsx = builder._render_layout_component(frame, indent=0)

        assert "<BrowserFrame" in jsx
        assert "content={" in jsx
        assert "WebPage" in jsx

    def test_render_browser_frame_without_content(self):
        """Test rendering BrowserFrame without content falls back to simple."""
        builder = CompositionBuilder()
        frame = ComponentInstance(
            component_type="BrowserFrame",
            start_frame=0,
            duration_frames=90,
            props={"url": "https://example.com"},
        )

        jsx = builder._render_layout_component(frame, indent=0)

        assert "<BrowserFrame" in jsx
        assert "/>" in jsx

    def test_render_device_frame_with_content(self):
        """Test rendering DeviceFrame with content."""
        builder = CompositionBuilder()
        content = ComponentInstance(
            component_type="ImageContent", start_frame=0, duration_frames=90
        )
        frame = ComponentInstance(
            component_type="DeviceFrame",
            start_frame=0,
            duration_frames=90,
            props={"content": content, "device_type": "iphone"},
        )

        jsx = builder._render_layout_component(frame, indent=0)

        assert "<DeviceFrame" in jsx
        assert "content={" in jsx
        assert "ImageContent" in jsx

    def test_render_terminal_with_content(self):
        """Test rendering Terminal with content."""
        builder = CompositionBuilder()
        content = ComponentInstance(component_type="TypingCode", start_frame=0, duration_frames=90)
        terminal = ComponentInstance(
            component_type="Terminal",
            start_frame=0,
            duration_frames=90,
            props={"content": content},
        )

        jsx = builder._render_layout_component(terminal, indent=0)

        assert "<Terminal" in jsx
        assert "content={" in jsx
        assert "TypingCode" in jsx

    def test_render_pixel_transition(self):
        """Test rendering PixelTransition."""
        builder = CompositionBuilder()
        first = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        second = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        transition = ComponentInstance(
            component_type="PixelTransition",
            start_frame=0,
            duration_frames=90,
            props={"firstContent": first, "secondContent": second},
        )

        jsx = builder._render_layout_component(transition, indent=0)

        assert "<PixelTransition" in jsx
        assert "firstContent={" in jsx
        assert "secondContent={" in jsx
        assert "TitleScene" in jsx
        assert "CodeBlock" in jsx

    def test_render_layout_transition(self):
        """Test rendering LayoutTransition."""
        builder = CompositionBuilder()
        before = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        after = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        transition = ComponentInstance(
            component_type="LayoutTransition",
            start_frame=0,
            duration_frames=90,
            props={"before": before, "after": after},
        )

        jsx = builder._render_layout_component(transition, indent=0)

        assert "<LayoutTransition" in jsx
        assert "before={" in jsx
        assert "after={" in jsx
        assert "TitleScene" in jsx
        assert "CodeBlock" in jsx

    def test_render_panel_cascade(self):
        """Test rendering PanelCascade."""
        builder = CompositionBuilder()
        panels = [
            ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90),
            ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90),
        ]
        cascade = ComponentInstance(
            component_type="PanelCascade",
            start_frame=0,
            duration_frames=90,
            props={"panels": panels},
        )

        jsx = builder._render_layout_component(cascade, indent=0)

        assert "<PanelCascade" in jsx
        assert "panels={[" in jsx
        assert "TitleScene" in jsx
        assert "CodeBlock" in jsx

    def test_render_text_overlay_with_content(self):
        """Test rendering TextOverlay with content."""
        builder = CompositionBuilder()
        content = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        overlay = ComponentInstance(
            component_type="TextOverlay",
            start_frame=0,
            duration_frames=90,
            props={"content": content, "text": "Hello"},
        )

        jsx = builder._render_layout_component(overlay, indent=0)

        assert "<TextOverlay" in jsx
        assert "</TextOverlay>" in jsx
        assert "CodeBlock" in jsx

    def test_render_text_overlay_without_content(self):
        """Test rendering TextOverlay without content."""
        builder = CompositionBuilder()
        overlay = ComponentInstance(
            component_type="TextOverlay",
            start_frame=0,
            duration_frames=90,
            props={"text": "Hello"},
        )

        jsx = builder._render_layout_component(overlay, indent=0)

        assert "<TextOverlay" in jsx
        assert "/>" in jsx

    def test_render_layout_entrance_with_content(self):
        """Test rendering LayoutEntrance with content."""
        builder = CompositionBuilder()
        content = ComponentInstance(component_type="Grid", start_frame=0, duration_frames=90)
        entrance = ComponentInstance(
            component_type="LayoutEntrance",
            start_frame=0,
            duration_frames=90,
            props={"content": content},
        )

        jsx = builder._render_layout_component(entrance, indent=0)

        assert "<LayoutEntrance" in jsx
        assert "</LayoutEntrance>" in jsx
        assert "Grid" in jsx

    def test_render_container_with_multiple_children(self):
        """Test rendering Container with multiple children."""
        builder = CompositionBuilder()
        children = [
            ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90),
            ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90),
        ]
        container = ComponentInstance(
            component_type="Container",
            start_frame=0,
            duration_frames=90,
            props={"children": children},
        )

        jsx = builder._render_layout_component(container, indent=0)

        assert "<Container" in jsx
        assert "</Container>" in jsx
        assert "TitleScene" in jsx
        assert "CodeBlock" in jsx

    def test_render_container_empty_children(self):
        """Test rendering Container with empty children array."""
        builder = CompositionBuilder()
        container = ComponentInstance(
            component_type="Container",
            start_frame=0,
            duration_frames=90,
            props={"children": []},
        )

        jsx = builder._render_layout_component(container, indent=0)

        assert "<Container" in jsx
        assert "</Container>" in jsx

    def test_render_component_jsx_uses_custom_renderer(self):
        """Test that _render_component_jsx uses custom renderer first."""
        builder = CompositionBuilder()

        def custom_renderer(comp, render_fn, indent, snake_to_camel_fn, format_prop_fn):
            return "<CustomComponent />"

        CompositionBuilder._component_renderers["TitleScene"] = custom_renderer

        try:
            comp = ComponentInstance(
                component_type="TitleScene",
                start_frame=0,
                duration_frames=90,
            )

            jsx = builder._render_component_jsx(comp, indent=0)

            assert jsx == "<CustomComponent />"
        finally:
            del CompositionBuilder._component_renderers["TitleScene"]

    def test_render_component_jsx_fallback_to_simple(self):
        """Test that unknown components render as simple components."""
        builder = CompositionBuilder()
        comp = ComponentInstance(
            component_type="UnknownComponent",
            start_frame=0,
            duration_frames=90,
            props={"text": "Hello"},
        )

        jsx = builder._render_component_jsx(comp, indent=0)

        assert "<UnknownComponent" in jsx
        assert "/>" in jsx


class TestCompositionBuilderFindTypesAdvanced:
    """Test finding types in complex nested structures."""

    def test_find_types_split_screen_left_right(self):
        """Test finding types in SplitScreen left/right."""
        builder = CompositionBuilder()
        left = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        right = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        split = ComponentInstance(
            component_type="SplitScreen",
            start_frame=0,
            duration_frames=90,
            props={"left": left, "right": right},
        )

        types = builder._find_all_component_types([split])

        assert "SplitScreen" in types
        assert "CodeBlock" in types
        assert "TitleScene" in types

    def test_find_types_specialized_layout_keys(self):
        """Test finding types with specialized layout keys."""
        builder = CompositionBuilder()
        main_content = ComponentInstance(
            component_type="CodeBlock", start_frame=0, duration_frames=90
        )
        focus_content = ComponentInstance(
            component_type="TitleScene", start_frame=0, duration_frames=90
        )
        layout = ComponentInstance(
            component_type="FocusStrip",
            start_frame=0,
            duration_frames=90,
            props={"main_content": main_content, "focus_content": focus_content},
        )

        types = builder._find_all_component_types([layout])

        assert "FocusStrip" in types
        assert "CodeBlock" in types
        assert "TitleScene" in types

    def test_find_nested_children_specialized_keys(self):
        """Test finding nested children with specialized keys."""
        builder = CompositionBuilder()
        content = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        container = ComponentInstance(
            component_type="Container",
            start_frame=0,
            duration_frames=90,
            props={"content": content},
        )

        nested = builder._find_nested_children([container])

        assert id(content) in nested


class TestCompositionBuilderSerializeAdvanced:
    """Test advanced serialization scenarios."""

    def test_serialize_pydantic_model(self):
        """Test serializing Pydantic models."""
        from pydantic import BaseModel

        class TestModel(BaseModel):
            name: str
            value: int

        builder = CompositionBuilder()
        model = TestModel(name="test", value=42)

        result = builder._serialize_value(model)

        assert result == {"name": "test", "value": 42}

    def test_serialize_dataclass(self):
        """Test serializing dataclasses."""
        from dataclasses import dataclass

        @dataclass
        class TestData:
            name: str
            value: int

        builder = CompositionBuilder()
        data = TestData(name="test", value=42)

        result = builder._serialize_value(data)

        assert result == {"name": "test", "value": 42}

    def test_format_prop_with_pydantic_model(self):
        """Test formatting Pydantic model as prop value."""
        from pydantic import BaseModel

        class TestModel(BaseModel):
            name: str

        builder = CompositionBuilder()
        model = TestModel(name="test")

        result = builder._format_prop_value(model)

        assert '"name"' in result
        assert '"test"' in result


class TestCompositionBuilderCustomRendererException:
    """Test custom renderer exception handling."""

    def test_custom_renderer_failure_returns_none(self):
        """Test that failing custom renderer returns None."""
        builder = CompositionBuilder()

        def failing_renderer(comp, render_fn, indent, snake_to_camel_fn, format_prop_fn):
            raise RuntimeError("Simulated failure")

        CompositionBuilder._component_renderers["TestComponent"] = failing_renderer

        try:
            comp = ComponentInstance(
                component_type="TestComponent",
                start_frame=0,
                duration_frames=90,
            )

            result = builder._try_custom_renderer(comp, indent=0)

            # Should return None when renderer fails
            assert result is None
        finally:
            del CompositionBuilder._component_renderers["TestComponent"]


class TestCompositionBuilderMoreLayoutTypes:
    """Test more layout component types for better coverage."""

    def test_render_mosaic_with_clips(self):
        """Test rendering Mosaic with clips array."""
        builder = CompositionBuilder()
        clips = [
            ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90),
            ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90),
        ]
        mosaic = ComponentInstance(
            component_type="Mosaic",
            start_frame=0,
            duration_frames=90,
            props={"clips": clips},
        )

        jsx = builder._render_layout_component(mosaic, indent=0)

        assert "<Mosaic" in jsx
        assert "clips={[" in jsx
        assert "content:" in jsx

    def test_render_three_by_three_grid(self):
        """Test rendering ThreeByThreeGrid with cells."""
        builder = CompositionBuilder()
        cells = [
            ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
            for _ in range(9)
        ]
        grid = ComponentInstance(
            component_type="ThreeByThreeGrid",
            start_frame=0,
            duration_frames=90,
            props={"children": cells},
        )

        jsx = builder._render_layout_component(grid, indent=0)

        assert "<ThreeByThreeGrid" in jsx
        assert "children={[" in jsx

    def test_render_asymmetric_layout(self):
        """Test rendering AsymmetricLayout."""
        builder = CompositionBuilder()
        main = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        top_side = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        bottom_side = ComponentInstance(
            component_type="LineChart", start_frame=0, duration_frames=90
        )
        layout = ComponentInstance(
            component_type="AsymmetricLayout",
            start_frame=0,
            duration_frames=90,
            props={"main": main, "top_side": top_side, "bottom_side": bottom_side},
        )

        jsx = builder._render_layout_component(layout, indent=0)

        assert "<AsymmetricLayout" in jsx
        assert "main={" in jsx

    def test_render_over_the_shoulder(self):
        """Test rendering OverTheShoulder layout."""
        builder = CompositionBuilder()
        screen = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        overlay = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        layout = ComponentInstance(
            component_type="OverTheShoulder",
            start_frame=0,
            duration_frames=90,
            props={"screen_content": screen, "shoulder_overlay": overlay},
        )

        jsx = builder._render_layout_component(layout, indent=0)

        assert "<OverTheShoulder" in jsx

    def test_render_dialogue_frame(self):
        """Test rendering DialogueFrame layout."""
        builder = CompositionBuilder()
        left = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        center = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        right = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        layout = ComponentInstance(
            component_type="DialogueFrame",
            start_frame=0,
            duration_frames=90,
            props={"left_speaker": left, "center_content": center, "right_speaker": right},
        )

        jsx = builder._render_layout_component(layout, indent=0)

        assert "<DialogueFrame" in jsx

    def test_render_hud_style(self):
        """Test rendering HUDStyle layout."""
        builder = CompositionBuilder()
        main = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        layout = ComponentInstance(
            component_type="HUDStyle",
            start_frame=0,
            duration_frames=90,
            props={"main_content": main},
        )

        jsx = builder._render_layout_component(layout, indent=0)

        assert "<HUDStyle" in jsx

    def test_render_pip(self):
        """Test rendering PiP (Picture-in-Picture) layout."""
        builder = CompositionBuilder()
        main = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        pip = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        layout = ComponentInstance(
            component_type="PiP",
            start_frame=0,
            duration_frames=90,
            props={"main_content": main, "pip_content": pip},
        )

        jsx = builder._render_layout_component(layout, indent=0)

        assert "<PiP" in jsx

    def test_render_vertical_layout(self):
        """Test rendering Vertical layout - not all layouts have children support."""
        builder = CompositionBuilder()
        layout = ComponentInstance(
            component_type="Vertical",
            start_frame=0,
            duration_frames=90,
            props={"gap": 20},
        )

        jsx = builder._render_layout_component(layout, indent=0)

        # Vertical is a simple component without nested children support
        assert "<Vertical" in jsx
        assert "/>" in jsx

    def test_render_timeline_layout(self):
        """Test rendering Timeline layout."""
        builder = CompositionBuilder()
        children = [
            ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90),
        ]
        layout = ComponentInstance(
            component_type="Timeline",
            start_frame=0,
            duration_frames=90,
            props={"children": children},
        )

        jsx = builder._render_layout_component(layout, indent=0)

        assert "<Timeline" in jsx

    def test_render_performance_multi_cam(self):
        """Test rendering PerformanceMultiCam layout."""
        builder = CompositionBuilder()
        primary = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        secondary = [
            ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90),
        ]
        layout = ComponentInstance(
            component_type="PerformanceMultiCam",
            start_frame=0,
            duration_frames=90,
            props={"primary_cam": primary, "secondary_cams": secondary},
        )

        jsx = builder._render_layout_component(layout, indent=0)

        assert "<PerformanceMultiCam" in jsx

    def test_render_lower_third_with_content(self):
        """Test rendering LowerThird with content."""
        builder = CompositionBuilder()
        content = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        overlay = ComponentInstance(
            component_type="LowerThird",
            start_frame=0,
            duration_frames=90,
            props={"content": content, "name": "Test"},
        )

        jsx = builder._render_layout_component(overlay, indent=0)

        assert "<LowerThird" in jsx
        assert "</LowerThird>" in jsx
        assert "CodeBlock" in jsx

    def test_render_subscribe_button_with_content(self):
        """Test rendering SubscribeButton with content."""
        builder = CompositionBuilder()
        content = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        overlay = ComponentInstance(
            component_type="SubscribeButton",
            start_frame=0,
            duration_frames=90,
            props={"content": content},
        )

        jsx = builder._render_layout_component(overlay, indent=0)

        assert "<SubscribeButton" in jsx
        assert "</SubscribeButton>" in jsx

    def test_render_with_extra_props(self):
        """Test rendering layout with extra non-child props."""
        builder = CompositionBuilder()
        left = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        right = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        split = ComponentInstance(
            component_type="SplitScreen",
            start_frame=0,
            duration_frames=90,
            props={
                "left": left,
                "right": right,
                "ratio": 0.6,
                "gap": 10,
            },
        )

        jsx = builder._render_layout_component(split, indent=0)

        assert "<SplitScreen" in jsx
        assert "ratio={0.6}" in jsx
        assert "gap={10}" in jsx


class TestCompositionBuilderSpecializedLayouts:
    """Test specialized layout prop keys."""

    def test_find_nested_children_focus_content(self):
        """Test finding nested children in focus_content prop."""
        builder = CompositionBuilder()
        focus = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        layout = ComponentInstance(
            component_type="FocusStrip",
            start_frame=0,
            duration_frames=90,
            props={"focus_content": focus},
        )

        nested = builder._find_nested_children([layout])

        assert id(focus) in nested

    def test_find_nested_children_demo_props(self):
        """Test finding nested children in demo1/demo2 props."""
        builder = CompositionBuilder()
        demo1 = ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        demo2 = ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90)
        layout = ComponentInstance(
            component_type="AsymmetricLayout",
            start_frame=0,
            duration_frames=90,
            props={"demo1": demo1, "demo2": demo2},
        )

        nested = builder._find_nested_children([layout])

        assert id(demo1) in nested
        assert id(demo2) in nested

    def test_find_types_with_array_prop(self):
        """Test finding types with array specialized props."""
        builder = CompositionBuilder()
        clips = [
            ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90),
            ComponentInstance(component_type="CodeBlock", start_frame=0, duration_frames=90),
        ]
        mosaic = ComponentInstance(
            component_type="Mosaic",
            start_frame=0,
            duration_frames=90,
            props={"clips": clips},
        )

        types = builder._find_all_component_types([mosaic])

        assert "Mosaic" in types
        assert "TitleScene" in types
        assert "CodeBlock" in types
