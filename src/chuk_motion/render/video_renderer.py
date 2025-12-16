"""
Video Renderer - Renders Remotion projects to MP4 using CLI.

This module handles:
1. Setting up node_modules (copy from cache or npm install)
2. Running npx remotion render to generate MP4
3. Returning render result with file info
4. Background rendering with status polling
"""

import asyncio
import logging
import shutil
import subprocess
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Pre-cached node_modules location (set in Dockerfile)
REMOTION_BASE_DIR = Path("/app/remotion-base")

# In-memory render job tracking
_render_jobs: dict[str, "RenderJob"] = {}


@dataclass
class RenderJob:
    """Tracks a background render job."""

    job_id: str
    project_name: str
    status: str  # "pending", "rendering", "completed", "failed"
    started_at: datetime
    completed_at: datetime | None = None
    progress: int = 0  # 0-100
    message: str | None = None  # Human-readable progress message
    output_path: Path | None = None
    artifact_id: str | None = None
    download_url: str | None = None
    error: str | None = None
    file_size_bytes: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


def get_render_job(job_id: str) -> RenderJob | None:
    """Get a render job by ID."""
    return _render_jobs.get(job_id)


def create_render_job(project_name: str) -> RenderJob:
    """Create a new render job."""
    job_id = str(uuid.uuid4())[:8]
    job = RenderJob(
        job_id=job_id,
        project_name=project_name,
        status="pending",
        started_at=datetime.now(),
    )
    _render_jobs[job_id] = job
    return job


def update_render_job(job_id: str, message: str | None = None, **kwargs) -> RenderJob | None:
    """
    Update a render job with progress information.

    Args:
        job_id: The job ID to update
        message: Optional progress message
        **kwargs: Fields to update on the job (progress, status, etc.)
    """
    job = _render_jobs.get(job_id)
    if job:
        # Update the message field
        if message is not None:
            job.message = message

        # Update other fields
        for key, value in kwargs.items():
            if hasattr(job, key):
                setattr(job, key, value)

    return job


async def render_video(
    project_dir: Path,
    composition_id: str,
    output_path: Path | None = None,
    timeout: int = 300,
    job_id: str | None = None,
) -> dict[str, Any]:
    """
    Render a Remotion project to MP4.

    Args:
        project_dir: Path to the Remotion project directory
        composition_id: The composition ID to render
        output_path: Path for the output MP4 file (default: project_dir/out/video.mp4)
        timeout: Timeout in seconds for npm install and render (default: 300)
        job_id: Optional job ID to update progress during render

    Returns:
        Dict with render result:
        - success: bool
        - output_path: str (if successful)
        - file_size_bytes: int (if successful)
        - error: str (if failed)
    """
    project_dir = Path(project_dir)
    output_path = project_dir / "out" / "video.mp4" if output_path is None else Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Set up node_modules - copy from cache if available, otherwise npm install
    try:
        await _setup_node_modules(project_dir, timeout)
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to set up node_modules: {str(e)}",
        }

    # Run remotion render with streaming output for progress
    logger.info(f"Rendering video to {output_path}")
    render_cmd = [
        "npx",
        "remotion",
        "render",
        "src/index.ts",  # Entry point with registerRoot
        composition_id,
        str(output_path),
    ]

    try:
        render = await _run_command_with_progress(
            render_cmd,
            project_dir,
            timeout=timeout,
            job_id=job_id,
        )

        if render["returncode"] != 0:
            return {
                "success": False,
                "error": f"Remotion render failed: {render['stderr']}",
                "stdout": render["stdout"],
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Render error: {str(e)}",
        }

    # Check output file
    if output_path.exists():
        file_size = output_path.stat().st_size
        logger.info(f"Video rendered: {output_path} ({file_size} bytes)")
        return {
            "success": True,
            "output_path": str(output_path),
            "file_size_bytes": file_size,
            "file_size_mb": round(file_size / (1024 * 1024), 2),
        }
    else:
        return {
            "success": False,
            "error": "Output file not created",
        }


async def _run_command_with_progress(
    cmd: list[str],
    cwd: Path,
    timeout: int = 300,
    job_id: str | None = None,
) -> dict[str, Any]:
    """
    Run a command asynchronously with progress updates.

    Parses Remotion render output to extract frame progress.

    Args:
        cmd: Command and arguments
        cwd: Working directory
        timeout: Timeout in seconds
        job_id: Optional job ID to update progress

    Returns:
        Dict with returncode, stdout, stderr
    """
    import re

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout_lines: list[str] = []
        stderr_lines: list[str] = []

        # Pattern to match Remotion progress output like "Rendered 50/100 frames"
        # or percentage patterns like "50%" or "(50%)"
        frame_pattern = re.compile(r"(\d+)/(\d+)")
        percent_pattern = re.compile(r"(\d+)%")

        async def read_stream(stream, lines_list, is_stderr=False):
            while True:
                line = await stream.readline()
                if not line:
                    break
                decoded = line.decode("utf-8", errors="replace").strip()
                lines_list.append(decoded)

                # Try to extract progress from output
                if job_id and decoded:
                    # Look for frame progress (e.g., "50/100")
                    frame_match = frame_pattern.search(decoded)
                    if frame_match:
                        current = int(frame_match.group(1))
                        total = int(frame_match.group(2))
                        if total > 0:
                            # Map frame progress to 40-80% range
                            render_progress = 40 + int((current / total) * 40)
                            update_render_job(
                                job_id,
                                progress=render_progress,
                                message=f"Rendering frame {current}/{total}...",
                            )
                    else:
                        # Look for percentage
                        percent_match = percent_pattern.search(decoded)
                        if percent_match:
                            pct = int(percent_match.group(1))
                            # Map percentage to 40-80% range
                            render_progress = 40 + int(pct * 0.4)
                            update_render_job(
                                job_id, progress=render_progress, message=f"Rendering {pct}%..."
                            )

        # Read both streams concurrently
        try:
            await asyncio.wait_for(
                asyncio.gather(
                    read_stream(process.stdout, stdout_lines),
                    read_stream(process.stderr, stderr_lines, is_stderr=True),
                ),
                timeout=timeout,
            )
        except TimeoutError:
            process.kill()
            return {
                "returncode": -1,
                "stdout": "\n".join(stdout_lines),
                "stderr": f"Command timed out after {timeout}s",
            }

        await process.wait()

        return {
            "returncode": process.returncode,
            "stdout": "\n".join(stdout_lines),
            "stderr": "\n".join(stderr_lines),
        }

    except Exception as e:
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
        }


async def _setup_node_modules(project_dir: Path, timeout: int = 300) -> None:
    """
    Set up node_modules for the project.

    Tries to copy from pre-cached location first (fast), falls back to npm install.

    Args:
        project_dir: Path to the Remotion project directory
        timeout: Timeout in seconds for npm install fallback
    """
    node_modules_target = project_dir / "node_modules"
    cached_node_modules = REMOTION_BASE_DIR / "node_modules"

    # Check if we have pre-cached node_modules (in Docker container)
    if cached_node_modules.exists():
        logger.info(f"Copying cached node_modules to {project_dir}")
        await asyncio.to_thread(
            shutil.copytree,
            cached_node_modules,
            node_modules_target,
            symlinks=True,
        )
        logger.info("Copied cached node_modules (fast path)")
    else:
        # Fall back to npm install (slow path, used locally)
        logger.info(f"Running npm install in {project_dir}")
        npm_install = await asyncio.to_thread(
            _run_command,
            ["npm", "install"],
            project_dir,
            timeout=timeout,
        )
        if npm_install["returncode"] != 0:
            raise RuntimeError(f"npm install failed: {npm_install['stderr']}")
        logger.info("npm install completed")


def _run_command(
    cmd: list[str],
    cwd: Path,
    timeout: int = 300,
) -> dict[str, Any]:
    """
    Run a command synchronously.

    Args:
        cmd: Command and arguments
        cwd: Working directory
        timeout: Timeout in seconds

    Returns:
        Dict with returncode, stdout, stderr
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": f"Command timed out after {timeout}s",
        }
    except Exception as e:
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
        }
