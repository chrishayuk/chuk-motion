# chuk-mcp-remotion/src/chuk_mcp_remotion/components/content/StylizedWebPage/tool.py
"""StylizedWebPage MCP tool."""

import asyncio

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.models import ComponentResponse, ErrorResponse


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
        track: str = "main",
        gap_before: float | str | None = None,
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
            track: Track name (default: "main")
            gap_before: Gap before component in seconds or time string

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
                        "Get started today"
                    ]
                else:
                    content_lines_value = content_lines

                component = ComponentInstance(
                    component_type="StylizedWebPage",
                    start_frame=0,
                    duration_frames=0,
                    props={
                        "title": title,
                        "subtitle": subtitle,
                        "showHeader": show_header,
                        "showSidebar": show_sidebar,
                        "showFooter": show_footer,
                        "headerText": header_text,
                        "sidebarItems": sidebar_items_value,
                        "contentLines": content_lines_value,
                        "footerText": footer_text,
                        "theme": theme,
                        "accentColor": accent_color,
                    },
                    layer=0,
                )

                component = project_manager.current_timeline.add_component(
                    component, duration=duration, track=track, gap_before=gap_before
                )

                return ComponentResponse(
                    component="StylizedWebPage",
                    start_time=project_manager.current_timeline.frames_to_seconds(
                        component.start_frame
                    ),
                    duration=duration,
                ).model_dump_json()
            except Exception as e:
                return ErrorResponse(error=str(e)).model_dump_json()

        return await asyncio.get_event_loop().run_in_executor(None, _add)
