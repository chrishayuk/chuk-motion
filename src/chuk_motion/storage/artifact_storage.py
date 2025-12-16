"""
Artifact storage manager for chuk-motion.

Provides async-native, type-safe integration with chuk-artifacts for:
- Project storage (WORKSPACE namespaces)
- Render storage (BLOB namespaces)
- Asset management (BLOB namespaces)
- Checkpoint/versioning
"""

import hashlib
import logging
from datetime import datetime
from typing import Any

from chuk_artifacts import ArtifactStore
from chuk_artifacts import CheckpointInfo as ChukCheckpointInfo
from chuk_artifacts import NamespaceInfo as ChukNamespaceInfo
from chuk_artifacts import NamespaceType as ChukNamespaceType
from chuk_artifacts import StorageScope as ChukStorageScope
from chuk_virtual_fs import AsyncVirtualFileSystem

from ..models.artifact_models import (
    AssetInfo,
    AssetMetadata,
    CheckpointInfo,
    NamespaceInfo,
    NamespaceType,
    ProjectInfo,
    ProjectMetadata,
    ProviderType,
    RenderInfo,
    RenderMetadata,
    StorageScope,
)

logger = logging.getLogger(__name__)


class ArtifactStorageManager:
    """
    Manages artifact storage for chuk-motion using chuk-artifacts.

    This class provides a type-safe, async-native API for:
    - Creating and managing project workspaces
    - Storing rendered videos
    - Managing media assets
    - Versioning with checkpoints

    All operations use Pydantic models and proper enum types.
    """

    def __init__(
        self,
        provider_type: ProviderType = ProviderType.MEMORY,
        provider_config: dict[str, Any] | None = None,
    ):
        """
        Initialize artifact storage manager.

        Args:
            provider_type: Storage provider backend
            provider_config: Provider-specific configuration
        """
        self.provider_type = provider_type
        self.provider_config = provider_config or {}
        self._store: ArtifactStore | None = None

    async def initialize(self) -> None:
        """Initialize the artifact store (async context manager)."""
        if self._store is None:
            self._store = ArtifactStore(
                storage_provider=self.provider_type.value, **self.provider_config
            )
            await self._store.__aenter__()
            logger.info(f"Initialized artifact storage with {self.provider_type.value} provider")

    async def cleanup(self) -> None:
        """Cleanup the artifact store (async context manager)."""
        if self._store is not None:
            await self._store.__aexit__(None, None, None)
            self._store = None
            logger.info("Cleaned up artifact storage")

    @property
    def store(self) -> ArtifactStore:
        """Get the artifact store instance."""
        if self._store is None:
            raise RuntimeError("ArtifactStorageManager not initialized. Call initialize() first.")
        return self._store

    # =========================================================================
    # Project Management (WORKSPACE namespaces)
    # =========================================================================

    async def create_project(
        self,
        project_name: str,
        theme: str,
        fps: int,
        width: int,
        height: int,
        scope: StorageScope = StorageScope.USER,
        user_id: str | None = None,
        ttl_hours: int | None = None,
    ) -> ProjectInfo:
        """
        Create a new Remotion project as a WORKSPACE namespace.

        Args:
            project_name: Human-readable project name
            theme: Theme name (tech, finance, etc.)
            fps: Frames per second
            width: Video width in pixels
            height: Video height in pixels
            scope: Storage scope (SESSION, USER, SANDBOX)
            user_id: User ID (required for USER scope)
            ttl_hours: TTL in hours (SESSION scope only)

        Returns:
            ProjectInfo with namespace and metadata

        Raises:
            ValueError: If user_id is missing for USER scope
        """
        if scope == StorageScope.USER and not user_id:
            raise ValueError("user_id is required for USER scope")

        # Default TTL for SESSION scope if not specified
        if scope == StorageScope.SESSION and ttl_hours is None:
            ttl_hours = 24  # Default to 24 hours for session scope

        # Create workspace namespace
        chuk_namespace = await self.store.create_namespace(
            type=ChukNamespaceType.WORKSPACE,
            name=project_name,
            scope=self._to_chuk_scope(scope),
            user_id=user_id,
            ttl_hours=ttl_hours,
        )

        # Create project metadata
        metadata = ProjectMetadata(
            project_name=project_name,
            theme=theme,
            fps=fps,
            width=width,
            height=height,
        )

        # Store metadata in workspace
        vfs = self.store.get_namespace_vfs(chuk_namespace.namespace_id)
        await vfs.mkdir("/.chuk-motion")
        await vfs.write_file("/.chuk-motion/metadata.json", metadata.model_dump_json().encode())

        # Convert to our models
        namespace_info = self._convert_namespace_info(chuk_namespace)

        return ProjectInfo(namespace_info=namespace_info, metadata=metadata, checkpoints=[])

    async def get_project(self, namespace_id: str) -> ProjectInfo:
        """
        Get project information by namespace ID.

        Args:
            namespace_id: Namespace identifier

        Returns:
            ProjectInfo with namespace and metadata
        """
        # Get VFS for namespace
        vfs = self.store.get_namespace_vfs(namespace_id)

        # Load metadata
        metadata_json = await vfs.read_file("/.chuk-motion/metadata.json")
        metadata = ProjectMetadata.model_validate_json(metadata_json)

        # Get namespace info from store
        chuk_namespace = self.store.get_namespace_info(namespace_id)

        if not chuk_namespace:
            raise ValueError(f"Namespace not found: {namespace_id}")

        namespace_info = self._convert_namespace_info(chuk_namespace)

        # Get checkpoints
        chuk_checkpoints = await self.store.list_checkpoints(namespace_id)
        checkpoints = [self._convert_checkpoint_info(cp) for cp in chuk_checkpoints]

        return ProjectInfo(
            namespace_info=namespace_info, metadata=metadata, checkpoints=checkpoints
        )

    async def update_project_metadata(
        self, namespace_id: str, metadata: ProjectMetadata
    ) -> ProjectInfo:
        """
        Update project metadata.

        Args:
            namespace_id: Namespace identifier
            metadata: Updated project metadata

        Returns:
            Updated ProjectInfo
        """
        metadata.updated_at = datetime.now()

        # Update metadata in workspace
        vfs = self.store.get_namespace_vfs(namespace_id)
        await vfs.write_file("/.chuk-motion/metadata.json", metadata.model_dump_json().encode())

        return await self.get_project(namespace_id)

    async def get_project_vfs(self, namespace_id: str) -> AsyncVirtualFileSystem:
        """
        Get VFS for direct file operations on project.

        Args:
            namespace_id: Namespace identifier

        Returns:
            AsyncVirtualFileSystem instance for the project
        """
        return self.store.get_namespace_vfs(namespace_id)

    async def list_projects(
        self, scope: StorageScope | None = None, user_id: str | None = None
    ) -> list[ProjectInfo]:
        """
        List all projects with optional filtering.

        Args:
            scope: Filter by storage scope
            user_id: Filter by user ID

        Returns:
            List of ProjectInfo objects
        """
        namespaces = self.store.list_namespaces(type=ChukNamespaceType.WORKSPACE, user_id=user_id)

        projects = []
        for chuk_namespace in namespaces:
            try:
                # Skip if scope filter doesn't match
                if scope and self._from_chuk_scope(chuk_namespace.scope) != scope:
                    continue

                # Load project
                project = await self.get_project(chuk_namespace.namespace_id)
                projects.append(project)
            except Exception as e:
                logger.warning(f"Failed to load project {chuk_namespace.namespace_id}: {e}")

        return projects

    async def delete_project(self, namespace_id: str) -> None:
        """
        Delete a project workspace.

        Args:
            namespace_id: Namespace identifier
        """
        await self.store.destroy_namespace(namespace_id)
        logger.info(f"Deleted project namespace: {namespace_id}")

    # =========================================================================
    # Render Management (BLOB namespaces)
    # =========================================================================

    async def store_render(
        self,
        project_namespace_id: str,
        video_data: bytes,
        format: str,
        resolution: str,
        fps: int,
        duration_seconds: float,
        scope: StorageScope = StorageScope.USER,
        user_id: str | None = None,
        codec: str | None = None,
        bitrate_kbps: int | None = None,
    ) -> RenderInfo:
        """
        Store a rendered video as a BLOB namespace.

        Args:
            project_namespace_id: Source project namespace ID
            video_data: Video file bytes
            format: Video format (mp4, webm)
            resolution: Video resolution (1920x1080)
            fps: Frames per second
            duration_seconds: Total video duration
            scope: Storage scope
            user_id: User ID (required for USER scope)
            codec: Video codec (h264, vp9)
            bitrate_kbps: Video bitrate in kbps

        Returns:
            RenderInfo with namespace and metadata
        """
        if scope == StorageScope.USER and not user_id:
            raise ValueError("user_id is required for USER scope")

        # Calculate checksum
        checksum = hashlib.sha256(video_data).hexdigest()

        # Create blob namespace
        chuk_namespace = await self.store.create_namespace(
            type=ChukNamespaceType.BLOB,
            scope=self._to_chuk_scope(scope),
            user_id=user_id,
        )

        # Create render metadata
        metadata = RenderMetadata(
            project_namespace_id=project_namespace_id,
            format=format,
            resolution=resolution,
            fps=fps,
            duration_seconds=duration_seconds,
            file_size_bytes=len(video_data),
            checksum=checksum,
            codec=codec,
            bitrate_kbps=bitrate_kbps,
        )

        # Store metadata FIRST (as a path)
        await self.store.write_namespace(
            chuk_namespace.namespace_id,
            path="/.chuk-motion/metadata.json",
            data=metadata.model_dump_json().encode(),
        )

        # Write video data as default blob (no path = default content)
        await self.store.write_namespace(chuk_namespace.namespace_id, data=video_data)

        # Convert to our models
        namespace_info = self._convert_namespace_info(chuk_namespace)

        logger.info(
            f"Stored render: {namespace_info.namespace_id} ({len(video_data)} bytes, {format})"
        )

        return RenderInfo(namespace_info=namespace_info, metadata=metadata)

    async def get_render(self, namespace_id: str) -> RenderInfo:
        """
        Get render information by namespace ID.

        Args:
            namespace_id: Namespace identifier

        Returns:
            RenderInfo with namespace and metadata
        """
        # Load metadata
        metadata_json = await self.store.read_namespace(
            namespace_id, path="/.chuk-motion/metadata.json"
        )
        metadata = RenderMetadata.model_validate_json(metadata_json)

        # Get namespace info
        chuk_namespace = self.store.get_namespace_info(namespace_id)

        if not chuk_namespace:
            raise ValueError(f"Namespace not found: {namespace_id}")

        namespace_info = self._convert_namespace_info(chuk_namespace)

        return RenderInfo(namespace_info=namespace_info, metadata=metadata)

    async def read_render_data(self, namespace_id: str) -> bytes:
        """
        Read rendered video data.

        Args:
            namespace_id: Namespace identifier

        Returns:
            Video file bytes
        """
        # For BLOB namespaces, read default content (no path)
        return await self.store.read_namespace(namespace_id)

    # =========================================================================
    # Asset Management (BLOB namespaces)
    # =========================================================================

    async def store_asset(
        self,
        asset_data: bytes,
        asset_type: str,
        mime_type: str,
        tags: list[str] | None = None,
        project_namespace_ids: list[str] | None = None,
        width: int | None = None,
        height: int | None = None,
        duration_seconds: float | None = None,
        scope: StorageScope = StorageScope.USER,
        user_id: str | None = None,
    ) -> AssetInfo:
        """
        Store a media asset as a BLOB namespace.

        Args:
            asset_data: Asset file bytes
            asset_type: Asset type (image, audio, font)
            mime_type: MIME type
            tags: Searchable tags
            project_namespace_ids: Projects using this asset
            width: Image/video width in pixels
            height: Image/video height in pixels
            duration_seconds: Audio/video duration
            scope: Storage scope
            user_id: User ID (required for USER scope)

        Returns:
            AssetInfo with namespace and metadata
        """
        if scope == StorageScope.USER and not user_id:
            raise ValueError("user_id is required for USER scope")

        # Calculate checksum
        checksum = hashlib.sha256(asset_data).hexdigest()

        # Create blob namespace
        chuk_namespace = await self.store.create_namespace(
            type=ChukNamespaceType.BLOB,
            scope=self._to_chuk_scope(scope),
            user_id=user_id,
        )

        # Create asset metadata
        metadata = AssetMetadata(
            asset_type=asset_type,
            mime_type=mime_type,
            file_size_bytes=len(asset_data),
            tags=tags or [],
            project_namespace_ids=project_namespace_ids or [],
            width=width,
            height=height,
            duration_seconds=duration_seconds,
            checksum=checksum,
        )

        # Store metadata FIRST (as a path)
        await self.store.write_namespace(
            chuk_namespace.namespace_id,
            path="/.chuk-motion/metadata.json",
            data=metadata.model_dump_json().encode(),
        )

        # Write asset data as default blob (no path = default content)
        await self.store.write_namespace(chuk_namespace.namespace_id, data=asset_data)

        # Convert to our models
        namespace_info = self._convert_namespace_info(chuk_namespace)

        logger.info(
            f"Stored asset: {namespace_info.namespace_id} ({len(asset_data)} bytes, {asset_type})"
        )

        return AssetInfo(namespace_info=namespace_info, metadata=metadata)

    async def get_asset(self, namespace_id: str) -> AssetInfo:
        """
        Get asset information by namespace ID.

        Args:
            namespace_id: Namespace identifier

        Returns:
            AssetInfo with namespace and metadata
        """
        # Load metadata
        metadata_json = await self.store.read_namespace(
            namespace_id, path="/.chuk-motion/metadata.json"
        )
        metadata = AssetMetadata.model_validate_json(metadata_json)

        # Get namespace info
        chuk_namespace = self.store.get_namespace_info(namespace_id)

        if not chuk_namespace:
            raise ValueError(f"Namespace not found: {namespace_id}")

        namespace_info = self._convert_namespace_info(chuk_namespace)

        return AssetInfo(namespace_info=namespace_info, metadata=metadata)

    async def read_asset_data(self, namespace_id: str) -> bytes:
        """
        Read asset data.

        Args:
            namespace_id: Namespace identifier

        Returns:
            Asset file bytes
        """
        # For BLOB namespaces, read default content (no path)
        return await self.store.read_namespace(namespace_id)

    # =========================================================================
    # Checkpoint Management
    # =========================================================================

    async def create_checkpoint(
        self, namespace_id: str, name: str, description: str | None = None
    ) -> CheckpointInfo:
        """
        Create a checkpoint of a namespace (project or render).

        Args:
            namespace_id: Namespace identifier
            name: Checkpoint name
            description: Optional description

        Returns:
            CheckpointInfo
        """
        chuk_checkpoint = await self.store.checkpoint_namespace(
            namespace_id=namespace_id, name=name, description=description
        )

        checkpoint = self._convert_checkpoint_info(chuk_checkpoint)

        logger.info(f"Created checkpoint: {checkpoint.checkpoint_id} ({name})")

        return checkpoint

    async def list_checkpoints(self, namespace_id: str) -> list[CheckpointInfo]:
        """
        List all checkpoints for a namespace.

        Args:
            namespace_id: Namespace identifier

        Returns:
            List of CheckpointInfo objects (ordered by creation time, oldest first)
        """
        chuk_checkpoints = await self.store.list_checkpoints(namespace_id)
        checkpoints = [self._convert_checkpoint_info(cp) for cp in chuk_checkpoints]
        # Sort by created_at to ensure consistent ordering (oldest first)
        return sorted(checkpoints, key=lambda cp: cp.created_at)

    async def restore_checkpoint(self, namespace_id: str, checkpoint_id: str) -> None:
        """
        Restore a namespace from a checkpoint.

        Args:
            namespace_id: Namespace identifier
            checkpoint_id: Checkpoint identifier
        """
        await self.store.restore_namespace(namespace_id, checkpoint_id)
        logger.info(f"Restored namespace {namespace_id} from checkpoint {checkpoint_id}")

    async def delete_checkpoint(self, namespace_id: str, checkpoint_id: str) -> None:
        """
        Delete a checkpoint.

        Args:
            namespace_id: Namespace identifier
            checkpoint_id: Checkpoint identifier
        """
        await self.store.delete_checkpoint(namespace_id, checkpoint_id)  # type: ignore[attr-defined]
        logger.info(f"Deleted checkpoint: {checkpoint_id}")

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _to_chuk_scope(self, scope: StorageScope) -> ChukStorageScope:
        """Convert our StorageScope enum to chuk-artifacts StorageScope."""
        mapping = {
            StorageScope.SESSION: ChukStorageScope.SESSION,
            StorageScope.USER: ChukStorageScope.USER,
            StorageScope.SANDBOX: ChukStorageScope.SANDBOX,
        }
        return mapping[scope]

    def _from_chuk_scope(self, scope: ChukStorageScope) -> StorageScope:
        """Convert chuk-artifacts StorageScope to our enum."""
        mapping = {
            ChukStorageScope.SESSION: StorageScope.SESSION,
            ChukStorageScope.USER: StorageScope.USER,
            ChukStorageScope.SANDBOX: StorageScope.SANDBOX,
        }
        return mapping[scope]

    def _convert_namespace_info(self, chuk_namespace: ChukNamespaceInfo) -> NamespaceInfo:
        """Convert chuk-artifacts NamespaceInfo to our model."""
        return NamespaceInfo(
            namespace_id=chuk_namespace.namespace_id,
            namespace_type=(
                NamespaceType.WORKSPACE
                if chuk_namespace.type == ChukNamespaceType.WORKSPACE
                else NamespaceType.BLOB
            ),
            scope=self._from_chuk_scope(chuk_namespace.scope),
            name=getattr(chuk_namespace, "name", None),
            user_id=getattr(chuk_namespace, "user_id", None),
            session_id=getattr(chuk_namespace, "session_id", None),
            provider_type=ProviderType(chuk_namespace.provider_type),
            grid_path=chuk_namespace.grid_path,
            created_at=getattr(chuk_namespace, "created_at", datetime.now()),
            ttl_hours=getattr(chuk_namespace, "ttl_hours", None),
        )

    def _convert_checkpoint_info(self, chuk_checkpoint: ChukCheckpointInfo) -> CheckpointInfo:
        """Convert chuk-artifacts CheckpointInfo to our model."""
        # chuk-artifacts uses workspace_id, we use namespace_id
        workspace_id = getattr(chuk_checkpoint, "workspace_id", None) or getattr(
            chuk_checkpoint, "namespace_id", None
        )
        if not workspace_id:
            raise ValueError("Checkpoint must have workspace_id or namespace_id")

        return CheckpointInfo(
            checkpoint_id=chuk_checkpoint.checkpoint_id,
            namespace_id=workspace_id,
            name=chuk_checkpoint.name or "",
            description=getattr(chuk_checkpoint, "description", None),
            created_at=getattr(chuk_checkpoint, "created_at", datetime.now()),
            metadata=getattr(chuk_checkpoint, "metadata", {}),
        )
