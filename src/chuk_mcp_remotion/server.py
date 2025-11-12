#!/usr/bin/env python3
"""
Remotion MCP Server - AI-powered video generation with design system approach

This server provides MCP tools for creating Remotion video compositions using
a design-system-first approach inspired by shadcn/ui and chuk-mcp-pptx.
"""

import asyncio
import json
import logging
import os
import sys

from chuk_mcp_server import ChukMCPServer
from chuk_virtual_fs import AsyncVirtualFileSystem

# Import component auto-discovery system
from .components import get_component_registry, register_all_builders, register_all_tools
from .generator.composition_builder import CompositionBuilder
from .themes.youtube_themes import YOUTUBE_THEMES

# Import design system modules
from .tools.theme_tools import register_theme_tools
from .tools.token_tools import register_token_tools
from .utils.project_manager import ProjectManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server instance
mcp = ChukMCPServer("chuk-mcp-remotion")

# Create virtual filesystem instance (using file provider for actual file operations)
vfs = AsyncVirtualFileSystem(provider="file")

# Create project manager instance
project_manager = ProjectManager()

# Register composition builder methods dynamically from components
register_all_builders(CompositionBuilder)

# Register theme and token tools with virtual filesystem
register_theme_tools(mcp, project_manager, vfs)
register_token_tools(mcp, project_manager, vfs)

# Register all component tools automatically
register_all_tools(mcp, project_manager)

# Get component registry for discovery tools
COMPONENT_REGISTRY = get_component_registry()

# ============================================================================
# DISCOVERY TOOLS - Help LLMs explore the design system
# ============================================================================


@mcp.tool  # type: ignore[arg-type]
async def remotion_list_components(category: str | None = None) -> str:
    """
    List available Remotion video components with their schemas.

    Returns all available components organized by category. Each component
    includes its variants, properties, and usage examples. This helps LLMs
    discover what building blocks are available for video creation.

    Args:
        category: Optional category filter (scene, overlay, animation, chart, layout)
                 If not specified, returns all categories

    Returns:
        JSON object with component definitions organized by category

    Example:
        components = await remotion_list_components()
        # Returns all available components

        overlay_components = await remotion_list_components(category="overlay")
        # Returns only overlay components (lower thirds, captions, etc.)
    """

    def _list():
        if category:
            filtered = {
                name: comp
                for name, comp in COMPONENT_REGISTRY.items()
                if comp.get("category") == category
            }
            return json.dumps(filtered, indent=2)
        return json.dumps(COMPONENT_REGISTRY, indent=2)

    return await asyncio.get_event_loop().run_in_executor(None, _list)


@mcp.tool  # type: ignore[arg-type]
async def remotion_search_components(query: str) -> str:
    """
    Search for components by name or description.

    Performs a case-insensitive search across component names and descriptions.
    Useful when you know what you want but not the exact component name.

    Args:
        query: Search term to match against component names and descriptions

    Returns:
        JSON object with matching components and their details

    Example:
        results = await remotion_search_components(query="text")
        # Returns all components with "text" in name or description
        # (TitleScene, TextOverlay, TextAnimation, etc.)
    """

    def _search():
        query_lower = query.lower()
        results = {}

        for name, comp in COMPONENT_REGISTRY.items():
            # Search in component name
            if query_lower in name.lower():
                results[name] = comp
                continue

            # Search in description
            if query_lower in comp.get("description", "").lower():
                results[name] = comp
                continue

            # Search in category
            if query_lower in comp.get("category", "").lower():
                results[name] = comp

        return json.dumps(results, indent=2)

    return await asyncio.get_event_loop().run_in_executor(None, _search)


@mcp.tool  # type: ignore[arg-type]
async def remotion_get_component_schema(component_name: str) -> str:
    """
    Get detailed schema for a specific component.

    Returns the complete schema including all properties, variants, animations,
    and usage examples for a single component.

    Args:
        component_name: Name of the component (e.g., "LowerThird", "TitleScene")

    Returns:
        JSON object with component schema and examples

    Example:
        schema = await remotion_get_component_schema(component_name="LowerThird")
        # Returns full schema for lower third component including all variants
    """

    def _get_schema():
        if component_name not in COMPONENT_REGISTRY:
            return json.dumps({"error": f"Component '{component_name}' not found"})

        return json.dumps(COMPONENT_REGISTRY[component_name], indent=2)

    return await asyncio.get_event_loop().run_in_executor(None, _get_schema)


# Note: Theme tools (remotion_list_themes, remotion_get_theme_info, etc.)
# are now registered via register_theme_tools() above

# Note: Token tools (remotion_list_color_tokens, remotion_list_typography_tokens,
# remotion_list_motion_tokens, etc.) are now registered via register_token_tools() above


# ============================================================================
# PROJECT CREATION & GENERATION TOOLS
# ============================================================================
# Note: Component-specific tools (remotion_add_title_scene, remotion_add_chart, etc.)
# are now automatically registered via register_all_tools() from the components module


@mcp.tool  # type: ignore[arg-type]
async def remotion_create_project(
    name: str, theme: str = "tech", fps: int = 30, width: int = 1920, height: int = 1080
) -> str:
    """
    Create a new Remotion video project.

    Creates a complete Remotion project with package.json, TypeScript config,
    and project structure ready for video generation.

    Args:
        name: Project name (will be used as directory name)
        theme: Theme to use (tech, finance, education, lifestyle, gaming, minimal, business)
        fps: Frames per second (default: 30)
        width: Video width in pixels (default: 1920 for 1080p)
        height: Video height in pixels (default: 1080 for 1080p)

    Returns:
        JSON with project information

    Example:
        project = await remotion_create_project(
            name="my_video",
            theme="tech",
            fps=30,
            width=1920,
            height=1080
        )
    """

    def _create():
        try:
            result = project_manager.create_project(name, theme, fps, width, height)
            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    return await asyncio.get_event_loop().run_in_executor(None, _create)


@mcp.tool  # type: ignore[arg-type]
async def remotion_generate_video() -> str:
    """
    Generate the complete video composition and write all files.

    Generates all TSX components, the composition file, and updates the project
    with the complete video structure. After this, you can run 'npm install'
    and 'npm start' in the project directory to preview the video.

    Returns:
        JSON with generation results and next steps

    Example:
        result = await remotion_generate_video()
        # Video files generated! Run 'npm install' and 'npm start' to preview
    """

    def _generate():
        if not project_manager.current_project:
            return json.dumps({"error": "No active project. Create a project first."})

        if not project_manager.current_timeline:
            return json.dumps({"error": "No timeline created. Add components first."})

        try:
            # Generate components
            theme = project_manager.current_timeline.theme

            # Helper to recursively find all component types including nested ones
            def find_all_component_types(components):
                types = set()
                from chuk_mcp_remotion.generator.composition_builder import ComponentInstance

                def collect_types(comp):
                    if isinstance(comp, ComponentInstance):
                        types.add(comp.component_type)
                        # Check for nested children in props
                        for _key, value in comp.props.items():
                            if isinstance(value, ComponentInstance):
                                collect_types(value)
                            elif isinstance(value, list):
                                for item in value:
                                    if isinstance(item, ComponentInstance):
                                        collect_types(item)

                for comp in components:
                    collect_types(comp)

                return types

            # Get unique component types from all tracks (including nested)
            all_components = project_manager.current_timeline.get_all_components()
            component_types = find_all_component_types(all_components)

            generated_files = []

            for comp_type in component_types:
                # Get a sample config from the timeline
                # For nested components, use empty config as templates handle it
                file_path = project_manager.add_component_to_project(
                    comp_type, {}, theme
                )
                generated_files.append(file_path)

            # Generate main composition
            composition_file = project_manager.generate_composition()
            generated_files.append(composition_file)

            project_info = project_manager.get_project_info()

            return json.dumps(
                {
                    "status": "success",
                    "project": project_info,
                    "generated_files": generated_files,
                    "next_steps": [
                        f"cd {project_info['path']}",
                        "npm install",
                        "npm start  # Opens Remotion Studio",
                        "npm run build  # Renders the video",
                    ],
                },
                indent=2,
            )

        except Exception as e:
            return json.dumps({"error": str(e)})

    return await asyncio.get_event_loop().run_in_executor(None, _generate)


@mcp.tool  # type: ignore[arg-type]
async def remotion_get_composition_info() -> str:
    """
    Get information about the current composition.

    Returns details about the current composition including all components,
    timeline, duration, and configuration.

    Returns:
        JSON with composition information

    Example:
        info = await remotion_get_composition_info()
        # Returns composition details, components, timeline, etc.
    """

    def _get():
        if not project_manager.current_composition:
            return json.dumps({"error": "No active composition"})

        return json.dumps(project_manager.get_project_info(), indent=2)

    return await asyncio.get_event_loop().run_in_executor(None, _get)


@mcp.tool  # type: ignore[arg-type]
async def remotion_list_projects() -> str:
    """
    List all Remotion projects in the workspace.

    Returns:
        JSON array of projects

    Example:
        projects = await remotion_list_projects()
    """

    def _list():
        projects = project_manager.list_projects()
        return json.dumps(projects, indent=2)

    return await asyncio.get_event_loop().run_in_executor(None, _list)


# ============================================================================
# TRACK MANAGEMENT TOOLS
# ============================================================================


@mcp.tool  # type: ignore[arg-type]
async def remotion_add_track(
    name: str, layer: int, default_gap: float = 0, description: str = ""
) -> str:
    """
    Add a new track to the timeline.

    Args:
        name: Track name (unique identifier)
        layer: Z-index for rendering (higher = on top)
        default_gap: Default gap between components in seconds
        description: Human-readable description

    Returns:
        JSON with track information

    Example:
        result = await remotion_add_track(
            name="subtitles",
            layer=15,
            default_gap=0,
            description="Subtitle overlays"
        )
    """

    def _add():
        if not project_manager.current_timeline:
            return json.dumps({"error": "No active project. Create a project first."})

        try:
            project_manager.current_timeline.add_track(name, layer, default_gap, description)
            return json.dumps(
                {
                    "status": "success",
                    "track": {"name": name, "layer": layer, "default_gap": default_gap},
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)})

    return await asyncio.get_event_loop().run_in_executor(None, _add)


@mcp.tool  # type: ignore[arg-type]
async def remotion_list_tracks() -> str:
    """
    List all tracks in the timeline.

    Returns:
        JSON array of tracks with their properties

    Example:
        tracks = await remotion_list_tracks()
        # Returns tracks sorted by layer (highest first)
    """

    def _list():
        if not project_manager.current_timeline:
            return json.dumps({"error": "No active project"})

        tracks = project_manager.current_timeline.list_tracks()
        return json.dumps(tracks, indent=2)

    return await asyncio.get_event_loop().run_in_executor(None, _list)


@mcp.tool  # type: ignore[arg-type]
async def remotion_set_active_track(name: str) -> str:
    """
    Set the default track for component additions.

    Args:
        name: Track name to set as active

    Returns:
        JSON with status

    Example:
        result = await remotion_set_active_track(name="overlay")
        # Subsequent component additions will use the overlay track by default
    """

    def _set():
        if not project_manager.current_timeline:
            return json.dumps({"error": "No active project"})

        try:
            project_manager.current_timeline.set_active_track(name)
            return json.dumps({"status": "success", "active_track": name}, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    return await asyncio.get_event_loop().run_in_executor(None, _set)


@mcp.tool  # type: ignore[arg-type]
async def remotion_get_track_cursor(track_name: str) -> str:
    """
    Get the current cursor position for a track.

    Args:
        track_name: Track name

    Returns:
        JSON with cursor position in frames and seconds

    Example:
        cursor = await remotion_get_track_cursor(track_name="main")
    """

    def _get():
        if not project_manager.current_timeline:
            return json.dumps({"error": "No active project"})

        try:
            cursor_frames = project_manager.current_timeline.get_track_cursor(track_name)
            cursor_seconds = project_manager.current_timeline.frames_to_seconds(cursor_frames)
            return json.dumps(
                {
                    "track": track_name,
                    "cursor_frames": cursor_frames,
                    "cursor_seconds": cursor_seconds,
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)})

    return await asyncio.get_event_loop().run_in_executor(None, _get)


# ============================================================================
# INFO TOOLS
# ============================================================================


@mcp.tool  # type: ignore[arg-type]
async def remotion_get_info() -> str:
    """
    Get information about the Remotion MCP Server.

    Returns server version, capabilities, and statistics about available
    components, themes, and tools.

    Returns:
        JSON object with server information

    Example:
        info = await remotion_get_info()
        # Returns server version, component count, theme count, etc.
    """

    def _get_info():
        info = {
            "name": "chuk-mcp-remotion",
            "version": "0.1.0",
            "description": "AI-powered video generation with design system approach",
            "statistics": {
                "components": len(COMPONENT_REGISTRY),
                "themes": len(YOUTUBE_THEMES),
                "categories": len({c.get("category") for c in COMPONENT_REGISTRY.values()}),
            },
            "categories": list({c.get("category") for c in COMPONENT_REGISTRY.values()}),
        }
        return json.dumps(info, indent=2)

    return await asyncio.get_event_loop().run_in_executor(None, _get_info)


def main():
    """Main entry point for the MCP server.

    Automatically detects transport mode:
    - stdio: When stdin is piped or MCP_STDIO is set (for Claude Desktop)
    - HTTP: Default mode for API access
    """
    import argparse

    parser = argparse.ArgumentParser(description="Remotion MCP Server")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["stdio", "http"],
        default=None,
        help="Transport mode (stdio for Claude Desktop, http for API)",
    )
    parser.add_argument(
        "--host", default="localhost", help="Host for HTTP mode (default: localhost)"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP mode (default: 8000)")

    args = parser.parse_args()

    # Determine transport mode
    if args.mode == "stdio":
        # Explicitly requested stdio mode
        print("Remotion MCP Server starting in STDIO mode", file=sys.stderr)
        mcp.run(stdio=True)
    elif args.mode == "http":
        # Explicitly requested HTTP mode
        print(
            f"Remotion MCP Server starting in HTTP mode on {args.host}:{args.port}", file=sys.stderr
        )
        mcp.run(host=args.host, port=args.port, stdio=False)
    else:
        # Auto-detect mode based on environment
        if os.environ.get("MCP_STDIO") or (not sys.stdin.isatty()):
            print("Remotion MCP Server starting in STDIO mode (auto-detected)", file=sys.stderr)
            mcp.run(stdio=True)
        else:
            print(
                f"Remotion MCP Server starting in HTTP mode on {args.host}:{args.port}",
                file=sys.stderr,
            )
            mcp.run(host=args.host, port=args.port, stdio=False)


if __name__ == "__main__":
    main()
