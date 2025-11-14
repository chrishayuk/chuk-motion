"""
Token Tools for Remotion MCP Server

Provides async MCP tools for accessing design tokens (colors, typography, motion).
These tools give granular access to specific token categories and values.
"""

import asyncio
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chuk_virtual_fs import AsyncVirtualFileSystem

from ..tokens.colors import COLOR_TOKENS
from ..tokens.motion import MOTION_TOKENS
from ..tokens.token_manager import TokenManager
from ..tokens.typography import TYPOGRAPHY_TOKENS


def register_token_tools(mcp, project_manager, vfs: "AsyncVirtualFileSystem"):
    """
    Register design token tools with the MCP server.

    Args:
        mcp: ChukMCPServer instance
        project_manager: ProjectManager instance (for consistency)
        vfs: Virtual filesystem instance for file operations
    """

    # Create token manager instance with virtual filesystem
    token_manager = TokenManager(vfs)

    # ========================================================================
    # COLOR TOKEN TOOLS
    # ========================================================================

    @mcp.tool
    async def remotion_list_color_tokens() -> str:
        """
        List all available color tokens organized by theme.

        Returns the complete color palette system including primary, accent,
        gradient, background, text, and semantic colors for all themes.

        Returns:
            JSON object with color tokens for all themes

        Example:
            colors = await remotion_list_color_tokens()
            # Returns all color tokens across all themes
        """

        def _list():
            return json.dumps(COLOR_TOKENS, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _list)

    @mcp.tool
    async def remotion_get_theme_colors(theme_name: str) -> str:
        """
        Get color tokens for a specific theme.

        Returns all color tokens (primary, accent, gradients, backgrounds,
        text colors, and semantic colors) for a single theme.

        Args:
            theme_name: Theme identifier (e.g., "tech", "finance")

        Returns:
            JSON with theme colors

        Example:
            tech_colors = await remotion_get_theme_colors(theme_name="tech")
            # Returns tech theme colors only
        """

        def _get():
            if theme_name not in COLOR_TOKENS:
                return json.dumps(
                    {
                        "error": f"Theme '{theme_name}' not found",
                        "available_themes": list(COLOR_TOKENS.keys()),
                    }
                )

            return json.dumps({"theme": theme_name, "colors": COLOR_TOKENS[theme_name]}, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    @mcp.tool
    async def remotion_get_color_value(
        theme_name: str, color_type: str, index: int | None = None
    ) -> str:
        """
        Get a specific color value from a theme.

        Retrieves a single color value for use in components. Useful for
        getting exact hex values for custom styling.

        Args:
            theme_name: Theme identifier
            color_type: Color type (primary, accent, gradient, background, text, semantic)
            index: Optional index for array colors (0, 1, 2 for primary/accent)

        Returns:
            JSON with color value

        Example:
            primary = await remotion_get_color_value(
                theme_name="tech",
                color_type="primary",
                index=0
            )
            # Returns "#0066FF"
        """

        def _get():
            if theme_name not in COLOR_TOKENS:
                return json.dumps({"error": f"Theme '{theme_name}' not found"})

            theme_colors = COLOR_TOKENS[theme_name]

            if color_type not in theme_colors:
                return json.dumps(
                    {
                        "error": f"Color type '{color_type}' not found",
                        "available_types": list(theme_colors.keys()),
                    }
                )

            color_value = theme_colors[color_type]

            # Handle array colors (primary, accent)
            if isinstance(color_value, list):
                if index is None:
                    return json.dumps(
                        {"theme": theme_name, "color_type": color_type, "values": color_value},
                        indent=2,
                    )
                elif 0 <= index < len(color_value):
                    return json.dumps(
                        {
                            "theme": theme_name,
                            "color_type": color_type,
                            "index": index,
                            "value": color_value[index],
                        }
                    )
                else:
                    return json.dumps(
                        {
                            "error": f"Index {index} out of range",
                            "available_indices": list(range(len(color_value))),
                        }
                    )

            # Handle dict colors (background, text, semantic)
            elif isinstance(color_value, dict):
                return json.dumps(
                    {"theme": theme_name, "color_type": color_type, "values": color_value}, indent=2
                )

            # Handle string colors (gradient)
            else:
                return json.dumps(
                    {"theme": theme_name, "color_type": color_type, "value": color_value}
                )

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    # ========================================================================
    # TYPOGRAPHY TOKEN TOOLS
    # ========================================================================

    @mcp.tool
    async def remotion_list_typography_tokens() -> str:
        """
        List all available typography tokens.

        Returns font families, sizes (for all resolutions), weights,
        line heights, letter spacing, and text styles.

        Returns:
            JSON object with complete typography system

        Example:
            typography = await remotion_list_typography_tokens()
            # Returns font families, sizes, weights, text styles
        """

        def _list():
            return json.dumps(TYPOGRAPHY_TOKENS, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _list)

    @mcp.tool
    async def remotion_get_font_families() -> str:
        """
        Get available font families.

        Returns all font family definitions including display, body,
        monospace, and decorative fonts.

        Returns:
            JSON with font family definitions

        Example:
            fonts = await remotion_get_font_families()
            # Returns display, body, mono, decorative font stacks
        """

        def _get():
            return json.dumps({"font_families": TYPOGRAPHY_TOKENS["font_families"]}, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    @mcp.tool
    async def remotion_get_font_sizes(resolution: str = "video_1080p") -> str:
        """
        Get font sizes for a specific video resolution.

        Returns font size scale (xs, sm, base, lg, xl, 2xl, 3xl, 4xl)
        optimized for the specified resolution.

        Args:
            resolution: Video resolution (video_1080p, video_4k, video_720p)

        Returns:
            JSON with font sizes

        Example:
            sizes = await remotion_get_font_sizes(resolution="video_1080p")
            # Returns sizes optimized for 1080p video
        """

        def _get():
            if resolution not in TYPOGRAPHY_TOKENS["font_sizes"]:
                return json.dumps(
                    {
                        "error": f"Resolution '{resolution}' not found",
                        "available_resolutions": list(TYPOGRAPHY_TOKENS["font_sizes"].keys()),
                    }
                )

            return json.dumps(
                {
                    "resolution": resolution,
                    "font_sizes": TYPOGRAPHY_TOKENS["font_sizes"][resolution],
                },
                indent=2,
            )

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    @mcp.tool
    async def remotion_get_text_style(style_name: str) -> str:
        """
        Get a specific text style preset.

        Returns a pre-configured text style combining font size, weight,
        line height, letter spacing, and font family.

        Args:
            style_name: Style name (hero_title, title, heading, subheading, body, caption, small)

        Returns:
            JSON with text style configuration

        Example:
            style = await remotion_get_text_style(style_name="hero_title")
            # Returns hero title style (4xl, black weight, tight line height)
        """

        def _get():
            if style_name not in TYPOGRAPHY_TOKENS["text_styles"]:
                return json.dumps(
                    {
                        "error": f"Style '{style_name}' not found",
                        "available_styles": list(TYPOGRAPHY_TOKENS["text_styles"].keys()),
                    }
                )

            return json.dumps(
                {"style_name": style_name, "style": TYPOGRAPHY_TOKENS["text_styles"][style_name]},
                indent=2,
            )

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    # ========================================================================
    # MOTION TOKEN TOOLS
    # ========================================================================

    @mcp.tool
    async def remotion_list_motion_tokens() -> str:
        """
        List all available motion design tokens.

        Returns spring configurations, easing curves, duration presets,
        animation presets, and YouTube optimization guidelines.

        Returns:
            JSON object with complete motion system

        Example:
            motion = await remotion_list_motion_tokens()
            # Returns springs, easings, durations, animation presets
        """

        def _list():
            return json.dumps(MOTION_TOKENS, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _list)

    @mcp.tool
    async def remotion_get_spring_configs() -> str:
        """
        Get available spring animation configurations.

        Returns all spring configs (gentle, smooth, bouncy, snappy, elastic)
        with their damping, mass, and stiffness values.

        Returns:
            JSON with spring configurations

        Example:
            springs = await remotion_get_spring_configs()
            # Returns all spring animation configs
        """

        def _get():
            return json.dumps({"spring_configs": MOTION_TOKENS["spring_configs"]}, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    @mcp.tool
    async def remotion_get_spring_config(spring_name: str) -> str:
        """
        Get a specific spring animation configuration.

        Returns details for a single spring config including damping,
        mass, stiffness, and usage recommendations.

        Args:
            spring_name: Spring name (gentle, smooth, bouncy, snappy, elastic)

        Returns:
            JSON with spring configuration

        Example:
            bouncy = await remotion_get_spring_config(spring_name="bouncy")
            # Returns bouncy spring config with playful overshoot
        """

        def _get():
            if spring_name not in MOTION_TOKENS["spring_configs"]:
                return json.dumps(
                    {
                        "error": f"Spring '{spring_name}' not found",
                        "available_springs": list(MOTION_TOKENS["spring_configs"].keys()),
                    }
                )

            return json.dumps(
                {
                    "spring_name": spring_name,
                    "config": MOTION_TOKENS["spring_configs"][spring_name],
                },
                indent=2,
            )

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    @mcp.tool
    async def remotion_get_easing_curves() -> str:
        """
        Get available easing curve definitions.

        Returns all easing curves with their cubic bezier values and
        CSS equivalents.

        Returns:
            JSON with easing curves

        Example:
            easings = await remotion_get_easing_curves()
            # Returns linear, ease-in, ease-out, ease-in-out, back easings, etc.
        """

        def _get():
            return json.dumps({"easing_curves": MOTION_TOKENS["easing_curves"]}, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    @mcp.tool
    async def remotion_get_easing_curve(easing_name: str) -> str:
        """
        Get a specific easing curve definition.

        Returns details for a single easing curve including bezier values,
        CSS value, and usage recommendations.

        Args:
            easing_name: Easing name (linear, ease_in, ease_out, ease_in_out, etc.)

        Returns:
            JSON with easing curve definition

        Example:
            ease = await remotion_get_easing_curve(easing_name="ease_out_back")
            # Returns ease_out_back with overshoot effect
        """

        def _get():
            if easing_name not in MOTION_TOKENS["easing_curves"]:
                return json.dumps(
                    {
                        "error": f"Easing '{easing_name}' not found",
                        "available_easings": list(MOTION_TOKENS["easing_curves"].keys()),
                    }
                )

            return json.dumps(
                {"easing_name": easing_name, "curve": MOTION_TOKENS["easing_curves"][easing_name]},
                indent=2,
            )

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    @mcp.tool
    async def remotion_get_durations() -> str:
        """
        Get available duration presets.

        Returns standardized timing values in both frames and seconds
        for consistent animation durations.

        Returns:
            JSON with duration presets

        Example:
            durations = await remotion_get_durations()
            # Returns instant, ultra_fast, fast, normal, moderate, slow, etc.
        """

        def _get():
            return json.dumps({"durations": MOTION_TOKENS["durations"]}, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    @mcp.tool
    async def remotion_get_duration(duration_name: str) -> str:
        """
        Get a specific duration preset.

        Returns frame count and seconds for a specific duration preset.

        Args:
            duration_name: Duration name (instant, ultra_fast, fast, normal, etc.)

        Returns:
            JSON with duration values

        Example:
            normal = await remotion_get_duration(duration_name="normal")
            # Returns 20 frames / 0.667 seconds
        """

        def _get():
            if duration_name not in MOTION_TOKENS["durations"]:
                return json.dumps(
                    {
                        "error": f"Duration '{duration_name}' not found",
                        "available_durations": list(MOTION_TOKENS["durations"].keys()),
                    }
                )

            return json.dumps(
                {
                    "duration_name": duration_name,
                    "duration": MOTION_TOKENS["durations"][duration_name],
                },
                indent=2,
            )

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    @mcp.tool
    async def remotion_get_animation_presets() -> str:
        """
        Get available animation presets.

        Returns pre-configured animation combinations (fade, slide, scale, bounce)
        with their properties, easing, and duration settings.

        Returns:
            JSON with animation presets

        Example:
            presets = await remotion_get_animation_presets()
            # Returns fade_in, slide_up, scale_in, bounce_in, etc.
        """

        def _get():
            return json.dumps({"animation_presets": MOTION_TOKENS["animation_presets"]}, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    @mcp.tool
    async def remotion_get_animation_preset(preset_name: str) -> str:
        """
        Get a specific animation preset.

        Returns configuration for a single animation preset including
        properties, from/to values, easing, and duration.

        Args:
            preset_name: Preset name (fade_in, slide_up, scale_in, etc.)

        Returns:
            JSON with animation preset

        Example:
            fade = await remotion_get_animation_preset(preset_name="fade_in")
            # Returns fade_in animation: opacity 0 → 1, ease_out, normal duration
        """

        def _get():
            if preset_name not in MOTION_TOKENS["animation_presets"]:
                return json.dumps(
                    {
                        "error": f"Preset '{preset_name}' not found",
                        "available_presets": list(MOTION_TOKENS["animation_presets"].keys()),
                    }
                )

            return json.dumps(
                {
                    "preset_name": preset_name,
                    "preset": MOTION_TOKENS["animation_presets"][preset_name],
                },
                indent=2,
            )

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    @mcp.tool
    async def remotion_get_youtube_optimizations() -> str:
        """
        Get YouTube optimization guidelines for motion design.

        Returns recommendations for hook timing (first 3 seconds),
        pattern interrupts, and retention timing to maximize viewer engagement.

        Returns:
            JSON with YouTube optimization guidelines

        Example:
            youtube_opts = await remotion_get_youtube_optimizations()
            # Returns timing recommendations for YouTube content
        """

        def _get():
            return json.dumps(
                {"youtube_optimizations": MOTION_TOKENS["youtube_optimizations"]}, indent=2
            )

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    # ========================================================================
    # TOKEN IMPORT/EXPORT TOOLS
    # ========================================================================

    @mcp.tool
    async def remotion_export_typography_tokens(
        file_path: str | None = None,
        include_all: bool = True,
        font_families_only: bool = False,
        text_styles_only: bool = False,
    ) -> str:
        """
        Export typography tokens to a JSON file.

        Saves typography tokens (font families, sizes, weights, text styles)
        to a file for sharing across projects or version control.

        Args:
            file_path: Output file path (default: typography_tokens.json)
            include_all: Include all typography tokens (default: True)
            font_families_only: Export only font families
            text_styles_only: Export only text styles

        Returns:
            JSON with export status and file path

        Example:
            result = await remotion_export_typography_tokens(
                file_path="my_typography.json",
                include_all=True
            )
        """
        result = await token_manager.export_typography_tokens(
            file_path=file_path,
            include_all=include_all,
            font_families_only=font_families_only,
            text_styles_only=text_styles_only,
        )

        if result.startswith("Error"):
            return json.dumps({"error": result})

        return json.dumps(
            {
                "status": "success",
                "file_path": result,
                "message": "Typography tokens exported successfully",
            },
            indent=2,
        )

    @mcp.tool
    async def remotion_import_typography_tokens(file_path: str, merge: bool = True) -> str:
        """
        Import typography tokens from a JSON file.

        Loads typography tokens from a file and merges them with existing
        custom tokens or replaces them entirely.

        Args:
            file_path: Path to typography tokens JSON file
            merge: Merge with existing custom tokens (default: True)

        Returns:
            JSON with import status

        Example:
            result = await remotion_import_typography_tokens(
                file_path="custom_typography.json",
                merge=True
            )
        """
        result = await token_manager.import_typography_tokens(file_path=file_path, merge=merge)

        if result.startswith("Error"):
            return json.dumps({"error": result})

        return json.dumps({"status": "success", "message": result}, indent=2)

    @mcp.tool
    async def remotion_export_color_tokens(
        file_path: str | None = None, theme_name: str | None = None
    ) -> str:
        """
        Export color tokens to a JSON file.

        Saves color tokens to a file. Can export all themes or a specific theme.

        Args:
            file_path: Output file path (default: color_tokens.json)
            theme_name: Export only specific theme (default: all themes)

        Returns:
            JSON with export status and file path

        Example:
            result = await remotion_export_color_tokens(
                file_path="my_colors.json",
                theme_name="tech"
            )
        """
        result = await token_manager.export_color_tokens(file_path=file_path, theme_name=theme_name)

        if result.startswith("Error"):
            return json.dumps({"error": result})

        return json.dumps(
            {
                "status": "success",
                "file_path": result,
                "message": "Color tokens exported successfully",
            },
            indent=2,
        )

    @mcp.tool
    async def remotion_import_color_tokens(file_path: str, merge: bool = True) -> str:
        """
        Import color tokens from a JSON file.

        Loads color tokens from a file and merges them with existing
        custom tokens or replaces them entirely.

        Args:
            file_path: Path to color tokens JSON file
            merge: Merge with existing custom tokens (default: True)

        Returns:
            JSON with import status

        Example:
            result = await remotion_import_color_tokens(
                file_path="custom_colors.json",
                merge=True
            )
        """
        result = await token_manager.import_color_tokens(file_path=file_path, merge=merge)

        if result.startswith("Error"):
            return json.dumps({"error": result})

        return json.dumps({"status": "success", "message": result}, indent=2)

    @mcp.tool
    async def remotion_export_motion_tokens(
        file_path: str | None = None,
        springs_only: bool = False,
        easings_only: bool = False,
        presets_only: bool = False,
    ) -> str:
        """
        Export motion tokens to a JSON file.

        Saves motion tokens (springs, easings, durations, presets) to a file.

        Args:
            file_path: Output file path (default: motion_tokens.json)
            springs_only: Export only spring configs
            easings_only: Export only easing curves
            presets_only: Export only animation presets

        Returns:
            JSON with export status and file path

        Example:
            result = await remotion_export_motion_tokens(
                file_path="my_motion.json",
                springs_only=False
            )
        """
        result = await token_manager.export_motion_tokens(
            file_path=file_path,
            springs_only=springs_only,
            easings_only=easings_only,
            presets_only=presets_only,
        )

        if result.startswith("Error"):
            return json.dumps({"error": result})

        return json.dumps(
            {
                "status": "success",
                "file_path": result,
                "message": "Motion tokens exported successfully",
            },
            indent=2,
        )

    @mcp.tool
    async def remotion_import_motion_tokens(file_path: str, merge: bool = True) -> str:
        """
        Import motion tokens from a JSON file.

        Loads motion tokens from a file and merges them with existing
        custom tokens or replaces them entirely.

        Args:
            file_path: Path to motion tokens JSON file
            merge: Merge with existing custom tokens (default: True)

        Returns:
            JSON with import status

        Example:
            result = await remotion_import_motion_tokens(
                file_path="custom_motion.json",
                merge=True
            )
        """
        result = await token_manager.import_motion_tokens(file_path=file_path, merge=merge)

        if result.startswith("Error"):
            return json.dumps({"error": result})

        return json.dumps({"status": "success", "message": result}, indent=2)

    @mcp.tool
    async def remotion_export_all_tokens(output_dir: str) -> str:
        """
        Export all token types to separate files in a directory.

        Creates three files: typography_tokens.json, color_tokens.json, and
        motion_tokens.json in the specified directory.

        Args:
            output_dir: Directory to save token files

        Returns:
            JSON with export status and file paths

        Example:
            result = await remotion_export_all_tokens(
                output_dir="my_tokens"
            )
        """
        results = await token_manager.export_all_tokens(output_dir)

        return json.dumps(
            {"status": "success", "files": results, "message": "All tokens exported successfully"},
            indent=2,
        )
