#!/usr/bin/env python3
"""
End-to-End Artifacts Demo

Demonstrates the complete workflow for:
1. Creating a video project using artifact storage
2. Adding components and building the video composition
3. Rendering the video using Remotion
4. Storing the render as an artifact
5. Getting a presigned download URL

This example shows how chuk-motion handles video artifacts similar to
how chuk-mcp-pptx handles PowerPoint presentations.

Prerequisites:
- For download URLs: Set CHUK_ARTIFACTS_PROVIDER=s3 and configure S3/Tigris credentials
- For rendering: Node.js and npm installed (for Remotion CLI)

Usage:
    # Run with default memory storage (no download URLs)
    python examples/artifacts_e2e_demo.py

    # Run with S3 storage for download URLs
    CHUK_ARTIFACTS_PROVIDER=s3 python examples/artifacts_e2e_demo.py
"""
import asyncio
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_motion.models.artifact_models import ProviderType, StorageScope
from chuk_motion.utils.async_project_manager import AsyncProjectManager


async def demo_artifact_workflow():
    """
    Demonstrate the complete artifact workflow.

    This shows all the steps from project creation to getting a download URL,
    matching the capabilities of chuk-mcp-pptx.
    """
    print("\n" + "=" * 70)
    print("CHUK-MOTION END-TO-END ARTIFACTS DEMO")
    print("=" * 70)

    # Determine storage provider from environment
    storage_provider_env = os.environ.get("CHUK_MOTION_STORAGE_PROVIDER", "vfs-filesystem")
    try:
        storage_provider = ProviderType(storage_provider_env)
    except ValueError:
        print(f"Invalid storage provider '{storage_provider_env}', defaulting to vfs-filesystem")
        storage_provider = ProviderType.FILESYSTEM

    print(f"\nStorage Provider: {storage_provider.value}")

    # Check for S3 configuration
    has_s3 = (
        os.environ.get("CHUK_ARTIFACTS_PROVIDER") == "s3" or
        storage_provider == ProviderType.S3
    )
    if has_s3:
        print("Download URLs: ENABLED (S3/Tigris configured)")
    else:
        print("Download URLs: DISABLED (No S3 configuration)")
        print("  Set CHUK_ARTIFACTS_PROVIDER=s3 and configure S3 credentials for download URLs")

    # Create async project manager
    print("\n" + "-" * 70)
    print("STEP 1: Initialize Artifact Storage")
    print("-" * 70)

    project_manager = AsyncProjectManager(provider_type=storage_provider)
    await project_manager.initialize()
    print(f"  Initialized AsyncProjectManager with {storage_provider.value} provider")

    # Create a new project
    print("\n" + "-" * 70)
    print("STEP 2: Create a New Video Project")
    print("-" * 70)

    project_info = await project_manager.create_project(
        name="demo_video",
        theme="tech",
        fps=30,
        width=1920,
        height=1080,
        scope=StorageScope.SESSION,  # Temporary project
    )

    print(f"  Project Name: {project_info.metadata.project_name}")
    print(f"  Namespace ID: {project_info.namespace_info.namespace_id}")
    print(f"  Theme: {project_info.metadata.theme}")
    print(f"  Resolution: {project_info.metadata.width}x{project_info.metadata.height}")
    print(f"  FPS: {project_info.metadata.fps}")
    print(f"  Scope: {project_info.namespace_info.scope.value}")

    # Show project metadata
    print("\n" + "-" * 70)
    print("STEP 3: View Project Metadata")
    print("-" * 70)

    project = await project_manager.storage.get_project(
        project_info.namespace_info.namespace_id
    )
    print(f"  Created At: {project.metadata.created_at}")
    print(f"  Updated At: {project.metadata.updated_at}")
    print(f"  Component Count: {project.metadata.component_count}")
    print(f"  Total Duration: {project.metadata.total_duration_seconds}s")

    # Create a checkpoint
    print("\n" + "-" * 70)
    print("STEP 4: Create a Checkpoint (Version Snapshot)")
    print("-" * 70)

    checkpoint = await project_manager.create_checkpoint(
        name="v1.0",
        description="Initial project state"
    )
    print(f"  Checkpoint ID: {checkpoint.checkpoint_id}")
    print(f"  Name: {checkpoint.name}")
    print(f"  Description: {checkpoint.description}")
    print(f"  Created At: {checkpoint.created_at}")

    # List checkpoints
    print("\n" + "-" * 70)
    print("STEP 5: List All Checkpoints")
    print("-" * 70)

    checkpoints = await project_manager.storage.list_checkpoints(
        project_info.namespace_info.namespace_id
    )
    for cp in checkpoints:
        print(f"  - {cp.name}: {cp.description or 'No description'} ({cp.checkpoint_id})")

    # Simulate storing a render (using dummy video data)
    print("\n" + "-" * 70)
    print("STEP 6: Store a Rendered Video as Artifact")
    print("-" * 70)

    # Create dummy video data (in real usage, this would be the actual rendered video)
    # For demo purposes, we'll create a small MP4 header-like structure
    dummy_video_data = b"MOCK_MP4_VIDEO_DATA_" * 1000  # ~20KB dummy data

    render_info = await project_manager.storage.store_render(
        project_namespace_id=project_info.namespace_info.namespace_id,
        video_data=dummy_video_data,
        format="mp4",
        resolution="1920x1080",
        fps=30,
        duration_seconds=10.0,
        scope=StorageScope.SESSION,
        codec="h264",
        bitrate_kbps=5000,
    )

    render_id = render_info.namespace_info.namespace_id
    print(f"  Render ID: {render_id}")
    print(f"  Format: {render_info.metadata.format}")
    print(f"  Resolution: {render_info.metadata.resolution}")
    print(f"  Duration: {render_info.metadata.duration_seconds}s")
    print(f"  File Size: {render_info.metadata.file_size_bytes:,} bytes")
    print(f"  Checksum: {render_info.metadata.checksum[:16]}...")

    # Read back the render data
    print("\n" + "-" * 70)
    print("STEP 7: Read Back Render Data")
    print("-" * 70)

    retrieved_data = await project_manager.storage.read_render_data(render_id)
    print(f"  Retrieved {len(retrieved_data):,} bytes")
    print(f"  Data matches: {retrieved_data == dummy_video_data}")

    # Get render info - use the already retrieved render_info instead of calling get_render
    # (get_render may have issues with BLOB namespace metadata paths)
    print("\n" + "-" * 70)
    print("STEP 8: Get Render Metadata (from store_render response)")
    print("-" * 70)

    print(f"  Project Ref: {render_info.metadata.project_namespace_id}")
    print(f"  Codec: {render_info.metadata.codec}")
    print(f"  Bitrate: {render_info.metadata.bitrate_kbps} kbps")

    # Demonstrate presigned URL generation (if S3 is configured)
    print("\n" + "-" * 70)
    print("STEP 9: Generate Download URL (if S3 configured)")
    print("-" * 70)

    try:
        from chuk_mcp_server import get_artifact_store, has_artifact_store

        if has_artifact_store():
            store = get_artifact_store()

            # Store as artifact for presigned URL
            artifact_id = await store.store(
                data=dummy_video_data,
                mime="video/mp4",
                summary=f"video_{render_id}.mp4",
                meta={
                    "filename": f"video_{render_id}.mp4",
                    "render_id": render_id,
                    "format": "mp4",
                    "resolution": "1920x1080",
                },
            )
            print(f"  Artifact ID: {artifact_id}")

            # Generate presigned URL
            download_url = await store.presign(artifact_id, expires=3600)
            print(f"  Download URL: {download_url[:80]}...")
            print("  Expires In: 3600 seconds (1 hour)")
        else:
            print("  No artifact store configured for presigned URLs")
            print("  To enable download URLs:")
            print("    1. Set CHUK_ARTIFACTS_PROVIDER=s3")
            print("    2. Configure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
            print("    3. Set AWS_ENDPOINT_URL_S3 for Tigris: https://fly.storage.tigris.dev")
            print("    4. Set BUCKET_NAME for your S3 bucket")
    except ImportError:
        print("  chuk_mcp_server not available for presigned URLs")
    except Exception as e:
        print(f"  Error generating download URL: {e}")

    # Export as base64 (always available)
    print("\n" + "-" * 70)
    print("STEP 10: Export as Base64 (Always Available)")
    print("-" * 70)

    import base64
    b64_data = base64.b64encode(dummy_video_data).decode("utf-8")
    print(f"  Base64 Length: {len(b64_data):,} characters")
    print(f"  Data URI: data:video/mp4;base64,{b64_data[:50]}...")

    # Clean up (optional - SESSION scope will auto-cleanup)
    print("\n" + "-" * 70)
    print("STEP 11: Cleanup")
    print("-" * 70)

    await project_manager.cleanup()
    print("  Project manager cleaned up")
    print("  (SESSION-scoped artifacts will auto-delete after TTL)")

    # Summary
    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("""
This demo showed the complete artifact workflow:

1. Project Creation  - Create projects with artifact storage backend
2. Metadata Storage  - Track project info (theme, fps, resolution)
3. Checkpointing    - Create version snapshots for rollback
4. Render Storage   - Store rendered videos as artifacts
5. Data Retrieval   - Read back stored video data
6. Download URLs    - Generate presigned URLs (with S3/Tigris)
7. Base64 Export    - Always-available data export

For production use with download URLs:
  - Deploy to Fly.io with `fly deploy`
  - Configure Tigris S3 storage via secrets
  - Use artifact_get_download_url() MCP tool

See docs/artifact-mcp-tools.md for full API reference.
""")


async def demo_mcp_tool_simulation():
    """
    Simulate how the MCP tools would be called by Claude.

    This shows the JSON responses that Claude would receive.
    """
    print("\n" + "=" * 70)
    print("MCP TOOL SIMULATION")
    print("Simulating how Claude would interact with artifact tools")
    print("=" * 70)

    # Simulate artifact_create_project response
    create_response = {
        "success": True,
        "namespace_id": "ns_demo123",
        "name": "demo_video",
        "theme": "tech",
        "fps": 30,
        "resolution": "1920x1080",
        "scope": "session",
        "grid_path": "chuk-motion://projects/demo_video",
        "provider": "vfs-filesystem",
    }
    print("\n--- artifact_create_project Response ---")
    print(json.dumps(create_response, indent=2))

    # Simulate artifact_render_video response
    render_response = {
        "success": True,
        "composition_id": "demo-video",
        "format": "mp4",
        "quality": "high",
        "resolution": "1920x1080",
        "fps": 30,
        "duration_seconds": 10.0,
        "file_size_bytes": 1048576,
        "render_id": "ns_render456",
        "message": "Video rendered and stored as artifact",
    }
    print("\n--- artifact_render_video Response ---")
    print(json.dumps(render_response, indent=2))

    # Simulate artifact_get_download_url response
    download_response = {
        "success": True,
        "url": "https://fly.storage.tigris.dev/chuk-motion-artifacts/...",
        "render_id": "ns_render456",
        "artifact_id": "art_789",
        "expires_in": 3600,
        "filename": "video_ns_render456.mp4",
        "format": "mp4",
        "resolution": "1920x1080",
        "size_bytes": 1048576,
    }
    print("\n--- artifact_get_download_url Response ---")
    print(json.dumps(download_response, indent=2))

    # Simulate artifact_status response
    status_response = {
        "success": True,
        "artifact_store_available": True,
        "storage_provider": "s3",
        "current_project_id": "ns_demo123",
        "features": {
            "download_urls": True,
            "base64_export": True,
            "checkpoints": True,
            "render_storage": True,
        },
        "message": "Artifact store configured. Download URLs are available.",
    }
    print("\n--- artifact_status Response ---")
    print(json.dumps(status_response, indent=2))


def main():
    """Run the end-to-end demo."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    CHUK-MOTION ARTIFACTS DEMO                       ║
║                                                                      ║
║  This demo shows the complete video artifact workflow:               ║
║  • Project creation with artifact storage                            ║
║  • Checkpointing and versioning                                      ║
║  • Render storage and retrieval                                      ║
║  • Download URL generation (with S3)                                 ║
║                                                                      ║
║  Same pattern as chuk-mcp-pptx for PowerPoint artifacts!            ║
╚══════════════════════════════════════════════════════════════════════╝
""")

    # Run the artifact workflow demo
    asyncio.run(demo_artifact_workflow())

    # Also show MCP tool simulation
    asyncio.run(demo_mcp_tool_simulation())


if __name__ == "__main__":
    main()
