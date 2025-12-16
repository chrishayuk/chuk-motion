# chuk-motion/src/chuk_motion/components/content/StylizedWebPage/tool.py
"""StylizedWebPage MCP tool."""

import asyncio

from chuk_motion.models import ComponentResponse, ErrorResponse


def register_tool(mcp, project_manager):
    """Register the StylizedWebPage tool with the MCP server."""

    @mcp.tool
    async def remotion_add_stylized_webpage(
        title: str = "Website Title",
        subtitle: str = "Tagline or description",
        show_header: bool = True,
        show_sidebar: bool = False,
        show_footer: bool = False,
        header_text: str = "Navigation",
        sidebar_items: list[str] | None = None,
        content_lines: list[str] | None = None,
        footer_text: str = "© 2024 Company",
        theme: str = "light",
        accent_color: str = "primary",
        duration: float | str = 5.0,
    ) -> str:
        """
        Add StylizedWebPage to the composition.

        Stylized webpage mockup with header, sidebar, content blocks, and footer.
        Perfect for showing clean, simplified web page layouts in browser frames.

        Args:
            title: Page title displayed in header
            subtitle: Hero section subtitle
            show_header: Show header/navbar
            show_sidebar: Show sidebar navigation
            show_footer: Show footer
            header_text: Text in header nav area
            sidebar_items: List of sidebar navigation items (default: Dashboard, Analytics, Settings)
            content_lines: Main content block text lines (default: Welcome, Explore, Get started)
            footer_text: Footer text
            theme: Visual theme (light, dark)
            accent_color: Accent color (primary, accent, secondary)
            duration: Duration in seconds or time string (e.g., "2s", "500ms")

        Returns:
            JSON with component info
        """

        def _add():
            if not project_manager.current_timeline:
                return ErrorResponse(error="No active project.").model_dump_json()

            try:
                # Default values for lists
                if sidebar_items is None:
                    sidebar_items_value = ["Dashboard", "Analytics", "Settings"]
                else:
                    sidebar_items_value = sidebar_items

                if content_lines is None:
                    content_lines_value = [
                        "Welcome to our site",
                        "Explore our features",
                        "Get started today",
                    ]
                else:
                    content_lines_value = content_lines

                # Get builder and start time
                builder = project_manager.current_timeline
                start_time = builder.get_total_duration_seconds()

                # Add component using builder
                builder.add_stylized_web_page(
                    title=title,
                    subtitle=subtitle,
                    start_time=start_time,
                    show_header=show_header,
                    show_sidebar=show_sidebar,
                    show_footer=show_footer,
                    header_text=header_text,
                    sidebar_items=sidebar_items_value,
                    content_lines=content_lines_value,
                    footer_text=footer_text,
                    theme=theme,
                    accent_color=accent_color,
                    duration=duration,
                )

                return ComponentResponse(
                    component="StylizedWebPage",
                    start_time=start_time,
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
