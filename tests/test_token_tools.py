# chuk-motion/tests/test_token_tools.py
"""
Tests for token MCP tools.
"""

import json

import pytest

from chuk_motion.tools.token_tools import register_token_tools


@pytest.mark.asyncio
class TestTokenTools:
    """Test token MCP tools."""

    @pytest.fixture
    async def mcp_with_token_tools(self, mock_mcp_server, project_manager, vfs):
        """Register token tools and return MCP server."""
        register_token_tools(mock_mcp_server, project_manager, vfs)
        return mock_mcp_server

    async def test_tools_registered(self, mcp_with_token_tools):
        """Test that all token tools are registered."""
        tools = mcp_with_token_tools.tools

        expected_tools = [
            "remotion_list_color_tokens",
            "remotion_get_theme_colors",
            "remotion_get_color_value",
            "remotion_list_typography_tokens",
            "remotion_get_font_families",
            "remotion_get_font_sizes",
            "remotion_get_text_style",
            "remotion_list_motion_tokens",
            "remotion_get_spring_configs",
            "remotion_get_spring_config",
            "remotion_get_easing_curves",
            "remotion_get_easing_curve",
            "remotion_get_durations",
            "remotion_get_duration",
            "remotion_get_animation_presets",
            "remotion_get_animation_preset",
            "remotion_get_youtube_optimizations",
            # Import/Export tools
            "remotion_export_typography_tokens",
            "remotion_import_typography_tokens",
            "remotion_export_color_tokens",
            "remotion_import_color_tokens",
            "remotion_export_motion_tokens",
            "remotion_import_motion_tokens",
            "remotion_export_all_tokens",
        ]

        for tool in expected_tools:
            assert tool in tools, f"Tool {tool} not registered"


class TestColorTokenTools:
    """Test color token tools."""

    @pytest.fixture
    async def mcp_with_token_tools(self, mock_mcp_server, project_manager, vfs):
        """Register token tools and return MCP server."""
        register_token_tools(mock_mcp_server, project_manager, vfs)
        return mock_mcp_server

    @pytest.mark.asyncio
    async def test_list_color_tokens(self, mcp_with_token_tools):
        """Test listing all color tokens."""
        tool = mcp_with_token_tools.tools["remotion_list_color_tokens"]
        result = await tool()

        data = json.loads(result)
        assert "tech" in data
        assert "finance" in data
        assert isinstance(data, dict)

    @pytest.mark.asyncio
    async def test_get_theme_colors(self, mcp_with_token_tools):
        """Test getting colors for specific theme."""
        tool = mcp_with_token_tools.tools["remotion_get_theme_colors"]
        result = await tool(theme_name="tech")

        data = json.loads(result)
        assert data["theme"] == "tech"
        assert "colors" in data
        assert "primary" in data["colors"]
        assert "accent" in data["colors"]

    @pytest.mark.asyncio
    async def test_get_theme_colors_invalid(self, mcp_with_token_tools):
        """Test getting colors for invalid theme."""
        tool = mcp_with_token_tools.tools["remotion_get_theme_colors"]
        result = await tool(theme_name="nonexistent")

        data = json.loads(result)
        assert "error" in data
        assert "available_themes" in data

    @pytest.mark.asyncio
    async def test_get_color_value_array(self, mcp_with_token_tools):
        """Test getting color value from array."""
        tool = mcp_with_token_tools.tools["remotion_get_color_value"]
        result = await tool(theme_name="tech", color_type="primary", index=0)

        data = json.loads(result)
        assert "value" in data
        assert data["value"].startswith("#")

    @pytest.mark.asyncio
    async def test_get_color_value_no_index(self, mcp_with_token_tools):
        """Test getting color value without index."""
        tool = mcp_with_token_tools.tools["remotion_get_color_value"]
        result = await tool(theme_name="tech", color_type="primary")

        data = json.loads(result)
        assert "values" in data
        assert isinstance(data["values"], list)

    @pytest.mark.asyncio
    async def test_get_color_value_dict(self, mcp_with_token_tools):
        """Test getting color value from dict."""
        tool = mcp_with_token_tools.tools["remotion_get_color_value"]
        result = await tool(theme_name="tech", color_type="background")

        data = json.loads(result)
        assert "values" in data
        assert "dark" in data["values"]

    @pytest.mark.asyncio
    async def test_get_color_value_invalid_index(self, mcp_with_token_tools):
        """Test getting color with invalid index."""
        tool = mcp_with_token_tools.tools["remotion_get_color_value"]
        result = await tool(theme_name="tech", color_type="primary", index=99)

        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_get_color_value_invalid_theme(self, mcp_with_token_tools):
        """Test getting color value with invalid theme."""
        tool = mcp_with_token_tools.tools["remotion_get_color_value"]
        result = await tool(theme_name="invalid_theme", color_type="primary")

        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_get_color_value_invalid_color_type(self, mcp_with_token_tools):
        """Test getting color value with invalid color type."""
        tool = mcp_with_token_tools.tools["remotion_get_color_value"]
        result = await tool(theme_name="tech", color_type="invalid_color")

        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_get_color_value_string(self, mcp_with_token_tools):
        """Test getting string color value (gradient)."""
        tool = mcp_with_token_tools.tools["remotion_get_color_value"]
        result = await tool(theme_name="tech", color_type="gradient")

        data = json.loads(result)
        assert "value" in data
        assert isinstance(data["value"], str)


class TestTypographyTokenTools:
    """Test typography token tools."""

    @pytest.fixture
    async def mcp_with_token_tools(self, mock_mcp_server, project_manager, vfs):
        """Register token tools and return MCP server."""
        register_token_tools(mock_mcp_server, project_manager, vfs)
        return mock_mcp_server

    @pytest.mark.asyncio
    async def test_list_typography_tokens(self, mcp_with_token_tools):
        """Test listing all typography tokens."""
        tool = mcp_with_token_tools.tools["remotion_list_typography_tokens"]
        result = await tool()

        data = json.loads(result)
        assert "font_families" in data
        assert "font_sizes" in data
        assert "font_weights" in data

    @pytest.mark.asyncio
    async def test_get_font_families(self, mcp_with_token_tools):
        """Test getting font families."""
        tool = mcp_with_token_tools.tools["remotion_get_font_families"]
        result = await tool()

        data = json.loads(result)
        assert "font_families" in data
        assert "display" in data["font_families"]
        assert "body" in data["font_families"]

    @pytest.mark.asyncio
    async def test_get_font_sizes_1080p(self, mcp_with_token_tools):
        """Test getting font sizes for 1080p."""
        tool = mcp_with_token_tools.tools["remotion_get_font_sizes"]
        result = await tool(resolution="video_1080p")

        data = json.loads(result)
        assert data["resolution"] == "video_1080p"
        assert "font_sizes" in data
        assert "xl" in data["font_sizes"]

    @pytest.mark.asyncio
    async def test_get_font_sizes_invalid_resolution(self, mcp_with_token_tools):
        """Test getting font sizes for invalid resolution."""
        tool = mcp_with_token_tools.tools["remotion_get_font_sizes"]
        result = await tool(resolution="invalid_resolution")

        data = json.loads(result)
        assert "error" in data
        assert "available_resolutions" in data

    @pytest.mark.asyncio
    async def test_get_text_style(self, mcp_with_token_tools):
        """Test getting text style."""
        tool = mcp_with_token_tools.tools["remotion_get_text_style"]
        result = await tool(style_name="hero_title")

        data = json.loads(result)
        assert data["style_name"] == "hero_title"
        assert "style" in data
        assert "fontSize" in data["style"]

    @pytest.mark.asyncio
    async def test_get_text_style_invalid(self, mcp_with_token_tools):
        """Test getting invalid text style."""
        tool = mcp_with_token_tools.tools["remotion_get_text_style"]
        result = await tool(style_name="nonexistent_style")

        data = json.loads(result)
        assert "error" in data


class TestMotionTokenTools:
    """Test motion token tools."""

    @pytest.fixture
    async def mcp_with_token_tools(self, mock_mcp_server, project_manager, vfs):
        """Register token tools and return MCP server."""
        register_token_tools(mock_mcp_server, project_manager, vfs)
        return mock_mcp_server

    @pytest.mark.asyncio
    async def test_list_motion_tokens(self, mcp_with_token_tools):
        """Test listing all motion tokens."""
        tool = mcp_with_token_tools.tools["remotion_list_motion_tokens"]
        result = await tool()

        data = json.loads(result)
        assert "spring_configs" in data
        assert "easing" in data
        assert "duration" in data
        assert "enter" in data

    @pytest.mark.asyncio
    async def test_get_spring_configs(self, mcp_with_token_tools):
        """Test getting all spring configs."""
        tool = mcp_with_token_tools.tools["remotion_get_spring_configs"]
        result = await tool()

        data = json.loads(result)
        assert "spring_configs" in data
        assert "smooth" in data["spring_configs"]
        assert "bouncy" in data["spring_configs"]

    @pytest.mark.asyncio
    async def test_get_spring_config(self, mcp_with_token_tools):
        """Test getting specific spring config."""
        tool = mcp_with_token_tools.tools["remotion_get_spring_config"]
        result = await tool(spring_name="bouncy")

        data = json.loads(result)
        assert data["spring_name"] == "bouncy"
        assert "config" in data
        assert "damping" in data["config"]["config"]

    @pytest.mark.asyncio
    async def test_get_spring_config_invalid(self, mcp_with_token_tools):
        """Test getting invalid spring config."""
        tool = mcp_with_token_tools.tools["remotion_get_spring_config"]
        result = await tool(spring_name="nonexistent")

        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_get_easing_curves(self, mcp_with_token_tools):
        """Test getting all easing curves."""
        tool = mcp_with_token_tools.tools["remotion_get_easing_curves"]
        result = await tool()

        data = json.loads(result)
        assert "easing" in data
        assert "ease_out" in data["easing"]

    @pytest.mark.asyncio
    async def test_get_easing_curve(self, mcp_with_token_tools):
        """Test getting specific easing curve."""
        tool = mcp_with_token_tools.tools["remotion_get_easing_curve"]
        result = await tool(easing_name="ease_out_back")

        data = json.loads(result)
        assert data["easing_name"] == "ease_out_back"
        assert "curve" in data
        assert "curve" in data["curve"]

    @pytest.mark.asyncio
    async def test_get_easing_curve_invalid(self, mcp_with_token_tools):
        """Test getting invalid easing curve."""
        tool = mcp_with_token_tools.tools["remotion_get_easing_curve"]
        result = await tool(easing_name="nonexistent")

        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_get_durations(self, mcp_with_token_tools):
        """Test getting all durations."""
        tool = mcp_with_token_tools.tools["remotion_get_durations"]
        result = await tool()

        data = json.loads(result)
        assert "duration" in data
        assert "normal" in data["duration"]

    @pytest.mark.asyncio
    async def test_get_duration(self, mcp_with_token_tools):
        """Test getting specific duration."""
        tool = mcp_with_token_tools.tools["remotion_get_duration"]
        result = await tool(duration_name="normal")

        data = json.loads(result)
        assert data["duration_name"] == "normal"
        assert "duration" in data
        assert "frames_30fps" in data["duration"] or "frames_60fps" in data["duration"]

    @pytest.mark.asyncio
    async def test_get_duration_invalid(self, mcp_with_token_tools):
        """Test getting invalid duration."""
        tool = mcp_with_token_tools.tools["remotion_get_duration"]
        result = await tool(duration_name="nonexistent")

        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_get_animation_presets(self, mcp_with_token_tools):
        """Test getting all animation presets."""
        tool = mcp_with_token_tools.tools["remotion_get_animation_presets"]
        result = await tool()

        data = json.loads(result)
        assert "enter" in data
        assert "fade_in" in data["enter"]

    @pytest.mark.asyncio
    async def test_get_animation_preset(self, mcp_with_token_tools):
        """Test getting specific animation preset."""
        tool = mcp_with_token_tools.tools["remotion_get_animation_preset"]
        result = await tool(preset_name="fade_in")

        data = json.loads(result)
        assert data["preset_name"] == "fade_in"
        assert "preset" in data
        assert "properties" in data["preset"]

    @pytest.mark.asyncio
    async def test_get_animation_preset_invalid(self, mcp_with_token_tools):
        """Test getting invalid animation preset."""
        tool = mcp_with_token_tools.tools["remotion_get_animation_preset"]
        result = await tool(preset_name="nonexistent")

        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_get_youtube_optimizations(self, mcp_with_token_tools):
        """Test getting YouTube optimizations."""
        tool = mcp_with_token_tools.tools["remotion_get_youtube_optimizations"]
        result = await tool()

        data = json.loads(result)
        assert "youtube_optimizations" in data
        # Check for platform-specific timings
        assert (
            "tiktok" in data["youtube_optimizations"]
            or "youtube_shorts" in data["youtube_optimizations"]
        )


class TestTokenImportExportTools:
    """Test token import/export MCP tools."""

    @pytest.fixture
    async def mcp_with_token_tools(self, mock_mcp_server, project_manager, vfs):
        """Register token tools and return MCP server."""
        register_token_tools(mock_mcp_server, project_manager, vfs)
        return mock_mcp_server

    # Typography Token Export/Import Tests

    @pytest.mark.asyncio
    async def test_export_typography_tokens(self, mcp_with_token_tools):
        """Test exporting typography tokens via MCP tool."""
        tool = mcp_with_token_tools.tools["remotion_export_typography_tokens"]
        result = await tool(file_path="test_typo.json", include_all=True)

        data = json.loads(result)
        assert data["status"] == "success"
        assert data["file_path"] == "test_typo.json"
        assert "Typography tokens exported successfully" in data["message"]

    @pytest.mark.asyncio
    async def test_export_typography_tokens_font_families_only(self, mcp_with_token_tools):
        """Test exporting only font families."""
        tool = mcp_with_token_tools.tools["remotion_export_typography_tokens"]
        result = await tool(file_path="families.json", include_all=False, font_families_only=True)

        data = json.loads(result)
        assert data["status"] == "success"
        assert data["file_path"] == "families.json"

    @pytest.mark.asyncio
    async def test_export_typography_tokens_text_styles_only(self, mcp_with_token_tools):
        """Test exporting only text styles."""
        tool = mcp_with_token_tools.tools["remotion_export_typography_tokens"]
        result = await tool(file_path="styles.json", include_all=False, text_styles_only=True)

        data = json.loads(result)
        assert data["status"] == "success"
        assert data["file_path"] == "styles.json"

    @pytest.mark.asyncio
    async def test_import_typography_tokens(self, mcp_with_token_tools, vfs):
        """Test importing typography tokens via MCP tool."""
        # First export to create a file
        export_tool = mcp_with_token_tools.tools["remotion_export_typography_tokens"]
        await export_tool(file_path="import_test.json")

        # Then import it
        import_tool = mcp_with_token_tools.tools["remotion_import_typography_tokens"]
        result = await import_tool(file_path="import_test.json", merge=True)

        data = json.loads(result)
        assert data["status"] == "success"
        assert "Successfully imported" in data["message"]

    @pytest.mark.asyncio
    async def test_import_typography_tokens_no_merge(self, mcp_with_token_tools, vfs):
        """Test importing typography tokens without merge."""
        # First export to create a file
        export_tool = mcp_with_token_tools.tools["remotion_export_typography_tokens"]
        await export_tool(file_path="replace_test.json")

        # Then import without merging
        import_tool = mcp_with_token_tools.tools["remotion_import_typography_tokens"]
        result = await import_tool(file_path="replace_test.json", merge=False)

        data = json.loads(result)
        assert data["status"] == "success"

    @pytest.mark.asyncio
    async def test_import_typography_tokens_invalid_file(self, mcp_with_token_tools, vfs):
        """Test importing from non-existent file."""
        import_tool = mcp_with_token_tools.tools["remotion_import_typography_tokens"]
        result = await import_tool(file_path="nonexistent.json")

        data = json.loads(result)
        assert "error" in data

    # Color Token Export/Import Tests

    @pytest.mark.asyncio
    async def test_export_color_tokens(self, mcp_with_token_tools):
        """Test exporting color tokens via MCP tool."""
        tool = mcp_with_token_tools.tools["remotion_export_color_tokens"]
        result = await tool(file_path="test_colors.json")

        data = json.loads(result)
        assert data["status"] == "success"
        assert data["file_path"] == "test_colors.json"
        assert "Color tokens exported successfully" in data["message"]

    @pytest.mark.asyncio
    async def test_export_color_tokens_specific_theme(self, mcp_with_token_tools):
        """Test exporting specific theme colors."""
        tool = mcp_with_token_tools.tools["remotion_export_color_tokens"]
        result = await tool(file_path="tech_colors.json", theme_name="tech")

        data = json.loads(result)
        assert data["status"] == "success"
        assert data["file_path"] == "tech_colors.json"

    @pytest.mark.asyncio
    async def test_export_color_tokens_invalid_theme(self, mcp_with_token_tools):
        """Test exporting invalid theme returns error."""
        tool = mcp_with_token_tools.tools["remotion_export_color_tokens"]
        result = await tool(theme_name="nonexistent_theme")

        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_import_color_tokens(self, mcp_with_token_tools, vfs):
        """Test importing color tokens via MCP tool."""
        # First export to create a file
        export_tool = mcp_with_token_tools.tools["remotion_export_color_tokens"]
        await export_tool(file_path="import_colors.json")

        # Then import it
        import_tool = mcp_with_token_tools.tools["remotion_import_color_tokens"]
        result = await import_tool(file_path="import_colors.json", merge=True)

        data = json.loads(result)
        assert data["status"] == "success"
        assert "Successfully imported" in data["message"]

    @pytest.mark.asyncio
    async def test_import_color_tokens_no_merge(self, mcp_with_token_tools, vfs):
        """Test importing color tokens without merge."""
        # First export to create a file
        export_tool = mcp_with_token_tools.tools["remotion_export_color_tokens"]
        await export_tool(file_path="replace_colors.json")

        # Then import without merging
        import_tool = mcp_with_token_tools.tools["remotion_import_color_tokens"]
        result = await import_tool(file_path="replace_colors.json", merge=False)

        data = json.loads(result)
        assert data["status"] == "success"

    @pytest.mark.asyncio
    async def test_import_color_tokens_invalid_file(self, mcp_with_token_tools, vfs):
        """Test importing from non-existent color file."""
        import_tool = mcp_with_token_tools.tools["remotion_import_color_tokens"]
        result = await import_tool(file_path="nonexistent_colors.json")

        data = json.loads(result)
        assert "error" in data

    # Motion Token Export/Import Tests

    @pytest.mark.asyncio
    async def test_export_motion_tokens(self, mcp_with_token_tools):
        """Test exporting motion tokens via MCP tool."""
        tool = mcp_with_token_tools.tools["remotion_export_motion_tokens"]
        result = await tool(file_path="test_motion.json")

        data = json.loads(result)
        assert data["status"] == "success"
        assert data["file_path"] == "test_motion.json"
        assert "Motion tokens exported successfully" in data["message"]

    @pytest.mark.asyncio
    async def test_export_motion_tokens_springs_only(self, mcp_with_token_tools):
        """Test exporting only spring configs."""
        tool = mcp_with_token_tools.tools["remotion_export_motion_tokens"]
        result = await tool(file_path="springs.json", springs_only=True)

        data = json.loads(result)
        assert data["status"] == "success"
        assert data["file_path"] == "springs.json"

    @pytest.mark.asyncio
    async def test_export_motion_tokens_easings_only(self, mcp_with_token_tools):
        """Test exporting only easing curves."""
        tool = mcp_with_token_tools.tools["remotion_export_motion_tokens"]
        result = await tool(file_path="easings.json", easings_only=True)

        data = json.loads(result)
        assert data["status"] == "success"
        assert data["file_path"] == "easings.json"

    @pytest.mark.asyncio
    async def test_export_motion_tokens_presets_only(self, mcp_with_token_tools):
        """Test exporting only animation presets."""
        tool = mcp_with_token_tools.tools["remotion_export_motion_tokens"]
        result = await tool(file_path="presets.json", presets_only=True)

        data = json.loads(result)
        assert data["status"] == "success"
        assert data["file_path"] == "presets.json"

    @pytest.mark.asyncio
    async def test_import_motion_tokens(self, mcp_with_token_tools, vfs):
        """Test importing motion tokens via MCP tool."""
        # First export to create a file
        export_tool = mcp_with_token_tools.tools["remotion_export_motion_tokens"]
        await export_tool(file_path="import_motion.json")

        # Then import it
        import_tool = mcp_with_token_tools.tools["remotion_import_motion_tokens"]
        result = await import_tool(file_path="import_motion.json", merge=True)

        data = json.loads(result)
        assert data["status"] == "success"
        assert "Successfully imported" in data["message"]

    @pytest.mark.asyncio
    async def test_import_motion_tokens_no_merge(self, mcp_with_token_tools, vfs):
        """Test importing motion tokens without merge."""
        # First export to create a file
        export_tool = mcp_with_token_tools.tools["remotion_export_motion_tokens"]
        await export_tool(file_path="replace_motion.json")

        # Then import without merging
        import_tool = mcp_with_token_tools.tools["remotion_import_motion_tokens"]
        result = await import_tool(file_path="replace_motion.json", merge=False)

        data = json.loads(result)
        assert data["status"] == "success"

    @pytest.mark.asyncio
    async def test_import_motion_tokens_invalid_file(self, mcp_with_token_tools, vfs):
        """Test importing from non-existent motion file."""
        import_tool = mcp_with_token_tools.tools["remotion_import_motion_tokens"]
        result = await import_tool(file_path="nonexistent_motion.json")

        data = json.loads(result)
        assert "error" in data

    # Export All Tokens Test

    @pytest.mark.asyncio
    async def test_export_all_tokens(self, mcp_with_token_tools):
        """Test exporting all token types at once."""
        tool = mcp_with_token_tools.tools["remotion_export_all_tokens"]
        result = await tool(output_dir="all_tokens")

        data = json.loads(result)
        assert data["status"] == "success"
        assert "files" in data
        assert "typography" in data["files"]
        assert "colors" in data["files"]
        assert "motion" in data["files"]
        assert "All tokens exported successfully" in data["message"]

    # Error Path Tests

    @pytest.mark.asyncio
    async def test_export_typography_tokens_error_path(
        self, mock_mcp_server, project_manager, mocker
    ):
        """Test typography export error handling."""
        # Create a mock VFS that raises an exception on write_file
        mock_vfs = mocker.AsyncMock()
        mock_vfs.write_file.side_effect = Exception("VFS write error")

        register_token_tools(mock_mcp_server, project_manager, mock_vfs)
        tool = mock_mcp_server.tools["remotion_export_typography_tokens"]

        result = await tool(file_path="error_test.json")
        data = json.loads(result)
        assert "error" in data
        assert "VFS write error" in data["error"] or "Error" in data["error"]

    @pytest.mark.asyncio
    async def test_export_motion_tokens_error_path(self, mock_mcp_server, project_manager, mocker):
        """Test motion token export error handling."""
        # Create a mock VFS that raises an exception on write_file
        mock_vfs = mocker.AsyncMock()
        mock_vfs.write_file.side_effect = Exception("VFS write error")

        register_token_tools(mock_mcp_server, project_manager, mock_vfs)
        tool = mock_mcp_server.tools["remotion_export_motion_tokens"]

        result = await tool(file_path="error_test.json")
        data = json.loads(result)
        assert "error" in data
        assert "VFS write error" in data["error"] or "Error" in data["error"]
