# chuk-motion/src/chuk_motion/themes/themes_manager.py
"""
Theme manager for Remotion video compositions.
Central system for managing and applying themes.

The theme system provides:
- Built-in YouTube-optimized themes
- Custom theme creation and registration
- Theme discovery and comparison
- Theme validation
- Export/import for sharing
"""

import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from chuk_virtual_fs import AsyncVirtualFileSystem

from .models import Theme
from .youtube_themes import YOUTUBE_THEMES


class ThemeManager:
    """
    Manages themes for Remotion video compositions.
    Provides theme registration, selection, discovery, and application.
    """

    def __init__(self, vfs: "AsyncVirtualFileSystem"):
        """
        Initialize theme manager with built-in themes.

        Args:
            vfs: Virtual filesystem for file operations
        """
        self.vfs = vfs
        self.themes: dict[str, Theme] = {}
        self.current_theme: str | None = None
        self._register_builtin_themes()

    def _register_builtin_themes(self):
        """Register all built-in YouTube-optimized themes."""
        # YOUTUBE_THEMES is now a ThemeCollection with Pydantic Theme models
        for theme_key, theme in YOUTUBE_THEMES.items():
            self.themes[theme_key] = theme

    def register_theme(self, theme_key: str, theme: Theme) -> None:
        """
        Register a custom theme.

        Args:
            theme_key: Unique identifier for the theme
            theme: Theme object to register
        """
        self.themes[theme_key] = theme

    def list_themes(self) -> list[str]:
        """
        List all registered theme keys.

        Returns:
            List of theme keys
        """
        return list(self.themes.keys())

    def get_theme(self, theme_key: str) -> Theme | None:
        """
        Get a theme by key.

        Args:
            theme_key: Theme identifier

        Returns:
            Theme object or None if not found
        """
        return self.themes.get(theme_key)

    def get_theme_info(self, theme_key: str) -> dict[str, Any] | None:
        """
        Get detailed information about a theme.

        Args:
            theme_key: Theme identifier

        Returns:
            Dictionary with theme information or None
        """
        theme = self.get_theme(theme_key)
        if not theme:
            return None

        # Use model_dump() to convert Pydantic models to dicts
        return theme.model_dump()

    def set_current_theme(self, theme_key: str) -> bool:
        """
        Set the current active theme.

        Args:
            theme_key: Theme identifier

        Returns:
            True if successful, False if theme not found
        """
        if theme_key not in self.themes:
            return False
        self.current_theme = theme_key
        return True

    def get_current_theme(self) -> str | None:
        """
        Get the currently active theme key.

        Returns:
            Current theme key or None
        """
        return self.current_theme

    def compare_themes(self, theme_key1: str, theme_key2: str) -> dict[str, Any]:
        """
        Compare two themes side by side.

        Args:
            theme_key1: First theme identifier
            theme_key2: Second theme identifier

        Returns:
            Dictionary with comparison data
        """
        theme1 = self.get_theme(theme_key1)
        theme2 = self.get_theme(theme_key2)

        if not theme1 or not theme2:
            return {"error": "One or both themes not found"}

        return {
            "themes": [theme_key1, theme_key2],
            "comparison": {
                "names": [theme1.name, theme2.name],
                "descriptions": [theme1.description, theme2.description],
                "primary_colors": [
                    theme1.colors.primary,
                    theme2.colors.primary,
                ],
                "accent_colors": [theme1.colors.accent, theme2.colors.accent],
                "motion_feel": [
                    theme1.motion.default_spring.feel,
                    theme2.motion.default_spring.feel,
                ],
                "use_cases": [theme1.use_cases, theme2.use_cases],
            },
        }

    def search_themes(self, query: str) -> list[str]:
        """
        Search themes by name, description, or use case.

        Args:
            query: Search query string

        Returns:
            List of matching theme keys
        """
        query_lower = query.lower()
        matches = []

        for theme_key, theme in self.themes.items():
            # Search in name
            if query_lower in theme.name.lower():
                matches.append(theme_key)
                continue

            # Search in description
            if query_lower in theme.description.lower():
                matches.append(theme_key)
                continue

            # Search in use cases
            for use_case in theme.use_cases:
                if query_lower in use_case.lower():
                    matches.append(theme_key)
                    break

        return matches

    def get_themes_by_category(self, category: str) -> list[str]:
        """
        Get themes suitable for a content category.

        Args:
            category: Content category (e.g., "gaming", "education", "business")

        Returns:
            List of suitable theme keys
        """
        return self.search_themes(category)

    def validate_theme(self, theme_data: dict[str, Any]) -> dict[str, Any]:
        """
        Validate theme data structure using Pydantic model.

        Args:
            theme_data: Theme dictionary to validate

        Returns:
            Dictionary with validation results
        """
        try:
            # Pydantic will validate the structure
            Theme(**theme_data)
            return {"valid": True, "errors": []}
        except Exception as e:
            return {"valid": False, "errors": [str(e)]}

    async def export_theme(self, theme_key: str, file_path: str | None = None) -> str:
        """
        Export theme to JSON file.

        Args:
            theme_key: Theme identifier
            file_path: Optional output file path (defaults to theme_name.json)

        Returns:
            Path to exported file or error message
        """
        theme = self.get_theme(theme_key)
        if not theme:
            return f"Error: Theme '{theme_key}' not found"

        if not file_path:
            file_path = f"{theme_key}_theme.json"

        try:
            # Use model_dump_json() for direct JSON serialization
            json_content = theme.model_dump_json(indent=2)
            await self.vfs.write_file(file_path, json_content)
            return file_path
        except Exception as e:
            return f"Error exporting theme: {str(e)}"

    async def import_theme(self, file_path: str, theme_key: str | None = None) -> str:
        """
        Import theme from JSON file.

        Args:
            file_path: Path to JSON file
            theme_key: Optional key to register theme under (defaults to name from file)

        Returns:
            Success message or error
        """
        try:
            json_content = await self.vfs.read_text(file_path)
            theme_data = json.loads(json_content)

            # Validate and create theme using Pydantic
            theme = Theme(**theme_data)

            # Register theme
            key = theme_key or theme.name.lower().replace(" ", "_")
            self.register_theme(key, theme)

            return f"Successfully imported theme '{theme.name}' as '{key}'"

        except Exception as e:
            return f"Error importing theme: {str(e)}"

    def create_custom_theme(
        self,
        name: str,
        description: str,
        base_theme: str | None = None,
        color_overrides: dict[str, Any] | None = None,
        typography_overrides: dict[str, Any] | None = None,
        motion_overrides: dict[str, Any] | None = None,
    ) -> str:
        """
        Create a custom theme, optionally based on an existing theme.

        Args:
            name: Custom theme name
            description: Theme description
            base_theme: Optional base theme to start from
            color_overrides: Color tokens to override
            typography_overrides: Typography tokens to override
            motion_overrides: Motion tokens to override

        Returns:
            Theme key of created theme or error message
        """
        try:
            # Start with base theme or use defaults
            if base_theme and base_theme in self.themes:
                base = self.themes[base_theme]
                # Use model_copy for Pydantic models
                theme_dict = base.model_dump()

                # Apply overrides
                if color_overrides:
                    theme_dict["colors"].update(color_overrides)
                if typography_overrides:
                    theme_dict["typography"].update(typography_overrides)
                if motion_overrides:
                    theme_dict["motion"].update(motion_overrides)

                # Update name and description
                theme_dict["name"] = name
                theme_dict["description"] = description

                # Create new theme from modified dict
                theme = Theme(**theme_dict)
            else:
                # Create minimal theme (will fail validation, user must provide all required fields)
                return "Error: Must provide a base_theme or all required token overrides"

            # Register
            theme_key = name.lower().replace(" ", "_")
            self.register_theme(theme_key, theme)

            return theme_key

        except Exception as e:
            return f"Error creating custom theme: {str(e)}"
