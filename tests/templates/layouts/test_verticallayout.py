"""
Tests for VerticalLayout template generation.
"""

import pytest

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)

pytestmark = pytest.mark.skip(reason="Component not yet migrated to modular structure")


class TestVerticalLayoutBasic:
    """Basic VerticalLayout generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic VerticalLayout generation."""
        tsx = component_builder.build_component("VerticalLayout", {}, theme_name)

        assert tsx is not None
        assert "VerticalLayout" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "VerticalLayout")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_named_props(self, component_builder, theme_name):
        """Test uses named props (topContent, bottomContent, captionBar)."""
        tsx = component_builder.build_component("VerticalLayout", {}, theme_name)

        assert "topContent" in tsx
        assert "bottomContent" in tsx
        assert "captionBar" in tsx
