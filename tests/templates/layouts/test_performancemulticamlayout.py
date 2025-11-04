"""
Tests for PerformanceMultiCamLayout template generation.
"""

import pytest

from ..conftest import (
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check,
    assert_valid_typescript,
)

pytestmark = pytest.mark.skip(reason="Component not yet migrated to modular structure")


class TestPerformanceMultiCamLayoutBasic:
    """Basic PerformanceMultiCamLayout generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic PerformanceMultiCamLayout generation."""
        tsx = component_builder.build_component("PerformanceMultiCamLayout", {}, theme_name)

        assert tsx is not None
        assert "PerformanceMultiCamLayout" in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, "PerformanceMultiCamLayout")
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_named_props(self, component_builder, theme_name):
        """Test uses named props (frontCam, overheadCam, handCam, detailCam)."""
        tsx = component_builder.build_component("PerformanceMultiCamLayout", {}, theme_name)

        assert "frontCam" in tsx
        assert "overheadCam" in tsx
        assert "handCam" in tsx
        assert "detailCam" in tsx
