"""
Video Manager for Remotion MCP Server

Manages video compositions with support for chuk-artifacts integration.
Each project is stored as a WORKSPACE namespace for persistence.

Uses chuk-mcp-server's built-in artifact store context for storage.
Uses Pydantic models throughout for type safety and validation.

Pattern follows chuk-mcp-pptx's PresentationManager exactly.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .generator.composition_builder import CompositionBuilder

logger = logging.getLogger(__name__)


# =============================================================================
# Pydantic Models
# =============================================================================


class VideoMetadata(BaseModel):
    """Metadata for a video project."""

    project_name: str
    theme: str = "tech"
    fps: int = 30
    width: int = 1920
    height: int = 1080
    total_duration_seconds: float = 0.0
    component_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class VideoInfo(BaseModel):
    """Information about a video project."""

    name: str
    namespace_id: str | None = None
    artifact_uri: str | None = None
    metadata: VideoMetadata


class RenderResult(BaseModel):
    """Result of a video render."""

    success: bool
    render_id: str | None = None
    output_path: str | None = None
    format: str = "mp4"
    resolution: str | None = None
    fps: int | None = None
    duration_seconds: float | None = None
    file_size_bytes: int | None = None
    download_url: str | None = None
    error: str | None = None


class ComponentResponse(BaseModel):
    """Response from adding a component."""

    component: str
    start_time: float
    duration: float


class ProjectResponse(BaseModel):
    """Response from creating a project."""

    name: str
    path: str
    namespace_id: str | None = None
    theme: str
    fps: int
    width: int
    height: int


# =============================================================================
# Video Manager
# =============================================================================


class VideoManager:
    """
    Manages video compositions with chuk-artifacts integration.

    Uses chuk-mcp-server's built-in artifact store context for flexible storage
    (memory, filesystem, sqlite, s3). Each project is stored as a WORKSPACE
    namespace with automatic session management.

    Pattern follows chuk-mcp-pptx's PresentationManager exactly.
    """

    def __init__(self, base_path: str = "videos") -> None:
        """
        Initialize the video manager.

        Args:
            base_path: Base path prefix for project names
        """
        self.base_path = base_path
        self._builders: dict[str, CompositionBuilder] = {}
        self._metadata: dict[str, VideoMetadata] = {}
        self._namespace_ids: dict[str, str] = {}
        self._current_project: str | None = None
        logger.info(f"VideoManager initialized, base path: {base_path}")

    def _get_store(self):
        """Get the artifact store from context."""
        from chuk_mcp_server import get_artifact_store, has_artifact_store

        if has_artifact_store():
            return get_artifact_store()
        return None

    def _sanitize_name(self, name: str) -> str:
        """Sanitize project name to prevent directory traversal."""
        safe_name = "".join(c for c in name if c.isalnum() or c in ("-", "_"))
        if not safe_name:
            safe_name = "video"
        return safe_name

    def get_namespace_id(self, name: str) -> str | None:
        """Get the namespace ID for a project by name."""
        return self._namespace_ids.get(name)

    def get_artifact_uri(self, name: str) -> str | None:
        """Get the artifact URI for a project."""
        namespace_id = self._namespace_ids.get(name)
        if namespace_id:
            return f"artifact://chuk-motion/{self.base_path}/{name}"
        return None

    # =========================================================================
    # Project Management
    # =========================================================================

    async def create_project(
        self,
        name: str,
        theme: str = "tech",
        fps: int = 30,
        width: int = 1920,
        height: int = 1080,
    ) -> ProjectResponse:
        """
        Create a new video project.

        Args:
            name: Project name
            theme: Theme name
            fps: Frames per second
            width: Video width
            height: Video height

        Returns:
            ProjectResponse with project info
        """
        safe_name = self._sanitize_name(name)

        # Create composition builder (only accepts fps, width, height, transparent)
        builder = CompositionBuilder(
            fps=fps,
            width=width,
            height=height,
        )
        # Set theme separately
        builder.theme = theme

        # Store builder and metadata
        self._builders[safe_name] = builder
        self._metadata[safe_name] = VideoMetadata(
            project_name=safe_name,
            theme=theme,
            fps=fps,
            width=width,
            height=height,
        )
        self._current_project = safe_name

        # Save to artifact store if available
        namespace_id = await self._save_to_store(safe_name)

        logger.info(f"Created project: {safe_name}")

        return ProjectResponse(
            name=safe_name,
            path=self.get_artifact_uri(safe_name) or f"local://{safe_name}",
            namespace_id=namespace_id,
            theme=theme,
            fps=fps,
            width=width,
            height=height,
        )

    async def _save_to_store(self, name: str) -> str | None:
        """
        Save project to artifact store.

        Args:
            name: Project name

        Returns:
            Namespace ID if successful, None otherwise
        """
        store = self._get_store()
        if not store:
            logger.debug("No artifact store available, skipping persistence")
            return None

        from chuk_mcp_server import NamespaceType, StorageScope

        try:
            # Check if namespace already exists
            namespace_id = self._namespace_ids.get(name)

            if not namespace_id:
                # Create new WORKSPACE namespace
                safe_name = self._sanitize_name(name)
                namespace_info = await store.create_namespace(
                    type=NamespaceType.WORKSPACE,
                    scope=StorageScope.SESSION,
                    name=f"{self.base_path}/{safe_name}",
                    metadata={
                        "project_name": name,
                        "type": "remotion_project",
                    },
                )
                self._namespace_ids[name] = namespace_info.namespace_id
                namespace_id = namespace_info.namespace_id
                logger.info(f"Created namespace for project: {name} ({namespace_id})")

            return namespace_id

        except Exception as e:
            logger.error(f"Failed to save to artifact store: {e}")
            return None

    def get_current_builder(self) -> CompositionBuilder | None:
        """Get the current project's composition builder."""
        if self._current_project:
            return self._builders.get(self._current_project)
        return None

    @property
    def current_timeline(self) -> CompositionBuilder | None:
        """Get the current timeline (alias for get_current_builder for component tools)."""
        return self.get_current_builder()

    def get_builder(self, name: str) -> CompositionBuilder | None:
        """Get a project's composition builder by name."""
        return self._builders.get(name)

    def get_metadata(self, name: str | None = None) -> VideoMetadata | None:
        """Get project metadata."""
        name = name or self._current_project
        if name:
            return self._metadata.get(name)
        return None

    def list_projects(self) -> list[VideoInfo]:
        """List all projects."""
        projects = []
        for name, metadata in self._metadata.items():
            projects.append(
                VideoInfo(
                    name=name,
                    namespace_id=self._namespace_ids.get(name),
                    artifact_uri=self.get_artifact_uri(name),
                    metadata=metadata,
                )
            )
        return projects

    # =========================================================================
    # Component Addition
    # =========================================================================

    def add_component(
        self,
        component_type: str,
        duration: float = 3.0,
        **kwargs: Any,
    ) -> ComponentResponse:
        """
        Add a component to the current project.

        Args:
            component_type: Type of component (e.g., "title_scene", "fuzzy_text")
            duration: Duration in seconds
            **kwargs: Component-specific parameters

        Returns:
            ComponentResponse with component info
        """
        builder = self.get_current_builder()
        if not builder:
            raise ValueError("No active project. Create a project first.")

        # Get the add method for this component type
        method_name = f"add_{component_type}"
        if not hasattr(builder, method_name):
            raise ValueError(f"Unknown component type: {component_type}")

        method = getattr(builder, method_name)

        # Track start time before adding
        start_time = builder.get_total_duration_seconds()

        # Add the component
        method(duration=duration, **kwargs)

        # Update metadata
        if self._current_project and self._current_project in self._metadata:
            meta = self._metadata[self._current_project]
            meta.component_count += 1
            meta.total_duration_seconds = builder.get_total_duration_seconds()
            meta.updated_at = datetime.utcnow()

        return ComponentResponse(
            component=component_type,
            start_time=start_time,
            duration=duration,
        )

    # =========================================================================
    # Video Generation
    # =========================================================================

    async def generate_video(
        self,
        name: str | None = None,
    ) -> dict[str, Any]:
        """
        Generate video composition files.

        Args:
            name: Project name (uses current if not specified)

        Returns:
            Dict with generation result
        """
        name = name or self._current_project
        if not name:
            raise ValueError("No active project. Create a project first.")

        builder = self._builders.get(name)
        if not builder:
            raise ValueError(f"Project not found: {name}")

        # Build the composition (to_dict() exports all composition data)
        composition = builder.to_dict()

        # Get namespace ID for reference
        namespace_id = self._namespace_ids.get(name)

        logger.info(f"Generated composition for project: {name}")

        return {
            "status": "success",
            "project": {
                "namespace_id": namespace_id,
                "name": name,
                "path": self.get_artifact_uri(name) or f"local://{name}",
            },
            "composition": {
                "fps": composition.get("fps", 30),
                "width": composition.get("width", 1920),
                "height": composition.get("height", 1080),
                "durationInFrames": composition.get("duration_frames", 0),
                "components": len(composition.get("components", [])),
            },
        }

    # =========================================================================
    # Download URL Generation
    # =========================================================================

    async def get_download_url(
        self,
        render_id: str,
        expires_in: int = 3600,
    ) -> dict[str, Any]:
        """
        Get a presigned download URL for a rendered video.

        Args:
            render_id: Render/artifact ID
            expires_in: URL expiration time in seconds

        Returns:
            Dict with download URL info
        """
        store = self._get_store()
        if not store:
            return {"error": "No artifact store configured for download URLs"}

        try:
            # Generate presigned URL
            url = await store.presign(render_id, expires=expires_in)

            return {
                "success": True,
                "url": url,
                "render_id": render_id,
                "expires_in": expires_in,
            }

        except Exception as e:
            logger.error(f"Failed to generate download URL: {e}")
            return {"error": f"Failed to generate download URL: {str(e)}"}

    async def store_render(
        self,
        video_data: bytes,
        format: str = "mp4",
        project_name: str | None = None,
    ) -> dict[str, Any]:
        """
        Store a rendered video as an artifact.

        Args:
            video_data: Video file bytes
            format: Video format (mp4, webm)
            project_name: Associated project name

        Returns:
            Dict with artifact info including ID for download URL
        """
        store = self._get_store()
        if not store:
            return {"error": "No artifact store configured"}

        try:
            project_name = project_name or self._current_project
            filename = f"{project_name or 'video'}.{format}"

            # Store as artifact
            artifact_id = await store.store(
                data=video_data,
                mime=f"video/{format}",
                summary=filename,
                meta={
                    "filename": filename,
                    "format": format,
                    "project_name": project_name,
                    "size_bytes": len(video_data),
                },
            )

            logger.info(f"Stored render as artifact: {artifact_id}")

            return {
                "success": True,
                "artifact_id": artifact_id,
                "filename": filename,
                "format": format,
                "size_bytes": len(video_data),
            }

        except Exception as e:
            logger.error(f"Failed to store render: {e}")
            return {"error": f"Failed to store render: {str(e)}"}
