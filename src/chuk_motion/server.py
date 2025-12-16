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
from .components import (
    get_component_registry,
    register_all_builders,
    register_all_renderers,
    register_all_tools,
)
from .generator.composition_builder import CompositionBuilder
from .models.artifact_models import ProviderType
from .storage import ArtifactStorageManager
from .themes.youtube_themes import YOUTUBE_THEMES

# Import design system modules
from .tools.artifact_tools import register_artifact_tools
from .tools.theme_tools import register_theme_tools
from .tools.token_tools import register_token_tools
from .utils.async_project_manager import AsyncProjectManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server instance
mcp = ChukMCPServer("chuk-motion")

# Create virtual filesystem instance (using file provider for actual file operations)
vfs = AsyncVirtualFileSystem(provider="file")

# Determine storage provider from environment
STORAGE_PROVIDER_ENV = os.environ.get("CHUK_MOTION_STORAGE_PROVIDER", "vfs-filesystem")
try:
    storage_provider = ProviderType(STORAGE_PROVIDER_ENV)
except ValueError:
    logger.warning(
        f"Invalid storage provider '{STORAGE_PROVIDER_ENV}', defaulting to vfs-filesystem"
    )
    storage_provider = ProviderType.FILESYSTEM

# Create artifact storage manager
artifact_storage = ArtifactStorageManager(provider_type=storage_provider)

# Create async project manager with artifact storage
async_project_manager = AsyncProjectManager(provider_type=storage_provider)

# For compatibility: alias async_project_manager as project_manager
# This allows existing tools to work with the new async manager
project_manager = async_project_manager

logger.info(f"Using storage provider: {storage_provider.value}")

# Register composition builder methods dynamically from components
register_all_builders(CompositionBuilder)
register_all_renderers(CompositionBuilder)

# Register theme and token tools with virtual filesystem
register_theme_tools(mcp, project_manager, vfs)
register_token_tools(mcp, project_manager, vfs)

# Register artifact-based tools (async-native with chuk-artifacts)
register_artifact_tools(mcp, async_project_manager)

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
    and project structure ready for video generation. Uses chuk-artifacts
    for modern, async-native storage.

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
    try:
        from .models.artifact_models import StorageScope

        # Create project using artifact storage (SESSION scope by default for compatibility)
        project_info = await async_project_manager.create_project(
            name=name,
            theme=theme,
            fps=fps,
            width=width,
            height=height,
            scope=StorageScope.SESSION,
        )

        # Return compatible format
        result = {
            "name": project_info.metadata.project_name,
            "path": f"artifact://{project_info.namespace_info.namespace_id}",
            "namespace_id": project_info.namespace_info.namespace_id,
            "theme": project_info.metadata.theme,
            "fps": str(project_info.metadata.fps),
            "resolution": f"{project_info.metadata.width}x{project_info.metadata.height}",
            "provider": project_info.namespace_info.provider_type.value,
            "scope": project_info.namespace_info.scope.value,
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        logger.exception("Error creating project")
        return json.dumps({"error": str(e)})


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
    if not async_project_manager.current_project_id:
        return json.dumps({"error": "No active project. Create a project first."})

    if not async_project_manager.current_timeline:
        return json.dumps({"error": "No timeline created. Add components first."})

    try:
        # Generate components
        theme = async_project_manager.current_timeline.theme

        # Get unique component types from all tracks (including nested)
        all_components = async_project_manager.current_timeline.get_all_components()
        component_types = async_project_manager._find_all_component_types_recursive(all_components)

        generated_files = []

        for comp_type in component_types:
            # Get a sample config from the timeline
            # For nested components, use empty config as templates handle it
            file_path = await async_project_manager.add_component_to_project(comp_type, {}, theme)
            generated_files.append(file_path)

        # Generate main composition
        composition_file = await async_project_manager.generate_composition()
        generated_files.append(composition_file)

        # Get project info from artifact storage
        project_info = await async_project_manager.storage.get_project(
            async_project_manager.current_project_id
        )

        return json.dumps(
            {
                "status": "success",
                "project": {
                    "namespace_id": project_info.namespace_info.namespace_id,
                    "name": project_info.metadata.project_name,
                    "theme": project_info.metadata.theme,
                    "grid_path": project_info.namespace_info.grid_path,
                },
                "generated_files": generated_files,
                "next_steps": [
                    "Use artifact_render_video() to render the composition",
                    "Or export and run locally with: npm install && npm start",
                ],
            },
            indent=2,
        )

    except Exception as e:
        logger.exception("Error generating video")
        return json.dumps({"error": str(e)})


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
    if not async_project_manager.current_composition:
        return json.dumps({"error": "No active composition"})

    if not async_project_manager.current_project_id:
        return json.dumps({"error": "No active project"})

    # Get project info from artifact storage
    project_info = await async_project_manager.storage.get_project(
        async_project_manager.current_project_id
    )

    return json.dumps(
        {
            "namespace_id": project_info.namespace_info.namespace_id,
            "name": project_info.metadata.project_name,
            "theme": project_info.metadata.theme,
            "fps": project_info.metadata.fps,
            "resolution": f"{project_info.metadata.width}x{project_info.metadata.height}",
            "composition": async_project_manager.current_composition,
        },
        indent=2,
    )


@mcp.tool  # type: ignore[arg-type]
async def remotion_list_projects() -> str:
    """
    List all Remotion projects in the workspace.

    Returns:
        JSON array of projects

    Example:
        projects = await remotion_list_projects()
    """
    # List all projects from artifact storage
    projects = await async_project_manager.storage.list_projects()

    return json.dumps(
        [
            {
                "namespace_id": p.namespace_info.namespace_id,
                "name": p.metadata.project_name,
                "theme": p.metadata.theme,
                "created_at": p.metadata.created_at.isoformat(),
                "grid_path": p.namespace_info.grid_path,
            }
            for p in projects
        ],
        indent=2,
    )


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
    if not async_project_manager.current_timeline:
        return json.dumps({"error": "No active project. Create a project first."})

    try:
        async_project_manager.current_timeline.add_track(name, layer, default_gap, description)
        return json.dumps(
            {
                "status": "success",
                "track": {"name": name, "layer": layer, "default_gap": default_gap},
            },
            indent=2,
        )
    except Exception as e:
        return json.dumps({"error": str(e)})


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
    if not async_project_manager.current_timeline:
        return json.dumps({"error": "No active project"})

    tracks = async_project_manager.current_timeline.list_tracks()
    return json.dumps(tracks, indent=2)


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
    if not async_project_manager.current_timeline:
        return json.dumps({"error": "No active project"})

    try:
        async_project_manager.current_timeline.set_active_track(name)
        return json.dumps({"status": "success", "active_track": name}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


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
    if not async_project_manager.current_timeline:
        return json.dumps({"error": "No active project"})

    try:
        cursor_frames = async_project_manager.current_timeline.get_track_cursor(track_name)
        cursor_seconds = async_project_manager.current_timeline.frames_to_seconds(cursor_frames)
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
    info = {
        "name": "chuk-motion",
        "version": "0.1.0",
        "description": "AI-powered video generation with design system approach",
        "storage": {
            "provider": storage_provider.value,
            "artifact_storage": "chuk-artifacts",
            "async_native": True,
        },
        "statistics": {
            "components": len(COMPONENT_REGISTRY),
            "themes": len(YOUTUBE_THEMES),
            "categories": len({c.get("category") for c in COMPONENT_REGISTRY.values()}),
        },
        "categories": list({c.get("category") for c in COMPONENT_REGISTRY.values()}),
    }
    return json.dumps(info, indent=2)


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

    # Initialize async managers on startup
    async def startup():
        """Initialize async resources."""
        await artifact_storage.initialize()
        await async_project_manager.initialize()
        logger.info("Async managers initialized")

    # Cleanup async managers on shutdown
    async def shutdown():
        """Cleanup async resources."""
        await async_project_manager.cleanup()
        await artifact_storage.cleanup()
        logger.info("Async managers cleaned up")

    # Register startup/shutdown hooks
    mcp.on_startup(startup)
    mcp.on_shutdown(shutdown)

    # Determine transport mode
    if args.mode == "stdio":
        # Explicitly requested stdio mode
        logger.debug("Remotion MCP Server starting in STDIO mode")
        mcp.run(stdio=True)
    elif args.mode == "http":
        # Explicitly requested HTTP mode
        logger.info(f"Remotion MCP Server starting in HTTP mode on {args.host}:{args.port}")
        mcp.run(host=args.host, port=args.port, stdio=False)
    else:
        # Auto-detect mode based on environment
        if os.environ.get("MCP_STDIO") or (not sys.stdin.isatty()):
            logger.debug("Remotion MCP Server starting in STDIO mode (auto-detected)")
            mcp.run(stdio=True)
        else:
            logger.info(f"Remotion MCP Server starting in HTTP mode on {args.host}:{args.port}")
            mcp.run(host=args.host, port=args.port, stdio=False)


if __name__ == "__main__":
    main()
