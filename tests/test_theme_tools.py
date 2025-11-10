# chuk-mcp-remotion/tests/test_theme_tools.py
"""
Tests for theme MCP tools.
"""

import json

import pytest

from chuk_mcp_remotion.tools.theme_tools import register_theme_tools


@pytest.mark.asyncio
class TestThemeTools:
    """Test theme MCP tools."""

    @pytest.fixture
    async def mcp_with_theme_tools(self, mock_mcp_server, project_manager, vfs):
        """Register theme tools and return MCP server."""
        register_theme_tools(mock_mcp_server, project_manager, vfs)
        return mock_mcp_server

    async def test_tools_registered(self, mcp_with_theme_tools):
        """Test that all theme tools are registered."""
        tools = mcp_with_theme_tools.tools

        expected_tools = [
            "remotion_list_themes",
            "remotion_get_theme_info",
            "remotion_search_themes",
            "remotion_compare_themes",
            "remotion_set_current_theme",
            "remotion_get_current_theme",
            "remotion_validate_theme",
            "remotion_create_custom_theme",
            "remotion_export_theme",
            "remotion_import_theme",
            "remotion_get_theme_for_content",
        ]

        for tool in expected_tools:
            assert tool in tools, f"Tool {tool} not registered"

    async def test_list_themes(self, mcp_with_theme_tools):
        """Test remotion_list_themes tool."""
        tool = mcp_with_theme_tools.tools["remotion_list_themes"]
        result = await tool()

        data = json.loads(result)
        assert "themes" in data
        assert len(data["themes"]) > 0

        # Check first theme structure
        first_theme = data["themes"][0]
        assert "key" in first_theme
        assert "name" in first_theme
        assert "description" in first_theme
        assert "primary_color" in first_theme
        assert "use_cases" in first_theme

    async def test_get_theme_info_valid(self, mcp_with_theme_tools):
        """Test getting info for valid theme."""
        tool = mcp_with_theme_tools.tools["remotion_get_theme_info"]
        result = await tool(theme_name="tech")

        data = json.loads(result)
        assert "name" in data
        assert data["name"] == "Tech"
        assert "colors" in data
        assert "typography" in data
        assert "motion" in data

    async def test_get_theme_info_invalid(self, mcp_with_theme_tools):
        """Test getting info for invalid theme."""
        tool = mcp_with_theme_tools.tools["remotion_get_theme_info"]
        result = await tool(theme_name="nonexistent")

        data = json.loads(result)
        assert "error" in data
        assert "available_themes" in data

    async def test_search_themes(self, mcp_with_theme_tools):
        """Test searching themes."""
        tool = mcp_with_theme_tools.tools["remotion_search_themes"]
        result = await tool(query="tech")

        data = json.loads(result)
        assert "query" in data
        assert data["query"] == "tech"
        assert "matches" in data
        assert len(data["matches"]) > 0

    async def test_compare_themes(self, mcp_with_theme_tools):
        """Test comparing two themes."""
        tool = mcp_with_theme_tools.tools["remotion_compare_themes"]
        result = await tool(theme1="tech", theme2="gaming")

        data = json.loads(result)
        assert "themes" in data
        assert data["themes"] == ["tech", "gaming"]
        assert "comparison" in data

        comparison = data["comparison"]
        assert "primary_colors" in comparison
        assert "motion_feel" in comparison

    async def test_set_current_theme_valid(self, mcp_with_theme_tools):
        """Test setting valid current theme."""
        tool = mcp_with_theme_tools.tools["remotion_set_current_theme"]
        result = await tool(theme_name="tech")

        data = json.loads(result)
        assert data["status"] == "success"
        assert data["current_theme"] == "tech"

    async def test_set_current_theme_invalid(self, mcp_with_theme_tools):
        """Test setting invalid current theme."""
        tool = mcp_with_theme_tools.tools["remotion_set_current_theme"]
        result = await tool(theme_name="nonexistent")

        data = json.loads(result)
        assert data["status"] == "error"

    async def test_get_current_theme_none(self, mcp_with_theme_tools):
        """Test getting current theme when none set."""
        tool = mcp_with_theme_tools.tools["remotion_get_current_theme"]
        result = await tool()

        data = json.loads(result)
        assert data["current_theme"] is None

    async def test_get_current_theme_set(self, mcp_with_theme_tools):
        """Test getting current theme after setting."""
        set_tool = mcp_with_theme_tools.tools["remotion_set_current_theme"]
        await set_tool(theme_name="tech")

        get_tool = mcp_with_theme_tools.tools["remotion_get_current_theme"]
        result = await get_tool()

        data = json.loads(result)
        assert data["current_theme"] == "tech"
        assert "info" in data

    async def test_validate_theme_valid(self, mcp_with_theme_tools, sample_theme):
        """Test validating valid theme."""
        tool = mcp_with_theme_tools.tools["remotion_validate_theme"]
        theme_dict = sample_theme.model_dump()
        result = await tool(theme_data=json.dumps(theme_dict))

        data = json.loads(result)
        assert data["valid"] is True
        assert len(data["errors"]) == 0

    async def test_validate_theme_invalid(self, mcp_with_theme_tools):
        """Test validating invalid theme."""
        invalid_data = {"name": "Invalid"}
        tool = mcp_with_theme_tools.tools["remotion_validate_theme"]
        result = await tool(theme_data=json.dumps(invalid_data))

        data = json.loads(result)
        assert data["valid"] is False
        assert len(data["errors"]) > 0

    async def test_validate_theme_bad_json(self, mcp_with_theme_tools):
        """Test validating with invalid JSON."""
        tool = mcp_with_theme_tools.tools["remotion_validate_theme"]
        result = await tool(theme_data="not valid json")

        data = json.loads(result)
        assert data["valid"] is False
        assert "Invalid JSON" in data["errors"][0]

    async def test_create_custom_theme(self, mcp_with_theme_tools):
        """Test creating custom theme."""
        tool = mcp_with_theme_tools.tools["remotion_create_custom_theme"]
        result = await tool(
            name="My Custom",
            description="Custom theme",
            base_theme="tech",
            primary_colors='["#FF0000", "#CC0000", "#990000"]',
        )

        data = json.loads(result)
        assert data["status"] == "success"
        assert "theme_key" in data
        assert "theme" in data

    async def test_create_custom_theme_no_base(self, mcp_with_theme_tools):
        """Test creating custom theme without base (defaults to tech)."""
        tool = mcp_with_theme_tools.tools["remotion_create_custom_theme"]
        result = await tool(
            name="Standalone",
            description="No base theme",
            # Will default to "tech" base theme
        )

        data = json.loads(result)
        # Should succeed with default base
        assert data["status"] == "success"
        assert data["theme_key"] == "standalone"

    async def test_export_theme(self, mcp_with_theme_tools):
        """Test exporting theme."""
        export_path = "exported.json"
        tool = mcp_with_theme_tools.tools["remotion_export_theme"]
        result = await tool(theme_name="tech", file_path=export_path)

        data = json.loads(result)
        assert data["status"] == "success"
        assert "file_path" in data

    async def test_import_theme(self, mcp_with_theme_tools, sample_theme, vfs):
        """Test importing theme."""
        # Create a theme file in vfs - convert Pydantic model to dict first
        theme_dict = sample_theme.model_dump()
        await vfs.write_file("test_theme.json", json.dumps(theme_dict))

        tool = mcp_with_theme_tools.tools["remotion_import_theme"]
        result = await tool(file_path="test_theme.json", theme_key="imported_test")

        data = json.loads(result)
        assert data["status"] == "success"
        assert "Successfully imported" in data["message"]

    async def test_get_theme_for_content(self, mcp_with_theme_tools):
        """Test getting theme recommendations for content type."""
        tool = mcp_with_theme_tools.tools["remotion_get_theme_for_content"]
        result = await tool(content_type="gaming")

        data = json.loads(result)
        assert "content_type" in data
        assert data["content_type"] == "gaming"
        assert "recommendations" in data
        assert len(data["recommendations"]) > 0

    async def test_get_theme_for_unknown_content(self, mcp_with_theme_tools):
        """Test getting theme for unknown content type."""
        tool = mcp_with_theme_tools.tools["remotion_get_theme_for_content"]
        result = await tool(content_type="unknown_xyz")

        data = json.loads(result)
        assert "popular_themes" in data or "recommendations" in data
