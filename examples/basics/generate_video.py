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
import shutil
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_motion.generator.composition_builder import ComponentInstance
from chuk_motion.utils.project_manager import ProjectManager


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

    # Step 2: Add title scene to main track (auto-stacks at frame 0)
    print("\n🎬 Step 2: Adding title scene to main track...")
    title = ComponentInstance(
        component_type="TitleScene",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "The Future of AI",
            "subtitle": "How AI is transforming technology",
            "variant": "bold",
            "animation": "fade_zoom"
        },
        layer=0
    )
    manager.current_timeline.add_component(title, duration=3.0, track="main")
    print("✓ Title scene added to main track")
    print("  Duration: 3.0 seconds")
    print("  Animation: fade_zoom")

    # Step 3: Add lower thirds to overlay track (layers on top)
    print("\n📋 Step 3: Adding lower thirds to overlay track...")

    # Lower third at 0.5 seconds (aligned to main track start + offset)
    lower_third_1 = ComponentInstance(
        component_type="LowerThird",
        start_frame=0,
        duration_frames=0,
        props={
            "name": "Dr. Sarah Chen",
            "title": "AI Researcher, Stanford University",
            "variant": "glass",
            "position": "bottom_left"
        },
        layer=10
    )
    manager.current_timeline.add_component(
        lower_third_1,
        duration=4.0,
        track="overlay",
        align_to="main",
        offset=0.5
    )
    print("✓ Lower third #1 added to overlay track")
    print("  Name: Dr. Sarah Chen")
    print("  Aligned to main track + 0.5s offset")

    # Lower third at 5.0 seconds (aligned to main track start + offset)
    lower_third_2 = ComponentInstance(
        component_type="LowerThird",
        start_frame=0,
        duration_frames=0,
        props={
            "name": "Machine Learning",
            "title": "Transforming Industries",
            "variant": "bold",
            "position": "bottom_center"
        },
        layer=10
    )
    manager.current_timeline.add_component(
        lower_third_2,
        duration=3.0,
        track="overlay",
        align_to="main",
        offset=5.0
    )
    print("✓ Lower third #2 added to overlay track")
    print("  Text: Machine Learning")
    print("  Aligned to main track + 5.0s offset")

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
        c for c in manager.current_timeline.get_all_components()
        if c.component_type == "TitleScene"
    )
    title_file = manager.add_component_to_project(
        "TitleScene",
        title_component.props,
        manager.current_timeline.theme
    )
    print(f"✓ Generated: {Path(title_file).name}")

    # Generate LowerThird component
    lower_third_component = next(
        c for c in manager.current_timeline.get_all_components()
        if c.component_type == "LowerThird"
    )
    lower_third_file = manager.add_component_to_project(
        "LowerThird",
        lower_third_component.props,
        manager.current_timeline.theme
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
