"""
TSX Component Builder - Generates Remotion React components from templates.

Uses Jinja2 templates to generate type-safe TSX components.
"""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from ..themes.youtube_themes import YOUTUBE_THEMES
from ..tokens.spacing import SPACING_TOKENS
from ..tokens.typography import TYPOGRAPHY_TOKENS


class ComponentBuilder:
    """Builds TSX components from templates and configurations."""

    def __init__(self):
        """Initialize the component builder with Jinja2 environment."""
        # Get template directory - now in components folder
        self.components_dir = Path(__file__).parent.parent / "components"

        # Also keep old template directory for backwards compatibility
        self.old_template_dir = Path(__file__).parent / "templates"

        # Create Jinja2 environment with multiple search paths
        search_paths = [str(self.components_dir)]
        if self.old_template_dir.exists():
            search_paths.append(str(self.old_template_dir))

        self.env = Environment(
            loader=FileSystemLoader(search_paths),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=False,  # Don't escape TSX code
            # Use [[ ]] for variables and [% %] for statements to avoid JSX {} conflicts
            variable_start_string="[[",
            variable_end_string="]]",
            block_start_string="[%",
            block_end_string="%]",
        )

        # Add custom filters
        self.env.filters["to_camel_case"] = self._to_camel_case
        self.env.filters["to_pascal_case"] = self._to_pascal_case

        # Template categories for organized template discovery
        self.template_categories = [
            "charts",
            "overlays",
            "layouts",
            "code",
            "animations",
            "content",
            "demo_realism",
        ]

    def _to_camel_case(self, snake_str: str) -> str:
        """Convert snake_case to camelCase."""
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    def _to_pascal_case(self, snake_str: str) -> str:
        """Convert snake_case to PascalCase."""
        return "".join(x.title() for x in snake_str.split("_"))

    def _find_template(self, component_name: str) -> str:
        """
        Find template file in component folders or old template structure.

        Args:
            component_name: Name of the component (e.g., "LowerThird")

        Returns:
            Template path relative to search paths
        """
        # New structure: components/[category]/[Component]/template.tsx.j2
        for category in self.template_categories:
            component_template = self.components_dir / category / component_name / "template.tsx.j2"
            if component_template.exists():
                return f"{category}/{component_name}/template.tsx.j2"

        # Old structure: templates/[category]/[Component].tsx.j2 (backwards compatibility)
        template_filename = f"{component_name}.tsx.j2"

        # Try old root directory
        if self.old_template_dir.exists():
            root_template = self.old_template_dir / template_filename
            if root_template.exists():
                return template_filename

            # Try old category subdirectories
            for category in self.template_categories:
                category_template = self.old_template_dir / category / template_filename
                if category_template.exists():
                    return f"{category}/{template_filename}"

        # If not found, raise error
        raise ValueError(f"Template {template_filename} not found in any category")

    def build_component(
        self, component_name: str, config: dict[str, Any], theme_name: str = "tech"
    ) -> str:
        """
        Build a TSX component from configuration.

        Args:
            component_name: Name of the component (e.g., "LowerThird")
            config: Component configuration dictionary
            theme_name: Theme to apply

        Returns:
            Generated TSX component code as string
        """
        # Get theme (now returns a Pydantic Theme model)
        theme = YOUTUBE_THEMES.get(theme_name, YOUTUBE_THEMES["tech"])
        assert theme is not None, f"Theme '{theme_name}' not found"

        # Find and get template
        try:
            template_path = self._find_template(component_name)
            template = self.env.get_template(template_path)
        except Exception as e:
            raise ValueError(f"Template not found for {component_name}: {e}") from e

        # Get font sizes for the theme's resolution
        resolution = theme.typography.default_resolution
        font_sizes = getattr(TYPOGRAPHY_TOKENS.font_sizes, resolution)

        # Build typography context with font_sizes for template compatibility
        # This maintains backwards compatibility with existing templates that expect typography.font_sizes
        typography_context = theme.typography.model_dump()
        typography_context["font_sizes"] = TYPOGRAPHY_TOKENS.font_sizes.model_dump()
        typography_context["font_weights"] = TYPOGRAPHY_TOKENS.font_weights.model_dump()
        typography_context["line_heights"] = TYPOGRAPHY_TOKENS.line_heights.model_dump()
        typography_context["letter_spacing"] = TYPOGRAPHY_TOKENS.letter_spacing.model_dump()

        # Render template - convert Pydantic models to dicts for Jinja2 template compatibility
        tsx_code = template.render(
            config=config,
            theme=theme.model_dump(),
            colors=theme.colors.model_dump(),
            typography=typography_context,
            motion=theme.motion.model_dump(),
            spacing=SPACING_TOKENS.model_dump(),
            font_sizes=font_sizes.model_dump(),
            # Also include global token singletons for convenience
            TYPOGRAPHY_TOKENS=TYPOGRAPHY_TOKENS,
            SPACING_TOKENS=SPACING_TOKENS,
        )

        return tsx_code

    def build_lower_third(
        self,
        name: str,
        title: str | None = None,
        variant: str = "glass",
        position: str = "bottom_left",
        theme_name: str = "tech",
    ) -> str:
        """
        Build a LowerThird component.

        Args:
            name: Main name/text
            title: Optional subtitle
            variant: Style variant (minimal, standard, glass, bold, animated)
            position: Screen position
            theme_name: Theme to apply

        Returns:
            TSX component code
        """
        config = {"name": name, "title": title, "variant": variant, "position": position}
        return self.build_component("LowerThird", config, theme_name)

    def build_title_scene(
        self,
        text: str,
        subtitle: str | None = None,
        variant: str = "bold",
        animation: str = "fade_zoom",
        theme_name: str = "tech",
    ) -> str:
        """
        Build a TitleScene component.

        Args:
            text: Main title text
            subtitle: Optional subtitle
            variant: Style variant (minimal, standard, bold, kinetic)
            animation: Animation style
            theme_name: Theme to apply

        Returns:
            TSX component code
        """
        config = {"text": text, "subtitle": subtitle, "variant": variant, "animation": animation}
        return self.build_component("TitleScene", config, theme_name)

    def get_theme_styles(self, theme_name: str) -> str:
        """
        Generate CSS-in-JS styles for a theme.

        Args:
            theme_name: Name of the theme

        Returns:
            JavaScript object with theme styles
        """
        theme = YOUTUBE_THEMES.get(theme_name, YOUTUBE_THEMES["tech"])
        assert theme is not None, f"Theme '{theme_name}' not found"
        colors = theme.colors

        styles = {
            "primary": colors.primary[0] if isinstance(colors.primary, list) else colors.primary,
            "accent": colors.accent[0] if isinstance(colors.accent, list) else colors.accent,
            "gradient": colors.gradient,
            "background": colors.background.model_dump(),
            "text": colors.text.model_dump(),
        }

        return f"export const themeStyles = {styles};"
