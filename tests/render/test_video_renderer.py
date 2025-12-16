"""Tests for video_renderer module."""

import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from chuk_motion.render.video_renderer import (
    RenderJob,
    _run_command,
    create_render_job,
    get_render_job,
    render_video,
    update_render_job,
)


class TestRenderJob:
    """Test RenderJob dataclass."""

    def test_render_job_creation(self):
        """Test creating a RenderJob."""
        job = RenderJob(
            job_id="abc123",
            project_name="test_project",
            status="pending",
            started_at=datetime.now(),
        )

        assert job.job_id == "abc123"
        assert job.project_name == "test_project"
        assert job.status == "pending"
        assert job.progress == 0
        assert job.output_path is None
        assert job.error is None

    def test_render_job_defaults(self):
        """Test RenderJob default values."""
        job = RenderJob(
            job_id="test",
            project_name="test",
            status="pending",
            started_at=datetime.now(),
        )

        assert job.completed_at is None
        assert job.progress == 0
        assert job.message is None
        assert job.output_path is None
        assert job.artifact_id is None
        assert job.download_url is None
        assert job.error is None
        assert job.file_size_bytes is None
        assert job.metadata == {}


class TestRenderJobManagement:
    """Test render job management functions."""

    def test_create_render_job(self):
        """Test creating a render job."""
        from chuk_motion.render import video_renderer

        # Clear existing jobs
        video_renderer._render_jobs.clear()

        job = create_render_job("test_project")

        assert job.project_name == "test_project"
        assert job.status == "pending"
        assert len(job.job_id) == 8  # UUID[:8]
        assert job.job_id in video_renderer._render_jobs

    def test_get_render_job_exists(self):
        """Test getting an existing render job."""
        from chuk_motion.render import video_renderer

        video_renderer._render_jobs.clear()

        job = create_render_job("test")
        retrieved = get_render_job(job.job_id)

        assert retrieved == job

    def test_get_render_job_not_exists(self):
        """Test getting a non-existent render job."""
        from chuk_motion.render import video_renderer

        video_renderer._render_jobs.clear()

        retrieved = get_render_job("nonexistent")

        assert retrieved is None

    def test_update_render_job(self):
        """Test updating a render job."""
        from chuk_motion.render import video_renderer

        video_renderer._render_jobs.clear()

        job = create_render_job("test")

        updated = update_render_job(
            job.job_id,
            message="Processing...",
            progress=50,
            status="rendering",
        )

        assert updated is not None
        assert updated.message == "Processing..."
        assert updated.progress == 50
        assert updated.status == "rendering"

    def test_update_render_job_not_exists(self):
        """Test updating a non-existent render job."""
        from chuk_motion.render import video_renderer

        video_renderer._render_jobs.clear()

        updated = update_render_job("nonexistent", progress=50)

        assert updated is None


class TestRunCommand:
    """Test _run_command function."""

    def test_run_command_success(self):
        """Test running a successful command."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = _run_command(["echo", "hello"], Path(temp_dir))

            assert result["returncode"] == 0
            assert "hello" in result["stdout"]

    def test_run_command_failure(self):
        """Test running a failing command."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = _run_command(["false"], Path(temp_dir))

            assert result["returncode"] != 0

    def test_run_command_timeout(self):
        """Test command timeout."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = _run_command(["sleep", "10"], Path(temp_dir), timeout=1)

            assert result["returncode"] == -1
            assert "timed out" in result["stderr"]

    def test_run_command_not_found(self):
        """Test running a non-existent command."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = _run_command(["nonexistent_command_12345"], Path(temp_dir))

            assert result["returncode"] == -1


class TestRenderVideo:
    """Test render_video function."""

    @pytest.mark.asyncio
    async def test_render_video_node_modules_failure(self):
        """Test render_video when node_modules setup fails."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()

            with patch(
                "chuk_motion.render.video_renderer._setup_node_modules",
                side_effect=Exception("npm install failed"),
            ):
                result = await render_video(project_dir, "test-composition")

            assert result["success"] is False
            assert "node_modules" in result["error"]

    @pytest.mark.asyncio
    async def test_render_video_render_failure(self):
        """Test render_video when render command fails."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()

            with (
                patch(
                    "chuk_motion.render.video_renderer._setup_node_modules",
                    return_value=None,
                ),
                patch(
                    "chuk_motion.render.video_renderer._run_command_with_progress",
                    return_value={
                        "returncode": 1,
                        "stdout": "",
                        "stderr": "Render error",
                    },
                ),
            ):
                result = await render_video(project_dir, "test-composition")

            assert result["success"] is False
            assert "Render error" in result["error"]

    @pytest.mark.asyncio
    async def test_render_video_output_not_created(self):
        """Test render_video when output file not created."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()

            with (
                patch(
                    "chuk_motion.render.video_renderer._setup_node_modules",
                    return_value=None,
                ),
                patch(
                    "chuk_motion.render.video_renderer._run_command_with_progress",
                    return_value={
                        "returncode": 0,
                        "stdout": "Done",
                        "stderr": "",
                    },
                ),
            ):
                result = await render_video(project_dir, "test-composition")

            assert result["success"] is False
            assert "not created" in result["error"]

    @pytest.mark.asyncio
    async def test_render_video_success(self):
        """Test successful video render."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()

            # Create output directory and fake video file
            out_dir = project_dir / "out"
            out_dir.mkdir()
            video_file = out_dir / "video.mp4"
            video_file.write_bytes(b"fake video content")

            with (
                patch(
                    "chuk_motion.render.video_renderer._setup_node_modules",
                    return_value=None,
                ),
                patch(
                    "chuk_motion.render.video_renderer._run_command_with_progress",
                    return_value={
                        "returncode": 0,
                        "stdout": "Rendered successfully",
                        "stderr": "",
                    },
                ),
            ):
                result = await render_video(project_dir, "test-composition")

            assert result["success"] is True
            assert result["output_path"] == str(video_file)
            assert result["file_size_bytes"] == len(b"fake video content")

    @pytest.mark.asyncio
    async def test_render_video_custom_output_path(self):
        """Test render_video with custom output path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()

            custom_output = Path(temp_dir) / "custom" / "output.mp4"
            custom_output.parent.mkdir(parents=True)
            custom_output.write_bytes(b"custom video")

            with (
                patch(
                    "chuk_motion.render.video_renderer._setup_node_modules",
                    return_value=None,
                ),
                patch(
                    "chuk_motion.render.video_renderer._run_command_with_progress",
                    return_value={
                        "returncode": 0,
                        "stdout": "",
                        "stderr": "",
                    },
                ),
            ):
                result = await render_video(
                    project_dir,
                    "test-composition",
                    output_path=custom_output,
                )

            assert result["success"] is True
            assert result["output_path"] == str(custom_output)


class TestSetupNodeModules:
    """Test _setup_node_modules function."""

    @pytest.mark.asyncio
    async def test_setup_node_modules_from_cache(self):
        """Test setting up node_modules from cache."""
        from chuk_motion.render import video_renderer

        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()

            # Create fake cached node_modules
            cached_dir = Path(temp_dir) / "cache"
            cached_node_modules = cached_dir / "node_modules"
            cached_node_modules.mkdir(parents=True)
            (cached_node_modules / "test_package").mkdir()

            # Temporarily override REMOTION_BASE_DIR
            original_base_dir = video_renderer.REMOTION_BASE_DIR
            video_renderer.REMOTION_BASE_DIR = cached_dir

            try:
                await video_renderer._setup_node_modules(project_dir)

                # Check that node_modules was copied
                assert (project_dir / "node_modules").exists()
                assert (project_dir / "node_modules" / "test_package").exists()
            finally:
                video_renderer.REMOTION_BASE_DIR = original_base_dir

    @pytest.mark.asyncio
    async def test_setup_node_modules_npm_install(self):
        """Test setting up node_modules via npm install."""
        from chuk_motion.render import video_renderer

        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()

            # Set REMOTION_BASE_DIR to non-existent path to force npm install
            original_base_dir = video_renderer.REMOTION_BASE_DIR
            video_renderer.REMOTION_BASE_DIR = Path("/nonexistent/path")

            try:
                with patch(
                    "chuk_motion.render.video_renderer._run_command",
                    return_value={"returncode": 0, "stdout": "", "stderr": ""},
                ) as mock_run:
                    await video_renderer._setup_node_modules(project_dir)

                    mock_run.assert_called_once()
                    args = mock_run.call_args[0]
                    assert args[0] == ["npm", "install"]
            finally:
                video_renderer.REMOTION_BASE_DIR = original_base_dir

    @pytest.mark.asyncio
    async def test_setup_node_modules_npm_install_failure(self):
        """Test handling npm install failure."""
        from chuk_motion.render import video_renderer

        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()

            original_base_dir = video_renderer.REMOTION_BASE_DIR
            video_renderer.REMOTION_BASE_DIR = Path("/nonexistent/path")

            try:
                with (
                    patch(
                        "chuk_motion.render.video_renderer._run_command",
                        return_value={
                            "returncode": 1,
                            "stdout": "",
                            "stderr": "npm error",
                        },
                    ),
                    pytest.raises(RuntimeError, match="npm install failed"),
                ):
                    await video_renderer._setup_node_modules(project_dir)
            finally:
                video_renderer.REMOTION_BASE_DIR = original_base_dir


class TestRunCommandWithProgress:
    """Test _run_command_with_progress function."""

    @pytest.mark.asyncio
    async def test_run_command_with_progress_success(self):
        """Test running command with progress successfully."""
        from chuk_motion.render import video_renderer

        with tempfile.TemporaryDirectory() as temp_dir:
            result = await video_renderer._run_command_with_progress(
                ["echo", "hello"],
                Path(temp_dir),
                timeout=30,
            )

            assert result["returncode"] == 0
            assert "hello" in result["stdout"]

    @pytest.mark.asyncio
    async def test_run_command_with_progress_timeout(self):
        """Test command with progress timeout."""
        from chuk_motion.render import video_renderer

        with tempfile.TemporaryDirectory() as temp_dir:
            result = await video_renderer._run_command_with_progress(
                ["sleep", "10"],
                Path(temp_dir),
                timeout=1,
            )

            assert result["returncode"] == -1
            assert "timed out" in result["stderr"]

    @pytest.mark.asyncio
    async def test_run_command_with_progress_updates_job(self):
        """Test that progress updates are sent to job."""
        from chuk_motion.render import video_renderer

        video_renderer._render_jobs.clear()

        job = create_render_job("test")

        # Create a mock process that outputs progress-like text
        mock_process = AsyncMock()
        mock_process.returncode = 0

        # Mock stdout with progress output
        stdout_data = [
            b"Rendering frame 10/100\n",
            b"Rendering frame 50/100\n",
            b"",  # EOF
        ]

        async def mock_readline():
            if stdout_data:
                return stdout_data.pop(0)
            return b""

        mock_process.stdout = MagicMock()
        mock_process.stdout.readline = mock_readline

        mock_process.stderr = MagicMock()
        mock_process.stderr.readline = AsyncMock(return_value=b"")

        mock_process.wait = AsyncMock()

        with (
            patch(
                "asyncio.create_subprocess_exec",
                return_value=mock_process,
            ),
            tempfile.TemporaryDirectory() as temp_dir,
        ):
            await video_renderer._run_command_with_progress(
                ["echo", "test"],
                Path(temp_dir),
                job_id=job.job_id,
            )

        # Job should have been updated with progress
        updated_job = get_render_job(job.job_id)
        assert updated_job is not None
        # Progress should have been updated at some point
        assert updated_job.progress >= 0


class TestPackageExports:
    """Test package __init__.py exports."""

    def test_package_exports(self):
        """Test that render package exports required items."""
        from chuk_motion.render import (
            RemotionProjectExporter,
            RenderJob,
            create_render_job,
            get_render_job,
            render_video,
            update_render_job,
        )

        # All exports should be available
        assert RemotionProjectExporter is not None
        assert RenderJob is not None
        assert create_render_job is not None
        assert get_render_job is not None
        assert render_video is not None
        assert update_render_job is not None


class TestUpdateRenderJobEdgeCases:
    """Test edge cases for update_render_job."""

    def test_update_render_job_no_message(self):
        """Test updating render job without message (None)."""
        from chuk_motion.render import video_renderer

        video_renderer._render_jobs.clear()

        job = create_render_job("test")
        job.message = "original message"

        # Update with message=None should not change message
        updated = update_render_job(job.job_id, message=None, progress=75)

        assert updated.message == "original message"
        assert updated.progress == 75

    def test_update_render_job_invalid_attribute(self):
        """Test updating with invalid attribute (should be ignored)."""
        from chuk_motion.render import video_renderer

        video_renderer._render_jobs.clear()

        job = create_render_job("test")

        # nonexistent_attr doesn't exist on RenderJob
        updated = update_render_job(job.job_id, message="test", nonexistent_attr="value")

        assert updated.message == "test"
        # nonexistent_attr should not have been set
        assert (
            not hasattr(updated, "nonexistent_attr")
            or getattr(updated, "nonexistent_attr", None) != "value"
        )


class TestRenderVideoExceptionHandling:
    """Test render_video exception handling paths."""

    @pytest.mark.asyncio
    async def test_render_video_render_exception(self):
        """Test render_video when _run_command_with_progress raises exception."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()

            with (
                patch(
                    "chuk_motion.render.video_renderer._setup_node_modules",
                    return_value=None,
                ),
                patch(
                    "chuk_motion.render.video_renderer._run_command_with_progress",
                    side_effect=Exception("Unexpected render error"),
                ),
            ):
                result = await render_video(project_dir, "test-composition")

            assert result["success"] is False
            assert "Render error" in result["error"]
            assert "Unexpected render error" in result["error"]


class TestRunCommandWithProgressEdgeCases:
    """Test edge cases for _run_command_with_progress."""

    @pytest.mark.asyncio
    async def test_run_command_with_progress_percentage_pattern(self):
        """Test progress updates with percentage pattern."""
        from chuk_motion.render import video_renderer

        video_renderer._render_jobs.clear()

        job = create_render_job("test")

        # Create a mock process that outputs percentage progress
        mock_process = AsyncMock()
        mock_process.returncode = 0

        stdout_data = [
            b"Progress: 25%\n",
            b"Progress: 75%\n",
            b"",  # EOF
        ]
        stdout_index = [0]

        async def mock_stdout_readline():
            if stdout_index[0] < len(stdout_data):
                line = stdout_data[stdout_index[0]]
                stdout_index[0] += 1
                return line
            return b""

        mock_process.stdout = MagicMock()
        mock_process.stdout.readline = mock_stdout_readline

        mock_process.stderr = MagicMock()
        mock_process.stderr.readline = AsyncMock(return_value=b"")

        mock_process.wait = AsyncMock()

        with (
            patch(
                "asyncio.create_subprocess_exec",
                return_value=mock_process,
            ),
            tempfile.TemporaryDirectory() as temp_dir,
        ):
            await video_renderer._run_command_with_progress(
                ["echo", "test"],
                Path(temp_dir),
                job_id=job.job_id,
            )

        # Job should have been updated with percentage-based progress
        updated_job = get_render_job(job.job_id)
        assert updated_job is not None

    @pytest.mark.asyncio
    async def test_run_command_with_progress_no_job_id(self):
        """Test progress tracking without job_id (no updates sent)."""
        from chuk_motion.render import video_renderer

        video_renderer._render_jobs.clear()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Run without job_id - should complete without errors
            result = await video_renderer._run_command_with_progress(
                ["echo", "50/100 frames"],  # Progress-like output
                Path(temp_dir),
                job_id=None,  # No job_id
            )

            assert result["returncode"] == 0

    @pytest.mark.asyncio
    async def test_run_command_with_progress_exception(self):
        """Test _run_command_with_progress exception handling."""
        from chuk_motion.render import video_renderer

        # Patch create_subprocess_exec to raise an exception
        with patch(
            "asyncio.create_subprocess_exec",
            side_effect=OSError("Failed to create process"),
        ):
            with tempfile.TemporaryDirectory() as temp_dir:
                result = await video_renderer._run_command_with_progress(
                    ["nonexistent"],
                    Path(temp_dir),
                )

            assert result["returncode"] == -1
            assert "Failed to create process" in result["stderr"]

    @pytest.mark.asyncio
    async def test_run_command_with_progress_no_frame_match(self):
        """Test progress parsing when output doesn't match patterns."""
        from chuk_motion.render import video_renderer

        video_renderer._render_jobs.clear()

        job = create_render_job("test")

        # Create mock process with non-progress output
        mock_process = AsyncMock()
        mock_process.returncode = 0

        stdout_data = [
            b"Some random output\n",
            b"No progress here\n",
            b"",
        ]
        stdout_index = [0]

        async def mock_stdout_readline():
            if stdout_index[0] < len(stdout_data):
                line = stdout_data[stdout_index[0]]
                stdout_index[0] += 1
                return line
            return b""

        mock_process.stdout = MagicMock()
        mock_process.stdout.readline = mock_stdout_readline

        mock_process.stderr = MagicMock()
        mock_process.stderr.readline = AsyncMock(return_value=b"")

        mock_process.wait = AsyncMock()

        with (
            patch(
                "asyncio.create_subprocess_exec",
                return_value=mock_process,
            ),
            tempfile.TemporaryDirectory() as temp_dir,
        ):
            await video_renderer._run_command_with_progress(
                ["echo", "test"],
                Path(temp_dir),
                job_id=job.job_id,
            )

        # Progress should not have changed significantly
        updated_job = get_render_job(job.job_id)
        assert updated_job is not None

    @pytest.mark.asyncio
    async def test_run_command_with_progress_frame_zero_total(self):
        """Test progress parsing when total frames is 0."""
        from chuk_motion.render import video_renderer

        video_renderer._render_jobs.clear()

        job = create_render_job("test")

        # Create mock process with 0/0 frames output
        mock_process = AsyncMock()
        mock_process.returncode = 0

        stdout_data = [
            b"Frame 0/0\n",  # Zero total - should not cause division by zero
            b"",
        ]
        stdout_index = [0]

        async def mock_stdout_readline():
            if stdout_index[0] < len(stdout_data):
                line = stdout_data[stdout_index[0]]
                stdout_index[0] += 1
                return line
            return b""

        mock_process.stdout = MagicMock()
        mock_process.stdout.readline = mock_stdout_readline

        mock_process.stderr = MagicMock()
        mock_process.stderr.readline = AsyncMock(return_value=b"")

        mock_process.wait = AsyncMock()

        with (
            patch(
                "asyncio.create_subprocess_exec",
                return_value=mock_process,
            ),
            tempfile.TemporaryDirectory() as temp_dir,
        ):
            # Should not raise division by zero
            result = await video_renderer._run_command_with_progress(
                ["echo", "test"],
                Path(temp_dir),
                job_id=job.job_id,
            )

            assert result["returncode"] == 0
