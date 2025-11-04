"""
Tests for DemoBox template generation.
"""

import pytest

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)

pytestmark = pytest.mark.skip(reason="Component not yet migrated to modular structure")


class TestDemoBoxBasic:
    """Basic DemoBox generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic DemoBox generation."""
        tsx = component_builder.build_component(
            "DemoBox", {"label": "Test Box", "color": "primary"}, theme_name
        )

        assert tsx is not None
        assert "DemoBox" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "DemoBox")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test DemoBox with minimal props."""
        tsx = component_builder.build_component("DemoBox", {}, theme_name)

        assert tsx is not None
        # Should have defaults
        assert 'label = "DEMO"' in tsx or "label = " in tsx
        assert 'color = "primary"' in tsx or "color = " in tsx


class TestDemoBoxColors:
    """Tests for DemoBox color variants."""

    @pytest.mark.parametrize("color", ["primary", "secondary", "accent"])
    def test_color_variant(self, component_builder, theme_name, color):
        """Test each color variant."""
        tsx = component_builder.build_component("DemoBox", {"color": color}, theme_name)

        assert tsx is not None
        assert color in tsx
        assert "colorMap" in tsx

    def test_color_mapping(self, component_builder, theme_name):
        """Test color mapping is defined."""
        tsx = component_builder.build_component("DemoBox", {}, theme_name)

        assert "colorMap" in tsx
        assert "primary:" in tsx
        assert "secondary:" in tsx
        assert "accent:" in tsx


class TestDemoBoxStyling:
    """Tests for DemoBox styling."""

    def test_gradient_background(self, component_builder, theme_name):
        """Test has gradient background."""
        tsx = component_builder.build_component("DemoBox", {}, theme_name)

        assert "background" in tsx
        assert "linear-gradient" in tsx

    def test_border_styling(self, component_builder, theme_name):
        """Test has border."""
        tsx = component_builder.build_component("DemoBox", {}, theme_name)

        assert "border:" in tsx
        assert "borderRadius" in tsx

    def test_text_styling(self, component_builder, theme_name):
        """Test text is styled."""
        tsx = component_builder.build_component("DemoBox", {}, theme_name)

        assert "fontSize" in tsx
        assert "fontWeight" in tsx
        assert "textTransform" in tsx
        assert "letterSpacing" in tsx


class TestDemoBoxContent:
    """Tests for DemoBox content."""

    def test_label_prop(self, component_builder, theme_name):
        """Test label prop is used."""
        tsx = component_builder.build_component("DemoBox", {"label": "Custom Label"}, theme_name)

        assert "label" in tsx
        assert "{label}" in tsx

    def test_centering(self, component_builder, theme_name):
        """Test content is centered."""
        tsx = component_builder.build_component("DemoBox", {}, theme_name)

        assert "display: " in tsx
        assert "alignItems: " in tsx
        assert "justifyContent: " in tsx
