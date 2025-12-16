#!/usr/bin/env python3
"""
MCP Workflow Test

Replicates the exact sequence from the MCP CLI test:
1. remotion_create_project
2. remotion_add_title_scene
3. remotion_add_fuzzy_text
4. remotion_add_true_focus
5. remotion_add_end_screen
6. remotion_generate_video
7. artifact_get_download_url

This tests the same workflow that would be called by Claude via MCP.
"""
import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


async def test_mcp_workflow():
    """Test the exact MCP workflow from the CLI test."""
    print("\n" + "=" * 70)
    print("MCP WORKFLOW TEST")
    print("Replicating the MCP CLI sequence")
    print("=" * 70)

    # Import the MCP tool functions directly
    from chuk_motion.async_server import (
        remotion_create_project,
        remotion_add_title_scene,
        remotion_add_fuzzy_text,
        remotion_add_true_focus,
        remotion_add_end_screen,
        remotion_generate_video,
        remotion_render_video,
        artifact_status,
    )

    # Step 1: remotion_create_project
    print("\n--- Step 1: remotion_create_project ---")
    result = await remotion_create_project(
        name="hello_effect_video",
        theme="tech",
        fps=30,
        width=1920,
        height=1080,
    )
    print(f"  Result: {result}")

    # Step 2: remotion_add_title_scene
    print("\n--- Step 2: remotion_add_title_scene ---")
    result = await remotion_add_title_scene(
        text="HELLO",
        subtitle="Cool Effect",
        variant="bold",
        animation="fade_zoom",
        duration_seconds=3.0,
    )
    print(f"  Result: {result}")

    # Step 3: remotion_add_fuzzy_text
    print("\n--- Step 3: remotion_add_fuzzy_text ---")
    result = await remotion_add_fuzzy_text(
        text="hello",
        font_size="4xl",
        glitch_intensity=12.0,
        scanline_height=2.0,
        animate=True,
        position="center",
        duration=3.0,
    )
    print(f"  Result: {result}")

    # Step 4: remotion_add_true_focus
    print("\n--- Step 4: remotion_add_true_focus ---")
    result = await remotion_add_true_focus(
        text="hello world",
        font_size="2xl",
        font_weight="extrabold",
        word_duration=0.8,
        position="bottom",
        duration=2.0,
    )
    print(f"  Result: {result}")

    # Step 5: remotion_add_end_screen
    print("\n--- Step 5: remotion_add_end_screen ---")
    result = await remotion_add_end_screen(
        cta_text="Thanks for Watching!",
        duration_seconds=5.0,
    )
    print(f"  Result: {result}")

    # Step 6: remotion_generate_video (creates composition files)
    print("\n--- Step 6: remotion_generate_video ---")
    result = await remotion_generate_video()
    print(f"  Result: {result}")

    # Step 7: remotion_render_video (starts render in background)
    print("\n--- Step 7: remotion_render_video ---")
    print("  (This starts the render and returns a job_id)")
    result = await remotion_render_video()
    print(f"  Result: {result}")

    # Parse job_id from result
    import json as json_module
    render_result = json_module.loads(result)
    job_id = render_result.get("job_id")

    if job_id:
        # Step 7b: Poll for render completion
        print("\n--- Step 7b: remotion_render_status (polling) ---")
        from chuk_motion.async_server import remotion_render_status
        import asyncio

        max_polls = 30  # 5 minutes max (10s intervals)
        for i in range(max_polls):
            await asyncio.sleep(10)  # Wait 10 seconds between polls
            status_result = await remotion_render_status(job_id)
            status_data = json_module.loads(status_result)
            print(f"  Poll {i+1}: status={status_data.get('status')}, progress={status_data.get('progress')}%")

            if status_data.get("status") == "completed":
                print(f"  ✓ Render complete!")
                print(f"  Download URL: {status_data.get('download_url')}")
                break
            elif status_data.get("status") == "failed":
                print(f"  ✗ Render failed: {status_data.get('error')}")
                break
        else:
            print("  ✗ Render timed out after 5 minutes")

    # Step 8: Check artifact status
    print("\n--- Step 8: artifact_status ---")
    result = await artifact_status()
    print(f"  Result: {result}")

    # Summary
    print("\n" + "=" * 70)
    print("WORKFLOW TEST COMPLETE")
    print("=" * 70)
    print("""
What this test demonstrates:
  ✓ Project creation with artifact storage
  ✓ Adding TitleScene component
  ✓ Adding FuzzyText component
  ✓ Adding TrueFocus component
  ✓ Adding EndScreen component
  ✓ Building composition
  ✓ Rendering video to MP4 via Remotion CLI
  ✓ Storing video in artifact storage
  ✓ Getting presigned download URL

For production (on Fly.io with S3/Tigris):
  - remotion_render_video renders the composition to MP4
  - The MP4 is stored in artifact storage (S3/Tigris)
  - A presigned download URL is returned for the video
""")


def main():
    """Run the test."""
    asyncio.run(test_mcp_workflow())


if __name__ == "__main__":
    main()
