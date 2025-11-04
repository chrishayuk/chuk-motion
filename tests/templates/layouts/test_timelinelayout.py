"""
Tests for TimelineLayout template generation.
"""

import pytest

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)

pytestmark = pytest.mark.skip(reason="Component not yet migrated to modular structure")


class TestTimelineLayoutBasic:
    """Basic TimelineLayout generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic TimelineLayout generation."""
        tsx = component_builder.build_component("TimelineLayout", {}, theme_name)

        assert tsx is not None
        assert "TimelineLayout" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "TimelineLayout")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_named_props(self, component_builder, theme_name):
        """Test uses named props (mainContent, milestones)."""
        tsx = component_builder.build_component("TimelineLayout", {}, theme_name)

        assert "mainContent" in tsx
        assert "milestones" in tsx
