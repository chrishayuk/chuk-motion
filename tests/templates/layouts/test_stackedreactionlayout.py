"""
Tests for StackedReactionLayout template generation.
"""

import pytest

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)

pytestmark = pytest.mark.skip(reason="Component not yet migrated to modular structure")


class TestStackedReactionLayoutBasic:
    """Basic StackedReactionLayout generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic StackedReactionLayout generation."""
        tsx = component_builder.build_component("StackedReactionLayout", {}, theme_name)

        assert tsx is not None
        assert "StackedReactionLayout" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "StackedReactionLayout")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_named_props(self, component_builder, theme_name):
        """Test uses named props (originalClip, reactorFace)."""
        tsx = component_builder.build_component("StackedReactionLayout", {}, theme_name)

        assert "originalClip" in tsx
        assert "reactorFace" in tsx
