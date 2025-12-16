"""Integration tests for AsyncProjectManager."""

import pytest

from chuk_motion.models.artifact_models import ProviderType, StorageScope
from chuk_motion.utils.async_project_manager import AsyncProjectManager


@pytest.mark.asyncio
async def test_async_project_manager_create_project():
    """Test creating a project with AsyncProjectManager."""
    manager = AsyncProjectManager(provider_type=ProviderType.MEMORY)

    await manager.initialize()

    try:
        # Create project
        project = await manager.create_project(
            name="test_project",
            theme="tech",
            fps=30,
            width=1920,
            height=1080,
            scope=StorageScope.SESSION,
        )

        # Verify project was created
        assert project.namespace_info.namespace_id is not None
        assert project.metadata.project_name == "test_project"
        assert project.metadata.theme == "tech"
        assert project.metadata.fps == 30

        # Verify current project was set
        assert manager.current_project_id == project.namespace_info.namespace_id

        # Verify project files were created
        vfs = await manager.storage.get_project_vfs(project.namespace_info.namespace_id)

        # Check key files exist
        files = await vfs.ls("/")
        assert "package.json" in files
        assert "src" in files

        src_files = await vfs.ls("/src")
        assert "Root.tsx" in src_files
        assert "components" in src_files

    finally:
        await manager.cleanup()


@pytest.mark.asyncio
async def test_async_project_manager_with_checkpoints():
    """Test checkpoint functionality."""
    manager = AsyncProjectManager(provider_type=ProviderType.MEMORY)

    await manager.initialize()

    try:
        # Create project
        project = await manager.create_project(
            name="checkpoint_test",
            theme="tech",
            fps=30,
            width=1920,
            height=1080,
            scope=StorageScope.SESSION,
        )

        # Create checkpoint
        checkpoint = await manager.create_checkpoint(
            name="v1.0", description="Initial version"
        )

        assert checkpoint.checkpoint_id is not None
        assert checkpoint.name == "v1.0"
        assert checkpoint.namespace_id == project.namespace_info.namespace_id

    finally:
        await manager.cleanup()


@pytest.mark.asyncio
async def test_async_project_manager_get_project_info():
    """Test getting project info."""
    manager = AsyncProjectManager(provider_type=ProviderType.MEMORY)

    await manager.initialize()

    try:
        # Create project with timeline
        project = await manager.create_project(
            name="info_test",
            theme="tech",
            fps=30,
            width=1920,
            height=1080,
            scope=StorageScope.SESSION,
        )

        # Get project info
        info = await manager.get_project_info()

        assert info["name"] == "info_test"
        assert info["namespace_id"] == project.namespace_info.namespace_id
        assert "composition" in info
        assert info["composition"]["fps"] == 30

    finally:
        await manager.cleanup()
