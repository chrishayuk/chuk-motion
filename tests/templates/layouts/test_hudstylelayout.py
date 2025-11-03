"""
Tests for HUDStyleLayout template generation.
"""

import pytest

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)

pytestmark = pytest.mark.skip(reason="Component not yet migrated to modular structure")


class TestHUDStyleLayoutBasic:
    """Basic HUDStyleLayout generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic HUDStyleLayout generation."""
        tsx = component_builder.build_component("HUDStyleLayout", {}, theme_name)

        assert tsx is not None
        assert "HUDStyleLayout" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "HUDStyleLayout")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_named_props(self, component_builder, theme_name):
        """Test uses named props (gameplay, webcam, chatOverlay)."""
        tsx = component_builder.build_component("HUDStyleLayout", {}, theme_name)

        assert "gameplay" in tsx
        assert "webcam" in tsx
        assert "chatOverlay" in tsx
