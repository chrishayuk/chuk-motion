"""Tests for RemotionRenderer - async-native rendering with Pydantic models."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from chuk_motion.rendering import RemotionRenderer, RenderProgress, RenderResult, VideoMetadata


class TestRenderProgress:
    """Test RenderProgress Pydantic model."""

    def test_render_progress_creation(self):
        """Test creating RenderProgress model."""
        progress = RenderProgress(
            current_frame=50,
            total_frames=100,
            percent_complete=50.0,
            status="rendering",
            message="Rendering frame 50/100",
        )

        assert progress.current_frame == 50
        assert progress.total_frames == 100
        assert progress.percent_complete == 50.0
        assert progress.status == "rendering"
        assert progress.message == "Rendering frame 50/100"

    def test_render_progress_defaults(self):
        """Test RenderProgress defaults."""
        progress = RenderProgress()

        assert progress.current_frame == 0
        assert progress.total_frames == 0
        assert progress.percent_complete == 0.0
        assert progress.status == "starting"
        assert progress.message == ""


class TestRenderResult:
    """Test RenderResult Pydantic model."""

    def test_render_result_success(self):
        """Test successful RenderResult."""
        result = RenderResult(
            success=True,
            output_path="/path/to/output.mp4",
            duration_seconds=30.0,
            file_size_bytes=5000000,
            resolution="1920x1080",
            fps=30,
        )

        assert result.success is True
        assert result.output_path == "/path/to/output.mp4"
        assert result.duration_seconds == 30.0
        assert result.file_size_bytes == 5000000
        assert result.resolution == "1920x1080"
        assert result.fps == 30
        assert result.error is None

    def test_render_result_failure(self):
        """Test failed RenderResult."""
        result = RenderResult(
            success=False,
            error="Render failed: timeout",
        )

        assert result.success is False
        assert result.error == "Render failed: timeout"
        assert result.output_path is None


class TestVideoMetadata:
    """Test VideoMetadata Pydantic model."""

    def test_video_metadata_creation(self):
        """Test creating VideoMetadata model."""
        metadata = VideoMetadata(
            resolution="1920x1080",
            fps=30,
            duration=60.5,
        )

        assert metadata.resolution == "1920x1080"
        assert metadata.fps == 30
        assert metadata.duration == 60.5

    def test_video_metadata_defaults(self):
        """Test VideoMetadata defaults."""
        metadata = VideoMetadata()

        assert metadata.resolution == ""
        assert metadata.fps == 0
        assert metadata.duration == 0.0


class TestRemotionRenderer:
    """Test RemotionRenderer class."""

    def test_renderer_initialization(self):
        """Test RemotionRenderer initialization."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            assert renderer.project_path == Path(temp_dir)
            assert renderer.process is None
            assert renderer._progress_callbacks == []

    def test_on_progress_callback_registration(self):
        """Test registering progress callbacks."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            callback1 = MagicMock()
            callback2 = MagicMock()

            renderer.on_progress(callback1)
            renderer.on_progress(callback2)

            assert len(renderer._progress_callbacks) == 2
            assert callback1 in renderer._progress_callbacks
            assert callback2 in renderer._progress_callbacks

    def test_parse_progress_frame_pattern(self):
        """Test parsing frame progress from Remotion output."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            # Test "frames X/Y" pattern
            line = "Rendering frames 45/150 (30%)"
            progress = renderer._parse_progress(line)

            assert progress is not None
            assert progress.current_frame == 45
            assert progress.total_frames == 150
            assert progress.percent_complete == 30.0
            assert progress.status == "rendering"

    def test_parse_progress_percentage_pattern(self):
        """Test parsing percentage from Remotion output."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            line = "Progress: 75%"
            progress = renderer._parse_progress(line)

            assert progress is not None
            assert progress.percent_complete == 75.0
            assert progress.status == "rendering"

    def test_parse_progress_stitching(self):
        """Test parsing stitching phase."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            line = "Stitching frames..."
            progress = renderer._parse_progress(line)

            assert progress is not None
            assert progress.percent_complete == 90.0
            assert progress.status == "stitching"

    def test_parse_progress_encoding(self):
        """Test parsing encoding phase."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            line = "Encoding video..."
            progress = renderer._parse_progress(line)

            assert progress is not None
            assert progress.percent_complete == 95.0
            assert progress.status == "encoding"

    def test_build_render_command(self):
        """Test building Remotion CLI command."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            cmd = renderer._build_render_command(
                composition_id="test-video",
                output_path="/path/to/output.mp4",
                format="mp4",
                quality="high",
                concurrency=8,
            )

            assert cmd[0] == "npx"
            assert cmd[1] == "remotion"
            assert cmd[2] == "render"
            assert cmd[3] == "test-video"
            assert cmd[4] == "/path/to/output.mp4"
            assert "--concurrency" in cmd
            assert "8" in cmd
            assert "--crf" in cmd
            assert "18" in cmd  # high quality
            assert "--preset" in cmd
            assert "slow" in cmd  # high quality preset

    def test_build_render_command_quality_presets(self):
        """Test different quality presets."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            # Test low quality
            cmd_low = renderer._build_render_command(
                composition_id="test",
                output_path="/out.mp4",
                format="mp4",
                quality="low",
                concurrency=4,
            )
            assert "28" in cmd_low  # low CRF
            assert "fast" in cmd_low  # fast preset

            # Test medium quality
            cmd_med = renderer._build_render_command(
                composition_id="test",
                output_path="/out.mp4",
                format="mp4",
                quality="medium",
                concurrency=4,
            )
            assert "23" in cmd_med  # medium CRF
            assert "medium" in cmd_med  # medium preset

            # Test high quality
            cmd_high = renderer._build_render_command(
                composition_id="test",
                output_path="/out.mp4",
                format="mp4",
                quality="high",
                concurrency=4,
            )
            assert "18" in cmd_high  # high CRF
            assert "slow" in cmd_high  # slow preset

    @pytest.mark.asyncio
    async def test_get_video_metadata_returns_pydantic_model(self):
        """Test that _get_video_metadata returns VideoMetadata Pydantic model."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            # Mock ffprobe output
            mock_stdout = b"""{
                "streams": [
                    {
                        "codec_type": "video",
                        "width": 1920,
                        "height": 1080,
                        "r_frame_rate": "30/1"
                    }
                ],
                "format": {
                    "duration": "45.5"
                }
            }"""

            mock_proc = AsyncMock()
            mock_proc.communicate = AsyncMock(return_value=(mock_stdout, b""))

            with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
                metadata = await renderer._get_video_metadata(Path("/fake/video.mp4"))

                # Verify it's a Pydantic model
                assert isinstance(metadata, VideoMetadata)
                assert metadata.resolution == "1920x1080"
                assert metadata.fps == 30
                assert metadata.duration == 45.5

    @pytest.mark.asyncio
    async def test_get_video_metadata_handles_errors(self):
        """Test that _get_video_metadata returns empty VideoMetadata on error."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            # Mock ffprobe failure
            mock_proc = AsyncMock()
            mock_proc.communicate = AsyncMock(side_effect=Exception("ffprobe failed"))

            with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
                metadata = await renderer._get_video_metadata(Path("/fake/video.mp4"))

                # Should return empty VideoMetadata (no dict!)
                assert isinstance(metadata, VideoMetadata)
                assert metadata.resolution == ""
                assert metadata.fps == 0
                assert metadata.duration == 0.0

    @pytest.mark.asyncio
    async def test_render_timeout_returns_pydantic_result(self):
        """Test that render timeout returns RenderResult Pydantic model."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            # Mock a process that hangs
            mock_proc = AsyncMock()
            mock_proc.wait = AsyncMock(side_effect=TimeoutError())
            mock_proc.returncode = None

            with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
                result = await renderer.render(
                    composition_id="test",
                    output_path=Path(temp_dir) / "output.mp4",
                    timeout=1,  # 1 second timeout
                )

                # Verify Pydantic model returned
                assert isinstance(result, RenderResult)
                assert result.success is False
                assert "timed out" in result.error.lower()

    @pytest.mark.asyncio
    async def test_kill_process(self):
        """Test killing the render process."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            # Mock a running process
            mock_proc = AsyncMock()
            mock_proc.returncode = None
            mock_proc.kill = MagicMock()
            mock_proc.wait = AsyncMock()

            renderer.process = mock_proc

            await renderer._kill_process()

            mock_proc.kill.assert_called_once()
            mock_proc.wait.assert_awaited_once()


class TestRemotionRendererIntegration:
    """Integration tests for RemotionRenderer (no external dependencies)."""

    @pytest.mark.asyncio
    async def test_progress_callback_invocation(self):
        """Test that progress callbacks are invoked during monitoring."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            # Track callback invocations
            callback_invocations = []

            def sync_callback(progress: RenderProgress):
                callback_invocations.append(progress)

            async def async_callback(progress: RenderProgress):
                callback_invocations.append(progress)

            renderer.on_progress(sync_callback)
            renderer.on_progress(async_callback)

            # Mock process with stdout
            mock_proc = AsyncMock()
            mock_stdout_lines = [
                b"Rendering frames 10/100 (10%)\n",
                b"Rendering frames 50/100 (50%)\n",
                b"Stitching frames...\n",
                b"",  # EOF
            ]

            async def mock_readline():
                if mock_stdout_lines:
                    return mock_stdout_lines.pop(0)
                return b""

            mock_proc.stdout = AsyncMock()
            mock_proc.stdout.readline = mock_readline

            renderer.process = mock_proc

            # Monitor progress
            await renderer._monitor_progress()

            # Verify callbacks were invoked
            # 3 progress updates × 2 callbacks = 6 invocations
            assert len(callback_invocations) == 6

            # Verify Pydantic models were passed
            for progress in callback_invocations:
                assert isinstance(progress, RenderProgress)


class TestRemotionRendererRender:
    """Test render method scenarios."""

    @pytest.mark.asyncio
    async def test_render_success(self):
        """Test successful render."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)
            output_path = Path(temp_dir) / "output.mp4"

            # Create fake output file
            output_path.write_bytes(b"fake video content")

            # Mock successful process
            mock_proc = AsyncMock()
            mock_proc.returncode = 0
            mock_proc.wait = AsyncMock()
            mock_proc.stdout = AsyncMock()
            mock_proc.stdout.readline = AsyncMock(return_value=b"")

            # Mock video metadata
            mock_metadata = VideoMetadata(resolution="1920x1080", fps=30, duration=10.0)

            with (
                patch("asyncio.create_subprocess_exec", return_value=mock_proc),
                patch.object(renderer, "_get_video_metadata", return_value=mock_metadata),
            ):
                result = await renderer.render(
                    composition_id="test",
                    output_path=output_path,
                )

                assert isinstance(result, RenderResult)
                assert result.success is True
                assert result.output_path == str(output_path)
                assert result.resolution == "1920x1080"
                assert result.fps == 30

    @pytest.mark.asyncio
    async def test_render_process_failure(self):
        """Test render when process returns non-zero exit code."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)
            output_path = Path(temp_dir) / "output.mp4"

            # Mock process that fails
            mock_proc = AsyncMock()
            mock_proc.returncode = 1
            mock_proc.wait = AsyncMock()
            mock_proc.stdout = AsyncMock()
            mock_proc.stdout.readline = AsyncMock(return_value=b"")
            mock_proc.stderr = AsyncMock()
            mock_proc.stderr.read = AsyncMock(return_value=b"Error: render failed")

            with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
                result = await renderer.render(
                    composition_id="test",
                    output_path=output_path,
                )

                assert isinstance(result, RenderResult)
                assert result.success is False
                assert "render failed" in result.error

    @pytest.mark.asyncio
    async def test_render_output_not_found(self):
        """Test render when output file is not created."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)
            output_path = Path(temp_dir) / "output.mp4"

            # Mock successful process but no output file
            mock_proc = AsyncMock()
            mock_proc.returncode = 0
            mock_proc.wait = AsyncMock()
            mock_proc.stdout = AsyncMock()
            mock_proc.stdout.readline = AsyncMock(return_value=b"")

            with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
                result = await renderer.render(
                    composition_id="test",
                    output_path=output_path,
                )

                assert isinstance(result, RenderResult)
                assert result.success is False
                assert "not found" in result.error.lower()

    @pytest.mark.asyncio
    async def test_render_exception_handling(self):
        """Test render exception handling."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)
            output_path = Path(temp_dir) / "output.mp4"

            with patch(
                "asyncio.create_subprocess_exec", side_effect=Exception("Process creation failed")
            ):
                result = await renderer.render(
                    composition_id="test",
                    output_path=output_path,
                )

                assert isinstance(result, RenderResult)
                assert result.success is False
                assert "Process creation failed" in result.error


class TestRemotionRendererMetadata:
    """Test video metadata extraction scenarios."""

    @pytest.mark.asyncio
    async def test_get_video_metadata_fps_without_fraction(self):
        """Test parsing fps without fraction format."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            # Mock ffprobe output with simple fps
            mock_stdout = b"""{
                "streams": [
                    {
                        "codec_type": "video",
                        "width": 1280,
                        "height": 720,
                        "r_frame_rate": "24"
                    }
                ],
                "format": {
                    "duration": "30.0"
                }
            }"""

            mock_proc = AsyncMock()
            mock_proc.communicate = AsyncMock(return_value=(mock_stdout, b""))

            with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
                metadata = await renderer._get_video_metadata(Path("/fake/video.mp4"))

                assert metadata.fps == 24

    @pytest.mark.asyncio
    async def test_get_video_metadata_no_video_stream(self):
        """Test handling missing video stream."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            # Mock ffprobe output with no video stream
            mock_stdout = b"""{
                "streams": [
                    {"codec_type": "audio"}
                ],
                "format": {}
            }"""

            mock_proc = AsyncMock()
            mock_proc.communicate = AsyncMock(return_value=(mock_stdout, b""))

            with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
                metadata = await renderer._get_video_metadata(Path("/fake/video.mp4"))

                assert metadata.resolution == "0x0"
                assert metadata.fps == 0


class TestRemotionRendererProgressMonitoring:
    """Test progress monitoring edge cases."""

    @pytest.mark.asyncio
    async def test_monitor_progress_no_process(self):
        """Test monitor progress with no process."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)
            renderer.process = None

            # Should not raise
            await renderer._monitor_progress()

    @pytest.mark.asyncio
    async def test_monitor_progress_callback_error(self):
        """Test progress monitoring with callback error."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            def failing_callback(progress):
                raise ValueError("Callback error")

            renderer.on_progress(failing_callback)

            # Mock process with stdout
            mock_proc = AsyncMock()
            mock_stdout_lines = [
                b"Rendering frames 10/100\n",
                b"",
            ]

            async def mock_readline():
                if mock_stdout_lines:
                    return mock_stdout_lines.pop(0)
                return b""

            mock_proc.stdout = AsyncMock()
            mock_proc.stdout.readline = mock_readline
            renderer.process = mock_proc

            # Should not raise, error is logged
            await renderer._monitor_progress()

    def test_parse_progress_no_match(self):
        """Test parsing progress with no matching pattern."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            line = "Random log message"
            progress = renderer._parse_progress(line)

            assert progress is None


class TestRemotionRendererKillProcess:
    """Test process killing scenarios."""

    @pytest.mark.asyncio
    async def test_kill_process_no_process(self):
        """Test killing when no process exists."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)
            renderer.process = None

            # Should not raise
            await renderer._kill_process()

    @pytest.mark.asyncio
    async def test_kill_process_already_finished(self):
        """Test killing an already finished process."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            mock_proc = AsyncMock()
            mock_proc.returncode = 0  # Already finished
            mock_proc.kill = MagicMock()
            mock_proc.wait = AsyncMock()

            renderer.process = mock_proc

            await renderer._kill_process()

            # kill should not be called on finished process
            mock_proc.kill.assert_not_called()

    @pytest.mark.asyncio
    async def test_kill_process_exception(self):
        """Test kill process exception handling."""
        with TemporaryDirectory() as temp_dir:
            renderer = RemotionRenderer(temp_dir)

            mock_proc = AsyncMock()
            mock_proc.returncode = None
            mock_proc.kill = MagicMock(side_effect=OSError("Kill failed"))
            mock_proc.wait = AsyncMock()

            renderer.process = mock_proc

            # Should not raise
            await renderer._kill_process()


# Summary: All tests verify Pydantic-native implementation
# - No dictionary goop (all models are BaseModel)
# - Type-safe with proper validation
# - Async-native (all I/O is async)
# - Clean error handling
