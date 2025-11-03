#!/usr/bin/env python3
"""
Example: Generate a complete Remotion video

This example demonstrates the complete workflow for generating a video:
1. Create a project
2. Add components (title scene, lower thirds)
3. Generate TSX files
4. Instructions for rendering
"""
import asyncio
import json
import shutil
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_remotion.utils.project_manager import ProjectManager
from chuk_mcp_remotion.generator.composition_builder import CompositionBuilder


async def main():
    """Generate a complete video project."""
    print("\n" + "="*70)
    print("REMOTION VIDEO GENERATION EXAMPLE")
    print("="*70)

    # Initialize project manager
    manager = ProjectManager()
    project_name = "ai_explainer_video"

    # Clean up existing project if it exists
    project_path = manager.workspace_dir / project_name
    if project_path.exists():
        print(f"\n🔄 Removing existing project: {project_name}")
        shutil.rmtree(project_path)

    # Step 1: Create project
    print(f"\n📁 Step 1: Creating {project_name} project...")
    project = manager.create_project(
        name=project_name,
        theme="tech",
        fps=30,
        width=1920,
        height=1080
    )
    print(f"✓ Project created: {project['name']}")
    print(f"  Path: {project['path']}")
    print(f"  Theme: {project['theme']}")
    print(f"  Resolution: {project['resolution']}")

    # Step 2: Add title scene
    print("\n🎬 Step 2: Adding title scene...")
    manager.current_composition.add_title_scene(
        text="The Future of AI",
        subtitle="How AI is transforming technology",
        duration_seconds=3.0,
        variant="bold",
        animation="fade_zoom"
    )
    print("✓ Title scene added")
    print("  Duration: 3.0 seconds")
    print("  Animation: fade_zoom")

    # Step 3: Add lower thirds
    print("\n📋 Step 3: Adding lower thirds...")

    # Lower third at 0.5 seconds
    manager.current_composition.add_lower_third(
        name="Dr. Sarah Chen",
        title="AI Researcher, Stanford University",
        start_time=0.5,
        duration=4.0,
        variant="glass",
        position="bottom_left"
    )
    print("✓ Lower third #1 added")
    print("  Name: Dr. Sarah Chen")
    print("  Start: 0.5s, Duration: 4.0s")

    # Lower third at 5.0 seconds
    manager.current_composition.add_lower_third(
        name="Machine Learning",
        title="Transforming Industries",
        start_time=5.0,
        duration=3.0,
        variant="bold",
        position="bottom_center"
    )
    print("✓ Lower third #2 added")
    print("  Text: Machine Learning")
    print("  Start: 5.0s, Duration: 3.0s")

    # Step 4: Get composition info
    print("\n📊 Step 4: Composition summary...")
    info = manager.get_project_info()
    composition = info['composition']

    print(f"  Total duration: {composition['duration_seconds']:.1f} seconds")
    print(f"  Total frames: {composition['duration_frames']}")
    print(f"  Components: {len(composition['components'])}")

    print("\n  Timeline:")
    for comp in composition['components']:
        print(f"    • {comp['type']}: {comp['start_time']:.1f}s - {comp['start_time'] + comp['duration']:.1f}s")

    # Step 5: Generate TSX files
    print("\n⚙️  Step 5: Generating TSX components...")

    # Generate TitleScene component
    title_component = next(
        c for c in manager.current_composition.components
        if c.component_type == "TitleScene"
    )
    title_file = manager.add_component_to_project(
        "TitleScene",
        title_component.props,
        manager.current_composition.theme
    )
    print(f"✓ Generated: {Path(title_file).name}")

    # Generate LowerThird component
    lower_third_component = next(
        c for c in manager.current_composition.components
        if c.component_type == "LowerThird"
    )
    lower_third_file = manager.add_component_to_project(
        "LowerThird",
        lower_third_component.props,
        manager.current_composition.theme
    )
    print(f"✓ Generated: {Path(lower_third_file).name}")

    # Generate main composition
    print("\n📝 Step 6: Generating VideoComposition.tsx...")
    composition_file = manager.generate_composition()
    print(f"✓ Generated: {Path(composition_file).name}")

    # Step 7: Show next steps
    print("\n" + "="*70)
    print("🎉 VIDEO PROJECT GENERATED SUCCESSFULLY!")
    print("="*70)

    print(f"\nProject location: {project['path']}")
    print("\nNext steps to preview and render your video:")
    print("\n1. Install dependencies:")
    print(f"   cd {project['path']}")
    print("   npm install")

    print("\n2. Preview in Remotion Studio:")
    print("   npm start")
    print("   (Opens browser at http://localhost:3000)")

    print("\n3. Render video to MP4:")
    print("   npm run build")
    print("   (Generates video in ./out/ directory)")

    print("\n4. Custom render options:")
    print("   npx remotion render src/index.ts ai_explainer_video out/video.mp4")

    print("\n" + "="*70)
    print("\n✨ Your AI-powered video is ready to render!\n")


if __name__ == "__main__":
    asyncio.run(main())
