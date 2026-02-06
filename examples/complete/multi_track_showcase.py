#!/usr/bin/env python3
"""
Multi-Track Timeline Showcase

This example demonstrates the new track-based timeline system:
- Multiple independent tracks (main, overlay, background, custom)
- Auto-stacking components within tracks
- Track alignment and synchronization
- Parallel and sequential composition
- No manual frame calculations needed!
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
    """Generate a multi-track video showcasing the timeline system."""
    print("\n" + "="*80)
    print("MULTI-TRACK TIMELINE SHOWCASE")
    print("="*80)
    print("\nDemonstrating:")
    print("  ✓ Multiple independent tracks")
    print("  ✓ Auto-stacking within tracks")
    print("  ✓ Track alignment and layering")
    print("  ✓ Parallel and sequential composition")

    # Initialize project manager
    manager = ProjectManager()
    project_name = "multi_track_showcase"

    # Clean up existing project
    project_path = manager.workspace_dir / project_name
    if project_path.exists():
        print(f"\n🔄 Removing existing project: {project_name}")
        shutil.rmtree(project_path)

    # Create project
    print(f"\n📁 Creating project: {project_name}")
    project = manager.create_project(
        name=project_name,
        theme="tech",
        fps=30,
        width=1920,
        height=1080
    )
    print(f"✓ Project created at: {project['path']}")

    # Show default tracks
    print("\n🎯 Default Tracks:")
    tracks = manager.current_timeline.list_tracks()
    for track in tracks:
        print(f"  • {track['name']:<12} (layer {track['layer']:>3}, gap {track['default_gap']}s)")

    # Add custom track for picture-in-picture
    print("\n➕ Adding custom 'pip' track (layer 20)...")
    manager.current_timeline.add_track(
        name="pip",
        layer=20,
        default_gap=0,
        description="Picture-in-picture overlays"
    )
    print("✓ Custom track added")

    # ========================================================================
    # MAIN TRACK: Sequential content
    # ========================================================================
    print("\n" + "="*80)
    print("MAIN TRACK: Sequential auto-stacking content")
    print("="*80)

    # Title scene (auto-stacks at frame 0)
    print("\n🎬 Adding title scene...")
    title = ComponentInstance(
        component_type="TitleScene",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "Multi-Track Video System",
            "subtitle": "Powered by Remotion + Track-Based Timeline",
            "variant": "bold",
            "animation": "fade_zoom"
        },
        layer=0
    )
    manager.current_timeline.add_component(title, duration=4.0, track="main")
    cursor = manager.current_timeline.get_track_cursor("main")
    print(f"✓ Title scene: 0.0s - 4.0s (main track cursor now at {cursor} frames)")

    # Code block (auto-stacks after title with 0.5s gap)
    print("\n💻 Adding code demonstration...")
    code = ComponentInstance(
        component_type="CodeBlock",
        start_frame=0,
        duration_frames=0,
        props={
            "code": """# Track-based timeline example
timeline = Timeline(fps=30)

# Components auto-stack sequentially
timeline.add_component(title, duration=4.0, track="main")
timeline.add_component(code, duration=6.0, track="main")

# Overlays layer on top
timeline.add_component(caption, duration=3.0, track="overlay")""",
            "language": "python",
            "title": "timeline.py",
            "variant": "editor",
            "show_line_numbers": True
        },
        layer=0
    )
    manager.current_timeline.add_component(code, duration=6.0, track="main", gap_before=0.5)
    cursor = manager.current_timeline.get_track_cursor("main")
    print(f"✓ Code block: 4.5s - 10.5s (main track cursor now at {cursor} frames)")

    # Bar chart (continues auto-stacking)
    print("\n📊 Adding bar chart...")
    chart = ComponentInstance(
        component_type="BarChart",
        start_frame=0,
        duration_frames=0,
        props={
            "data": [
                {"label": "Manual Timing", "value": 45, "color": "#ef4444"},
                {"label": "Track-Based", "value": 95, "color": "#22c55e"}
            ],
            "title": "Developer Productivity",
            "ylabel": "Satisfaction %"
        },
        layer=0
    )
    manager.current_timeline.add_component(chart, duration=5.0, track="main", gap_before=0.5)
    cursor = manager.current_timeline.get_track_cursor("main")
    print(f"✓ Bar chart: 11.0s - 16.0s (main track cursor now at {cursor} frames)")

    # ========================================================================
    # OVERLAY TRACK: Text overlays that layer on top
    # ========================================================================
    print("\n" + "="*80)
    print("OVERLAY TRACK: Layered on top of main content")
    print("="*80)

    # Lower third aligned to title start
    print("\n📋 Adding lower third (aligned to title)...")
    lower_third_1 = ComponentInstance(
        component_type="LowerThird",
        start_frame=0,
        duration_frames=0,
        props={
            "name": "Track-Based System",
            "title": "No manual frame calculations!",
            "variant": "glass",
            "position": "bottom_left"
        },
        layer=10
    )
    manager.current_timeline.add_component(
        lower_third_1,
        duration=3.5,
        track="overlay",
        align_to="main",
        offset=0.5
    )
    print("✓ Lower third #1: 0.5s - 4.0s (layer 10, over title)")

    # Text overlay aligned to code block
    print("\n💬 Adding text overlay (aligned to code)...")
    text_overlay = ComponentInstance(
        component_type="TextOverlay",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "Auto-stacking + Layering = 🚀",
            "style": "caption",
            "animation": "fade_in",
            "position": "top_right"
        },
        layer=10
    )
    manager.current_timeline.add_component(
        text_overlay,
        duration=4.0,
        track="overlay",
        align_to="main",
        offset=5.0
    )
    print("✓ Text overlay: 5.0s - 9.0s (layer 10, over code)")

    # Another lower third aligned to chart
    print("\n📋 Adding lower third (aligned to chart)...")
    lower_third_2 = ComponentInstance(
        component_type="LowerThird",
        start_frame=0,
        duration_frames=0,
        props={
            "name": "Parallel Tracks",
            "title": "Independent timelines working together",
            "variant": "bold",
            "position": "bottom_center"
        },
        layer=10
    )
    manager.current_timeline.add_component(
        lower_third_2,
        duration=4.0,
        track="overlay",
        align_to="main",
        offset=11.5
    )
    print("✓ Lower third #2: 11.5s - 15.5s (layer 10, over chart)")

    # ========================================================================
    # PIP TRACK: Picture-in-picture overlay at the top layer
    # ========================================================================
    print("\n" + "="*80)
    print("PIP TRACK: High-level overlays (layer 20)")
    print("="*80)

    # Counter as PiP element
    print("\n🔢 Adding counter (top-right corner)...")
    counter = ComponentInstance(
        component_type="Counter",
        start_frame=0,
        duration_frames=0,
        props={
            "start_value": 0,
            "end_value": 100,
            "suffix": "%",
            "decimals": 0,
            "animation": "count_up"
        },
        layer=20
    )
    manager.current_timeline.add_component(
        counter,
        duration=8.0,
        track="pip",
        align_to="main",
        offset=4.0
    )
    print("✓ Counter: 4.0s - 12.0s (layer 20, highest layer)")

    # ========================================================================
    # BACKGROUND TRACK: Behind everything
    # ========================================================================
    print("\n" + "="*80)
    print("BACKGROUND TRACK: Sits behind all content (layer -10)")
    print("="*80)

    print("\n🎨 Adding background container...")
    # Note: Would typically add a solid color or video here
    # For now, adding a container as placeholder
    bg_container = ComponentInstance(
        component_type="Container",
        start_frame=0,
        duration_frames=0,
        props={
            "position": "center",
            "width": "100%",
            "height": "100%",
            "padding": 0
        },
        layer=-10
    )
    manager.current_timeline.add_component(
        bg_container,
        duration=16.0,
        track="background",
        start_frame=0  # Explicit start from beginning
    )
    print("✓ Background: 0.0s - 16.0s (layer -10, behind everything)")

    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "="*80)
    print("TIMELINE SUMMARY")
    print("="*80)

    info = manager.get_project_info()
    composition = info['composition']

    print("\n📊 Composition Stats:")
    print(f"  Total duration: {composition['duration_seconds']:.1f} seconds")
    print(f"  Total frames: {composition['duration_frames']}")
    print(f"  Total components: {len(composition['components'])}")

    print("\n🎯 Track Summary:")
    all_tracks = manager.current_timeline.list_tracks()
    for track in all_tracks:
        print(f"  • {track['name']:<12}: {track['component_count']} components, "
              f"cursor at {track['cursor_seconds']:.1f}s")

    print("\n📅 Timeline (sorted by start time):")
    sorted_components = sorted(composition['components'], key=lambda c: c['start_time'])
    for comp in sorted_components:
        layer_info = f"L{comp['layer']:>3}"
        time_info = f"{comp['start_time']:>5.1f}s - {comp['start_time'] + comp['duration']:>5.1f}s"
        print(f"    {layer_info} │ {time_info} │ {comp['type']}")

    print("\n📚 Visual Timeline:")
    print("    ─────────────────────────────────────────────────")
    print("    Background (L-10): [████████████████████████████]")
    print("    Main (L0):         [████][██████][███████]       ")
    print("    Overlay (L10):      [███]  [████]   [████]       ")
    print("    PIP (L20):              [████████]               ")
    print("    ─────────────────────────────────────────────────")
    print("    Time (s):          0    5    10   15             ")

    # ========================================================================
    # Generate files
    # ========================================================================
    print("\n" + "="*80)
    print("GENERATING VIDEO FILES")
    print("="*80)

    print("\n⚙️  Generating TSX components...")
    component_types = {c.component_type for c in manager.current_timeline.get_all_components()}

    for comp_type in sorted(component_types):
        sample = next(
            c for c in manager.current_timeline.get_all_components()
            if c.component_type == comp_type
        )
        manager.add_component_to_project(
            comp_type,
            sample.props,
            manager.current_timeline.theme
        )
        print(f"  ✓ {comp_type}.tsx")

    print("\n📝 Generating VideoComposition.tsx...")
    manager.generate_composition()
    print("  ✓ VideoComposition.tsx")

    # ========================================================================
    # Next steps
    # ========================================================================
    print("\n" + "="*80)
    print("🎉 MULTI-TRACK VIDEO GENERATED!")
    print("="*80)

    print(f"\n📁 Project: {project['path']}")

    print("\n🚀 Next steps:")
    print("\n1. Install dependencies:")
    print(f"   cd {project['path']}")
    print("   npm install")

    print("\n2. Preview in Remotion Studio:")
    print("   npm start")
    print("   → Opens at http://localhost:3000")

    print("\n3. Render video:")
    print("   npm run build")

    print("\n" + "="*80)
    print("\n✨ Key Features Demonstrated:")
    print("  ✓ 4 tracks: main, overlay, pip, background")
    print("  ✓ Auto-stacking: components added sequentially within tracks")
    print("  ✓ Track alignment: overlays sync with main track")
    print("  ✓ Layering: z-index from tracks (background → main → overlay → pip)")
    print("  ✓ No manual frames: all timing calculated automatically")
    print("\n💡 This is much easier than calculating frames manually!\n")


if __name__ == "__main__":
    asyncio.run(main())
