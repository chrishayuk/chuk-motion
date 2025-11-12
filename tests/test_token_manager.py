# chuk-motion/tests/test_token_manager.py
"""
Tests for TokenManager - token import/export functionality.
"""

import json

import pytest


class TestTokenManagerInit:
    """Test TokenManager initialization."""

    @pytest.mark.asyncio
    async def test_init_with_vfs(self, token_manager):
        """Test TokenManager initializes with virtual filesystem."""
        assert token_manager.vfs is not None
        assert token_manager.custom_typography_tokens == {}
        assert token_manager.custom_color_tokens == {}
        assert token_manager.custom_motion_tokens == {}


class TestTypographyTokenExportImport:
    """Test typography token export and import."""

    @pytest.mark.asyncio
    async def test_export_all_typography_tokens(self, token_manager):
        """Test exporting all typography tokens."""
        result = await token_manager.export_typography_tokens(
            file_path="test_typography.json", include_all=True
        )

        assert result == "test_typography.json"

        # Verify file was written
        content = await token_manager.vfs.read_text("test_typography.json")
        data = json.loads(content)

        assert "font_families" in data
        assert "font_sizes" in data
        assert "font_weights" in data

    @pytest.mark.asyncio
    async def test_export_font_families_only(self, token_manager):
        """Test exporting only font families."""
        result = await token_manager.export_typography_tokens(
            file_path="fonts_only.json", include_all=False, font_families_only=True
        )

        assert result == "fonts_only.json"

        content = await token_manager.vfs.read_text("fonts_only.json")
        data = json.loads(content)

        assert "font_families" in data
        assert "text_styles" not in data

    @pytest.mark.asyncio
    async def test_export_text_styles_only(self, token_manager):
        """Test exporting only text styles."""
        result = await token_manager.export_typography_tokens(
            file_path="styles_only.json", include_all=False, text_styles_only=True
        )

        assert result == "styles_only.json"

        content = await token_manager.vfs.read_text("styles_only.json")
        data = json.loads(content)

        assert "text_styles" in data
        assert "font_families" not in data

    @pytest.mark.asyncio
    async def test_export_with_custom_tokens(self, token_manager):
        """Test exporting includes custom tokens."""
        # Add custom tokens
        token_manager.custom_typography_tokens = {"custom_key": "custom_value"}

        await token_manager.export_typography_tokens(file_path="with_custom.json")

        content = await token_manager.vfs.read_text("with_custom.json")
        data = json.loads(content)

        assert "custom" in data
        assert data["custom"]["custom_key"] == "custom_value"

    @pytest.mark.asyncio
    async def test_export_default_filepath(self, token_manager):
        """Test exporting with default file path."""
        result = await token_manager.export_typography_tokens()

        assert result == "typography_tokens.json"
        assert await token_manager.vfs.exists("typography_tokens.json")

    @pytest.mark.asyncio
    async def test_import_typography_tokens(self, token_manager, sample_typography_tokens):
        """Test importing typography tokens."""
        # Create a file to import
        await token_manager.vfs.write_file(
            "import_typography.json", json.dumps(sample_typography_tokens)
        )

        result = await token_manager.import_typography_tokens(file_path="import_typography.json")

        assert "Successfully imported" in result
        assert token_manager.custom_typography_tokens == sample_typography_tokens

    @pytest.mark.asyncio
    async def test_import_typography_tokens_merge(self, token_manager, sample_typography_tokens):
        """Test importing typography tokens with merge."""
        # Set existing custom tokens
        token_manager.custom_typography_tokens = {"existing_key": "existing_value"}

        # Create a file to import
        await token_manager.vfs.write_file(
            "import_typography.json", json.dumps(sample_typography_tokens)
        )

        result = await token_manager.import_typography_tokens(
            file_path="import_typography.json", merge=True
        )

        assert "Successfully imported" in result
        assert "existing_key" in token_manager.custom_typography_tokens
        assert "font_families" in token_manager.custom_typography_tokens

    @pytest.mark.asyncio
    async def test_import_typography_tokens_replace(self, token_manager, sample_typography_tokens):
        """Test importing typography tokens without merge."""
        # Set existing custom tokens
        token_manager.custom_typography_tokens = {"existing_key": "existing_value"}

        # Create a file to import
        await token_manager.vfs.write_file(
            "import_typography.json", json.dumps(sample_typography_tokens)
        )

        result = await token_manager.import_typography_tokens(
            file_path="import_typography.json", merge=False
        )

        assert "Successfully imported" in result
        assert "existing_key" not in token_manager.custom_typography_tokens
        assert token_manager.custom_typography_tokens == sample_typography_tokens

    @pytest.mark.asyncio
    async def test_import_invalid_typography_tokens(self, token_manager):
        """Test importing invalid typography tokens."""
        # Create invalid file
        await token_manager.vfs.write_file("invalid_typography.json", json.dumps("not a dict"))

        result = await token_manager.import_typography_tokens(file_path="invalid_typography.json")

        assert "Error" in result


class TestColorTokenExportImport:
    """Test color token export and import."""

    @pytest.mark.asyncio
    async def test_export_all_color_tokens(self, token_manager):
        """Test exporting all color tokens."""
        result = await token_manager.export_color_tokens(file_path="test_colors.json")

        assert result == "test_colors.json"

        content = await token_manager.vfs.read_text("test_colors.json")
        data = json.loads(content)

        assert "tech" in data
        assert "finance" in data
        assert "education" in data

    @pytest.mark.asyncio
    async def test_export_specific_theme_colors(self, token_manager):
        """Test exporting specific theme colors."""
        result = await token_manager.export_color_tokens(
            file_path="tech_colors.json", theme_name="tech"
        )

        assert result == "tech_colors.json"

        content = await token_manager.vfs.read_text("tech_colors.json")
        data = json.loads(content)

        assert "tech" in data
        assert "finance" not in data

    @pytest.mark.asyncio
    async def test_export_nonexistent_theme(self, token_manager):
        """Test exporting nonexistent theme."""
        result = await token_manager.export_color_tokens(
            file_path="invalid_theme.json", theme_name="nonexistent"
        )

        assert "Error" in result
        assert "not found" in result

    @pytest.mark.asyncio
    async def test_import_color_tokens(self, token_manager, sample_color_tokens):
        """Test importing color tokens."""
        # Create a file to import
        await token_manager.vfs.write_file("import_colors.json", json.dumps(sample_color_tokens))

        result = await token_manager.import_color_tokens(file_path="import_colors.json")

        assert "Successfully imported" in result
        assert token_manager.custom_color_tokens == sample_color_tokens

    @pytest.mark.asyncio
    async def test_import_invalid_color_tokens(self, token_manager):
        """Test importing invalid color tokens."""
        await token_manager.vfs.write_file(
            "invalid_colors.json",
            json.dumps([1, 2, 3]),  # Not a dict
        )

        result = await token_manager.import_color_tokens(file_path="invalid_colors.json")

        assert "Error" in result

    @pytest.mark.asyncio
    async def test_export_color_tokens_default_filepath(self, token_manager):
        """Test exporting color tokens with default file path."""
        result = await token_manager.export_color_tokens()

        assert result == "color_tokens.json"
        assert await token_manager.vfs.exists("color_tokens.json")

    @pytest.mark.asyncio
    async def test_export_color_tokens_with_custom(self, token_manager):
        """Test exporting color tokens includes custom tokens."""
        token_manager.custom_color_tokens = {"custom_theme": {"primary": ["#FF0000"]}}

        await token_manager.export_color_tokens(file_path="colors_with_custom.json")

        content = await token_manager.vfs.read_text("colors_with_custom.json")
        data = json.loads(content)

        assert "custom" in data
        assert "custom_theme" in data["custom"]

    @pytest.mark.asyncio
    async def test_export_color_tokens_exception(self, token_manager):
        """Test export color tokens handles exceptions."""
        # Mock vfs to raise exception
        async def raise_exception(path, content):
            raise OSError("Write failed")

        token_manager.vfs.write_file = raise_exception

        result = await token_manager.export_color_tokens()

        assert "Error exporting color tokens" in result


class TestMotionTokenExportImport:
    """Test motion token export and import."""

    @pytest.mark.asyncio
    async def test_export_all_motion_tokens(self, token_manager):
        """Test exporting all motion tokens."""
        result = await token_manager.export_motion_tokens(file_path="test_motion.json")

        assert result == "test_motion.json"

        content = await token_manager.vfs.read_text("test_motion.json")
        data = json.loads(content)

        assert "spring_configs" in data
        assert "easing" in data
        assert "duration" in data

    @pytest.mark.asyncio
    async def test_export_springs_only(self, token_manager):
        """Test exporting only spring configs."""
        result = await token_manager.export_motion_tokens(
            file_path="springs_only.json", springs_only=True
        )

        assert result == "springs_only.json"

        content = await token_manager.vfs.read_text("springs_only.json")
        data = json.loads(content)

        assert "spring_configs" in data
        assert "easing_curves" not in data

    @pytest.mark.asyncio
    async def test_export_easings_only(self, token_manager):
        """Test exporting only easing curves."""
        result = await token_manager.export_motion_tokens(
            file_path="easings_only.json", easings_only=True
        )

        assert result == "easings_only.json"

        content = await token_manager.vfs.read_text("easings_only.json")
        data = json.loads(content)

        assert "easing" in data
        assert "spring_configs" not in data

    @pytest.mark.asyncio
    async def test_export_presets_only(self, token_manager):
        """Test exporting only animation presets."""
        result = await token_manager.export_motion_tokens(
            file_path="presets_only.json", presets_only=True
        )

        assert result == "presets_only.json"

        content = await token_manager.vfs.read_text("presets_only.json")
        data = json.loads(content)

        assert "enter" in data
        assert "exit" in data
        assert "spring_configs" not in data

    @pytest.mark.asyncio
    async def test_import_motion_tokens(self, token_manager, sample_motion_tokens):
        """Test importing motion tokens."""
        await token_manager.vfs.write_file("import_motion.json", json.dumps(sample_motion_tokens))

        result = await token_manager.import_motion_tokens(file_path="import_motion.json")

        assert "Successfully imported" in result
        assert token_manager.custom_motion_tokens == sample_motion_tokens

    @pytest.mark.asyncio
    async def test_export_motion_tokens_default_filepath(self, token_manager):
        """Test exporting motion tokens with default file path."""
        result = await token_manager.export_motion_tokens()

        assert result == "motion_tokens.json"
        assert await token_manager.vfs.exists("motion_tokens.json")

    @pytest.mark.asyncio
    async def test_export_motion_tokens_with_custom(self, token_manager):
        """Test exporting motion tokens includes custom tokens."""
        token_manager.custom_motion_tokens = {"custom_spring": {"stiffness": 100}}

        await token_manager.export_motion_tokens(file_path="motion_with_custom.json")

        content = await token_manager.vfs.read_text("motion_with_custom.json")
        data = json.loads(content)

        assert "custom" in data
        assert "custom_spring" in data["custom"]

    @pytest.mark.asyncio
    async def test_import_invalid_motion_tokens(self, token_manager):
        """Test importing invalid motion tokens."""
        await token_manager.vfs.write_file("invalid_motion.json", json.dumps([1, 2, 3]))

        result = await token_manager.import_motion_tokens(file_path="invalid_motion.json")

        assert "Error" in result


class TestExportAllTokens:
    """Test exporting all token types."""

    @pytest.mark.asyncio
    async def test_export_all_tokens(self, token_manager):
        """Test exporting all token types to directory."""
        result = await token_manager.export_all_tokens(output_dir="all_tokens")

        assert "typography" in result
        assert "colors" in result
        assert "motion" in result

        # Verify all files exist
        typo_content = await token_manager.vfs.read_text(result["typography"])
        color_content = await token_manager.vfs.read_text(result["colors"])
        motion_content = await token_manager.vfs.read_text(result["motion"])

        assert json.loads(typo_content)
        assert json.loads(color_content)
        assert json.loads(motion_content)


class TestTokenGetters:
    """Test token getter methods."""

    @pytest.mark.asyncio
    async def test_get_typography_token_from_default(self, token_manager):
        """Test getting typography token from defaults."""
        result = token_manager.get_typography_token("font_families", "display")

        assert result is not None
        assert "name" in result
        assert result["name"] == "Display"

    @pytest.mark.asyncio
    async def test_get_typography_token_from_custom(self, token_manager):
        """Test getting typography token from custom tokens."""
        token_manager.custom_typography_tokens = {
            "font_families": {"custom": {"name": "Custom Font"}}
        }

        result = token_manager.get_typography_token("font_families", use_custom=True)

        assert result is not None
        assert "custom" in result

    @pytest.mark.asyncio
    async def test_get_color_token_from_default(self, token_manager):
        """Test getting color token from defaults."""
        result = token_manager.get_color_token("tech", "primary")

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_get_motion_token_from_default(self, token_manager):
        """Test getting motion token from defaults."""
        result = token_manager.get_motion_token("spring_configs", "smooth")

        assert result is not None
        assert "config" in result

    @pytest.mark.asyncio
    async def test_get_typography_token_invalid_category(self, token_manager):
        """Test getting typography token with invalid category."""
        result = token_manager.get_typography_token("nonexistent_category")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_typography_token_custom_with_key(self, token_manager):
        """Test getting typography token from custom with specific key."""
        token_manager.custom_typography_tokens = {
            "font_families": {"custom_font": {"name": "CustomFont"}}
        }

        result = token_manager.get_typography_token("font_families", "custom_font", use_custom=True)

        assert result is not None
        assert result["name"] == "CustomFont"

    @pytest.mark.asyncio
    async def test_get_typography_token_no_model_dump(self, token_manager):
        """Test getting typography token when value is plain dict."""
        result = token_manager.get_typography_token("font_families")

        assert result is not None
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_get_color_token_invalid_theme(self, token_manager):
        """Test getting color token with invalid theme."""
        result = token_manager.get_color_token("nonexistent_theme")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_color_token_custom_with_type(self, token_manager):
        """Test getting color token from custom with specific color type."""
        token_manager.custom_color_tokens = {"tech": {"custom_primary": ["#FF0000"]}}

        result = token_manager.get_color_token("tech", "custom_primary", use_custom=True)

        assert result is not None
        assert result == ["#FF0000"]

    @pytest.mark.asyncio
    async def test_get_color_token_custom_whole_theme(self, token_manager):
        """Test getting entire custom color theme."""
        token_manager.custom_color_tokens = {"custom_theme": {"primary": ["#FF0000"]}}

        result = token_manager.get_color_token("custom_theme", use_custom=True)

        assert result is not None
        assert "primary" in result

    @pytest.mark.asyncio
    async def test_get_motion_token_invalid_category(self, token_manager):
        """Test getting motion token with invalid category."""
        result = token_manager.get_motion_token("nonexistent_category")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_motion_token_custom_with_key(self, token_manager):
        """Test getting motion token from custom with specific key."""
        token_manager.custom_motion_tokens = {
            "spring_configs": {"custom_spring": {"stiffness": 100}}
        }

        result = token_manager.get_motion_token("spring_configs", "custom_spring", use_custom=True)

        assert result is not None
        assert result["stiffness"] == 100

    @pytest.mark.asyncio
    async def test_get_motion_token_custom_whole_category(self, token_manager):
        """Test getting entire custom motion category."""
        token_manager.custom_motion_tokens = {"easing": {"custom_ease": "ease-in"}}

        result = token_manager.get_motion_token("easing", use_custom=True)

        assert result is not None
        assert "custom_ease" in result

    @pytest.mark.asyncio
    async def test_get_spacing_token_invalid_type(self, token_manager):
        """Test getting spacing token with invalid type."""
        result = token_manager.get_spacing_token("nonexistent_type")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_spacing_token_custom_with_key(self, token_manager):
        """Test getting spacing token from custom with specific key."""
        token_manager.custom_spacing_tokens = {"spacing": {"custom_xxl": 128}}

        result = token_manager.get_spacing_token("spacing", "custom_xxl", use_custom=True)

        assert result is not None
        assert result == 128

    @pytest.mark.asyncio
    async def test_get_typography_token_dict_value_with_key(self, token_manager):
        """Test getting typography token when value is dict with key."""
        # Set up custom typography tokens where value is a dict
        token_manager.custom_typography_tokens = {
            "font_families": {"custom_family": {"name": "CustomFont", "fallback": "sans-serif"}}
        }

        result = token_manager.get_typography_token("font_families", "custom_family", use_custom=True)

        assert result is not None
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_get_typography_token_dict_value_no_key(self, token_manager):
        """Test getting typography token when value is dict without key."""
        # Set up custom typography tokens where value is a dict
        token_manager.custom_typography_tokens = {
            "font_families": {"name": "CustomFont", "fallback": "sans-serif"}
        }

        result = token_manager.get_typography_token("font_families", use_custom=True)

        assert result is not None
        assert isinstance(result, dict)
        assert result.get("name") == "CustomFont"

    @pytest.mark.asyncio
    async def test_get_color_token_whole_theme(self, token_manager):
        """Test getting entire color theme without specifying color_type."""
        result = token_manager.get_color_token("tech", use_custom=False)

        assert result is not None
        assert isinstance(result, dict)
        assert "text" in result or "background" in result or "primary" in result

    @pytest.mark.asyncio
    async def test_get_motion_token_value_without_key(self, token_manager):
        """Test getting motion token value without specifying key."""
        # This tests the path where we return the value directly without extracting a key
        result = token_manager.get_motion_token("spring_configs")

        assert result is not None


class TestUtilityMethods:
    """Test utility methods."""

    @pytest.mark.asyncio
    async def test_list_custom_tokens(self, token_manager):
        """Test listing custom tokens."""
        token_manager.custom_typography_tokens = {"key1": "value1"}
        token_manager.custom_color_tokens = {"key2": "value2"}
        token_manager.custom_motion_tokens = {"key3": "value3"}

        result = token_manager.list_custom_tokens()

        assert "typography" in result
        assert "colors" in result
        assert "motion" in result
        assert "key1" in result["typography"]
        assert "key2" in result["colors"]
        assert "key3" in result["motion"]

    @pytest.mark.asyncio
    async def test_clear_typography_tokens(self, token_manager):
        """Test clearing typography tokens."""
        token_manager.custom_typography_tokens = {"key": "value"}

        token_manager.clear_custom_tokens("typography")

        assert token_manager.custom_typography_tokens == {}

    @pytest.mark.asyncio
    async def test_clear_all_tokens(self, token_manager):
        """Test clearing all custom tokens."""
        token_manager.custom_typography_tokens = {"key1": "value1"}
        token_manager.custom_color_tokens = {"key2": "value2"}
        token_manager.custom_motion_tokens = {"key3": "value3"}

        token_manager.clear_custom_tokens()

        assert token_manager.custom_typography_tokens == {}
        assert token_manager.custom_color_tokens == {}
        assert token_manager.custom_motion_tokens == {}


class TestSpacingTokenExportImport:
    """Test spacing token export and import."""

    @pytest.mark.asyncio
    async def test_export_all_spacing_tokens(self, token_manager):
        """Test exporting all spacing tokens."""
        result = await token_manager.export_spacing_tokens(file_path="test_spacing.json")

        assert result == "test_spacing.json"

        content = await token_manager.vfs.read_text("test_spacing.json")
        data = json.loads(content)

        assert "spacing" in data
        assert "safe_area" in data

    @pytest.mark.asyncio
    async def test_export_spacing_only(self, token_manager):
        """Test exporting only spacing scale."""
        result = await token_manager.export_spacing_tokens(
            file_path="spacing_only.json", spacing_only=True
        )

        assert result == "spacing_only.json"

        content = await token_manager.vfs.read_text("spacing_only.json")
        data = json.loads(content)

        assert "spacing" in data
        assert "safe_area" not in data

    @pytest.mark.asyncio
    async def test_export_safe_margins_only(self, token_manager):
        """Test exporting only safe margins."""
        result = await token_manager.export_spacing_tokens(
            file_path="safe_margins_only.json", safe_margins_only=True
        )

        assert result == "safe_margins_only.json"

        content = await token_manager.vfs.read_text("safe_margins_only.json")
        data = json.loads(content)

        assert "safe_area" in data
        assert "spacing" not in data

    @pytest.mark.asyncio
    async def test_export_spacing_with_custom_tokens(self, token_manager):
        """Test exporting includes custom spacing tokens."""
        token_manager.custom_spacing_tokens = {"custom_spacing": "custom_value"}

        await token_manager.export_spacing_tokens(file_path="with_custom_spacing.json")

        content = await token_manager.vfs.read_text("with_custom_spacing.json")
        data = json.loads(content)

        assert "custom" in data
        assert data["custom"]["custom_spacing"] == "custom_value"

    @pytest.mark.asyncio
    async def test_import_spacing_tokens(self, token_manager):
        """Test importing spacing tokens."""
        sample_spacing_tokens = {
            "spacing": {"custom_xs": 4, "custom_sm": 8},
            "safe_area": {"custom_margin": 20},
        }

        await token_manager.vfs.write_file("import_spacing.json", json.dumps(sample_spacing_tokens))

        result = await token_manager.import_spacing_tokens(file_path="import_spacing.json")

        assert "Successfully imported" in result
        assert token_manager.custom_spacing_tokens == sample_spacing_tokens

    @pytest.mark.asyncio
    async def test_import_spacing_tokens_merge(self, token_manager):
        """Test importing spacing tokens with merge."""
        token_manager.custom_spacing_tokens = {"existing_key": "existing_value"}

        sample_spacing_tokens = {"spacing": {"custom_xs": 4}}

        await token_manager.vfs.write_file("import_spacing.json", json.dumps(sample_spacing_tokens))

        result = await token_manager.import_spacing_tokens(
            file_path="import_spacing.json", merge=True
        )

        assert "Successfully imported" in result
        assert "existing_key" in token_manager.custom_spacing_tokens
        assert "spacing" in token_manager.custom_spacing_tokens

    @pytest.mark.asyncio
    async def test_import_spacing_tokens_replace(self, token_manager):
        """Test importing spacing tokens without merge."""
        token_manager.custom_spacing_tokens = {"existing_key": "existing_value"}

        sample_spacing_tokens = {"spacing": {"custom_xs": 4}}

        await token_manager.vfs.write_file("import_spacing.json", json.dumps(sample_spacing_tokens))

        result = await token_manager.import_spacing_tokens(
            file_path="import_spacing.json", merge=False
        )

        assert "Successfully imported" in result
        assert "existing_key" not in token_manager.custom_spacing_tokens
        assert token_manager.custom_spacing_tokens == sample_spacing_tokens

    @pytest.mark.asyncio
    async def test_import_invalid_spacing_tokens(self, token_manager):
        """Test importing invalid spacing tokens."""
        await token_manager.vfs.write_file("invalid_spacing.json", json.dumps("not a dict"))

        result = await token_manager.import_spacing_tokens(file_path="invalid_spacing.json")

        assert "Error" in result

    @pytest.mark.asyncio
    async def test_get_spacing_token_from_default(self, token_manager):
        """Test getting spacing token from defaults."""
        result = token_manager.get_spacing_token("spacing", "xs")

        assert result is not None
        # Spacing tokens can be strings like "8px" or numbers
        assert isinstance(result, (int, float, str))

    @pytest.mark.asyncio
    async def test_get_spacing_token_from_custom(self, token_manager):
        """Test getting spacing token from custom tokens."""
        token_manager.custom_spacing_tokens = {"spacing": {"custom_xl": 64}}

        result = token_manager.get_spacing_token("spacing", use_custom=True)

        assert result is not None
        assert "custom_xl" in result

    @pytest.mark.asyncio
    async def test_get_spacing_token_category_only(self, token_manager):
        """Test getting entire spacing category."""
        result = token_manager.get_spacing_token("spacing")

        assert result is not None
        assert isinstance(result, dict)
        assert "xs" in result or "sm" in result

    @pytest.mark.asyncio
    async def test_clear_spacing_tokens(self, token_manager):
        """Test clearing spacing tokens."""
        token_manager.custom_spacing_tokens = {"key": "value"}

        token_manager.clear_custom_tokens("spacing")

        assert token_manager.custom_spacing_tokens == {}

    @pytest.mark.asyncio
    async def test_export_all_tokens_includes_spacing(self, token_manager):
        """Test that export_all_tokens includes spacing tokens."""
        result = await token_manager.export_all_tokens(output_dir="all_tokens_with_spacing")

        assert "spacing" in result
        assert "all_tokens_with_spacing/spacing_tokens.json" in result["spacing"]

        # Verify the spacing file was created
        spacing_content = await token_manager.vfs.read_text(result["spacing"])
        spacing_data = json.loads(spacing_content)
        assert "spacing" in spacing_data or "safe_area" in spacing_data

    @pytest.mark.asyncio
    async def test_export_spacing_default_filepath(self, token_manager):
        """Test exporting spacing tokens with default file path."""
        result = await token_manager.export_spacing_tokens()

        assert result == "spacing_tokens.json"
        assert await token_manager.vfs.exists("spacing_tokens.json")

    @pytest.mark.asyncio
    async def test_export_spacing_exception(self, token_manager):
        """Test export spacing tokens handles exceptions."""
        # Mock vfs to raise exception
        async def raise_exception(path, content):
            raise OSError("Write failed")

        token_manager.vfs.write_file = raise_exception

        result = await token_manager.export_spacing_tokens()

        assert "Error exporting spacing tokens" in result

    @pytest.mark.asyncio
    async def test_import_spacing_exception(self, token_manager):
        """Test import spacing tokens handles exceptions."""
        # Try to import nonexistent file
        result = await token_manager.import_spacing_tokens(file_path="nonexistent.json")

        assert "Error importing spacing tokens" in result
