"""
Tests for ComponentBuilder class and infrastructure.
"""

import pytest


class TestComponentBuilderInit:
    """Tests for ComponentBuilder initialization."""

    def test_builder_creation(self, component_builder):
        """Test ComponentBuilder can be created."""
        assert component_builder is not None

    def test_template_dir_exists(self, component_builder):
        """Test component directory exists."""
        assert component_builder.components_dir.exists()
        assert component_builder.components_dir.is_dir()

    def test_jinja_env_configured(self, component_builder):
        """Test Jinja2 environment is properly configured."""
        env = component_builder.env
        assert env is not None
        assert env.loader is not None


class TestJinjaConfiguration:
    """Tests for Jinja2 environment configuration."""

    def test_custom_delimiters(self, component_builder):
        """Test custom delimiters to avoid JSX conflicts."""
        env = component_builder.env

        # Should use [[ ]] for variables instead of {{ }}
        assert env.variable_start_string == "[["
        assert env.variable_end_string == "]]"

        # Should use [% %] for blocks instead of {% %}
        assert env.block_start_string == "[%"
        assert env.block_end_string == "%]"

    def test_trim_blocks_enabled(self, component_builder):
        """Test trim_blocks is enabled for clean output."""
        assert component_builder.env.trim_blocks is True

    def test_lstrip_blocks_enabled(self, component_builder):
        """Test lstrip_blocks is enabled."""
        assert component_builder.env.lstrip_blocks is True

    def test_autoescape_disabled(self, component_builder):
        """Test autoescape is disabled for TSX code."""
        assert component_builder.env.autoescape is False


class TestCustomFilters:
    """Tests for custom Jinja2 filters."""

    def test_filters_registered(self, component_builder):
        """Test custom filters are registered."""
        assert "to_camel_case" in component_builder.env.filters
        assert "to_pascal_case" in component_builder.env.filters

    def test_to_camel_case_filter(self, component_builder):
        """Test to_camel_case filter functionality."""
        camel_case = component_builder.env.filters["to_camel_case"]

        assert camel_case("hello_world") == "helloWorld"
        assert camel_case("some_long_name") == "someLongName"
        assert camel_case("one") == "one"
        assert camel_case("a_b_c_d") == "aBCD"

    def test_to_pascal_case_filter(self, component_builder):
        """Test to_pascal_case filter functionality."""
        pascal_case = component_builder.env.filters["to_pascal_case"]

        assert pascal_case("hello_world") == "HelloWorld"
        assert pascal_case("some_long_name") == "SomeLongName"
        assert pascal_case("one") == "One"
        assert pascal_case("a_b_c_d") == "ABCD"


class TestTemplateDiscovery:
    """Tests for template file discovery."""

    def test_find_overlay_template(self, component_builder):
        """Test finding template in overlays directory."""
        path = component_builder._find_template("TitleScene")
        assert path == "overlays/TitleScene/template.tsx.j2"

    def test_find_content_template(self, component_builder):
        """Test finding template in code directory."""
        path = component_builder._find_template("CodeBlock")
        assert path == "code/CodeBlock/template.tsx.j2"

    def test_find_layout_template(self, component_builder):
        """Test finding template in layouts directory."""
        path = component_builder._find_template("Grid")
        assert path == "layouts/Grid/template.tsx.j2"

    def test_find_nonexistent_template(self, component_builder):
        """Test error handling for nonexistent template."""
        with pytest.raises(ValueError, match="not found"):
            component_builder._find_template("NonexistentComponent")


class TestBuildComponent:
    """Tests for build_component method."""

    def test_build_with_theme(self, component_builder, theme_name):
        """Test building component with theme."""
        tsx = component_builder.build_component("TitleScene", {"title": "Test"}, theme_name)

        assert tsx is not None
        assert isinstance(tsx, str)
        assert len(tsx) > 0

    def test_build_with_config(self, component_builder, theme_name):
        """Test config dict is passed to template."""
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Custom Title", "variant": "bold"}, theme_name
        )

        # Config values should be used in generation
        assert tsx is not None

    def test_build_with_invalid_template(self, component_builder, theme_name):
        """Test error handling for invalid template."""
        with pytest.raises(ValueError):
            component_builder.build_component("InvalidComponent", {}, theme_name)


class TestThemeIntegration:
    """Tests for theme integration in component building."""

    def test_theme_passed_to_template(self, component_builder, theme_name):
        """Test theme data is passed to template."""
        tsx = component_builder.build_component("LowerThird", {"name": "Test"}, theme_name)

        # Theme colors should be injected
        assert "#" in tsx  # Hex colors from theme

    def test_all_themes_work(self, component_builder, all_themes):
        """Test component can be built with all themes."""
        for theme in all_themes:
            tsx = component_builder.build_component("TitleScene", {"title": "Test"}, theme)

            assert tsx is not None
            assert "[[" not in tsx  # No unresolved vars


class TestTemplateCategories:
    """Tests for template category organization."""

    def test_template_categories_defined(self, component_builder):
        """Test template categories are defined."""
        assert component_builder.template_categories is not None
        assert isinstance(component_builder.template_categories, list)
        assert len(component_builder.template_categories) > 0

    def test_expected_categories_present(self, component_builder):
        """Test expected categories are present."""
        categories = component_builder.template_categories

        assert "layouts" in categories
        assert "overlays" in categories
        assert "content" in categories


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_theme_name(self, component_builder):
        """Test handling of invalid theme name."""
        # Should use default/fallback theme
        tsx = component_builder.build_component(
            "TitleScene", {"title": "Test"}, "nonexistent_theme"
        )

        # Should still generate something (fallback to tech theme)
        assert tsx is not None

    def test_empty_config(self, component_builder, theme_name):
        """Test handling of empty config dict."""
        tsx = component_builder.build_component("TitleScene", {}, theme_name)

        # Should use template defaults
        assert tsx is not None
