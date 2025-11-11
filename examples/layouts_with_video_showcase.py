#!/usr/bin/env python3
"""
Layouts with Video Showcase

A visually stunning demonstration of all 17 layout types with actual video playback.
Each cell shows video content instead of static boxes.

Usage:
    python examples/layouts_with_video_showcase.py
"""
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_remotion.utils.project_manager import ProjectManager
import shutil


# Sample video URLs (using Big Buck Bunny and other open source videos)
SAMPLE_VIDEOS = [
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    "https://upload.wikimedia.org/wikipedia/commons/2/20/Wave_at_Alcaraz%E2%80%93Tsitsipas_practice_at_the_2023_French_Open.webm",  # Tennis
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
]


def create_video_config(video_index: int = 0, label: str = ""):
    """Helper to create VideoContent config dict."""
    return {
        "type": "VideoContent",
        "config": {
            "src": SAMPLE_VIDEOS[video_index % len(SAMPLE_VIDEOS)],
            "muted": True,
            "fit": "cover",
            "playback_rate": 1.0,
            "loop": True  # Enable looping for all videos
        }
    }


def generate_layouts_with_video():
    """Generate stunning video showcase with all 17 layouts."""

    project_name = "layouts_with_video_showcase"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print(f"LAYOUTS WITH VIDEO SHOWCASE")
    print(f"ALL 17 Layout Types with Real Video")
    print(f"{'='*70}\n")

    # Create base project
    project_info = project_manager.create_project(project_name)
    project_path = Path(project_info["path"])

    print(f"✅ Created base project at: {project_path}")

    theme = "tech"
    scenes = []
    start_frame = 0
    scene_duration = 120  # 4 seconds per scene at 30fps

    # Helper to add scene and increment start_frame
    def add_scene(scene_dict, duration=scene_duration):
        nonlocal start_frame
        scene_dict["startFrame"] = start_frame
        scene_dict["durationInFrames"] = duration
        scenes.append(scene_dict)
        start_frame += duration

    # ========================================
    # INTRODUCTION
    # ========================================
    print("\n🎬 Creating Introduction")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Layouts with Video",
            "subtitle": "17 Professional Layouts • Real Video Content",
            "variant": "bold",
            "animation": "fade_zoom"
        }
    })

    # ========================================
    # CORE LAYOUTS
    # ========================================

    # 1. Grid (2x2)
    print("\n🎬 1. Grid Layout (2x2)")
    add_scene({
        "type": "Grid",
        "config": {
            "layout": "2x2",
            "padding": 40,
            "gap": 20,
            "border_width": 2
        },
        "children": [
            create_video_config(0),
            create_video_config(1),
            create_video_config(2),
            create_video_config(3)
        ]
    })

    # 2. ThreeByThreeGrid
    print("🎬 2. ThreeByThreeGrid")
    add_scene({
        "type": "ThreeByThreeGrid",
        "config": {
            "padding": 40,
            "gap": 15,
            "border_width": 2
        },
        "children": [create_video_config(i) for i in range(9)]
    })

    # 3. ThreeColumnLayout
    print("🎬 3. ThreeColumnLayout")
    add_scene({
        "type": "ThreeColumnLayout",
        "config": {
            "left_width": 30,
            "center_width": 40,
            "right_width": 30,
            "gap": 20,
            "border_width": 2
        },
        "left": create_video_config(0),
        "center": create_video_config(1),
        "right": create_video_config(2)
    })

    # 4. ThreeRowLayout
    print("🎬 4. ThreeRowLayout")
    add_scene({
        "type": "ThreeRowLayout",
        "config": {
            "top_height": 20,
            "middle_height": 60,
            "bottom_height": 20,
            "gap": 20,
            "border_width": 2
        },
        "top": create_video_config(0),
        "middle": create_video_config(1),
        "bottom": create_video_config(2)
    })

    # 5. AsymmetricLayout
    print("🎬 5. AsymmetricLayout")
    add_scene({
        "type": "AsymmetricLayout",
        "config": {
            "layout": "main-right",
            "main_ratio": 67,
            "gap": 20,
            "border_width": 2
        },
        "main": create_video_config(0),
        "top_side": create_video_config(1),
        "bottom_side": create_video_config(2)
    })

    # 6. SplitScreen
    print("🎬 6. SplitScreen")
    add_scene({
        "type": "SplitScreen",
        "config": {
            "orientation": "horizontal",
            "gap": 20,
            "divider_width": 3
        },
        "left": create_video_config(0),
        "right": create_video_config(1)
    })

    # 7. Container
    print("🎬 7. Container")
    add_scene({
        "type": "Container",
        "config": {
            "padding": 80,
            "border_width": 3,
            "border_radius": 12
        },
        "children": create_video_config(0)
    })

    # ========================================
    # SPECIALIZED LAYOUTS
    # ========================================

    # 8. OverTheShoulder
    print("🎬 8. OverTheShoulder")
    add_scene({
        "type": "OverTheShoulder",
        "config": {
            "overlay_position": "left",
            "overlay_size": 35,
            "gap": 20,
            "border_width": 2
        },
        "screen_content": create_video_config(0),
        "shoulder_overlay": create_video_config(1)
    })

    # 9. DialogueFrame
    print("🎬 9. DialogueFrame")
    add_scene({
        "type": "DialogueFrame",
        "config": {
            "speaker_size": 50,
            "gap": 20,
            "border_width": 2
        },
        "left_speaker": create_video_config(0),
        "right_speaker": create_video_config(1)
    })

    # 10. StackedReaction
    print("🎬 10. StackedReaction")
    add_scene({
        "type": "StackedReaction",
        "config": {
            "reaction_size": 35,
            "gap": 20,
            "border_width": 2
        },
        "original_content": create_video_config(0),
        "reaction_content": create_video_config(1)
    })

    # 11. HUDStyle
    print("🎬 11. HUDStyle")
    add_scene({
        "type": "HUDStyle",
        "config": {
            "overlay_size": 15,
            "border_width": 2
        },
        "main_content": create_video_config(0),
        "top_left": create_video_config(1),
        "bottom_right": create_video_config(2)
    })

    # 12. PerformanceMultiCam
    print("🎬 12. PerformanceMultiCam")
    add_scene({
        "type": "PerformanceMultiCam",
        "config": {
            "gap": 20,
            "border_width": 2
        },
        "primary_cam": create_video_config(0),
        "secondary_cams": [
            create_video_config(1),
            create_video_config(2),
            create_video_config(3)
        ]
    })

    # 13. FocusStrip
    print("🎬 13. FocusStrip")
    add_scene({
        "type": "FocusStrip",
        "config": {
            "strip_height": 30,
            "position": "center",
            "border_width": 2
        },
        "focus_content": create_video_config(0),
        "main_content": create_video_config(1)
    })

    # 14. PiP
    print("🎬 14. PiP")
    add_scene({
        "type": "PiP",
        "config": {
            "pip_position": "bottom-right",
            "pip_size": 20,
            "pip_border_width": 2
        },
        "mainContent": create_video_config(0),
        "pipContent": create_video_config(1)
    })

    # 15. Vertical (9:16 for Shorts)
    print("🎬 15. Vertical")
    add_scene({
        "type": "Vertical",
        "config": {
            "layout_style": "top-bottom",
            "top_ratio": 70,
            "gap": 10
        },
        "top": create_video_config(0),
        "bottom": create_video_config(1)
    })

    # 16. Timeline
    print("🎬 16. Timeline")
    add_scene({
        "type": "Timeline",
        "config": {
            "height": 15,
            "position": "bottom",
            "current_time": 30,
            "total_duration": 120
        },
        "main_content": create_video_config(0),
        "milestones": [
            {"time": 0, "label": "START"},
            {"time": 60, "label": "MID"},
            {"time": 120, "label": "END"}
        ]
    })

    # 17. Mosaic
    print("🎬 17. Mosaic")
    add_scene({
        "type": "Mosaic",
        "config": {
            "style": "hero-corners",
            "gap": 15,
            "border_width": 2
        },
        "clips": [
            {"content": create_video_config(0)},
            {"content": create_video_config(1)},
            {"content": create_video_config(2)},
            {"content": create_video_config(3)}
        ]
    })

    # ========================================
    # FINAL TITLE
    # ========================================
    print("\n🎬 Creating Final Title")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "17 Professional Layouts",
            "subtitle": "Powered by Real Video",
            "variant": "glass",
            "animation": "zoom"
        }
    })

    # ========================================
    # Build the composition
    # ========================================
    print("\n🎬 Building composition...")

    result = project_manager.build_composition_from_scenes(scenes, theme=theme)

    print("\n" + "="*70)
    print("✅ LAYOUTS WITH VIDEO SHOWCASE GENERATED!")
    print("="*70)
    print(f"\n📁 Project location: {project_path}")

    # Calculate stats
    total_frames = result['total_frames']
    total_duration = total_frames / 30.0

    print(f"\n⏱️  Total duration: {total_duration:.1f} seconds ({total_frames} frames @ 30fps)")
    print(f"\n📊 Showcase structure:")
    print(f"   • Introduction: 1 scene")
    print(f"   • Core Layouts (7): Grid, 3x3Grid, 3Column, 3Row, Asymmetric, SplitScreen, Container")
    print(f"   • Specialized Layouts (10): OverShoulder, Dialogue, Reaction, HUD, MultiCam, FocusStrip, PiP, Vertical, Timeline, Mosaic")
    print(f"   • Final Title: 1 scene")
    print(f"   • TOTAL: {len(scenes)} scenes")

    print(f"\n🎨 All 17 Layout Types with Video:")
    print("   Core Layouts (7):")
    print("   ✓ Grid (flexible)")
    print("   ✓ ThreeByThreeGrid")
    print("   ✓ ThreeColumnLayout")
    print("   ✓ ThreeRowLayout")
    print("   ✓ AsymmetricLayout")
    print("   ✓ SplitScreen")
    print("   ✓ Container")
    print("\n   Specialized Layouts (10):")
    print("   ✓ OverTheShoulder")
    print("   ✓ DialogueFrame")
    print("   ✓ StackedReaction")
    print("   ✓ HUDStyle")
    print("   ✓ PerformanceMultiCam")
    print("   ✓ FocusStrip")
    print("   ✓ PiP")
    print("   ✓ Vertical")
    print("   ✓ Timeline")
    print("   ✓ Mosaic")

    print(f"\n📦 Generated {len(result['component_types'])} component types:")
    for comp_type in sorted(result['component_types']):
        print(f"   • {comp_type}")

    print(f"\n✨ Generated {len(result['component_files'])} TSX files")

    print("\n📝 Next steps:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")

    print("\n💡 This showcase demonstrates:")
    print("   ✓ ALL 17 layout types with real video playback")
    print("   ✓ Multiple video sources (Big Buck Bunny, Sintel, etc.)")
    print("   ✓ Professional video handling with Remotion's OffthreadVideo")
    print("   ✓ Visually stunning showcase of layout capabilities")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n🎬 Layouts with Video Showcase Generator")
    print("   Stunning visual demo of all 17 layout types with real video\n")

    try:
        project_path = generate_layouts_with_video()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
