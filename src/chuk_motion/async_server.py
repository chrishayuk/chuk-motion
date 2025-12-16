#!/usr/bin/env python3
"""
Async Remotion MCP Server using chuk-mcp-server

This server provides async MCP tools for creating Remotion video compositions
using a design-system-first approach inspired by shadcn/ui and chuk-mcp-pptx.

Storage is managed through chuk-mcp-server's built-in artifact store context.
"""

import json
import logging
from typing import Any

from chuk_mcp_server import ChukMCPServer

# Import component auto-discovery system
from .components import (
    get_component_registry,
    register_all_builders,
    register_all_renderers,
    register_all_tools,
)
from .generator.composition_builder import CompositionBuilder
from .themes.youtube_themes import YOUTUBE_THEMES
from .video_manager import ComponentResponse, VideoManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server instance
mcp = ChukMCPServer("chuk-motion")

# Create video manager instance (uses chuk-mcp-server's artifact store context)
manager = VideoManager(base_path="videos")

# Register composition builder methods dynamically from components
register_all_builders(CompositionBuilder)
register_all_renderers(CompositionBuilder)

# Get component registry for discovery tools
COMPONENT_REGISTRY = get_component_registry()

# Register all component tools (charts, code, overlays, etc.)
register_all_tools(mcp, manager)


# =============================================================================
# PROJECT MANAGEMENT TOOLS
# =============================================================================


@mcp.tool  # type: ignore[arg-type]
async def remotion_create_project(
    name: str,
    theme: str = "tech",
    fps: int = 30,
    width: int = 1920,
    height: int = 1080,
) -> str:
    """
    Create a new Remotion video project.

    Args:
        name: Project name
        theme: Theme (tech, finance, education, lifestyle, gaming, minimal, business)
        fps: Frames per second (default: 30)
        width: Video width in pixels (default: 1920)
        height: Video height in pixels (default: 1080)

    Returns:
        JSON with project info
    """
    try:
        result = await manager.create_project(
            name=name,
            theme=theme,
            fps=fps,
            width=width,
            height=height,
        )
        return result.model_dump_json(indent=2)
    except Exception as e:
        logger.exception("Error creating project")
        return json.dumps({"error": str(e)})


@mcp.tool  # type: ignore[arg-type]
async def remotion_list_projects() -> str:
    """
    List all video projects.

    Returns:
        JSON array of projects
    """
    try:
        projects = manager.list_projects()
        return json.dumps(
            [p.model_dump() for p in projects],
            indent=2,
            default=str,
        )
    except Exception as e:
        logger.exception("Error listing projects")
        return json.dumps({"error": str(e)})


@mcp.tool  # type: ignore[arg-type]
async def remotion_get_info() -> str:
    """
    Get information about the current project and server.

    Returns:
        JSON with project info
    """
    try:
        from chuk_mcp_server import has_artifact_store

        metadata = manager.get_metadata()

        result: dict[str, Any] = {
            "current_project": manager._current_project,
            "artifact_store_available": has_artifact_store(),
            "projects": len(manager._builders),
        }

        if metadata:
            result["metadata"] = metadata.model_dump()

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.exception("Error getting info")
        return json.dumps({"error": str(e)})


# =============================================================================
# VIDEO GENERATION TOOLS
# =============================================================================


@mcp.tool  # type: ignore[arg-type]
async def remotion_generate_video(name: str | None = None) -> str:
    """
    Generate video composition files.

    Args:
        name: Project name (uses current if not specified)

    Returns:
        JSON with generation result
    """
    try:
        result = await manager.generate_video(name=name)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.exception("Error generating video")
        return json.dumps({"error": str(e)})


@mcp.tool  # type: ignore[arg-type]
async def remotion_render_video(name: str | None = None, expires_in: int = 3600) -> str:
    """
    Start rendering the video to MP4. Returns a job_id for status polling.

    For long videos, use remotion_render_status to poll for completion.
    The render runs in the background and typically takes 30-120 seconds.

    This tool:
    1. Exports the composition to a Remotion project
    2. Starts npx remotion render in background
    3. Returns job_id immediately for status polling
    4. Sends progress notifications if client supports them

    Args:
        name: Project name (uses current if not specified)
        expires_in: URL expiration time in seconds (default: 3600)

    Returns:
        JSON with job_id for polling via remotion_render_status
    """
    import asyncio
    import tempfile
    from datetime import datetime
    from pathlib import Path

    from chuk_mcp_server import get_artifact_store, has_artifact_store

    from .render import (
        RemotionProjectExporter,
        create_render_job,
        render_video,
        update_render_job,
    )

    try:
        # Get the builder
        project_name = name or manager._current_project
        if not project_name:
            return json.dumps({"error": "No active project. Create a project first."})

        builder = manager._builders.get(project_name)
        if not builder:
            return json.dumps({"error": f"Project not found: {project_name}"})

        # Create a render job
        job = create_render_job(project_name)
        job.metadata["expires_in"] = expires_in

        # Start the render in background
        async def do_render():
            try:
                update_render_job(job.job_id, status="rendering", progress=10)

                # Create a persistent temp directory (not auto-deleted)
                temp_dir = Path(tempfile.mkdtemp(prefix=f"remotion_{job.job_id}_"))
                project_dir = temp_dir / project_name

                # Export to Remotion project
                logger.info(f"[Job {job.job_id}] Exporting project {project_name}")
                update_render_job(job.job_id, progress=20, message="Exporting project...")
                exporter = RemotionProjectExporter(builder, project_name)
                export_result = exporter.export_to_directory(project_dir)

                # Store export metadata
                update_render_job(
                    job.job_id,
                    progress=30,
                    message="Project exported, starting render...",
                    metadata={
                        **job.metadata,
                        "fps": export_result["fps"],
                        "width": export_result["width"],
                        "height": export_result["height"],
                        "total_frames": export_result["total_frames"],
                        "duration_seconds": export_result["total_frames"] / export_result["fps"],
                    },
                )

                # Render to MP4 (progress will be updated during render)
                logger.info(f"[Job {job.job_id}] Rendering video")
                update_render_job(job.job_id, progress=40, message="Rendering video...")
                output_path = project_dir / "out" / "video.mp4"
                render_result = await render_video(
                    project_dir,
                    export_result["composition_id"],
                    output_path,
                    job_id=job.job_id,  # Pass job_id for progress updates
                )

                if not render_result["success"]:
                    update_render_job(
                        job.job_id,
                        status="failed",
                        error=render_result.get("error", "Render failed"),
                        message="Render failed",
                        completed_at=datetime.now(),
                    )
                    return

                update_render_job(job.job_id, progress=80, message="Uploading video...")

                # Store as artifact if available
                if has_artifact_store():
                    store = get_artifact_store()
                    mp4_data = output_path.read_bytes()

                    artifact_id = await store.store(
                        data=mp4_data,
                        mime="video/mp4",
                        summary=f"{project_name}.mp4",
                        meta={
                            "filename": f"{project_name}.mp4",
                            "project_name": project_name,
                            **job.metadata,
                            "file_size_bytes": render_result["file_size_bytes"],
                        },
                    )
                    logger.info(f"[Job {job.job_id}] Stored video as artifact: {artifact_id}")

                    # Generate presigned URL
                    url = await store.presign(artifact_id, expires=expires_in)
                    logger.info(f"[Job {job.job_id}] Generated presigned URL")

                    update_render_job(
                        job.job_id,
                        status="completed",
                        progress=100,
                        message="Render complete!",
                        artifact_id=artifact_id,
                        download_url=url,
                        file_size_bytes=render_result["file_size_bytes"],
                        output_path=output_path,
                        completed_at=datetime.now(),
                    )
                else:
                    update_render_job(
                        job.job_id,
                        status="completed",
                        progress=100,
                        message="Render complete (no download URL)",
                        file_size_bytes=render_result["file_size_bytes"],
                        output_path=output_path,
                        completed_at=datetime.now(),
                        error="No artifact store - no download URL available",
                    )

                # Cleanup temp directory
                import shutil

                shutil.rmtree(temp_dir, ignore_errors=True)

            except Exception as e:
                logger.exception(f"[Job {job.job_id}] Render failed")
                update_render_job(
                    job.job_id,
                    status="failed",
                    error=str(e),
                    message=f"Render failed: {str(e)}",
                    completed_at=datetime.now(),
                )

        # Start render in background task
        asyncio.create_task(do_render())

        return json.dumps(
            {
                "success": True,
                "job_id": job.job_id,
                "project": project_name,
                "status": "rendering",
                "message": "Render started. Poll remotion_render_status with job_id for completion.",
            },
            indent=2,
        )

    except Exception as e:
        logger.exception("Error starting render")
        return json.dumps({"error": str(e)})


@mcp.tool  # type: ignore[arg-type]
async def remotion_render_status(job_id: str) -> str:
    """
    Check the status of a video render job.

    Poll this tool every 10-15 seconds after calling remotion_render_video.
    When status is "completed", the download_url will be available.

    Args:
        job_id: The job ID returned by remotion_render_video

    Returns:
        JSON with job status, progress, message, and download_url when complete
    """
    from .render import get_render_job

    try:
        job = get_render_job(job_id)
        if not job:
            return json.dumps({"error": f"Job not found: {job_id}"})

        result = {
            "job_id": job.job_id,
            "project": job.project_name,
            "status": job.status,
            "progress": job.progress,
            "started_at": job.started_at.isoformat(),
        }

        # Include progress message if available
        if job.message:
            result["message"] = job.message

        if job.completed_at:
            result["completed_at"] = job.completed_at.isoformat()
            result["duration_seconds"] = (job.completed_at - job.started_at).total_seconds()

        if job.status == "completed":
            result["download_url"] = job.download_url
            result["artifact_id"] = job.artifact_id
            result["file_size_bytes"] = job.file_size_bytes
            if job.file_size_bytes:
                result["file_size_mb"] = round(job.file_size_bytes / (1024 * 1024), 2)
            result.update(job.metadata)

        if job.status == "failed":
            result["error"] = job.error

        return json.dumps(result, indent=2)

    except Exception as e:
        logger.exception("Error getting render status")
        return json.dumps({"error": str(e)})


@mcp.tool  # type: ignore[arg-type]
async def artifact_status() -> str:
    """
    Get artifact storage status.

    Returns:
        JSON with storage status
    """
    try:
        from chuk_mcp_server import has_artifact_store

        available = has_artifact_store()

        result = {
            "artifact_store_available": available,
            "current_project": manager._current_project,
            "projects": len(manager._builders),
            "features": {
                "download_urls": available,
                "persistence": available,
            },
        }

        if available:
            result["message"] = "Artifact store configured. Download URLs available."
        else:
            result["message"] = (
                "No artifact store. Set CHUK_ARTIFACTS_PROVIDER=s3 for download URLs."
            )

        return json.dumps(result, indent=2)
    except Exception as e:
        logger.exception("Error getting status")
        return json.dumps({"error": str(e)})


# =============================================================================
# COMPONENT TOOLS
# =============================================================================


@mcp.tool  # type: ignore[arg-type]
async def remotion_add_title_scene(
    text: str,
    subtitle: str | None = None,
    variant: str = "default",
    animation: str = "fade",
    duration_seconds: float = 3.0,
) -> str:
    """
    Add a title scene to the video.

    Args:
        text: Main title text
        subtitle: Optional subtitle
        variant: Style variant (default, bold, minimal)
        animation: Animation type (fade, fade_zoom, slide)
        duration_seconds: Duration in seconds

    Returns:
        JSON with component info
    """
    try:
        builder = manager.get_current_builder()
        if not builder:
            return json.dumps({"error": "No active project. Create a project first."})

        start_time = builder.get_total_duration_seconds()
        builder.add_title_scene(  # type: ignore[attr-defined]
            text=text,
            subtitle=subtitle,
            variant=variant,
            animation=animation,
            duration_seconds=duration_seconds,
        )

        response = ComponentResponse(
            component="TitleScene",
            start_time=start_time,
            duration=duration_seconds,
        )
        return response.model_dump_json()

    except Exception as e:
        logger.exception("Error adding title scene")
        return json.dumps({"error": str(e)})


@mcp.tool  # type: ignore[arg-type]
async def remotion_add_fuzzy_text(
    text: str,
    font_size: str = "2xl",
    glitch_intensity: float = 8.0,
    scanline_height: float = 2.0,
    animate: bool = True,
    position: str = "center",
    duration: float = 3.0,
) -> str:
    """
    Add fuzzy/glitch text effect.

    Args:
        text: Text to display
        font_size: Font size (sm, md, lg, xl, 2xl, 3xl, 4xl)
        glitch_intensity: Glitch effect intensity
        scanline_height: Scanline effect height
        animate: Enable animation
        position: Text position
        duration: Duration in seconds

    Returns:
        JSON with component info
    """
    try:
        builder = manager.get_current_builder()
        if not builder:
            return json.dumps({"error": "No active project. Create a project first."})

        start_time = builder.get_total_duration_seconds()
        builder.add_fuzzy_text(  # type: ignore[attr-defined]
            start_time=start_time,
            text=text,
            font_size=font_size,
            glitch_intensity=glitch_intensity,
            scanline_height=scanline_height,
            animate=animate,
            position=position,
            duration=duration,
        )

        response = ComponentResponse(
            component="FuzzyText",
            start_time=start_time,
            duration=duration,
        )
        return response.model_dump_json()

    except Exception as e:
        logger.exception("Error adding fuzzy text")
        return json.dumps({"error": str(e)})


@mcp.tool  # type: ignore[arg-type]
async def remotion_add_true_focus(
    text: str,
    font_size: str = "2xl",
    font_weight: str = "bold",
    word_duration: float = 0.8,
    position: str = "center",
    duration: float = 3.0,
) -> str:
    """
    Add true focus text animation (word-by-word focus).

    Args:
        text: Text to display
        font_size: Font size
        font_weight: Font weight
        word_duration: Duration per word
        position: Text position
        duration: Total duration in seconds

    Returns:
        JSON with component info
    """
    try:
        builder = manager.get_current_builder()
        if not builder:
            return json.dumps({"error": "No active project. Create a project first."})

        start_time = builder.get_total_duration_seconds()
        builder.add_true_focus(  # type: ignore[attr-defined]
            start_time=start_time,
            text=text,
            font_size=font_size,
            font_weight=font_weight,
            word_duration=word_duration,
            position=position,
            duration=duration,
        )

        response = ComponentResponse(
            component="TrueFocus",
            start_time=start_time,
            duration=duration,
        )
        return response.model_dump_json()

    except Exception as e:
        logger.exception("Error adding true focus")
        return json.dumps({"error": str(e)})


@mcp.tool  # type: ignore[arg-type]
async def remotion_add_end_screen(
    cta_text: str = "Thanks for Watching!",
    thumbnail_url: str | None = None,
    variant: str | None = None,
    duration_seconds: float = 5.0,
) -> str:
    """
    Add an end screen.

    Args:
        cta_text: End screen call-to-action text
        thumbnail_url: Optional thumbnail URL
        variant: Optional style variant
        duration_seconds: Duration in seconds

    Returns:
        JSON with component info
    """
    try:
        builder = manager.get_current_builder()
        if not builder:
            return json.dumps({"error": "No active project. Create a project first."})

        start_time = builder.get_total_duration_seconds()
        builder.add_end_screen(  # type: ignore[attr-defined]
            cta_text=cta_text,
            thumbnail_url=thumbnail_url,
            variant=variant,
            duration_seconds=duration_seconds,
        )

        response = ComponentResponse(
            component="EndScreen",
            start_time=start_time,
            duration=duration_seconds,
        )
        return response.model_dump_json()

    except Exception as e:
        logger.exception("Error adding end screen")
        return json.dumps({"error": str(e)})


# =============================================================================
# DISCOVERY TOOLS
# =============================================================================


@mcp.tool  # type: ignore[arg-type]
async def remotion_list_components(category: str | None = None) -> str:
    """
    List available video components grouped by category.

    Args:
        category: Optional category filter (e.g., 'chart', 'text-animation', 'layout')

    Returns:
        JSON with components grouped by category
    """
    try:
        # Group components by their category
        by_category: dict[str, list[str]] = {}
        for comp_name, metadata in COMPONENT_REGISTRY.items():
            cat = metadata.get("category", "unknown") if isinstance(metadata, dict) else "unknown"
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(comp_name)

        if category:
            # Return only the requested category
            components = by_category.get(category, [])
            return json.dumps(
                {
                    "category": category,
                    "components": sorted(components),
                    "count": len(components),
                },
                indent=2,
            )

        # Return all categories with their components
        result = {
            "categories": {cat: sorted(comps) for cat, comps in sorted(by_category.items())},
            "total_components": len(COMPONENT_REGISTRY),
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.exception("Error listing components")
        return json.dumps({"error": str(e)})


@mcp.tool  # type: ignore[arg-type]
async def remotion_list_themes() -> str:
    """
    List available themes.

    Returns:
        JSON with theme list
    """
    try:
        themes = list(YOUTUBE_THEMES.keys())
        return json.dumps({"themes": themes})
    except Exception as e:
        logger.exception("Error listing themes")
        return json.dumps({"error": str(e)})


# Run the server
if __name__ == "__main__":
    logger.info("Starting Remotion MCP Server...")
    logger.info(f"Base Path: {manager.base_path}")
    logger.info("Storage: Using chuk-mcp-server artifact store context")

    # Run in stdio mode when executed directly
    mcp.run(stdio=True)
