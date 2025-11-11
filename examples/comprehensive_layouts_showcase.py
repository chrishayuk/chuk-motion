#!/usr/bin/env python3
"""
Comprehensive YouTube Layouts Showcase

THE definitive showcase demonstrating ALL 17 layout types.
Uses the dictionary-based scene API (like youtube_layouts.py).

Usage:
    python examples/comprehensive_layouts_showcase.py
"""
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_remotion.utils.project_manager import ProjectManager
import shutil


def create_demo_box_config(label: str, color: str = "primary"):
    """Helper to create DemoBox config dict."""
    return {
        "type": "DemoBox",
        "config": {
            "label": label,
            "color": color
        }
    }


def generate_comprehensive_layouts_showcase():
    """Generate THE comprehensive showcase with all 17 layouts."""

    project_name = "comprehensive_layouts_showcase"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print(f"COMPREHENSIVE LAYOUTS SHOWCASE")
    print(f"ALL 17 Layout Types")
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
    print("\n📐 Creating Introduction")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Complete Layout System",
            "subtitle": "17 Professional Layouts for YouTube",
            "variant": "bold",
            "animation": "fade_zoom"
        }
    })

    # ========================================
    # CORE LAYOUTS (with DemoBox placeholders)
    # ========================================

    # 1. Grid (2x2)
    print("\n📐 1. Grid Layout (2x2)")
    add_scene({
        "type": "Grid",
        "config": {
            "layout": "2x2",
            "padding": 40,
            "gap": 20,
            "border_width": 2
        },
        "children": [
            create_demo_box_config("CELL 1", "primary"),
            create_demo_box_config("CELL 2", "accent"),
            create_demo_box_config("CELL 3", "secondary"),
            create_demo_box_config("CELL 4", "primary")
        ]
    })

    # 2. ThreeByThreeGrid
    print("📐 2. ThreeByThreeGrid")
    add_scene({
        "type": "ThreeByThreeGrid",
        "config": {
            "padding": 40,
            "gap": 15,
            "border_width": 2
        },
        "children": [create_demo_box_config(f"CELL {i+1}", "primary" if i % 2 == 0 else "accent") for i in range(9)]
    })

    # 3. ThreeColumnLayout
    print("📐 3. ThreeColumnLayout")
    add_scene({
        "type": "ThreeColumnLayout",
        "config": {
            "left_width": 30,
            "center_width": 40,
            "right_width": 30,
            "gap": 20,
            "border_width": 2
        },
        "left": create_demo_box_config("LEFT\\n30%", "primary"),
        "center": create_demo_box_config("CENTER\\n40%", "accent"),
        "right": create_demo_box_config("RIGHT\\n30%", "primary")
    })

    # 4. ThreeRowLayout
    print("📐 4. ThreeRowLayout")
    add_scene({
        "type": "ThreeRowLayout",
        "config": {
            "top_height": 20,
            "middle_height": 60,
            "bottom_height": 20,
            "gap": 20,
            "border_width": 2
        },
        "top": create_demo_box_config("TOP 20%", "accent"),
        "middle": create_demo_box_config("MIDDLE 60%", "primary"),
        "bottom": create_demo_box_config("BOTTOM 20%", "accent")
    })

    # 5. AsymmetricLayout
    print("📐 5. AsymmetricLayout")
    add_scene({
        "type": "AsymmetricLayout",
        "config": {
            "layout": "main-right",
            "main_ratio": 67,
            "gap": 20,
            "border_width": 2
        },
        "main": create_demo_box_config("MAIN\\n67%", "accent"),
        "top_side": create_demo_box_config("TOP SIDE", "primary"),
        "bottom_side": create_demo_box_config("BOTTOM", "primary")
    })

    # 6. SplitScreen
    print("📐 6. SplitScreen")
    add_scene({
        "type": "SplitScreen",
        "config": {
            "orientation": "horizontal",
            "gap": 20,
            "divider_width": 3
        },
        "left": create_demo_box_config("LEFT 50%", "primary"),
        "right": create_demo_box_config("RIGHT 50%", "accent")
    })

    # 7. Container
    print("📐 7. Container")
    add_scene({
        "type": "Container",
        "config": {
            "padding": 80,
            "border_width": 3,
            "border_radius": 12
        },
        "children": create_demo_box_config("CENTERED\\nCONTENT", "accent")
    })

    # ========================================
    # SPECIALIZED LAYOUTS
    # ========================================

    # 8. OverTheShoulder
    print("📐 8. OverTheShoulder")
    add_scene({
        "type": "OverTheShoulder",
        "config": {
            "overlay_position": "left",
            "overlay_size": 35,
            "gap": 20,
            "border_width": 2
        },
        "screen_content": create_demo_box_config("SCREEN\\n65%", "accent"),
        "shoulder_overlay": create_demo_box_config("HOST\\n35%", "primary")
    })

    # 9. DialogueFrame
    print("📐 9. DialogueFrame")
    add_scene({
        "type": "DialogueFrame",
        "config": {
            "speaker_size": 50,
            "gap": 20,
            "border_width": 2
        },
        "left_speaker": create_demo_box_config("PERSON A", "primary"),
        "right_speaker": create_demo_box_config("PERSON B", "secondary")
    })

    # 10. StackedReaction
    print("📐 10. StackedReaction")
    add_scene({
        "type": "StackedReaction",
        "config": {
            "reaction_size": 35,
            "gap": 20,
            "border_width": 2
        },
        "original_content": create_demo_box_config("ORIGINAL\\n65%", "accent"),
        "reaction_content": create_demo_box_config("REACTOR\\n35%", "primary")
    })

    # 11. HUDStyle
    print("📐 11. HUDStyle")
    add_scene({
        "type": "HUDStyle",
        "config": {
            "overlay_size": 15,
            "border_width": 2
        },
        "main_content": create_demo_box_config("GAMEPLAY", "accent"),
        "top_left": create_demo_box_config("CAM", "primary"),
        "bottom_right": create_demo_box_config("CHAT", "secondary")
    })

    # 12. PerformanceMultiCam
    print("📐 12. PerformanceMultiCam")
    add_scene({
        "type": "PerformanceMultiCam",
        "config": {
            "gap": 20,
            "border_width": 2
        },
        "primary_cam": create_demo_box_config("FRONT", "accent"),
        "secondary_cams": [
            create_demo_box_config("OVERHEAD", "primary"),
            create_demo_box_config("HAND", "primary"),
            create_demo_box_config("DETAIL", "primary")
        ]
    })

    # 13. FocusStrip
    print("📐 13. FocusStrip")
    add_scene({
        "type": "FocusStrip",
        "config": {
            "strip_height": 30,
            "position": "center",
            "border_width": 2
        },
        "focus_content": create_demo_box_config("HOST\\nSTRIP 30%", "primary"),
        "main_content": create_demo_box_config("B-ROLL\\nBACKGROUND", "accent")
    })

    # 14. PiP
    print("📐 14. PiP")
    add_scene({
        "type": "PiP",
        "config": {
            "pip_position": "bottom-right",
            "pip_size": 20,
            "pip_border_width": 2
        },
        "mainContent": create_demo_box_config("MAIN\\nCONTENT", "accent"),
        "pipContent": create_demo_box_config("PiP\\n20%", "primary")
    })

    # 15. Vertical (9:16 for Shorts)
    print("📐 15. Vertical")
    add_scene({
        "type": "Vertical",
        "config": {
            "layout_style": "top-bottom",
            "top_ratio": 70,
            "gap": 10
        },
        "top": create_demo_box_config("TOP\\n70%", "accent"),
        "bottom": create_demo_box_config("BOTTOM\\n30%", "primary")
    })

    # 16. Timeline
    print("📐 16. Timeline")
    add_scene({
        "type": "Timeline",
        "config": {
            "height": 15,
            "position": "bottom",
            "current_time": 30,
            "total_duration": 120
        },
        "main_content": create_demo_box_config("MAIN\\nCONTENT", "accent"),
        "milestones": [
            {"time": 0, "label": "START"},
            {"time": 60, "label": "MID"},
            {"time": 120, "label": "END"}
        ]
    })

    # 17. Mosaic
    print("📐 17. Mosaic")
    add_scene({
        "type": "Mosaic",
        "config": {
            "style": "hero-corners",
            "gap": 15,
            "border_width": 2
        },
        "clips": [
            {"content": create_demo_box_config("CLIP 1", "accent")},
            {"content": create_demo_box_config("CLIP 2", "primary")},
            {"content": create_demo_box_config("CLIP 3", "secondary")},
            {"content": create_demo_box_config("CLIP 4", "primary")}
        ]
    })

    # ========================================
    # FINAL TITLE
    # ========================================
    print("\n📐 Creating Final Title")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "17 Professional Layouts",
            "subtitle": "Build Any YouTube Video",
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
    print("✅ COMPREHENSIVE LAYOUTS SHOWCASE GENERATED!")
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

    print(f"\n🎨 All 17 Layout Types Demonstrated:")
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
    print("   ✓ ALL 17 layout types with DemoBox placeholders")
    print("   ✓ Clean structure-focused visualization")
    print("   ✓ Design token integration")
    print("   ✓ Flexible configuration options")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n🎬 Comprehensive YouTube Layouts Showcase Generator")
    print("   THE definitive showcase of all 17 layout types\n")

    try:
        project_path = generate_comprehensive_layouts_showcase()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
