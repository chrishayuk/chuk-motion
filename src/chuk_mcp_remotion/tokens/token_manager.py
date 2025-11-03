# chuk-mcp-remotion/src/chuk_mcp_remotion/tokens/token_manager.py
"""
Token Manager for individual token type management.

Provides import/export and customization for:
- Typography tokens (font families, sizes, weights, styles)
- Color tokens (palettes, themes)
- Motion tokens (springs, easings, durations, presets)
"""

import contextlib
import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from chuk_virtual_fs import AsyncVirtualFileSystem

from .colors import COLOR_TOKENS
from .motion import MOTION_TOKENS
from .typography import TYPOGRAPHY_TOKENS


class TokenManager:
    """
    Manages design tokens with import/export capabilities.

    Allows customization and sharing of token sets across projects.
    """

    def __init__(self, vfs: "AsyncVirtualFileSystem"):
        """
        Initialize token manager with default tokens.

        Args:
            vfs: Virtual filesystem for file operations
        """
        self.vfs = vfs
        self.custom_typography_tokens: dict[str, Any] = {}
        self.custom_color_tokens: dict[str, Any] = {}
        self.custom_motion_tokens: dict[str, Any] = {}

    # ========================================================================
    # TYPOGRAPHY TOKEN MANAGEMENT
    # ========================================================================

    async def export_typography_tokens(
        self,
        file_path: str | None = None,
        include_all: bool = True,
        font_families_only: bool = False,
        text_styles_only: bool = False,
    ) -> str:
        """
        Export typography tokens to JSON file.

        Args:
            file_path: Output file path (default: typography_tokens.json)
            include_all: Include all typography tokens (default: True)
            font_families_only: Export only font families
            text_styles_only: Export only text styles

        Returns:
            Path to exported file or error message
        """
        if not file_path:
            file_path = "typography_tokens.json"

        try:
            # Build export data
            export_data = {}

            if include_all:
                export_data = TYPOGRAPHY_TOKENS.copy()
            else:
                if font_families_only:
                    export_data["font_families"] = TYPOGRAPHY_TOKENS["font_families"]
                if text_styles_only:
                    export_data["text_styles"] = TYPOGRAPHY_TOKENS["text_styles"]

            # Add custom tokens if any
            if self.custom_typography_tokens:
                export_data["custom"] = self.custom_typography_tokens

            json_content = json.dumps(export_data, indent=2)

            # Write to virtual filesystem
            await self.vfs.write_file(file_path, json_content)
            return file_path

        except Exception as e:
            return f"Error exporting typography tokens: {str(e)}"

    async def import_typography_tokens(self, file_path: str, merge: bool = True) -> str:
        """
        Import typography tokens from JSON file.

        Args:
            file_path: Path to JSON file
            merge: Merge with existing custom tokens (default: True)

        Returns:
            Success message or error
        """
        try:
            # Read from virtual filesystem
            json_content = await self.vfs.read_text(file_path)
            imported_data = json.loads(json_content)

            # Validate structure
            if not isinstance(imported_data, dict):
                return "Error: Invalid typography token format"

            if merge:
                # Merge with existing custom tokens
                self.custom_typography_tokens.update(imported_data)
            else:
                # Replace custom tokens
                self.custom_typography_tokens = imported_data

            return f"Successfully imported typography tokens from {file_path}"

        except Exception as e:
            return f"Error importing typography tokens: {str(e)}"

    def get_typography_token(
        self, category: str, key: str | None = None, use_custom: bool = True
    ) -> Any | None:
        """
        Get a typography token value.

        Args:
            category: Token category (font_families, font_sizes, etc.)
            key: Optional specific key within category
            use_custom: Check custom tokens first (default: True)

        Returns:
            Token value or None
        """
        # Check custom tokens first if enabled
        if use_custom and category in self.custom_typography_tokens:
            custom_value = self.custom_typography_tokens[category]
            if key and isinstance(custom_value, dict):
                return custom_value.get(key)
            return custom_value

        # Fall back to default tokens
        if category not in TYPOGRAPHY_TOKENS:
            return None

        value = TYPOGRAPHY_TOKENS[category]
        if key and isinstance(value, dict):
            return value.get(key)

        return value

    # ========================================================================
    # COLOR TOKEN MANAGEMENT
    # ========================================================================

    async def export_color_tokens(
        self, file_path: str | None = None, theme_name: str | None = None
    ) -> str:
        """
        Export color tokens to JSON file.

        Args:
            file_path: Output file path (default: color_tokens.json)
            theme_name: Export only specific theme (default: all themes)

        Returns:
            Path to exported file or error message
        """
        if not file_path:
            file_path = "color_tokens.json"

        try:
            # Build export data
            if theme_name:
                if theme_name not in COLOR_TOKENS:
                    return f"Error: Theme '{theme_name}' not found"
                export_data = {theme_name: COLOR_TOKENS[theme_name]}
            else:
                export_data = COLOR_TOKENS.copy()

            # Add custom tokens if any
            if self.custom_color_tokens:
                export_data["custom"] = self.custom_color_tokens

            json_content = json.dumps(export_data, indent=2)

            # Write to virtual filesystem
            await self.vfs.write_file(file_path, json_content)
            return file_path

        except Exception as e:
            return f"Error exporting color tokens: {str(e)}"

    async def import_color_tokens(self, file_path: str, merge: bool = True) -> str:
        """
        Import color tokens from JSON file.

        Args:
            file_path: Path to JSON file
            merge: Merge with existing custom tokens (default: True)

        Returns:
            Success message or error
        """
        try:
            # Read from virtual filesystem
            json_content = await self.vfs.read_text(file_path)
            imported_data = json.loads(json_content)

            # Validate structure
            if not isinstance(imported_data, dict):
                return "Error: Invalid color token format"

            if merge:
                self.custom_color_tokens.update(imported_data)
            else:
                self.custom_color_tokens = imported_data

            return f"Successfully imported color tokens from {file_path}"

        except Exception as e:
            return f"Error importing color tokens: {str(e)}"

    def get_color_token(
        self, theme_name: str, color_type: str | None = None, use_custom: bool = True
    ) -> Any | None:
        """
        Get a color token value.

        Args:
            theme_name: Theme name
            color_type: Optional color type (primary, accent, etc.)
            use_custom: Check custom tokens first (default: True)

        Returns:
            Token value or None
        """
        # Check custom tokens first
        if use_custom and theme_name in self.custom_color_tokens:
            custom_theme = self.custom_color_tokens[theme_name]
            if color_type:
                return custom_theme.get(color_type)
            return custom_theme

        # Fall back to default tokens
        if theme_name not in COLOR_TOKENS:
            return None

        theme = COLOR_TOKENS[theme_name]
        if color_type:
            return theme.get(color_type)

        return theme

    # ========================================================================
    # MOTION TOKEN MANAGEMENT
    # ========================================================================

    async def export_motion_tokens(
        self,
        file_path: str | None = None,
        springs_only: bool = False,
        easings_only: bool = False,
        presets_only: bool = False,
    ) -> str:
        """
        Export motion tokens to JSON file.

        Args:
            file_path: Output file path (default: motion_tokens.json)
            springs_only: Export only spring configs
            easings_only: Export only easing curves
            presets_only: Export only animation presets

        Returns:
            Path to exported file or error message
        """
        if not file_path:
            file_path = "motion_tokens.json"

        try:
            # Build export data
            export_data = {}

            if springs_only:
                export_data["spring_configs"] = MOTION_TOKENS["spring_configs"]
            elif easings_only:
                export_data["easing_curves"] = MOTION_TOKENS["easing_curves"]
            elif presets_only:
                export_data["animation_presets"] = MOTION_TOKENS["animation_presets"]
            else:
                # Export all
                export_data = MOTION_TOKENS.copy()

            # Add custom tokens if any
            if self.custom_motion_tokens:
                export_data["custom"] = self.custom_motion_tokens

            json_content = json.dumps(export_data, indent=2)

            # Write to virtual filesystem
            await self.vfs.write_file(file_path, json_content)
            return file_path

        except Exception as e:
            return f"Error exporting motion tokens: {str(e)}"

    async def import_motion_tokens(self, file_path: str, merge: bool = True) -> str:
        """
        Import motion tokens from JSON file.

        Args:
            file_path: Path to JSON file
            merge: Merge with existing custom tokens (default: True)

        Returns:
            Success message or error
        """
        try:
            # Read from virtual filesystem
            json_content = await self.vfs.read_text(file_path)
            imported_data = json.loads(json_content)

            # Validate structure
            if not isinstance(imported_data, dict):
                return "Error: Invalid motion token format"

            if merge:
                self.custom_motion_tokens.update(imported_data)
            else:
                self.custom_motion_tokens = imported_data

            return f"Successfully imported motion tokens from {file_path}"

        except Exception as e:
            return f"Error importing motion tokens: {str(e)}"

    def get_motion_token(
        self, category: str, key: str | None = None, use_custom: bool = True
    ) -> Any | None:
        """
        Get a motion token value.

        Args:
            category: Token category (spring_configs, easing_curves, etc.)
            key: Optional specific key within category
            use_custom: Check custom tokens first (default: True)

        Returns:
            Token value or None
        """
        # Check custom tokens first
        if use_custom and category in self.custom_motion_tokens:
            custom_value = self.custom_motion_tokens[category]
            if key and isinstance(custom_value, dict):
                return custom_value.get(key)
            return custom_value

        # Fall back to default tokens
        if category not in MOTION_TOKENS:
            return None

        value = MOTION_TOKENS[category]
        if key and isinstance(value, dict):
            return value.get(key)

        return value

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def list_custom_tokens(self) -> dict[str, list[str]]:
        """
        List all custom tokens.

        Returns:
            Dictionary with custom token categories and their keys
        """
        return {
            "typography": list(self.custom_typography_tokens.keys()),
            "colors": list(self.custom_color_tokens.keys()),
            "motion": list(self.custom_motion_tokens.keys()),
        }

    def clear_custom_tokens(self, token_type: str | None = None) -> None:
        """
        Clear custom tokens.

        Args:
            token_type: Type to clear (typography, colors, motion), or None for all
        """
        if token_type == "typography" or token_type is None:
            self.custom_typography_tokens = {}

        if token_type == "colors" or token_type is None:
            self.custom_color_tokens = {}

        if token_type == "motion" or token_type is None:
            self.custom_motion_tokens = {}

    async def export_all_tokens(self, output_dir: str) -> dict[str, str]:
        """
        Export all token types to separate files.

        Args:
            output_dir: Directory to save token files

        Returns:
            Dictionary with file paths for each token type
        """
        # Ensure directory exists in virtual filesystem
        # Check if directory exists first (suppress errors if it already exists)
        with contextlib.suppress(Exception):
            await self.vfs.mkdir(output_dir)

        results = {
            "typography": await self.export_typography_tokens(
                f"{output_dir}/typography_tokens.json"
            ),
            "colors": await self.export_color_tokens(f"{output_dir}/color_tokens.json"),
            "motion": await self.export_motion_tokens(f"{output_dir}/motion_tokens.json"),
        }

        return results
