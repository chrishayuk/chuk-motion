"""
Pydantic models for artifact storage integration.

This module provides type-safe models for working with chuk-artifacts,
including namespace types, scopes, and metadata structures.
"""

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class NamespaceType(StrEnum):
    """Type of namespace in artifact storage."""

    BLOB = "blob"  # Single file (renders, assets)
    WORKSPACE = "workspace"  # Multi-file directory tree (projects)


class StorageScope(StrEnum):
    """Storage scope for namespace isolation."""

    SESSION = "session"  # Ephemeral (session lifetime)
    USER = "user"  # Persistent (user-owned)
    SANDBOX = "sandbox"  # Persistent (shared)


class ProviderType(StrEnum):
    """Storage provider backend type."""

    MEMORY = "vfs-memory"  # In-memory (development)
    FILESYSTEM = "vfs-filesystem"  # Filesystem (local)
    SQLITE = "vfs-sqlite"  # SQLite (embedded)
    S3 = "vfs-s3"  # S3 (production cloud)


class ProjectMetadata(BaseModel):
    """Metadata for a Remotion project namespace."""

    project_name: str = Field(..., description="Human-readable project name")
    theme: str = Field(..., description="Theme name (tech, finance, etc.)")
    fps: int = Field(..., description="Frames per second")
    width: int = Field(..., description="Video width in pixels")
    height: int = Field(..., description="Video height in pixels")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    total_duration_seconds: float = Field(default=0.0, description="Total video duration")
    component_count: int = Field(default=0, description="Number of components in composition")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "project_name": "my_tutorial_video",
                "theme": "tech",
                "fps": 30,
                "width": 1920,
                "height": 1080,
                "total_duration_seconds": 45.5,
                "component_count": 5,
            }
        }


class RenderMetadata(BaseModel):
    """Metadata for a rendered video artifact."""

    project_namespace_id: str = Field(..., description="Source project namespace ID")
    format: str = Field(..., description="Video format (mp4, webm)")
    resolution: str = Field(..., description="Video resolution (1920x1080)")
    fps: int = Field(..., description="Frames per second")
    duration_seconds: float = Field(..., description="Total video duration")
    file_size_bytes: int = Field(..., description="File size in bytes")
    render_date: datetime = Field(default_factory=datetime.now, description="Render timestamp")
    checksum: str | None = Field(None, description="SHA256 checksum")
    codec: str | None = Field(None, description="Video codec (h264, vp9)")
    bitrate_kbps: int | None = Field(None, description="Video bitrate in kbps")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "project_namespace_id": "ns_abc123",
                "format": "mp4",
                "resolution": "1920x1080",
                "fps": 30,
                "duration_seconds": 45.5,
                "file_size_bytes": 15728640,
                "codec": "h264",
                "bitrate_kbps": 5000,
            }
        }


class AssetMetadata(BaseModel):
    """Metadata for a media asset artifact."""

    asset_type: str = Field(..., description="Asset type (image, audio, font)")
    mime_type: str = Field(..., description="MIME type")
    file_size_bytes: int = Field(..., description="File size in bytes")
    tags: list[str] = Field(default_factory=list, description="Searchable tags")
    project_namespace_ids: list[str] = Field(
        default_factory=list, description="Projects using this asset"
    )
    width: int | None = Field(None, description="Image/video width in pixels")
    height: int | None = Field(None, description="Image/video height in pixels")
    duration_seconds: float | None = Field(None, description="Audio/video duration")
    uploaded_at: datetime = Field(default_factory=datetime.now, description="Upload timestamp")
    checksum: str | None = Field(None, description="SHA256 checksum")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "asset_type": "image",
                "mime_type": "image/png",
                "file_size_bytes": 524288,
                "tags": ["background", "tech", "gradient"],
                "width": 1920,
                "height": 1080,
            }
        }


class NamespaceInfo(BaseModel):
    """Information about a created namespace."""

    namespace_id: str = Field(..., description="Unique namespace identifier")
    namespace_type: NamespaceType = Field(..., description="Type of namespace")
    scope: StorageScope = Field(..., description="Storage scope")
    name: str | None = Field(None, description="Human-readable name (workspaces only)")
    user_id: str | None = Field(None, description="Owner user ID (USER scope only)")
    session_id: str | None = Field(None, description="Session ID (SESSION scope only)")
    provider_type: ProviderType = Field(..., description="Storage provider backend")
    grid_path: str = Field(..., description="Grid storage path")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    ttl_hours: int | None = Field(None, description="TTL in hours (SESSION scope only)")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "namespace_id": "ns_abc123",
                "namespace_type": "workspace",
                "scope": "user",
                "name": "my_video_project",
                "user_id": "alice",
                "provider_type": "vfs-s3",
                "grid_path": "grid/default/user-alice/ns_abc123",
            }
        }


class CheckpointInfo(BaseModel):
    """Information about a namespace checkpoint."""

    checkpoint_id: str = Field(..., description="Unique checkpoint identifier")
    namespace_id: str = Field(..., description="Source namespace ID")
    name: str = Field(..., description="Checkpoint name")
    description: str | None = Field(None, description="Optional description")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional checkpoint metadata"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "checkpoint_id": "cp_123",
                "namespace_id": "ns_abc123",
                "name": "v1.0-ready-for-review",
                "description": "All animations complete, awaiting feedback",
            }
        }


class ProjectInfo(BaseModel):
    """Complete project information with namespace details."""

    namespace_info: NamespaceInfo = Field(..., description="Namespace information")
    metadata: ProjectMetadata = Field(..., description="Project metadata")
    checkpoints: list[CheckpointInfo] = Field(
        default_factory=list, description="Project checkpoints"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "namespace_info": {
                    "namespace_id": "ns_abc123",
                    "namespace_type": "workspace",
                    "scope": "user",
                    "name": "my_video_project",
                    "user_id": "alice",
                },
                "metadata": {
                    "project_name": "my_tutorial_video",
                    "theme": "tech",
                    "fps": 30,
                    "width": 1920,
                    "height": 1080,
                },
                "checkpoints": [],
            }
        }


class RenderInfo(BaseModel):
    """Complete render information with namespace details."""

    namespace_info: NamespaceInfo = Field(..., description="Namespace information")
    metadata: RenderMetadata = Field(..., description="Render metadata")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "namespace_info": {
                    "namespace_id": "ns_render_xyz",
                    "namespace_type": "blob",
                    "scope": "user",
                    "user_id": "alice",
                },
                "metadata": {
                    "project_namespace_id": "ns_abc123",
                    "format": "mp4",
                    "resolution": "1920x1080",
                    "fps": 30,
                    "duration_seconds": 45.5,
                    "file_size_bytes": 15728640,
                },
            }
        }


class AssetInfo(BaseModel):
    """Complete asset information with namespace details."""

    namespace_info: NamespaceInfo = Field(..., description="Namespace information")
    metadata: AssetMetadata = Field(..., description="Asset metadata")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "namespace_info": {
                    "namespace_id": "ns_asset_123",
                    "namespace_type": "blob",
                    "scope": "user",
                    "user_id": "alice",
                },
                "metadata": {
                    "asset_type": "image",
                    "mime_type": "image/png",
                    "file_size_bytes": 524288,
                    "tags": ["background", "tech"],
                },
            }
        }
