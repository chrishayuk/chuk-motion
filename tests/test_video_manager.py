"""Tests for VideoManager."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from chuk_motion.video_manager import (
    ComponentResponse,
    ProjectResponse,
    RenderResult,
    VideoInfo,
    VideoManager,
    VideoMetadata,
)


class TestVideoMetadata:
    """Test VideoMetadata Pydantic model."""

    def test_video_metadata_creation(self):
        """Test creating VideoMetadata."""
        metadata = VideoMetadata(
            project_name="test_project",
            theme="tech",
            fps=30,
            width=1920,
            height=1080,
            total_duration_seconds=60.0,
            component_count=5,
        )

        assert metadata.project_name == "test_project"
        assert metadata.theme == "tech"
        assert metadata.fps == 30
        assert metadata.width == 1920
        assert metadata.height == 1080
        assert metadata.total_duration_seconds == 60.0
        assert metadata.component_count == 5

    def test_video_metadata_defaults(self):
        """Test VideoMetadata default values."""
        metadata = VideoMetadata(project_name="test")

        assert metadata.theme == "tech"
        assert metadata.fps == 30
        assert metadata.width == 1920
        assert metadata.height == 1080
        assert metadata.total_duration_seconds == 0.0
        assert metadata.component_count == 0


class TestVideoInfo:
    """Test VideoInfo Pydantic model."""

    def test_video_info_creation(self):
        """Test creating VideoInfo."""
        metadata = VideoMetadata(project_name="test")
        info = VideoInfo(
            name="test",
            namespace_id="ns_123",
            artifact_uri="artifact://test",
            metadata=metadata,
        )

        assert info.name == "test"
        assert info.namespace_id == "ns_123"
        assert info.artifact_uri == "artifact://test"
        assert info.metadata.project_name == "test"


class TestRenderResult:
    """Test RenderResult Pydantic model."""

    def test_render_result_success(self):
        """Test successful RenderResult."""
        result = RenderResult(
            success=True,
            render_id="render_123",
            output_path="/path/to/output.mp4",
            format="mp4",
            resolution="1920x1080",
            fps=30,
            duration_seconds=60.0,
            file_size_bytes=10000000,
        )

        assert result.success is True
        assert result.render_id == "render_123"
        assert result.error is None

    def test_render_result_failure(self):
        """Test failed RenderResult."""
        result = RenderResult(
            success=False,
            error="Render failed",
        )

        assert result.success is False
        assert result.error == "Render failed"


class TestComponentResponse:
    """Test ComponentResponse Pydantic model."""

    def test_component_response_creation(self):
        """Test creating ComponentResponse."""
        response = ComponentResponse(
            component="title_scene",
            start_time=0.0,
            duration=3.0,
        )

        assert response.component == "title_scene"
        assert response.start_time == 0.0
        assert response.duration == 3.0


class TestProjectResponse:
    """Test ProjectResponse Pydantic model."""

    def test_project_response_creation(self):
        """Test creating ProjectResponse."""
        response = ProjectResponse(
            name="test_project",
            path="local://test",
            namespace_id="ns_123",
            theme="tech",
            fps=30,
            width=1920,
            height=1080,
        )

        assert response.name == "test_project"
        assert response.path == "local://test"
        assert response.namespace_id == "ns_123"


class TestVideoManagerInitialization:
    """Test VideoManager initialization."""

    def test_default_initialization(self):
        """Test default initialization."""
        manager = VideoManager()

        assert manager.base_path == "videos"
        assert manager._builders == {}
        assert manager._metadata == {}
        assert manager._namespace_ids == {}
        assert manager._current_project is None

    def test_custom_base_path(self):
        """Test custom base path."""
        manager = VideoManager(base_path="custom/path")

        assert manager.base_path == "custom/path"


class TestVideoManagerSanitizeName:
    """Test name sanitization."""

    def test_sanitize_alphanumeric(self):
        """Test sanitizing alphanumeric name."""
        manager = VideoManager()

        assert manager._sanitize_name("test123") == "test123"

    def test_sanitize_with_special_chars(self):
        """Test sanitizing name with special characters."""
        manager = VideoManager()

        assert manager._sanitize_name("test/project") == "testproject"
        assert manager._sanitize_name("test..project") == "testproject"

    def test_sanitize_with_dashes_underscores(self):
        """Test sanitizing name with dashes and underscores."""
        manager = VideoManager()

        assert manager._sanitize_name("test-project") == "test-project"
        assert manager._sanitize_name("test_project") == "test_project"

    def test_sanitize_empty_name(self):
        """Test sanitizing empty name."""
        manager = VideoManager()

        assert manager._sanitize_name("") == "video"
        assert manager._sanitize_name("///") == "video"


class TestVideoManagerGetStore:
    """Test _get_store method."""

    def test_get_store_no_store(self):
        """Test getting store when none configured."""
        manager = VideoManager()

        # Mock the chuk_mcp_server module being imported
        mock_chuk_mcp = MagicMock()
        mock_chuk_mcp.has_artifact_store.return_value = False

        with patch.dict("sys.modules", {"chuk_mcp_server": mock_chuk_mcp}):
            store = manager._get_store()
            assert store is None

    def test_get_store_with_store(self):
        """Test getting store when configured."""
        manager = VideoManager()
        mock_store = MagicMock()

        mock_chuk_mcp = MagicMock()
        mock_chuk_mcp.has_artifact_store.return_value = True
        mock_chuk_mcp.get_artifact_store.return_value = mock_store

        with patch.dict("sys.modules", {"chuk_mcp_server": mock_chuk_mcp}):
            store = manager._get_store()
            assert store == mock_store


class TestVideoManagerProjectOperations:
    """Test project operations."""

    @pytest.mark.asyncio
    async def test_create_project(self):
        """Test creating a project."""
        manager = VideoManager()

        with patch.object(manager, "_save_to_store", return_value=None):
            result = await manager.create_project(
                name="test_project",
                theme="tech",
                fps=30,
                width=1920,
                height=1080,
            )

        assert result.name == "test_project"
        assert result.theme == "tech"
        assert result.fps == 30
        assert result.width == 1920
        assert result.height == 1080
        assert manager._current_project == "test_project"
        assert "test_project" in manager._builders
        assert "test_project" in manager._metadata

    @pytest.mark.asyncio
    async def test_create_project_sanitizes_name(self):
        """Test that create_project sanitizes the name."""
        manager = VideoManager()

        with patch.object(manager, "_save_to_store", return_value=None):
            result = await manager.create_project(name="test/project/../bad")

        assert result.name == "testprojectbad"

    def test_get_current_builder_none(self):
        """Test getting current builder when none set."""
        manager = VideoManager()

        assert manager.get_current_builder() is None

    def test_get_current_builder_exists(self):
        """Test getting current builder when set."""
        manager = VideoManager()
        manager._current_project = "test"
        manager._builders["test"] = MagicMock()

        builder = manager.get_current_builder()

        assert builder is not None

    def test_current_timeline_property(self):
        """Test current_timeline property."""
        manager = VideoManager()
        manager._current_project = "test"
        mock_builder = MagicMock()
        manager._builders["test"] = mock_builder

        assert manager.current_timeline == mock_builder

    def test_get_builder_by_name(self):
        """Test getting builder by name."""
        manager = VideoManager()
        mock_builder = MagicMock()
        manager._builders["test"] = mock_builder

        assert manager.get_builder("test") == mock_builder
        assert manager.get_builder("nonexistent") is None

    def test_get_metadata(self):
        """Test getting project metadata."""
        manager = VideoManager()
        metadata = VideoMetadata(project_name="test")
        manager._metadata["test"] = metadata
        manager._current_project = "test"

        assert manager.get_metadata() == metadata
        assert manager.get_metadata("test") == metadata
        assert manager.get_metadata("nonexistent") is None

    def test_list_projects(self):
        """Test listing projects."""
        manager = VideoManager()
        manager._metadata["project1"] = VideoMetadata(project_name="project1")
        manager._metadata["project2"] = VideoMetadata(project_name="project2")

        projects = manager.list_projects()

        assert len(projects) == 2
        names = [p.name for p in projects]
        assert "project1" in names
        assert "project2" in names


class TestVideoManagerNamespaceOperations:
    """Test namespace-related operations."""

    def test_get_namespace_id(self):
        """Test getting namespace ID."""
        manager = VideoManager()
        manager._namespace_ids["test"] = "ns_123"

        assert manager.get_namespace_id("test") == "ns_123"
        assert manager.get_namespace_id("nonexistent") is None

    def test_get_artifact_uri_with_namespace(self):
        """Test getting artifact URI when namespace exists."""
        manager = VideoManager()
        manager._namespace_ids["test"] = "ns_123"

        uri = manager.get_artifact_uri("test")

        assert uri == "artifact://chuk-motion/videos/test"

    def test_get_artifact_uri_without_namespace(self):
        """Test getting artifact URI when namespace doesn't exist."""
        manager = VideoManager()

        assert manager.get_artifact_uri("test") is None


class TestVideoManagerComponentAddition:
    """Test component addition."""

    def test_add_component_no_active_project(self):
        """Test adding component when no active project."""
        manager = VideoManager()

        with pytest.raises(ValueError, match="No active project"):
            manager.add_component("title_scene", duration=3.0)

    def test_add_component_unknown_type(self):
        """Test adding unknown component type."""
        manager = VideoManager()
        manager._current_project = "test"
        mock_builder = MagicMock(spec=[])  # No methods
        manager._builders["test"] = mock_builder

        with pytest.raises(ValueError, match="Unknown component type"):
            manager.add_component("unknown_component")

    def test_add_component_success(self):
        """Test successfully adding a component."""
        manager = VideoManager()
        manager._current_project = "test"
        mock_builder = MagicMock()
        mock_builder.get_total_duration_seconds.return_value = 0.0
        mock_builder.add_title_scene = MagicMock()
        manager._builders["test"] = mock_builder
        manager._metadata["test"] = VideoMetadata(project_name="test")

        # Update mock to return new duration after add
        mock_builder.get_total_duration_seconds.side_effect = [0.0, 3.0]

        result = manager.add_component("title_scene", duration=3.0, text="Hello")

        assert result.component == "title_scene"
        assert result.start_time == 0.0
        assert result.duration == 3.0
        mock_builder.add_title_scene.assert_called_once()


class TestVideoManagerVideoGeneration:
    """Test video generation."""

    @pytest.mark.asyncio
    async def test_generate_video_no_active_project(self):
        """Test generating video when no active project."""
        manager = VideoManager()

        with pytest.raises(ValueError, match="No active project"):
            await manager.generate_video()

    @pytest.mark.asyncio
    async def test_generate_video_project_not_found(self):
        """Test generating video for non-existent project."""
        manager = VideoManager()
        manager._current_project = "test"

        with pytest.raises(ValueError, match="Project not found"):
            await manager.generate_video()

    @pytest.mark.asyncio
    async def test_generate_video_success(self):
        """Test successful video generation."""
        manager = VideoManager()
        manager._current_project = "test"
        mock_builder = MagicMock()
        mock_builder.to_dict.return_value = {
            "fps": 30,
            "width": 1920,
            "height": 1080,
            "duration_frames": 90,
            "components": [{"type": "TitleScene"}],
        }
        manager._builders["test"] = mock_builder

        result = await manager.generate_video()

        assert result["status"] == "success"
        assert result["project"]["name"] == "test"
        assert result["composition"]["fps"] == 30


class TestVideoManagerDownloadUrl:
    """Test download URL generation."""

    @pytest.mark.asyncio
    async def test_get_download_url_no_store(self):
        """Test getting download URL when no store."""
        manager = VideoManager()

        with patch.object(manager, "_get_store", return_value=None):
            result = await manager.get_download_url("render_123")

        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_download_url_success(self):
        """Test successful download URL generation."""
        manager = VideoManager()
        mock_store = AsyncMock()
        mock_store.presign = AsyncMock(return_value="https://example.com/download")

        with patch.object(manager, "_get_store", return_value=mock_store):
            result = await manager.get_download_url("render_123", expires_in=3600)

        assert result["success"] is True
        assert result["url"] == "https://example.com/download"
        assert result["render_id"] == "render_123"
        assert result["expires_in"] == 3600


class TestVideoManagerStoreRender:
    """Test render storage."""

    @pytest.mark.asyncio
    async def test_store_render_no_store(self):
        """Test storing render when no store."""
        manager = VideoManager()

        with patch.object(manager, "_get_store", return_value=None):
            result = await manager.store_render(b"video data")

        assert "error" in result

    @pytest.mark.asyncio
    async def test_store_render_success(self):
        """Test successful render storage."""
        manager = VideoManager()
        manager._current_project = "test"
        mock_store = AsyncMock()
        mock_store.store = AsyncMock(return_value="artifact_123")

        with patch.object(manager, "_get_store", return_value=mock_store):
            result = await manager.store_render(
                video_data=b"fake video data",
                format="mp4",
                project_name="test",
            )

        assert result["success"] is True
        assert result["artifact_id"] == "artifact_123"
        assert result["format"] == "mp4"
        assert result["size_bytes"] == len(b"fake video data")


class TestVideoManagerSaveToStore:
    """Test _save_to_store method."""

    @pytest.mark.asyncio
    async def test_save_to_store_no_store(self):
        """Test saving to store when no store configured."""
        manager = VideoManager()

        with patch.object(manager, "_get_store", return_value=None):
            result = await manager._save_to_store("test")

        assert result is None

    @pytest.mark.asyncio
    async def test_save_to_store_creates_namespace(self):
        """Test saving to store creates namespace."""
        manager = VideoManager()
        mock_store = AsyncMock()
        mock_namespace_info = MagicMock()
        mock_namespace_info.namespace_id = "ns_123"
        mock_store.create_namespace = AsyncMock(return_value=mock_namespace_info)

        # Mock the chuk_mcp_server module
        mock_chuk_mcp = MagicMock()
        mock_chuk_mcp.NamespaceType = MagicMock()
        mock_chuk_mcp.StorageScope = MagicMock()

        with (
            patch.object(manager, "_get_store", return_value=mock_store),
            patch.dict("sys.modules", {"chuk_mcp_server": mock_chuk_mcp}),
        ):
            result = await manager._save_to_store("test")

        assert result == "ns_123"
        assert manager._namespace_ids["test"] == "ns_123"

    @pytest.mark.asyncio
    async def test_save_to_store_uses_existing_namespace(self):
        """Test saving to store uses existing namespace."""
        manager = VideoManager()
        manager._namespace_ids["test"] = "existing_ns"
        mock_store = MagicMock()

        with patch.object(manager, "_get_store", return_value=mock_store):
            result = await manager._save_to_store("test")

        assert result == "existing_ns"
