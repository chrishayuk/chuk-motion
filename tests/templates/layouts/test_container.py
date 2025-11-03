"""
Tests for Container template generation.
"""

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)


class TestContainerBasic:
    """Basic Container generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic Container generation."""
        tsx = component_builder.build_component("Container", {}, theme_name)

        assert tsx is not None
        assert "Container" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "Container")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_children_handling(self, component_builder, theme_name):
        """Test handles children."""
        tsx = component_builder.build_component("Container", {}, theme_name)

        assert "children" in tsx
