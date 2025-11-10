#!/usr/bin/env python3
"""
Layout Showcase - Demonstrates all 17 layout components with title slides.

Creates a comprehensive showcase video demonstrating every layout component
with numbered title slides before each demo.
"""

import shutil
from pathlib import Path

from chuk_mcp_remotion.utils.project_manager import ProjectManager


def create_demo_box(label, color="primary"):
    """Helper to create a demo box component."""
    return {"type": "DemoBox", "config": {"label": label, "color": color}}


def generate_layout_showcase():
    """Generate the complete layout showcase project."""

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
    scene_duration = 150  # 5 seconds per layout at 30fps
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
    # MAIN TITLE
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
        },
        duration=90,
    )

    # ========================================
    # CORE LAYOUTS (7)
    # ========================================
    print("\n📐 CORE LAYOUTS")

    print("  1. Container")
    add_layout_with_title(
        1,
        "Container",
        "Basic wrapper/frame",
        {
            "type": "Container",
            "config": {"padding": 60, "border_width": 3},
            "children": [create_demo_box("Container", "primary")],
        },
    )

    print("  2. Grid")
    add_layout_with_title(
        2,
        "Grid",
        "Multi-layout grid system",
        {
            "type": "Grid",
            "config": {"layout": "3x3", "padding": 40, "gap": 20, "border_width": 2},
            "children": [
                create_demo_box(f"{i+1}", ["primary", "accent", "secondary"][i % 3]) for i in range(9)
            ],
        },
    )

    print("  3. SplitScreen")
    add_layout_with_title(
        3,
        "SplitScreen",
        "Two-pane split",
        {
            "type": "SplitScreen",
            "config": {"split_ratio": 50, "orientation": "horizontal", "padding": 40, "gap": 20},
            "children": [create_demo_box("Left", "primary"), create_demo_box("Right", "accent")],
        },
    )

    print("  4. ThreeByThreeGrid")
    add_layout_with_title(
        4,
        "ThreeByThreeGrid",
        "Perfect 3x3 grid",
        {
            "type": "ThreeByThreeGrid",
            "config": {"padding": 40, "gap": 20, "border_width": 2},
            "children": [
                create_demo_box(f"{i+1}", ["primary", "accent", "secondary"][i % 3]) for i in range(9)
            ],
        },
    )

    print("  5. ThreeColumnLayout")
    add_layout_with_title(
        5,
        "ThreeColumnLayout",
        "Sidebar + Main + Sidebar",
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
            "left": create_demo_box("Left", "primary"),
            "center": create_demo_box("Main", "accent"),
            "right": create_demo_box("Right", "secondary"),
        },
    )

    print("  6. ThreeRowLayout")
    add_layout_with_title(
        6,
        "ThreeRowLayout",
        "Header + Main + Footer",
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
            "middle": create_demo_box("Main", "accent"),
            "bottom": create_demo_box("Footer", "secondary"),
        },
    )

    print("  7. AsymmetricLayout")
    add_layout_with_title(
        7,
        "AsymmetricLayout",
        "Main feed + stacked panels",
        {
            "type": "AsymmetricLayout",
            "config": {
                "layout": "main-left",
                "main_ratio": 66.67,
                "padding": 40,
                "gap": 20,
                "border_width": 2,
            },
            "main": create_demo_box("Main (2/3)", "primary"),
            "top_side": create_demo_box("Top (1/3)", "accent"),
            "bottom_side": create_demo_box("Bottom (1/3)", "secondary"),
        },
    )

    # ========================================
    # SPECIALIZED LAYOUTS (10)
    # ========================================
    print("\n🎯 SPECIALIZED LAYOUTS")

    print("  8. PiP")
    add_layout_with_title(
        8,
        "PiP",
        "Picture-in-Picture overlay",
        {
            "type": "PiP",
            "config": {"position": "bottom-right", "overlay_size": 25, "margin": 40},
            "mainContent": create_demo_box("Main", "primary"),
            "pipContent": create_demo_box("PiP", "accent"),
        },
    )

    print("  9. Vertical")
    add_layout_with_title(
        9,
        "Vertical",
        "9:16 mobile optimized",
        {
            "type": "Vertical",
            "config": {
                "layout_style": "content-caption",
                "top_ratio": 70,
                "padding": 40,
                "gap": 20,
                "border_width": 2,
            },
            "top": create_demo_box("Content", "primary"),
            "bottom": create_demo_box("Caption", "accent"),
        },
    )

    print("  10. DialogueFrame")
    add_layout_with_title(
        10,
        "DialogueFrame",
        "Conversation scenes",
        {
            "type": "DialogueFrame",
            "config": {"speaker_size": 35, "padding": 40, "gap": 20, "border_width": 2},
            "left_speaker": create_demo_box("Speaker 1", "primary"),
            "center_content": create_demo_box("Captions", "accent"),
            "right_speaker": create_demo_box("Speaker 2", "secondary"),
        },
    )

    print("  11. StackedReaction")
    add_layout_with_title(
        11,
        "StackedReaction",
        "Reaction video style",
        {
            "type": "StackedReaction",
            "config": {
                "layout": "vertical",
                "reaction_size": 40,
                "padding": 40,
                "gap": 20,
                "border_width": 2,
            },
            "original_content": create_demo_box("Original", "primary"),
            "reaction_content": create_demo_box("Reaction", "accent"),
        },
    )

    print("  12. FocusStrip")
    add_layout_with_title(
        12,
        "FocusStrip",
        "Focused banner/strip",
        {
            "type": "FocusStrip",
            "config": {"position": "center", "strip_height": 30, "padding": 40, "gap": 20},
            "main_content": create_demo_box("Background", "primary"),
            "focus_content": create_demo_box("Focus", "accent"),
        },
    )

    print("  13. OverTheShoulder")
    add_layout_with_title(
        13,
        "OverTheShoulder",
        "Screen recording perspective",
        {
            "type": "OverTheShoulder",
            "config": {"overlay_position": "bottom-left", "overlay_size": 30, "padding": 40},
            "screen_content": create_demo_box("Screen", "primary"),
            "shoulder_overlay": create_demo_box("Person", "accent"),
        },
    )

    print("  14. HUDStyle")
    add_layout_with_title(
        14,
        "HUDStyle",
        "Heads-up display with overlays",
        {
            "type": "HUDStyle",
            "config": {"overlay_size": 15, "padding": 40},
            "main_content": create_demo_box("Main", "primary"),
            "top_left": create_demo_box("TL", "accent"),
            "top_right": create_demo_box("TR", "secondary"),
            "bottom_left": create_demo_box("BL", "accent"),
            "bottom_right": create_demo_box("BR", "secondary"),
        },
    )

    print("  15. Timeline")
    add_layout_with_title(
        15,
        "Timeline",
        "Progress/milestone overlay",
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
            "main_content": create_demo_box("Main Content", "primary"),
        },
    )

    print("  16. PerformanceMultiCam")
    add_layout_with_title(
        16,
        "PerformanceMultiCam",
        "Multi-camera view",
        {
            "type": "PerformanceMultiCam",
            "config": {"layout": "primary-main", "padding": 40, "gap": 20, "border_width": 2},
            "primary_cam": create_demo_box("Primary", "primary"),
            "secondary_cams": [
                create_demo_box("Cam 2", "accent"),
                create_demo_box("Cam 3", "secondary"),
                create_demo_box("Cam 4", "accent"),
            ],
        },
    )

    print("  17. Mosaic")
    add_layout_with_title(
        17,
        "Mosaic",
        "Irregular collage layout",
        {
            "type": "Mosaic",
            "config": {"style": "hero-corners", "padding": 40, "gap": 10, "border_width": 2},
            "clips": [
                {"content": create_demo_box("Hero", "primary")},
                {"content": create_demo_box("C1", "accent")},
                {"content": create_demo_box("C2", "secondary")},
                {"content": create_demo_box("C3", "accent")},
                {"content": create_demo_box("C4", "secondary")},
            ],
        },
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

    total_scenes = len(scenes)
    duration_seconds = start_frame / 30.0

    print(f"\n{'='*70}")
    print(f"✅ Layout Showcase Created Successfully!")
    print(f"{'='*70}")
    print(f"📁 Project: {project_path}")
    print(f"🎬 Total Scenes: {total_scenes}")
    print(f"⏱️  Duration: {duration_seconds} seconds ({start_frame} frames)")
    print(f"📐 Layouts: 17 (7 core + 10 specialized)")
    print(f"\n🎥 To preview:")
    print(f"   cd {project_path}")
    print(f"   npm start")
    print(f"\n🎥 To generate video:")
    print(f"   cd {project_path}")
    print(f"   npm run build")
    print(f"\n{'='*70}\n")

    return str(project_path)


if __name__ == "__main__":
    project_path = generate_layout_showcase()
    print(f"✨ Showcase complete! Project at: {project_path}")
