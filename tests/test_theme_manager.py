# chuk-mcp-remotion/tests/test_theme_manager.py
"""
Tests for ThemeManager class.
"""

import json

import pytest

from chuk_mcp_remotion.themes.models import Theme
from chuk_mcp_remotion.themes.theme_manager import ThemeManager


class TestTheme:
    """Test Theme class (Pydantic model)."""

    def test_theme_creation(self, sample_theme):
        """Test creating a theme from Pydantic models."""
        assert sample_theme.name == "Test Theme"
        assert sample_theme.description == "A test theme"
        assert len(sample_theme.colors.primary) == 3
        assert len(sample_theme.use_cases) == 2

    def test_theme_to_dict(self, sample_theme):
        """Test converting theme to dictionary using model_dump()."""
        theme_dict = sample_theme.model_dump()

        assert isinstance(theme_dict, dict)
        assert "name" in theme_dict
        assert "description" in theme_dict
        assert "colors" in theme_dict
        assert "typography" in theme_dict
        assert "motion" in theme_dict

    def test_theme_roundtrip(self, sample_theme):
        """Test that model_dump and Theme(**dict) are inverses."""
        theme_dict = sample_theme.model_dump()
        theme2 = Theme(**theme_dict)

        assert sample_theme.name == theme2.name
        assert sample_theme.description == theme2.description
        assert sample_theme.colors.primary == theme2.colors.primary


class TestThemeManagerInit:
    """Test ThemeManager initialization."""

    @pytest.mark.asyncio
    async def test_manager_creation(self, vfs):
        """Test that ThemeManager can be created."""
        manager = ThemeManager(vfs)
        assert manager is not None
        assert isinstance(manager.themes, dict)

    @pytest.mark.asyncio
    async def test_builtin_themes_loaded(self, theme_manager):
        """Test that built-in themes are loaded on init."""
        themes = theme_manager.list_themes()

        assert len(themes) > 0
        assert "tech" in themes
        assert "finance" in themes
        assert "education" in themes

    @pytest.mark.asyncio
    async def test_all_seven_themes_present(self, theme_manager):
        """Test that all 7 YouTube themes are present."""
        themes = theme_manager.list_themes()
        expected = ["tech", "finance", "education", "lifestyle", "gaming", "minimal", "business"]

        assert len(themes) == 7
        for theme in expected:
            assert theme in themes

    @pytest.mark.asyncio
    async def test_current_theme_initially_none(self, theme_manager):
        """Test that current theme is None on init."""
        assert theme_manager.get_current_theme() is None


class TestThemeManagerRegistry:
    """Test theme registration and retrieval."""

    def test_register_theme(self, theme_manager, sample_theme):
        """Test registering a custom theme."""
        theme_manager.register_theme("custom", sample_theme)

        themes = theme_manager.list_themes()
        assert "custom" in themes

    def test_get_existing_theme(self, theme_manager):
        """Test getting an existing theme."""
        theme = theme_manager.get_theme("tech")

        assert theme is not None
        assert isinstance(theme, Theme)
        assert theme.name == "Tech"

    def test_get_nonexistent_theme(self, theme_manager):
        """Test getting a non-existent theme returns None."""
        theme = theme_manager.get_theme("nonexistent")
        assert theme is None

    def test_list_themes_returns_keys(self, theme_manager):
        """Test that list_themes returns theme keys."""
        themes = theme_manager.list_themes()

        assert isinstance(themes, list)
        assert all(isinstance(t, str) for t in themes)


class TestThemeManagerInfo:
    """Test get_theme_info method."""

    def test_get_theme_info_structure(self, theme_manager):
        """Test theme info structure."""
        info = theme_manager.get_theme_info("tech")

        assert info is not None
        assert "name" in info
        assert "description" in info
        assert "colors" in info
        assert "typography" in info
        assert "motion" in info
        assert "use_cases" in info

    def test_get_theme_info_colors(self, theme_manager):
        """Test that theme info includes all color categories."""
        info = theme_manager.get_theme_info("tech")
        colors = info["colors"]

        assert "primary" in colors
        assert "accent" in colors
        assert "gradient" in colors
        assert "background" in colors
        assert "text" in colors
        assert "semantic" in colors

    def test_get_theme_info_nonexistent(self, theme_manager):
        """Test getting info for non-existent theme."""
        info = theme_manager.get_theme_info("nonexistent")
        assert info is None


class TestThemeManagerCurrentTheme:
    """Test current theme management."""

    def test_set_current_theme_valid(self, theme_manager):
        """Test setting a valid current theme."""
        success = theme_manager.set_current_theme("tech")

        assert success is True
        assert theme_manager.get_current_theme() == "tech"

    def test_set_current_theme_invalid(self, theme_manager):
        """Test setting an invalid current theme."""
        success = theme_manager.set_current_theme("nonexistent")

        assert success is False
        assert theme_manager.get_current_theme() is None

    def test_change_current_theme(self, theme_manager):
        """Test changing the current theme."""
        theme_manager.set_current_theme("tech")
        assert theme_manager.get_current_theme() == "tech"

        theme_manager.set_current_theme("gaming")
        assert theme_manager.get_current_theme() == "gaming"


class TestThemeManagerComparison:
    """Test theme comparison."""

    def test_compare_two_themes(self, theme_manager):
        """Test comparing two valid themes."""
        comparison = theme_manager.compare_themes("tech", "gaming")

        assert "themes" in comparison
        assert "comparison" in comparison
        assert comparison["themes"] == ["tech", "gaming"]

    def test_comparison_structure(self, theme_manager):
        """Test comparison result structure."""
        comparison = theme_manager.compare_themes("tech", "finance")
        comp = comparison["comparison"]

        assert "names" in comp
        assert "descriptions" in comp
        assert "primary_colors" in comp
        assert "accent_colors" in comp
        assert "motion_feel" in comp
        assert "use_cases" in comp

        # Each should be a 2-element list
        assert len(comp["names"]) == 2
        assert len(comp["primary_colors"]) == 2

    def test_compare_nonexistent_theme(self, theme_manager):
        """Test comparing with non-existent theme."""
        comparison = theme_manager.compare_themes("tech", "nonexistent")

        assert "error" in comparison


class TestThemeManagerSearch:
    """Test theme search functionality."""

    def test_search_by_name(self, theme_manager):
        """Test searching themes by name."""
        results = theme_manager.search_themes("tech")

        assert "tech" in results

    def test_search_by_description(self, theme_manager):
        """Test searching themes by description."""
        # "gaming" should be in gaming theme description
        results = theme_manager.search_themes("gaming")

        assert "gaming" in results

    def test_search_by_use_case(self, theme_manager):
        """Test searching themes by use case."""
        # Search for a use case
        results = theme_manager.search_themes("professional")

        # Should find business and/or minimal themes
        assert len(results) > 0

    def test_search_case_insensitive(self, theme_manager):
        """Test that search is case-insensitive."""
        results_lower = theme_manager.search_themes("tech")
        results_upper = theme_manager.search_themes("TECH")

        assert results_lower == results_upper

    def test_search_no_matches(self, theme_manager):
        """Test search with no matches."""
        results = theme_manager.search_themes("xyznonexistent")

        assert len(results) == 0

    def test_get_themes_by_category(self, theme_manager):
        """Test getting themes by category."""
        # This is an alias for search_themes
        results = theme_manager.get_themes_by_category("education")

        assert "education" in results


class TestThemeManagerValidation:
    """Test theme validation."""

    def test_validate_valid_theme(self, theme_manager, sample_theme):
        """Test validating a valid theme."""
        # Convert to dict for validation
        theme_dict = sample_theme.model_dump()
        validation = theme_manager.validate_theme(theme_dict)

        assert validation["valid"] is True
        assert len(validation["errors"]) == 0

    def test_validate_missing_required_key(self, theme_manager):
        """Test validating theme missing required keys."""
        invalid_theme = {
            "name": "Test",
            "description": "Test theme",
            # Missing colors, typography, motion, spacing
        }

        validation = theme_manager.validate_theme(invalid_theme)

        assert validation["valid"] is False
        assert len(validation["errors"]) > 0

    def test_validate_missing_color_tokens(self, theme_manager, sample_theme):
        """Test validating theme with incomplete color tokens."""
        theme_dict = sample_theme.model_dump()
        del theme_dict["colors"]["primary"]

        validation = theme_manager.validate_theme(theme_dict)

        assert validation["valid"] is False
        assert any("primary" in error for error in validation["errors"])

    def test_validate_missing_typography_tokens(self, theme_manager, sample_theme):
        """Test validating theme with incomplete typography tokens."""
        theme_dict = sample_theme.model_dump()
        del theme_dict["typography"]["primary_font"]

        validation = theme_manager.validate_theme(theme_dict)

        assert validation["valid"] is False

    def test_validate_missing_motion_tokens(self, theme_manager, sample_theme):
        """Test validating theme with incomplete motion tokens."""
        theme_dict = sample_theme.model_dump()
        del theme_dict["motion"]["default_spring"]

        validation = theme_manager.validate_theme(theme_dict)

        assert validation["valid"] is False


class TestThemeManagerExportImport:
    """Test theme export and import."""

    @pytest.mark.asyncio
    async def test_export_theme(self, theme_manager):
        """Test exporting a theme to file."""
        export_path = "exported_theme.json"

        result = await theme_manager.export_theme("tech", export_path)

        assert "Error" not in result
        assert result == export_path

        # Check file content
        content = await theme_manager.vfs.read_text(export_path)
        data = json.loads(content)
        assert data["name"] == "Tech"

    @pytest.mark.asyncio
    async def test_export_nonexistent_theme(self, theme_manager):
        """Test exporting non-existent theme."""
        export_path = "exported.json"

        result = await theme_manager.export_theme("nonexistent", export_path)

        assert "Error" in result

    @pytest.mark.asyncio
    async def test_import_theme(self, theme_manager, sample_theme):
        """Test importing a theme from file."""
        # Create a file in vfs with properly formatted theme
        theme_dict = sample_theme.model_dump()
        await theme_manager.vfs.write_file("test_theme.json", json.dumps(theme_dict))

        result = await theme_manager.import_theme("test_theme.json", "imported")

        assert "Successfully imported" in result
        assert "imported" in theme_manager.list_themes()

    @pytest.mark.asyncio
    async def test_import_invalid_theme(self, theme_manager, invalid_theme_data):
        """Test importing invalid theme."""
        await theme_manager.vfs.write_file("invalid_theme.json", json.dumps(invalid_theme_data))

        result = await theme_manager.import_theme("invalid_theme.json", "invalid")

        assert "Error" in result

    @pytest.mark.asyncio
    async def test_import_nonexistent_file(self, theme_manager):
        """Test importing from non-existent file."""
        result = await theme_manager.import_theme("/nonexistent/file.json")

        assert "Error" in result

    @pytest.mark.asyncio
    async def test_export_import_roundtrip(self, theme_manager):
        """Test export then import preserves theme."""
        export_path = "roundtrip.json"

        # Export
        await theme_manager.export_theme("tech", export_path)

        # Import
        await theme_manager.import_theme(export_path, "reimported_tech")

        # Verify
        original = theme_manager.get_theme_info("tech")
        reimported = theme_manager.get_theme_info("reimported_tech")

        assert original["name"] == reimported["name"]
        assert original["description"] == reimported["description"]


class TestThemeManagerCustomThemes:
    """Test custom theme creation."""

    def test_create_custom_theme_from_scratch(self, theme_manager):
        """Test creating custom theme requires base theme now."""
        # With Pydantic models, we require a base_theme to ensure valid structure
        result = theme_manager.create_custom_theme(
            name="Custom",
            description="A custom theme",
        )

        # Should error without base_theme
        assert "Error" in result

    def test_create_custom_theme_from_base(self, theme_manager):
        """Test creating custom theme based on existing theme."""
        result = theme_manager.create_custom_theme(
            name="Custom Tech",
            description="Tech with custom colors",
            base_theme="tech",
            color_overrides={"primary": ["#FF0000", "#CC0000", "#990000"]},
        )

        assert "Error" not in result
        theme_key = result

        theme_info = theme_manager.get_theme_info(theme_key)
        assert theme_info["colors"]["primary"][0] == "#FF0000"

    def test_create_custom_theme_invalid(self, theme_manager):
        """Test creating invalid custom theme without base."""
        result = theme_manager.create_custom_theme(
            name="No Base", description="No base theme provided"
        )

        # Should fail without base theme
        assert "Error" in result

    def test_custom_theme_key_format(self, theme_manager):
        """Test that custom theme keys are formatted correctly."""
        result = theme_manager.create_custom_theme(
            name="My Custom Theme", description="Test", base_theme="tech"
        )

        assert result == "my_custom_theme"  # Spaces should become underscores


class TestThemeManagerEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_theme_list_after_init(self, theme_manager):
        """Test that theme list is never empty after init."""
        themes = theme_manager.list_themes()
        assert len(themes) > 0

    def test_register_duplicate_theme_key(self, theme_manager, sample_theme):
        """Test registering theme with duplicate key overwrites."""
        theme_manager.register_theme("custom", sample_theme)

        # Register again with same key
        new_theme = Theme(
            name="New Theme",
            description="Different theme",
            colors=sample_theme.colors,
            typography=sample_theme.typography,
            motion=sample_theme.motion,
            spacing=sample_theme.spacing,
        )
        theme_manager.register_theme("custom", new_theme)

        # Should be overwritten
        theme = theme_manager.get_theme("custom")
        assert theme.name == "New Theme"

    def test_validate_empty_theme(self, theme_manager):
        """Test validating completely empty theme."""
        validation = theme_manager.validate_theme({})

        assert validation["valid"] is False
        assert len(validation["errors"]) > 0

    @pytest.mark.asyncio
    async def test_export_with_default_filename(self, theme_manager):
        """Test export with default filename."""
        result = await theme_manager.export_theme("tech")

        # Should create file with default name
        assert "Error" not in result
        assert "tech_theme.json" in result
