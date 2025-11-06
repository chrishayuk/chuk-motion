#!/usr/bin/env python3
"""
Complete Layout Showcase - All 17 Layouts

Demonstrates every layout component in the system with beautiful examples.
Uses the new modular layout structure with design tokens.

Usage:
    python examples/layout_showcase.py
"""
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_remotion.utils.project_manager import ProjectManager
import shutil


def create_demo_box(label: str, color: str = "primary"):
    """Helper to create DemoBox config dict."""
    return {
        "type": "DemoBox",
        "config": {
            "label": label,
            "color": color,
        },
    }


def create_text_box(text: str, size: str = "lg"):
    """Helper to create text config."""
    return {
        "type": "Text",
        "config": {
            "text": text,
            "size": size,
        },
    }


def generate_layout_showcase():
    """Generate comprehensive layout showcase."""

    project_name = "layout_showcase"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print(f"COMPLETE LAYOUT SHOWCASE")
    print(f"Demonstrating All 17 Layout Components")
    print(f"{'='*70}\n")

    # Create base project
    project_info = project_manager.create_project(project_name)
    project_path = Path(project_info["path"])

    print(f"✅ Created base project at: {project_path}")

    theme = "tech"
    scenes = []
    start_frame = 0
    scene_duration = 150  # 5 seconds per scene at 30fps
    title_duration = 60  # 2 seconds for title slides

    def add_scene(scene_dict, duration=scene_duration):
        nonlocal start_frame
        scene_dict["startFrame"] = start_frame
        scene_dict["durationInFrames"] = duration
        scenes.append(scene_dict)
        start_frame += duration

    def add_layout_with_title(number, name, description, layout_scene_dict):
        """Add a title slide followed by the layout demo."""
        # Add title slide
        add_scene(
            {
                "type": "TitleScene",
                "config": {
                    "text": f"{number}. {name}",
                    "subtitle": description,
                    "variant": "minimal",
                    "animation": "fade",
                },
            },
            duration=title_duration,
        )
        # Add layout demo
        add_scene(layout_scene_dict)

    # ========================================
    # TITLE
    # ========================================
    print("\n🎬 Creating Title Scene")
    add_scene(
        {
            "type": "TitleScene",
            "config": {
                "text": "Layout Showcase",
                "subtitle": "17 Professional Layouts",
                "variant": "bold",
                "animation": "fade_zoom",
            },
        }
    )

    # ========================================
    # CORE LAYOUTS
    # ========================================
    print("\n📐 CORE LAYOUTS")

    # 1. Container
    print("  1. Container Layout")
    add_layout_with_title(
        1,
        "Container",
        "Basic wrapper/frame",
        {
            "type": "Container",
            "config": {
                "padding": 60,
                "border_width": 3,
            },
            "children": [create_demo_box("Container", "primary")],
        },
    )

    # 2. Grid (3x3)
    print("  2. Grid Layout (3x3)")
    add_layout_with_title(
        2,
        "Grid",
        "Multi-layout grid system",
        {
            "type": "Grid",
            "config": {
                "layout": "3x3",
                "padding": 40,
                "gap": 20,
                "border_width": 2,
            },
            "children": [
                create_demo_box(f"Cell {i+1}", ["primary", "accent", "secondary"][i % 3])
                for i in range(9)
            ],
        },
    )

    # 3. SplitScreen
    print("  3. SplitScreen Layout")
    add_layout_with_title(
        3,
        "SplitScreen",
        "Two-pane split",
        {
            "type": "SplitScreen",
            "config": {
                "split_ratio": 50,
                "direction": "horizontal",
                "padding": 40,
                "gap": 20,
            },
            "children": [
                create_demo_box("Left", "primary"),
                create_demo_box("Right", "accent"),
            ],
        },
    )

    # 4. ThreeByThreeGrid
    print("  4. ThreeByThreeGrid Layout")
    add_scene(
        {
            "type": "ThreeByThreeGrid",
            "config": {
                "padding": 40,
                "gap": 20,
                "border_width": 2,
            },
            "children": [
                create_demo_box(f"Grid {i+1}", ["primary", "accent", "secondary"][i % 3])
                for i in range(9)
            ],
        }
    )

    # 5. ThreeColumnLayout
    print("  5. ThreeColumnLayout")
    add_scene(
        {
            "type": "ThreeColumnLayout",
            "config": {
                "left_width": 25,
                "center_width": 50,
                "right_width": 25,
                "padding": 40,
                "gap": 20,
                "border_width": 2,
            },
            "left": create_demo_box("Left Sidebar", "primary"),
            "center": create_demo_box("Main Content", "accent"),
            "right": create_demo_box("Right Sidebar", "secondary"),
        }
    )

    # 6. ThreeRowLayout
    print("  6. ThreeRowLayout")
    add_scene(
        {
            "type": "ThreeRowLayout",
            "config": {
                "top_height": 20,
                "middle_height": 60,
                "bottom_height": 20,
                "padding": 40,
                "gap": 20,
                "border_width": 2,
            },
            "top": create_demo_box("Header", "primary"),
            "middle": create_demo_box("Main Content", "accent"),
            "bottom": create_demo_box("Footer", "secondary"),
        }
    )

    # 7. AsymmetricLayout
    print("  7. AsymmetricLayout")
    add_scene(
        {
            "type": "AsymmetricLayout",
            "config": {
                "layout": "main-left",
                "main_ratio": 66.67,
                "padding": 40,
                "gap": 20,
                "border_width": 2,
            },
            "main": create_demo_box("Main Content (2/3)", "primary"),
            "top_side": create_demo_box("Top Panel (1/3)", "accent"),
            "bottom_side": create_demo_box("Bottom Panel (1/3)", "secondary"),
        }
    )

    # ========================================
    # SPECIALIZED LAYOUTS
    # ========================================
    print("\n🎯 SPECIALIZED LAYOUTS")

    # 8. PiP
    print("  8. PiP (Picture-in-Picture)")
    add_scene(
        {
            "type": "PiP",
            "config": {
                "position": "bottom-right",
                "overlay_size": 25,
                "margin": 40,
            },
            "mainContent": create_demo_box("Main Screen", "primary"),
            "pipContent": create_demo_box("PiP Overlay", "accent"),
        }
    )

    # 9. Vertical
    print("  9. Vertical (9:16 Mobile)")
    add_scene(
        {
            "type": "Vertical",
            "config": {
                "layout_style": "content-caption",
                "top_ratio": 70,
                "padding": 40,
                "gap": 20,
                "border_width": 2,
            },
            "top": create_demo_box("Main Content", "primary"),
            "bottom": create_demo_box("Caption Area", "accent"),
        }
    )

    # 10. DialogueFrame
    print("  10. DialogueFrame")
    add_scene(
        {
            "type": "DialogueFrame",
            "config": {
                "speaker_size": 35,
                "padding": 40,
                "gap": 20,
                "border_width": 2,
            },
            "left_speaker": create_demo_box("Speaker 1", "primary"),
            "center_content": create_demo_box("Captions", "accent"),
            "right_speaker": create_demo_box("Speaker 2", "secondary"),
        }
    )

    # 11. StackedReaction
    print("  11. StackedReaction")
    add_scene(
        {
            "type": "StackedReaction",
            "config": {
                "layout": "vertical",
                "reaction_size": 40,
                "padding": 40,
                "gap": 20,
                "border_width": 2,
            },
            "original_content": create_demo_box("Original Video", "primary"),
            "reaction_content": create_demo_box("Reaction", "accent"),
        }
    )

    # 12. FocusStrip
    print("  12. FocusStrip")
    add_scene(
        {
            "type": "FocusStrip",
            "config": {
                "position": "center",
                "strip_height": 30,
                "padding": 40,
                "gap": 20,
            },
            "main_content": create_demo_box("Background", "primary"),
            "focus_content": create_demo_box("Focused Message", "accent"),
        }
    )

    # 13. OverTheShoulder
    print("  13. OverTheShoulder")
    add_scene(
        {
            "type": "OverTheShoulder",
            "config": {
                "overlay_position": "bottom-left",
                "overlay_size": 30,
                "padding": 40,
            },
            "screen_content": create_demo_box("Screen Content", "primary"),
            "shoulder_overlay": create_demo_box("Person", "accent"),
        }
    )

    # 14. HUDStyle
    print("  14. HUDStyle")
    add_scene(
        {
            "type": "HUDStyle",
            "config": {
                "overlay_size": 15,
                "padding": 40,
            },
            "main_content": create_demo_box("Main View", "primary"),
            "top_left": create_demo_box("TL", "accent"),
            "top_right": create_demo_box("TR", "secondary"),
            "bottom_left": create_demo_box("BL", "accent"),
            "bottom_right": create_demo_box("BR", "secondary"),
            "center": create_demo_box("Center HUD", "primary"),
        }
    )

    # 15. Timeline
    print("  15. Timeline")
    add_scene(
        {
            "type": "Timeline",
            "config": {
                "position": "bottom",
                "height": 100,
                "current_time": 3,
                "total_duration": 10,
                "milestones": [
                    {"time": 0, "label": "Start", "icon": "●"},
                    {"time": 5, "label": "Middle", "icon": "●"},
                    {"time": 10, "label": "End", "icon": "●"},
                ],
            },
            "main_content": create_demo_box("Main Content with Timeline", "primary"),
        }
    )

    # 16. PerformanceMultiCam
    print("  16. PerformanceMultiCam")
    add_scene(
        {
            "type": "PerformanceMultiCam",
            "config": {
                "layout": "primary-main",
                "padding": 40,
                "gap": 20,
                "border_width": 2,
            },
            "primary_cam": create_demo_box("Primary Camera", "primary"),
            "secondary_cams": [
                create_demo_box("Cam 2", "accent"),
                create_demo_box("Cam 3", "secondary"),
                create_demo_box("Cam 4", "accent"),
            ],
        }
    )

    # 17. Mosaic
    print("  17. Mosaic")
    add_scene(
        {
            "type": "Mosaic",
            "config": {
                "style": "hero-corners",
                "padding": 40,
                "gap": 10,
                "border_width": 2,
            },
            "clips": [
                {"content": create_demo_box("Hero", "primary")},
                {"content": create_demo_box("Corner 1", "accent")},
                {"content": create_demo_box("Corner 2", "secondary")},
                {"content": create_demo_box("Corner 3", "accent")},
                {"content": create_demo_box("Corner 4", "secondary")},
            ],
        }
    )

    # ========================================
    # OUTRO
    # ========================================
    print("\n🎬 Creating Outro")
    add_scene(
        {
            "type": "TitleScene",
            "config": {
                "text": "All 17 Layouts",
                "subtitle": "Ready for Your Videos",
                "variant": "minimal",
                "animation": "fade",
            },
        },
        duration=90,
    )

    # ========================================
    # BUILD COMPOSITION
    # ========================================
    print(f"\n💾 Building composition...")

    result = project_manager.build_composition_from_scenes(scenes, theme=theme)

    print(f"\n{'='*70}")
    print(f"✅ Layout Showcase Created Successfully!")
    print(f"{'='*70}")
    print(f"📁 Project: {project_path}")
    print(f"🎬 Total Scenes: {len(scenes)}")
    print(f"⏱️  Duration: {start_frame / 30:.1f} seconds ({start_frame} frames)")
    print(f"📐 Layouts: 17 (7 core + 10 specialized)")

    if result.get("generated_files"):
        print(f"\n📝 Generated Files:")
        for file_path in result["generated_files"]:
            print(f"   ✓ {file_path}")

    print(f"\n🎥 To generate video:")
    print(f"   cd {project_path}")
    print(f"   npm install (if first time)")
    print(f"   npm run build")
    print(f"\n{'='*70}\n")

    # Print layout summary
    print("\n📊 Layout Summary:")
    print("\nCore Layouts (7):")
    print("  1. Container - Basic wrapper/frame")
    print("  2. Grid - Multi-layout grid system")
    print("  3. SplitScreen - Two-pane split")
    print("  4. ThreeByThreeGrid - Perfect 3x3 grid")
    print("  5. ThreeColumnLayout - Sidebar + Main + Sidebar")
    print("  6. ThreeRowLayout - Header + Main + Footer")
    print("  7. AsymmetricLayout - Main feed + stacked panels")

    print("\nSpecialized Layouts (10):")
    print("  8. PiP - Picture-in-Picture overlay")
    print("  9. Vertical - 9:16 mobile optimized")
    print("  10. DialogueFrame - Conversation scenes")
    print("  11. StackedReaction - Reaction video style")
    print("  12. FocusStrip - Focused banner/strip")
    print("  13. OverTheShoulder - Screen recording perspective")
    print("  14. HUDStyle - Heads-up display with overlays")
    print("  15. Timeline - Progress/milestone overlay")
    print("  16. PerformanceMultiCam - Multi-camera view")
    print("  17. Mosaic - Irregular collage layout")

    return project_path


if __name__ == "__main__":
    try:
        project_path = generate_layout_showcase()
        print("\n✨ Showcase generation complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
