# chuk-mcp-remotion/tests/test_token_manager.py
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
        assert "easing_curves" in data
        assert "durations" in data

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

        assert "easing_curves" in data
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

        assert "animation_presets" in data
        assert "spring_configs" not in data

    @pytest.mark.asyncio
    async def test_import_motion_tokens(self, token_manager, sample_motion_tokens):
        """Test importing motion tokens."""
        await token_manager.vfs.write_file("import_motion.json", json.dumps(sample_motion_tokens))

        result = await token_manager.import_motion_tokens(file_path="import_motion.json")

        assert "Successfully imported" in result
        assert token_manager.custom_motion_tokens == sample_motion_tokens


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
