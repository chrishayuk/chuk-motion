"""
MCP tools for artifact-based project management.

These tools use AsyncProjectManager with chuk-artifacts for
modern, async-native project and artifact storage.
"""

import json
import logging
from pathlib import Path
from tempfile import TemporaryDirectory

from ..models.artifact_models import StorageScope
from ..rendering import RemotionRenderer
from ..utils.async_project_manager import AsyncProjectManager

logger = logging.getLogger(__name__)


async def _export_vfs_to_directory(vfs, vfs_path: str, local_dir: Path):
    """
    Recursively export VFS directory to local filesystem.

    Args:
        vfs: AsyncVirtualFileSystem instance
        vfs_path: VFS path to export from
        local_dir: Local directory to export to
    """
    # List contents
    contents = await vfs.ls(vfs_path)

    for item_name in contents:
        item_path = f"{vfs_path}/{item_name}".replace("//", "/")
        local_path = local_dir / item_name

        # Check if directory
        node_info = await vfs.get_node_info(item_path)
        # EnhancedNodeInfo has is_dir as an attribute, not a dict key
        is_directory = getattr(node_info, "is_dir", False) if node_info else False
        if is_directory:
            # Create directory and recurse
            local_path.mkdir(exist_ok=True)
            await _export_vfs_to_directory(vfs, item_path, local_path)
        else:
            # Copy file
            try:
                data = await vfs.read_file(item_path)
                local_path.write_bytes(data)
            except Exception as e:
                logger.warning(f"Could not export {item_path}: {e}")


def register_artifact_tools(mcp, async_project_manager: AsyncProjectManager):
    """
    Register artifact-based project management tools.

    Args:
        mcp: MCP server instance
        async_project_manager: AsyncProjectManager instance
    """

    @mcp.tool  # type: ignore[arg-type]
    async def artifact_create_project(
        name: str,
        theme: str = "tech",
        fps: int = 30,
        width: int = 1920,
        height: int = 1080,
        scope: str = "session",
        user_id: str | None = None,
    ) -> str:
        """
        Create a new Remotion project using chuk-artifacts storage.

        This is the modern, async-native version of remotion_create_project
        that uses chuk-artifacts for storage with support for multiple
        storage providers (memory, filesystem, S3, SQLite).

        Args:
            name: Project name
            theme: Theme to use (tech, finance, education, lifestyle, gaming, minimal, business)
            fps: Frames per second (default: 30)
            width: Video width in pixels (default: 1920 for 1080p)
            height: Video height in pixels (default: 1080 for 1080p)
            scope: Storage scope - "session" (temporary), "user" (persistent), or "sandbox" (shared)
            user_id: User ID (required for "user" scope, optional for others)

        Returns:
            JSON with project information including namespace ID

        Example:
            # Create a temporary session-scoped project
            project = await artifact_create_project(
                name="demo_video",
                theme="tech",
                scope="session"
            )

            # Create a persistent user-scoped project
            project = await artifact_create_project(
                name="my_tutorial",
                theme="education",
                scope="user",
                user_id="alice"
            )
        """
        try:
            # Parse scope
            try:
                storage_scope = StorageScope(scope.lower())
            except ValueError:
                return json.dumps(
                    {"error": f"Invalid scope '{scope}'. Must be 'session', 'user', or 'sandbox'"}
                )

            # Create project
            project_info = await async_project_manager.create_project(
                name=name,
                theme=theme,
                fps=fps,
                width=width,
                height=height,
                scope=storage_scope,
                user_id=user_id,
            )

            # Return project info
            result = {
                "success": True,
                "namespace_id": project_info.namespace_info.namespace_id,
                "name": project_info.metadata.project_name,
                "theme": project_info.metadata.theme,
                "fps": project_info.metadata.fps,
                "resolution": f"{project_info.metadata.width}x{project_info.metadata.height}",
                "scope": project_info.namespace_info.scope.value,
                "grid_path": project_info.namespace_info.grid_path,
                "provider": project_info.namespace_info.provider_type.value,
            }

            if project_info.namespace_info.user_id:
                result["user_id"] = project_info.namespace_info.user_id

            return json.dumps(result, indent=2)

        except Exception as e:
            logger.exception("Error creating project with artifacts")
            return json.dumps({"error": str(e)})

    @mcp.tool  # type: ignore[arg-type]
    async def artifact_get_project(namespace_id: str) -> str:
        """
        Get project information by namespace ID.

        Args:
            namespace_id: The namespace ID returned from artifact_create_project

        Returns:
            JSON with complete project information

        Example:
            info = await artifact_get_project(namespace_id="ns_abc123")
        """
        try:
            project_info = await async_project_manager.storage.get_project(namespace_id)

            result = {
                "success": True,
                "namespace_id": project_info.namespace_info.namespace_id,
                "name": project_info.metadata.project_name,
                "theme": project_info.metadata.theme,
                "fps": project_info.metadata.fps,
                "width": project_info.metadata.width,
                "height": project_info.metadata.height,
                "total_duration_seconds": project_info.metadata.total_duration_seconds,
                "component_count": project_info.metadata.component_count,
                "created_at": project_info.metadata.created_at.isoformat(),
                "updated_at": project_info.metadata.updated_at.isoformat(),
                "scope": project_info.namespace_info.scope.value,
                "checkpoints": [
                    {
                        "checkpoint_id": cp.checkpoint_id,
                        "name": cp.name,
                        "description": cp.description,
                        "created_at": cp.created_at.isoformat(),
                    }
                    for cp in project_info.checkpoints
                ],
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            logger.exception("Error getting project")
            return json.dumps({"error": str(e)})

    @mcp.tool  # type: ignore[arg-type]
    async def artifact_create_checkpoint(name: str, description: str | None = None) -> str:
        """
        Create a checkpoint (version snapshot) of the current project.

        Checkpoints allow you to save the state of your project at different
        points in time, enabling you to restore previous versions if needed.

        Args:
            name: Checkpoint name (e.g., "v1.0", "draft-1", "final")
            description: Optional description of this checkpoint

        Returns:
            JSON with checkpoint information

        Example:
            checkpoint = await artifact_create_checkpoint(
                name="v1.0",
                description="First complete draft"
            )
        """
        try:
            if not async_project_manager.current_project_id:
                return json.dumps({"error": "No active project. Create a project first."})

            checkpoint = await async_project_manager.create_checkpoint(
                name=name, description=description
            )

            result = {
                "success": True,
                "checkpoint_id": checkpoint.checkpoint_id,
                "namespace_id": checkpoint.namespace_id,
                "name": checkpoint.name,
                "description": checkpoint.description,
                "created_at": checkpoint.created_at.isoformat(),
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            logger.exception("Error creating checkpoint")
            return json.dumps({"error": str(e)})

    @mcp.tool  # type: ignore[arg-type]
    async def artifact_list_checkpoints() -> str:
        """
        List all checkpoints for the current project.

        Returns:
            JSON array of checkpoints with their metadata

        Example:
            checkpoints = await artifact_list_checkpoints()
        """
        try:
            if not async_project_manager.current_project_id:
                return json.dumps({"error": "No active project. Create a project first."})

            checkpoints = await async_project_manager.storage.list_checkpoints(
                async_project_manager.current_project_id
            )

            result = {
                "success": True,
                "namespace_id": async_project_manager.current_project_id,
                "checkpoints": [
                    {
                        "checkpoint_id": cp.checkpoint_id,
                        "name": cp.name,
                        "description": cp.description,
                        "created_at": cp.created_at.isoformat(),
                    }
                    for cp in checkpoints
                ],
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            logger.exception("Error listing checkpoints")
            return json.dumps({"error": str(e)})

    @mcp.tool  # type: ignore[arg-type]
    async def artifact_restore_checkpoint(checkpoint_id: str) -> str:
        """
        Restore the current project to a previous checkpoint.

        WARNING: This will replace the current project state with the
        checkpoint version. Consider creating a new checkpoint before
        restoring to preserve your current work.

        Args:
            checkpoint_id: The checkpoint ID to restore

        Returns:
            JSON confirmation

        Example:
            result = await artifact_restore_checkpoint(checkpoint_id="cp_123")
        """
        try:
            if not async_project_manager.current_project_id:
                return json.dumps({"error": "No active project. Create a project first."})

            await async_project_manager.restore_checkpoint(checkpoint_id)

            result = {
                "success": True,
                "namespace_id": async_project_manager.current_project_id,
                "checkpoint_id": checkpoint_id,
                "message": "Project restored successfully",
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            logger.exception("Error restoring checkpoint")
            return json.dumps({"error": str(e)})

    @mcp.tool  # type: ignore[arg-type]
    async def artifact_store_render(
        video_data_path: str,
        format: str = "mp4",
        codec: str | None = None,
        bitrate_kbps: int | None = None,
    ) -> str:
        """
        Store a rendered video as an artifact.

        Args:
            video_data_path: Path to the rendered video file
            format: Video format (mp4, webm)
            codec: Video codec (h264, vp9, etc.)
            bitrate_kbps: Video bitrate in kbps

        Returns:
            JSON with render artifact information

        Example:
            render = await artifact_store_render(
                video_data_path="/path/to/output.mp4",
                format="mp4",
                codec="h264",
                bitrate_kbps=5000
            )
        """
        try:
            if not async_project_manager.current_project_id:
                return json.dumps({"error": "No active project. Create a project first."})

            # Read video data
            import aiofiles  # type: ignore[import-untyped]

            async with aiofiles.open(video_data_path, "rb") as f:
                video_data = await f.read()

            # Get current project info
            project_info = await async_project_manager.storage.get_project(
                async_project_manager.current_project_id
            )

            # Store render
            render_info = await async_project_manager.storage.store_render(
                project_namespace_id=async_project_manager.current_project_id,
                video_data=video_data,
                format=format,
                resolution=f"{project_info.metadata.width}x{project_info.metadata.height}",
                fps=project_info.metadata.fps,
                duration_seconds=project_info.metadata.total_duration_seconds,
                scope=project_info.namespace_info.scope,
                user_id=project_info.namespace_info.user_id,
                codec=codec,
                bitrate_kbps=bitrate_kbps,
            )

            result = {
                "success": True,
                "render_id": render_info.namespace_info.namespace_id,
                "project_id": async_project_manager.current_project_id,
                "format": render_info.metadata.format,
                "size_bytes": render_info.metadata.file_size_bytes,
                "duration_seconds": render_info.metadata.duration_seconds,
                "checksum": render_info.metadata.checksum,
                "grid_path": render_info.namespace_info.grid_path,
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            logger.exception("Error storing render")
            return json.dumps({"error": str(e)})

    @mcp.tool  # type: ignore[arg-type]
    async def artifact_render_video(
        composition_id: str | None = None,
        output_format: str = "mp4",
        quality: str = "high",
        concurrency: int = 4,
        store_as_artifact: bool = True,
    ) -> str:
        """
        Render the current project using Remotion CLI.

        Automatically exports the project to a temporary directory, runs the
        Remotion render, and optionally stores the result as an artifact.

        Args:
            composition_id: Composition ID to render (auto-detected if not provided)
            output_format: Output format (mp4, webm)
            quality: Quality preset (low, medium, high)
            concurrency: Number of concurrent render threads
            store_as_artifact: If True, stores the rendered video as an artifact

        Returns:
            JSON with render information

        Example:
            result = await artifact_render_video(
                quality="high",
                output_format="mp4"
            )
        """
        try:
            if not async_project_manager.current_project_id:
                return json.dumps({"error": "No active project. Create a project first."})

            # Get project info
            project_info = await async_project_manager.storage.get_project(
                async_project_manager.current_project_id
            )

            # Auto-detect composition ID if not provided
            if not composition_id:
                # Use project name as composition ID (sanitized for Remotion)
                composition_id = project_info.metadata.project_name.replace("_", "-")

            # Get project VFS
            vfs = await async_project_manager.storage.get_project_vfs(
                async_project_manager.current_project_id
            )

            # Export project to temporary directory for rendering
            with TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                project_dir = temp_path / "project"
                project_dir.mkdir()

                # Export all project files from VFS
                await _export_vfs_to_directory(vfs, "/", project_dir)

                # Install dependencies
                logger.info("Installing npm dependencies...")
                import asyncio

                proc = await asyncio.create_subprocess_exec(
                    "npm",
                    "install",
                    cwd=str(project_dir),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await proc.wait()

                if proc.returncode != 0:
                    stderr = await proc.stderr.read() if proc.stderr else b""
                    return json.dumps({"error": f"npm install failed: {stderr.decode()}"})

                # Render video
                output_path = temp_path / f"output.{output_format}"

                renderer = RemotionRenderer(str(project_dir))

                # Add progress logging
                def log_progress(progress):
                    logger.info(
                        f"Rendering: {progress.percent_complete:.1f}% "
                        f"({progress.current_frame}/{progress.total_frames}) "
                        f"- {progress.status}"
                    )

                renderer.on_progress(log_progress)

                # Render
                logger.info(f"Starting render: {composition_id}")
                result = await renderer.render(
                    composition_id=composition_id,
                    output_path=output_path,
                    format=output_format,
                    quality=quality,
                    concurrency=concurrency,
                    timeout=600,  # 10 minutes
                )

                if not result.success:
                    return json.dumps({"error": f"Render failed: {result.error}"})

                # Store as artifact if requested
                render_id = None
                if store_as_artifact and result.output_path:
                    logger.info("Storing render as artifact...")

                    # Read rendered video
                    import aiofiles  # type: ignore[import-untyped]

                    async with aiofiles.open(result.output_path, "rb") as f:
                        video_data = await f.read()

                    # Store render
                    render_info = await async_project_manager.storage.store_render(
                        project_namespace_id=async_project_manager.current_project_id,
                        video_data=video_data,
                        format=output_format,
                        resolution=result.resolution,
                        fps=result.fps,
                        duration_seconds=result.duration_seconds,
                        scope=project_info.namespace_info.scope,
                        user_id=project_info.namespace_info.user_id,
                        codec="h264" if output_format == "mp4" else "vp9",
                    )

                    render_id = render_info.namespace_info.namespace_id
                    logger.info(f"Stored render as artifact: {render_id}")

                # Return success
                response = {
                    "success": True,
                    "composition_id": composition_id,
                    "format": output_format,
                    "quality": quality,
                    "resolution": result.resolution,
                    "fps": result.fps,
                    "duration_seconds": result.duration_seconds,
                    "file_size_bytes": result.file_size_bytes,
                }

                if render_id:
                    response["render_id"] = render_id
                    response["message"] = "Video rendered and stored as artifact"
                else:
                    response["output_path"] = str(result.output_path)
                    response["message"] = "Video rendered successfully"

                return json.dumps(response, indent=2)

        except Exception as e:
            logger.exception("Error rendering video")
            return json.dumps({"error": str(e)})

    @mcp.tool  # type: ignore[arg-type]
    async def artifact_get_download_url(render_id: str, expires_in: int = 3600) -> str:
        """
        Get a presigned download URL for a rendered video.

        Generates a temporary URL that can be used to download the video
        directly from cloud storage (S3/Tigris). The URL expires after the specified
        duration.

        Args:
            render_id: The render/namespace ID returned from artifact_render_video
            expires_in: URL expiration time in seconds (default: 3600 = 1 hour)

        Returns:
            JSON string with download URL or error

        Example:
            result = await artifact_get_download_url(render_id="ns_abc123")
            # Returns: {"url": "https://...", "expires_in": 3600}
        """
        try:
            from chuk_mcp_server import get_artifact_store, has_artifact_store

            # Get artifact store
            if not has_artifact_store():
                return json.dumps(
                    {
                        "error": "No artifact store configured. Set up S3/Tigris storage for download URLs."
                    }
                )

            store = get_artifact_store()

            # Read the video data from the render namespace
            video_data = await async_project_manager.storage.read_render_data(render_id)
            if not video_data:
                return json.dumps({"error": f"Render not found: {render_id}"})

            # Get render metadata
            render_info = await async_project_manager.storage.get_render(render_id)

            # Store as artifact to get presigned URL
            filename = f"video_{render_id}.{render_info.metadata.format}"
            artifact_id = await store.store(
                data=video_data,
                mime=f"video/{render_info.metadata.format}",
                summary=filename,
                meta={
                    "filename": filename,
                    "render_id": render_id,
                    "format": render_info.metadata.format,
                    "resolution": render_info.metadata.resolution,
                },
            )
            logger.info(f"Stored video as artifact: {artifact_id}")

            # Generate presigned URL
            url = await store.presign(artifact_id, expires=expires_in)
            logger.info(f"Generated presigned URL for {render_id}")

            return json.dumps(
                {
                    "success": True,
                    "url": url,
                    "render_id": render_id,
                    "artifact_id": artifact_id,
                    "expires_in": expires_in,
                    "filename": filename,
                    "format": render_info.metadata.format,
                    "resolution": render_info.metadata.resolution,
                    "size_bytes": render_info.metadata.file_size_bytes,
                }
            )

        except Exception as e:
            logger.exception("Error generating download URL")
            return json.dumps({"error": f"Failed to generate download URL: {str(e)}"})

    @mcp.tool  # type: ignore[arg-type]
    async def artifact_list_renders(project_namespace_id: str | None = None) -> str:
        """
        List all renders for a project.

        Args:
            project_namespace_id: Project namespace ID (uses current if not specified)

        Returns:
            JSON array of renders with their metadata

        Example:
            renders = await artifact_list_renders()
        """
        try:
            namespace_id = project_namespace_id or async_project_manager.current_project_id
            if not namespace_id:
                return json.dumps({"error": "No active project. Create a project first."})

            # Note: This would need to be implemented in the storage layer
            # For now, return a placeholder response
            result = {
                "success": True,
                "project_namespace_id": namespace_id,
                "message": "Use artifact_get_download_url with a render_id to get download URLs",
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            logger.exception("Error listing renders")
            return json.dumps({"error": str(e)})

    @mcp.tool  # type: ignore[arg-type]
    async def artifact_export_base64(render_id: str) -> str:
        """
        Export a rendered video as a base64-encoded string.

        Exports the rendered video as a base64 string that can be
        saved, transmitted, or used in data URIs.

        Args:
            render_id: The render/namespace ID returned from artifact_render_video

        Returns:
            JSON string with base64 data and metadata

        Example:
            result = await artifact_export_base64(render_id="ns_abc123")
        """
        try:
            import base64

            # Read the video data
            video_data = await async_project_manager.storage.read_render_data(render_id)
            if not video_data:
                return json.dumps({"error": f"Render not found: {render_id}"})

            # Get render metadata
            render_info = await async_project_manager.storage.get_render(render_id)

            # Encode as base64
            b64_data = base64.b64encode(video_data).decode("utf-8")

            return json.dumps(
                {
                    "success": True,
                    "render_id": render_id,
                    "format": render_info.metadata.format,
                    "mime_type": f"video/{render_info.metadata.format}",
                    "resolution": render_info.metadata.resolution,
                    "size_bytes": render_info.metadata.file_size_bytes,
                    "data": b64_data,
                }
            )

        except Exception as e:
            logger.exception("Error exporting as base64")
            return json.dumps({"error": f"Failed to export: {str(e)}"})

    @mcp.tool  # type: ignore[arg-type]
    async def artifact_status() -> str:
        """
        Get the status of artifact storage and configuration.

        Returns:
            JSON with artifact storage status and capabilities

        Example:
            status = await artifact_status()
        """
        try:
            from chuk_mcp_server import has_artifact_store

            artifact_store_available = has_artifact_store()

            result = {
                "success": True,
                "artifact_store_available": artifact_store_available,
                "storage_provider": async_project_manager.storage.provider_type.value,
                "current_project_id": async_project_manager.current_project_id,
                "features": {
                    "download_urls": artifact_store_available,
                    "base64_export": True,
                    "checkpoints": True,
                    "render_storage": True,
                },
            }

            if artifact_store_available:
                result["message"] = "Artifact store configured. Download URLs are available."
            else:
                result["message"] = (
                    "No artifact store configured. "
                    "Set CHUK_ARTIFACTS_PROVIDER=s3 and configure S3 credentials for download URLs."
                )

            return json.dumps(result, indent=2)

        except Exception as e:
            logger.exception("Error getting status")
            return json.dumps({"error": str(e)})

    logger.info("Registered artifact-based project management tools")
