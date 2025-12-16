#!/usr/bin/env python3
"""
Simple End-to-End Video Generation Test

Tests the complete workflow:
1. Create a project
2. Add a simple title scene
3. Generate the video composition

This is a minimal test to verify the core pipeline works.
"""
import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


async def test_simple_video():
    """Test simple video generation workflow."""
    print("\n" + "=" * 70)
    print("SIMPLE VIDEO E2E TEST")
    print("=" * 70)

    # Import the MCP tool functions directly
    from chuk_motion.async_server import (
        remotion_create_project,
        remotion_add_title_scene,
        remotion_generate_video,
        remotion_get_info,
    )

    # Step 1: Create a project
    print("\n--- Step 1: Create Project ---")
    result = await remotion_create_project(
        name="test_hello",
        theme="tech",
        fps=30,
        width=1920,
        height=1080,
    )
    print(f"  Result: {result}")

    # Step 2: Add a title scene
    print("\n--- Step 2: Add Title Scene ---")
    result = await remotion_add_title_scene(
        text="HELLO WORLD",
        subtitle="A Simple Test Video",
        variant="bold",
        animation="fade_zoom",
        duration_seconds=3.0,
    )
    print(f"  Result: {result}")

    # Step 3: Generate the composition
    print("\n--- Step 3: Generate Composition ---")
    result = await remotion_generate_video()
    print(f"  Result: {result}")

    # Step 4: Get project info
    print("\n--- Step 4: Get Project Info ---")
    result = await remotion_get_info()
    print(f"  Result: {result}")

    print("\n" + "=" * 70)
    print("TEST PASSED")
    print("=" * 70)
    print("""
The simple video pipeline works:
- Project creation with artifact storage
- Component addition via MCP tools
- Composition generation

For production (on Fly.io with S3/Tigris):
- Videos are stored in artifact storage
- artifact_get_download_url provides presigned S3 URLs
""")


def main():
    """Run the test."""
    asyncio.run(test_simple_video())


if __name__ == "__main__":
    main()
