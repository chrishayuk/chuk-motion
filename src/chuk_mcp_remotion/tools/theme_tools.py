"""
Theme Tools for Remotion MCP Server

Provides async MCP tools for managing and applying themes to video compositions.
Consolidates all theme-related functionality in one place.
"""

import asyncio
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chuk_virtual_fs import AsyncVirtualFileSystem

from ..themes.theme_manager import ThemeManager


def register_theme_tools(mcp, project_manager, vfs: "AsyncVirtualFileSystem"):
    """
    Register all theme-related tools with the MCP server.

    Args:
        mcp: ChukMCPServer instance
        project_manager: ProjectManager instance for applying themes
        vfs: Virtual filesystem instance for file operations
    """

    # Create a single theme manager instance with virtual filesystem
    theme_manager = ThemeManager(vfs)

    @mcp.tool
    async def remotion_list_themes() -> str:
        """
        List all available video themes with descriptions.

        Returns a list of built-in YouTube-optimized themes including their
        characteristics, primary colors, and recommended use cases.

        Returns:
            JSON array of themes with metadata

        Example:
            themes = await remotion_list_themes()
            # Returns: tech, finance, education, lifestyle, gaming, minimal, business
        """

        def _list():
            theme_keys = theme_manager.list_themes()
            theme_list = []

            for key in theme_keys:
                theme = theme_manager.get_theme(key)
                if theme:
                    theme_list.append(
                        {
                            "key": key,
                            "name": theme.name,
                            "description": theme.description,
                            "primary_color": theme.colors.primary[0] if theme.colors.primary else "N/A",
                            "accent_color": theme.colors.accent[0] if theme.colors.accent else "N/A",
                            "use_cases": theme.use_cases[:3],  # First 3 use cases
                        }
                    )

            return json.dumps({"themes": theme_list}, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _list)

    @mcp.tool
    async def remotion_get_theme_info(theme_name: str) -> str:
        """
        Get detailed information about a specific theme.

        Returns complete theme configuration including colors, typography,
        motion design, and usage recommendations.

        Args:
            theme_name: Theme identifier (e.g., "tech", "finance", "education")

        Returns:
            JSON object with complete theme information

        Example:
            info = await remotion_get_theme_info(theme_name="tech")
            # Returns tech theme with all design tokens
        """

        def _get_info():
            info = theme_manager.get_theme_info(theme_name)

            if not info:
                return json.dumps(
                    {
                        "error": f"Theme '{theme_name}' not found",
                        "available_themes": theme_manager.list_themes(),
                    }
                )

            return json.dumps(info, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _get_info)

    @mcp.tool
    async def remotion_search_themes(query: str) -> str:
        """
        Search themes by name, description, or use case.

        Performs a case-insensitive search across theme metadata to help
        find suitable themes for specific content types.

        Args:
            query: Search term (e.g., "gaming", "professional", "education")

        Returns:
            JSON array of matching theme keys

        Example:
            results = await remotion_search_themes(query="professional")
            # Returns: ["business", "minimal", "finance"]
        """

        def _search():
            matches = theme_manager.search_themes(query)
            theme_details = []

            for key in matches:
                theme = theme_manager.get_theme(key)
                if theme:
                    theme_details.append(
                        {
                            "key": key,
                            "name": theme.name,
                            "description": theme.description,
                            "use_cases": theme.use_cases,
                        }
                    )

            return json.dumps({"query": query, "matches": theme_details}, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _search)

    @mcp.tool
    async def remotion_compare_themes(theme1: str, theme2: str) -> str:
        """
        Compare two themes side by side.

        Returns a comparison of colors, motion feel, and use cases to help
        choose between themes or understand their differences.

        Args:
            theme1: First theme identifier
            theme2: Second theme identifier

        Returns:
            JSON object with side-by-side comparison

        Example:
            comparison = await remotion_compare_themes(theme1="tech", theme2="gaming")
            # Shows differences in colors, motion, and use cases
        """

        def _compare():
            comparison = theme_manager.compare_themes(theme1, theme2)
            return json.dumps(comparison, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _compare)

    @mcp.tool
    async def remotion_set_current_theme(theme_name: str) -> str:
        """
        Set the active theme for the current session.

        Sets the default theme that will be used for new components and
        compositions. This doesn't affect existing compositions.

        Args:
            theme_name: Theme identifier to set as active

        Returns:
            JSON with success status

        Example:
            result = await remotion_set_current_theme(theme_name="gaming")
            # Sets gaming theme as default
        """

        def _set():
            success = theme_manager.set_current_theme(theme_name)

            if success:
                return json.dumps(
                    {
                        "status": "success",
                        "current_theme": theme_name,
                        "message": f"Current theme set to '{theme_name}'",
                    }
                )
            else:
                return json.dumps(
                    {
                        "status": "error",
                        "message": f"Theme '{theme_name}' not found",
                        "available_themes": theme_manager.list_themes(),
                    }
                )

        return await asyncio.get_event_loop().run_in_executor(None, _set)

    @mcp.tool
    async def remotion_get_current_theme() -> str:
        """
        Get the currently active theme.

        Returns the theme key that's currently set as default for new
        compositions and components.

        Returns:
            JSON with current theme information

        Example:
            current = await remotion_get_current_theme()
            # Returns current theme key or null if none set
        """

        def _get():
            current = theme_manager.get_current_theme()

            if current:
                theme_info = theme_manager.get_theme_info(current)
                return json.dumps({"current_theme": current, "info": theme_info}, indent=2)
            else:
                return json.dumps({"current_theme": None, "message": "No theme currently set"})

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    @mcp.tool
    async def remotion_validate_theme(theme_data: str) -> str:
        """
        Validate a theme data structure.

        Checks if a theme JSON has all required fields and proper structure.
        Useful before importing or creating custom themes.

        Args:
            theme_data: JSON string with theme data to validate

        Returns:
            JSON with validation results and any errors

        Example:
            result = await remotion_validate_theme(theme_data='{"name": "Custom", ...}')
            # Returns validation status and error list if invalid
        """

        def _validate():
            try:
                theme_dict = json.loads(theme_data)
                validation = theme_manager.validate_theme(theme_dict)
                return json.dumps(validation, indent=2)
            except json.JSONDecodeError as e:
                return json.dumps({"valid": False, "errors": [f"Invalid JSON: {str(e)}"]})

        return await asyncio.get_event_loop().run_in_executor(None, _validate)

    @mcp.tool
    async def remotion_create_custom_theme(
        name: str,
        description: str,
        base_theme: str | None = None,
        primary_colors: str | None = None,
        accent_colors: str | None = None,
    ) -> str:
        """
        Create a custom theme based on an existing theme.

        Creates a new theme by starting with an existing theme and applying
        custom color overrides. More advanced customization can be done by
        exporting, editing, and importing the theme JSON.

        Args:
            name: Custom theme name
            description: Theme description
            base_theme: Base theme to start from (default: "tech")
            primary_colors: JSON array of primary colors (optional)
            accent_colors: JSON array of accent colors (optional)

        Returns:
            JSON with created theme key and details

        Example:
            theme = await remotion_create_custom_theme(
                name="My Brand",
                description="Custom brand colors",
                base_theme="tech",
                primary_colors='["#FF0000", "#CC0000", "#990000"]',
                accent_colors='["#00FF00", "#00CC00", "#009900"]'
            )
        """

        def _create():
            try:
                # Parse color overrides if provided
                color_overrides = {}
                if primary_colors:
                    color_overrides["primary"] = json.loads(primary_colors)
                if accent_colors:
                    color_overrides["accent"] = json.loads(accent_colors)

                result = theme_manager.create_custom_theme(
                    name=name,
                    description=description,
                    base_theme=base_theme or "tech",
                    color_overrides=color_overrides if color_overrides else None,
                )

                # Check if result is an error message
                if result.startswith("Error"):
                    return json.dumps({"error": result})

                # Success - return theme info
                theme_info = theme_manager.get_theme_info(result)
                return json.dumps(
                    {"status": "success", "theme_key": result, "theme": theme_info}, indent=2
                )

            except json.JSONDecodeError as e:
                return json.dumps({"error": f"Invalid color JSON: {str(e)}"})
            except Exception as e:
                return json.dumps({"error": str(e)})

        return await asyncio.get_event_loop().run_in_executor(None, _create)

    @mcp.tool
    async def remotion_export_theme(theme_name: str, file_path: str | None = None) -> str:
        """
        Export a theme to a JSON file.

        Saves a theme to a JSON file that can be shared, version controlled,
        or edited externally. The file can later be imported.

        Args:
            theme_name: Theme identifier to export
            file_path: Output file path (default: theme_name_theme.json)

        Returns:
            JSON with export status and file path

        Example:
            result = await remotion_export_theme(
                theme_name="tech",
                file_path="my_tech_theme.json"
            )
        """
        result = await theme_manager.export_theme(theme_name, file_path)

        if result.startswith("Error"):
            return json.dumps({"error": result})

        return json.dumps(
            {
                "status": "success",
                "file_path": result,
                "message": f"Theme '{theme_name}' exported successfully",
            },
            indent=2,
        )

    @mcp.tool
    async def remotion_import_theme(file_path: str, theme_key: str | None = None) -> str:
        """
        Import a theme from a JSON file.

        Loads a theme from a JSON file and registers it for use. The theme
        will be available immediately for new compositions.

        Args:
            file_path: Path to theme JSON file
            theme_key: Optional key to register under (default: from file)

        Returns:
            JSON with import status and theme key

        Example:
            result = await remotion_import_theme(
                file_path="custom_theme.json",
                theme_key="my_custom"
            )
        """
        result = await theme_manager.import_theme(file_path, theme_key)

        if result.startswith("Error"):
            return json.dumps({"error": result})

        return json.dumps({"status": "success", "message": result}, indent=2)

    @mcp.tool
    async def remotion_get_theme_for_content(content_type: str) -> str:
        """
        Get recommended themes for a content type.

        Suggests suitable themes based on the type of content you're creating.
        Searches theme use cases and descriptions for matches.

        Args:
            content_type: Type of content (e.g., "tutorial", "vlog", "review")

        Returns:
            JSON with recommended themes

        Example:
            recommendations = await remotion_get_theme_for_content(
                content_type="gaming"
            )
            # Returns gaming theme and possibly tech theme
        """

        def _get():
            matches = theme_manager.search_themes(content_type)

            if not matches:
                # If no direct matches, suggest popular themes
                return json.dumps(
                    {
                        "content_type": content_type,
                        "recommendations": [],
                        "message": "No specific matches found",
                        "popular_themes": ["tech", "minimal", "business"],
                    },
                    indent=2,
                )

            recommendations = []
            for key in matches:
                theme = theme_manager.get_theme(key)
                if theme:
                    recommendations.append(
                        {
                            "key": key,
                            "name": theme.name,
                            "description": theme.description,
                            "use_cases": theme.use_cases,
                        }
                    )

            return json.dumps(
                {"content_type": content_type, "recommendations": recommendations}, indent=2
            )

        return await asyncio.get_event_loop().run_in_executor(None, _get)
