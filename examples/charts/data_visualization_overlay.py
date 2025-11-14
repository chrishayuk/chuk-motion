#!/usr/bin/env python3
"""
Data Visualization Overlay Example

Demonstrates animated line charts with transparent backgrounds,
perfect for overlaying on top of video content.
"""
import asyncio
import shutil
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_motion.utils.project_manager import ProjectManager
from chuk_motion.generator.composition_builder import CompositionBuilder


async def main():
    """Generate a data visualization overlay video."""
    print("\n" + "="*70)
    print("DATA VISUALIZATION OVERLAY EXAMPLE")
    print("="*70)

    # Initialize project manager
    manager = ProjectManager()
    project_name = "data_viz_overlay"

    # Clean up existing project if it exists
    project_path = manager.workspace_dir / project_name
    if project_path.exists():
        print(f"\n🔄 Removing existing project: {project_name}")
        shutil.rmtree(project_path)

    # Step 1: Create project with transparent background
    print(f"\n📊 Step 1: Creating {project_name} project...")
    project = manager.create_project(
        name=project_name,
        theme="tech",
        fps=30,
        width=1920,
        height=1080
    )
    print(f"✓ Project created: {project['name']}")
    print(f"  Theme: {project['theme']}")
    print(f"  Resolution: {project['resolution']}")

    # Use transparent background for overlays
    manager.current_composition = CompositionBuilder(
        fps=30,
        width=1920,
        height=1080,
        transparent=True  # Key feature: transparent background!
    )
    manager.current_composition.theme = "tech"

    print("\n  🎨 Using TRANSPARENT background for video overlay")

    # Step 2: Add sample data for different metrics
    print("\n📈 Step 2: Adding animated line charts...")

    # Chart 1: Revenue growth (appears at 0s)
    revenue_data = [
        [1, 10000],
        [2, 15000],
        [3, 18000],
        [4, 25000],
        [5, 35000],
        [6, 42000],
        [7, 55000],
        [8, 68000]
    ]

    manager.current_composition.add_line_chart(
        data=revenue_data,
        title="Monthly Revenue Growth",
        xlabel="Month",
        ylabel="Revenue ($)",
        start_time=0.5,
        duration=4.0
    )
    print("✓ Chart #1: Revenue Growth")
    print("  Data points: 8")
    print("  Duration: 4.0s")
    print("  Animation: Line draws from left to right")

    # Chart 2: User engagement (appears at 5s)
    engagement_data = [
        [1, 45],
        [2, 52],
        [3, 48],
        [4, 65],
        [5, 72],
        [6, 78],
        [7, 85],
        [8, 92]
    ]

    manager.current_composition.add_line_chart(
        data=engagement_data,
        title="User Engagement Score",
        xlabel="Week",
        ylabel="Score",
        start_time=5.0,
        duration=4.0
    )
    print("\n✓ Chart #2: User Engagement")
    print("  Data points: 8")
    print("  Duration: 4.0s")
    print("  Start time: 5.0s")

    # Chart 3: Performance metrics (appears at 10s)
    performance_data = [
        [0, 120],
        [1, 115],
        [2, 95],
        [3, 85],
        [4, 75],
        [5, 65],
        [6, 58],
        [7, 52]
    ]

    manager.current_composition.add_line_chart(
        data=performance_data,
        title="Page Load Time Improvement",
        xlabel="Sprint",
        ylabel="Load Time (ms)",
        start_time=10.0,
        duration=4.0
    )
    print("\n✓ Chart #3: Performance Metrics")
    print("  Data points: 8")
    print("  Duration: 4.0s")
    print("  Start time: 10.0s")

    # Add text overlays for context
    print("\n💬 Step 3: Adding contextual lower thirds...")

    manager.current_composition.add_lower_third(
        name="Q4 2024 Performance",
        title="Data-Driven Insights",
        start_time=1.0,
        duration=3.0,
        variant="glass",
        position="bottom_left"
    )
    print("✓ Lower third added at 1.0s")

    # Step 3: Get composition info
    print("\n📊 Step 4: Composition summary...")
    info = manager.get_project_info()
    composition = info['composition']

    print(f"  Total duration: {composition['duration_seconds']:.1f} seconds")
    print(f"  Total frames: {composition['duration_frames']}")
    print(f"  Components: {len(composition['components'])}")
    print(f"  Background: TRANSPARENT (for overlay)")

    print("\n  Timeline:")
    for comp in composition['components']:
        comp_type = comp['type']
        start = comp['start_time']
        end = comp['start_time'] + comp['duration']
        if comp_type == "LineChart":
            title = comp['props'].get('title', 'Chart')
            print(f"    📈 {title}: {start:.1f}s - {end:.1f}s")
        else:
            print(f"    • {comp_type}: {start:.1f}s - {end:.1f}s")

    # Step 4: Generate TSX files
    print("\n⚙️  Step 5: Generating TSX components...")

    # Generate LineChart component
    chart_component = next(
        c for c in manager.current_composition.components
        if c.component_type == "LineChart"
    )
    chart_file = manager.add_component_to_project(
        "LineChart",
        chart_component.props,
        manager.current_composition.theme
    )
    print(f"✓ Generated: {Path(chart_file).name}")

    # Generate LowerThird if present
    if any(c.component_type == "LowerThird" for c in manager.current_composition.components):
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
    print("  Background: transparent (ready for overlay)")

    # Step 5: Show next steps
    print("\n" + "="*70)
    print("🎉 DATA VISUALIZATION OVERLAY GENERATED!")
    print("="*70)

    print(f"\nProject location: {project['path']}")

    print("\n✨ Key Features:")
    print("  • Transparent background (perfect for overlays)")
    print("  • Animated line charts with gradient colors")
    print("  • Sequential chart appearances")
    print("  • Tech theme with blue/cyan gradients")

    print("\nNext steps:")
    print("\n1. Install dependencies:")
    print(f"   cd {project['path']}")
    print("   npm install")

    print("\n2. Preview in Remotion Studio:")
    print("   npm start")
    print("   (Check 'Transparent' option to see transparency)")

    print("\n3. Render with transparency:")
    print("   npx remotion render src/index.ts data-viz-overlay out/overlay.mov \\")
    print("     --codec prores \\")
    print("     --prores-profile 4444 \\")
    print("     --image-format png")
    print("   (ProRes 4444 supports alpha channel)")

    print("\n4. Use as overlay:")
    print("   • Import the rendered video in your video editor")
    print("   • Place it on top of your main video track")
    print("   • The transparent background allows your video to show through")
    print("   • Charts and text appear as overlays")

    print("\n💡 Use Cases:")
    print("  • Financial presentations")
    print("  • Data-driven storytelling")
    print("  • Educational content")
    print("  • Business reports")
    print("  • Tech demos with metrics")

    print("\n" + "="*70)
    print("\n✨ Your transparent data visualization overlay is ready!\n")


if __name__ == "__main__":
    asyncio.run(main())
