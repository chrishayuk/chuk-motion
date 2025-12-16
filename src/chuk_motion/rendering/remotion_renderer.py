"""
Remotion Renderer - Async subprocess management for Remotion CLI rendering.

Provides async-native rendering with progress tracking, error handling,
and automatic artifact storage integration.
"""

import asyncio
import json
import logging
import re
from pathlib import Path

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class RenderProgress(BaseModel):
    """Progress information from Remotion render."""

    current_frame: int = 0
    total_frames: int = 0
    percent_complete: float = 0.0
    status: str = "starting"
    message: str = ""


class RenderResult(BaseModel):
    """Result of a Remotion render operation."""

    success: bool
    output_path: str | None = None
    error: str | None = None
    duration_seconds: float = 0.0
    file_size_bytes: int = 0
    resolution: str = ""
    fps: int = 0


class VideoMetadata(BaseModel):
    """Video metadata from ffprobe."""

    resolution: str = ""
    fps: int = 0
    duration: float = 0.0


class RemotionRenderer:
    """
    Async-native Remotion CLI renderer.

    Handles subprocess management, progress tracking, and error handling
    for Remotion video rendering operations.
    """

    def __init__(self, project_path: str):
        """
        Initialize renderer for a project.

        Args:
            project_path: Path to the Remotion project directory
        """
        self.project_path = Path(project_path)
        self.process: asyncio.subprocess.Process | None = None
        self._progress_callbacks: list = []

    def on_progress(self, callback):
        """
        Register a progress callback.

        Args:
            callback: Function to call with RenderProgress updates
        """
        self._progress_callbacks.append(callback)

    async def render(
        self,
        composition_id: str,
        output_path: str | Path,
        format: str = "mp4",
        quality: str = "high",
        concurrency: int = 4,
        timeout: int = 600,
    ) -> RenderResult:
        """
        Render a Remotion composition.

        Args:
            composition_id: The composition ID to render
            output_path: Where to save the rendered video
            format: Output format (mp4, webm, etc.)
            quality: Quality preset (low, medium, high)
            concurrency: Number of concurrent render threads
            timeout: Maximum render time in seconds

        Returns:
            RenderResult with success status and metadata

        Example:
            renderer = RemotionRenderer("/path/to/project")
            result = await renderer.render(
                composition_id="my-video",
                output_path="/path/to/output.mp4",
                quality="high"
            )
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Build Remotion CLI command
        cmd = self._build_render_command(
            composition_id=composition_id,
            output_path=str(output_path),
            format=format,
            quality=quality,
            concurrency=concurrency,
        )

        logger.info(f"Starting render: {' '.join(cmd)}")

        try:
            # Start render process
            self.process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.project_path),
            )

            # Track progress
            render_task = asyncio.create_task(self._monitor_progress())

            # Wait for completion with timeout
            try:
                await asyncio.wait_for(self.process.wait(), timeout=timeout)
            except TimeoutError:
                logger.error(f"Render timed out after {timeout} seconds")
                await self._kill_process()
                return RenderResult(
                    success=False,
                    error=f"Render timed out after {timeout} seconds"
                )

            # Cancel progress monitoring
            render_task.cancel()
            from contextlib import suppress
            with suppress(asyncio.CancelledError):
                await render_task

            # Check result
            if self.process.returncode == 0:
                # Get output file metadata
                if output_path.exists():
                    file_size = output_path.stat().st_size

                    # Try to get video metadata from Remotion output
                    metadata = await self._get_video_metadata(output_path)

                    return RenderResult(
                        success=True,
                        output_path=str(output_path),
                        file_size_bytes=file_size,
                        resolution=metadata.resolution,
                        fps=metadata.fps,
                        duration_seconds=metadata.duration,
                    )
                else:
                    return RenderResult(
                        success=False,
                        error="Render completed but output file not found"
                    )
            else:
                # Get error from stderr
                error_msg = "Unknown render error"
                if self.process.stderr:
                    stderr = await self.process.stderr.read()
                    error_msg = stderr.decode() if stderr else "Unknown render error"
                logger.error(f"Render failed: {error_msg}")

                return RenderResult(
                    success=False,
                    error=error_msg
                )

        except Exception as e:
            logger.exception("Error during render")
            await self._kill_process()
            return RenderResult(
                success=False,
                error=str(e)
            )

    async def _monitor_progress(self):
        """Monitor render progress from stdout."""
        if not self.process or not self.process.stdout:
            return

        try:
            while True:
                line = await self.process.stdout.readline()
                if not line:
                    break

                line_str = line.decode().strip()
                if not line_str:
                    continue

                # Parse progress from Remotion CLI output
                progress = self._parse_progress(line_str)
                if progress:
                    # Notify callbacks
                    for callback in self._progress_callbacks:
                        try:
                            if asyncio.iscoroutinefunction(callback):
                                await callback(progress)
                            else:
                                callback(progress)
                        except Exception as e:
                            logger.exception(f"Progress callback error: {e}")

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.exception(f"Error monitoring progress: {e}")

    def _parse_progress(self, line: str) -> RenderProgress | None:
        """
        Parse progress from Remotion CLI output.

        Remotion outputs lines like:
        "Rendering frames 45/150 (30%)"
        "Stitching frames..."
        """
        # Match "frame X/Y" pattern
        frame_match = re.search(r'frame[s]?\s+(\d+)/(\d+)', line, re.IGNORECASE)
        if frame_match:
            current = int(frame_match.group(1))
            total = int(frame_match.group(2))
            percent = (current / total * 100) if total > 0 else 0

            return RenderProgress(
                current_frame=current,
                total_frames=total,
                percent_complete=percent,
                status="rendering",
                message=line
            )

        # Match percentage pattern
        percent_match = re.search(r'(\d+)%', line)
        if percent_match:
            percent = float(percent_match.group(1))
            return RenderProgress(
                percent_complete=percent,
                status="rendering",
                message=line
            )

        # Detect stitching phase
        if "stitch" in line.lower():
            return RenderProgress(
                percent_complete=90.0,
                status="stitching",
                message=line
            )

        # Detect encoding phase
        if "encod" in line.lower():
            return RenderProgress(
                percent_complete=95.0,
                status="encoding",
                message=line
            )

        return None

    def _build_render_command(
        self,
        composition_id: str,
        output_path: str,
        format: str,
        quality: str,
        concurrency: int,
    ) -> list[str]:
        """Build the Remotion CLI render command."""
        cmd = [
            "npx",
            "remotion",
            "render",
            composition_id,
            output_path,
            "--concurrency", str(concurrency),
        ]

        # Add quality settings
        quality_settings = {
            "low": {"crf": "28", "preset": "fast"},
            "medium": {"crf": "23", "preset": "medium"},
            "high": {"crf": "18", "preset": "slow"},
        }

        settings = quality_settings.get(quality, quality_settings["medium"])
        cmd.extend([
            "--crf", settings["crf"],
            "--preset", settings["preset"],
        ])

        return cmd

    async def _get_video_metadata(self, video_path: Path) -> VideoMetadata:
        """
        Get video metadata using ffprobe.

        Args:
            video_path: Path to video file

        Returns:
            VideoMetadata with resolution, fps, duration
        """
        try:
            # Use ffprobe to get metadata
            proc = await asyncio.create_subprocess_exec(
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(video_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, _ = await proc.communicate()
            data = json.loads(stdout.decode())

            # Extract video stream info
            video_stream: dict = next(
                (s for s in data.get("streams", []) if s.get("codec_type") == "video"),
                {}
            )

            width = video_stream.get("width", 0)
            height = video_stream.get("height", 0)
            fps_str = video_stream.get("r_frame_rate", "0/1")
            duration = float(data.get("format", {}).get("duration", 0.0))

            # Parse fps (format is "num/denom")
            if "/" in fps_str:
                num, denom = map(int, fps_str.split("/"))
                fps = int(num / denom) if denom > 0 else 0
            else:
                fps = int(float(fps_str))

            return VideoMetadata(
                resolution=f"{width}x{height}",
                fps=fps,
                duration=duration,
            )

        except Exception as e:
            logger.warning(f"Could not get video metadata: {e}")
            return VideoMetadata()

    async def _kill_process(self):
        """Kill the render process if running."""
        if self.process and self.process.returncode is None:
            try:
                self.process.kill()
                await self.process.wait()
            except Exception as e:
                logger.warning(f"Error killing process: {e}")
