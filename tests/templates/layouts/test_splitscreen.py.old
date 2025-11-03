"""
Tests for SplitScreen layout template generation.
"""

import pytest
from ..conftest import (
    assert_valid_typescript,
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check
)


class TestSplitScreenBasic:
    """Basic SplitScreen generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic SplitScreen generation."""
        tsx = component_builder.build_component(
            'SplitScreen',
            {},
            theme_name
        )

        assert tsx is not None
        assert 'SplitScreen' in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, 'SplitScreen')
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_named_props(self, component_builder, theme_name):
        """Test uses named props (leftPanel, rightPanel)."""
        tsx = component_builder.build_component(
            'SplitScreen',
            {},
            theme_name
        )

        assert 'leftPanel' in tsx
        assert 'rightPanel' in tsx
