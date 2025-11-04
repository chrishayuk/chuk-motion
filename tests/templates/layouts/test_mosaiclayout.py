"""
Tests for MosaicLayout template generation.
"""

import pytest

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)

pytestmark = pytest.mark.skip(reason="Component not yet migrated to modular structure")


class TestMosaicLayoutBasic:
    """Basic MosaicLayout generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic MosaicLayout generation."""
        tsx = component_builder.build_component("MosaicLayout", {}, theme_name)

        assert tsx is not None
        assert "MosaicLayout" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "MosaicLayout")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_children_handling(self, component_builder, theme_name):
        """Test handles children."""
        tsx = component_builder.build_component("MosaicLayout", {}, theme_name)

        assert "children" in tsx
