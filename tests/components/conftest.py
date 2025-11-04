"""
Shared fixtures for component template tests.
"""

import pytest

from chuk_mcp_remotion.generator.component_builder import ComponentBuilder
from chuk_mcp_remotion.themes.youtube_themes import YOUTUBE_THEMES


@pytest.fixture
def component_builder():
    """Create a ComponentBuilder instance."""
    return ComponentBuilder()


@pytest.fixture
def theme_name():
    """Default theme for testing."""
    return "tech"


@pytest.fixture
def tech_theme():
    """Get the tech theme."""
    return YOUTUBE_THEMES["tech"]


@pytest.fixture
def all_themes():
    """Get all available themes."""
    return list(YOUTUBE_THEMES.keys())


def assert_valid_typescript(tsx: str):
    """Common assertions for TypeScript validity."""
    # No unresolved template variables
    assert "[[" not in tsx, "Found unresolved template variables"
    assert "]]" not in tsx, "Found unresolved template variables"
    assert "[%" not in tsx, "Found unresolved template blocks"
    assert "%]" not in tsx, "Found unresolved template blocks"

    # Has proper imports
    assert "from 'react'" in tsx, "Missing React import"
    assert "from 'remotion'" in tsx, "Missing Remotion import"

    # Has balanced JSX tags for common elements
    assert tsx.count("<AbsoluteFill") == tsx.count("</AbsoluteFill>"), (
        "Unbalanced AbsoluteFill tags"
    )


def assert_has_interface(tsx: str, component_name: str):
    """Assert component has proper TypeScript interface."""
    assert f"interface {component_name}Props" in tsx, f"Missing {component_name}Props interface"
    assert f"React.FC<{component_name}Props>" in tsx, "Missing React.FC type"


def assert_has_timing_props(tsx: str):
    """Assert component has frame-based timing props."""
    assert "startFrame" in tsx, "Missing startFrame prop"
    assert "durationInFrames" in tsx, "Missing durationInFrames prop"


def assert_has_visibility_check(tsx: str):
    """Assert component has frame-based visibility check."""
    assert "frame < startFrame" in tsx, "Missing startFrame check"
    assert "frame >= startFrame + durationInFrames" in tsx, "Missing durationInFrames check"
    assert "return null" in tsx, "Missing early return"


def assert_design_tokens_injected(tsx: str):
    """Assert design tokens are properly injected (not template variables)."""
    # Should have hex colors (design tokens injected)
    assert "#" in tsx, "No color values found"
    # Should not have unresolved variables
    assert "[[" not in tsx, "Unresolved template variables"
