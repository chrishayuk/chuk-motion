"""
Tests for LineChart template generation.
"""

import pytest
from ..conftest import (
    assert_valid_typescript,
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check
)


class TestLineChartBasic:
    """Basic LineChart generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic LineChart generation with all props."""
        tsx = component_builder.build_component(
            'LineChart',
            {
                'data_points': [10, 25, 15, 30, 40],
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                'title': 'Sales Growth',
                'xlabel': 'Month',
                'ylabel': 'Revenue'
            },
            theme_name
        )

        assert tsx is not None
        assert 'LineChart' in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, 'LineChart')
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)

    def test_minimal_props(self, component_builder, theme_name):
        """Test LineChart with minimal props."""
        tsx = component_builder.build_component(
            'LineChart',
            {},
            theme_name
        )

        assert tsx is not None
        # Should have defaults
        assert "data_points = []" in tsx or "data_points = " in tsx


class TestLineChartDataHandling:
    """Tests for data handling."""

    def test_data_points_prop(self, component_builder, theme_name):
        """Test data_points prop is used."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert 'data_points' in tsx
        assert 'dataPoints' in tsx

    def test_labels_prop(self, component_builder, theme_name):
        """Test labels prop is used."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3], 'labels': ['A', 'B', 'C']},
            theme_name
        )

        assert 'labels' in tsx

    def test_empty_data_handling(self, component_builder, theme_name):
        """Test handling of empty data."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': []},
            theme_name
        )

        assert 'dataPoints.length === 0' in tsx
        assert 'return null' in tsx


class TestLineChartSVG:
    """Tests for SVG rendering."""

    def test_svg_element(self, component_builder, theme_name):
        """Test SVG element is created."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert '<svg' in tsx
        assert 'width=' in tsx
        assert 'height=' in tsx

    def test_chart_dimensions(self, component_builder, theme_name):
        """Test chart has proper dimensions."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert 'chartWidth' in tsx
        assert 'chartHeight' in tsx
        assert 'padding' in tsx

    def test_svg_gradients(self, component_builder, theme_name):
        """Test SVG gradients are defined."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert '<defs>' in tsx
        assert 'linearGradient' in tsx
        assert 'bgGradient' in tsx
        assert 'lineGradient' in tsx

    def test_svg_filters(self, component_builder, theme_name):
        """Test SVG filters for glow effect."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert '<filter' in tsx
        assert 'feGaussianBlur' in tsx
        assert 'glow' in tsx


class TestLineChartPath:
    """Tests for line path generation."""

    def test_path_generation(self, component_builder, theme_name):
        """Test SVG path is generated."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert '<path' in tsx
        assert 'pathData' in tsx
        assert 'd={pathData}' in tsx

    def test_path_styling(self, component_builder, theme_name):
        """Test path has proper styling."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert 'stroke=' in tsx
        assert 'strokeWidth' in tsx
        assert 'strokeLinecap' in tsx
        assert 'strokeLinejoin' in tsx

    def test_coordinate_scaling(self, component_builder, theme_name):
        """Test coordinate scaling functions."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert 'scaleX' in tsx
        assert 'scaleY' in tsx


class TestLineChartAnimation:
    """Tests for chart animations."""

    def test_entrance_animation(self, component_builder, theme_name):
        """Test chart has entrance animation."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert 'entranceProgress' in tsx
        assert 'spring' in tsx
        assert 'scale' in tsx

    def test_exit_animation(self, component_builder, theme_name):
        """Test chart has exit animation."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert 'exitProgress' in tsx
        assert 'exitDuration' in tsx
        assert 'opacity' in tsx

    def test_line_drawing_animation(self, component_builder, theme_name):
        """Test line is drawn progressively."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert 'lineProgress' in tsx
        assert 'numPointsToShow' in tsx
        assert 'visiblePoints' in tsx

    def test_data_points_pulse(self, component_builder, theme_name):
        """Test data points have pulse animation."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert 'pulseScale' in tsx
        assert 'Math.sin' in tsx


class TestLineChartElements:
    """Tests for chart visual elements."""

    def test_background_rect(self, component_builder, theme_name):
        """Test chart has background."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert '<rect' in tsx
        assert 'fill=' in tsx

    def test_grid_lines(self, component_builder, theme_name):
        """Test chart has grid lines."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert '<line' in tsx
        assert 'stroke=' in tsx

    def test_axes(self, component_builder, theme_name):
        """Test chart has axes."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        # Should have x and y axes
        assert '<line' in tsx

    def test_data_point_circles(self, component_builder, theme_name):
        """Test data points are rendered as circles."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert '<circle' in tsx
        assert 'cx=' in tsx
        assert 'cy=' in tsx
        assert 'r=' in tsx


class TestLineChartLabels:
    """Tests for chart labels."""

    def test_title_optional(self, component_builder, theme_name):
        """Test title is optional."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3]},
            theme_name
        )

        assert 'title' in tsx
        assert 'title &&' in tsx

    def test_xlabel_optional(self, component_builder, theme_name):
        """Test x-axis label is optional."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3], 'xlabel': 'Time'},
            theme_name
        )

        assert 'xlabel' in tsx
        assert 'xlabel &&' in tsx
        assert '<text' in tsx

    def test_ylabel_optional(self, component_builder, theme_name):
        """Test y-axis label is optional."""
        tsx = component_builder.build_component(
            'LineChart',
            {'data_points': [1, 2, 3], 'ylabel': 'Value'},
            theme_name
        )

        assert 'ylabel' in tsx
        assert 'ylabel &&' in tsx
        assert '<text' in tsx
