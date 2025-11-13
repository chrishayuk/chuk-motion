#!/usr/bin/env python3
"""
PixelTransition Demo

Demonstrates the PixelTransition component - pixelated dissolve transitions.

Usage:
    python examples/pixel_transition_demo.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_motion.utils.project_manager import ProjectManager
import shutil


def generate_pixel_transition_demo():
    """Generate a showcase of PixelTransition effects."""

    project_name = "pixel_transition_demo"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print(f"PIXEL TRANSITION DEMO")
    print(f"Pixelated dissolve transition effects")
    print(f"{'='*70}\n")

    # Create base project
    project_info = project_manager.create_project(project_name, theme="tech")
    project_path = Path(project_info["path"])

    print(f"✅ Created base project at: {project_path}")

    scenes = []
    start_frame = 0

    def add_scene(scene_dict, duration_frames):
        nonlocal start_frame
        scene_dict["startFrame"] = start_frame
        scene_dict["durationInFrames"] = duration_frames
        scenes.append(scene_dict)
        start_frame += duration_frames

    # ========================================
    # SCENE 1: Basic Text Transition
    # ========================================
    print("\n🎬 Creating basic text transition...")
    add_scene({
        "type": "PixelTransition",
        "config": {
            "firstContent": {
                "type": "TitleScene",
                "config": {
                    "text": "Before",
                    "subtitle": "Original Content",
                    "variant": "bold",
                    "animation": "fade"
                }
            },
            "secondContent": {
                "type": "TitleScene",
                "config": {
                    "text": "After",
                    "subtitle": "Transformed Content",
                    "variant": "glass",
                    "animation": "fade"
                }
            },
            "gridSize": 12,
            "transitionStart": 60,  # 2 seconds
            "transitionDuration": 30  # 1 second
        }
    }, 150)  # 5 seconds total

    # ========================================
    # SCENE 2: Chart to Text Transition
    # ========================================
    print("🎬 Creating chart to text transition...")
    add_scene({
        "type": "PixelTransition",
        "config": {
            "firstContent": {
                "type": "BarChart",
                "config": {
                    "data": [
                        {"label": "Q1", "value": 45},
                        {"label": "Q2", "value": 67},
                        {"label": "Q3", "value": 89},
                        {"label": "Q4", "value": 120}
                    ],
                    "title": "Quarterly Growth",
                    "ylabel": "Revenue ($K)"
                }
            },
            "secondContent": {
                "type": "TextOverlay",
                "config": {
                    "text": "Record Breaking Year!",
                    "size": "large",
                    "style": "bold",
                    "position": "center"
                }
            },
            "gridSize": 15,
            "transitionStart": 75,  # 2.5 seconds
            "transitionDuration": 30
        }
    }, 150)

    # ========================================
    # SCENE 3: Fine Grid Transition
    # ========================================
    print("🎬 Creating fine grid transition...")
    add_scene({
        "type": "PixelTransition",
        "config": {
            "firstContent": {
                "type": "TitleScene",
                "config": {
                    "text": "Smooth",
                    "subtitle": "High Resolution",
                    "variant": "kinetic",
                    "animation": "fade"
                }
            },
            "secondContent": {
                "type": "TitleScene",
                "config": {
                    "text": "Transition",
                    "subtitle": "Pixel Perfect",
                    "variant": "bold",
                    "animation": "fade"
                }
            },
            "gridSize": 20,  # More pixels = smoother
            "transitionStart": 60,
            "transitionDuration": 45  # Slower = more dramatic
        }
    }, 150)

    # ========================================
    # SCENE 4: Coarse Grid Transition
    # ========================================
    print("🎬 Creating coarse grid transition...")
    add_scene({
        "type": "PixelTransition",
        "config": {
            "firstContent": {
                "type": "Counter",
                "config": {
                    "startValue": 0,
                    "endValue": 10000,
                    "suffix": " Users",
                    "animation": "count_up"
                }
            },
            "secondContent": {
                "type": "Counter",
                "config": {
                    "startValue": 10000,
                    "endValue": 50000,
                    "suffix": " Users",
                    "animation": "count_up"
                }
            },
            "gridSize": 8,  # Fewer pixels = chunkier, retro
            "transitionStart": 60,
            "transitionDuration": 30
        }
    }, 150)

    # ========================================
    # Build the composition
    # ========================================
    print("\n🎬 Building composition...")

    result = project_manager.build_composition_from_scenes(scenes, theme="tech")

    print("\n" + "="*70)
    print("✅ PIXEL TRANSITION DEMO GENERATED!")
    print("="*70)
    print(f"\n📁 Project location: {project_path}")

    total_frames = result['total_frames']
    total_duration = total_frames / 30.0

    print(f"\n⏱️  Total duration: {total_duration:.1f} seconds ({total_frames} frames @ 30fps)")
    print(f"\n📊 Demo structure:")
    print(f"   • Text Transition: 1 scene")
    print(f"   • Chart to Text: 1 scene")
    print(f"   • Fine Grid: 1 scene")
    print(f"   • Coarse Grid: 1 scene")
    print(f"   • TOTAL: {len(scenes)} scenes")

    print(f"\n🎨 PixelTransition Variations:")
    print("   ✓ Different grid sizes (8x8 to 20x20)")
    print("   ✓ Variable transition timing")
    print("   ✓ Text, charts, and counters")
    print("   ✓ Smooth vs. chunky pixel effects")

    print(f"\n📦 Generated {len(result['component_types'])} component types:")
    for comp_type in sorted(result['component_types']):
        print(f"   • {comp_type}")

    print(f"\n✨ Generated {len(result['component_files'])} TSX files")

    print("\n📝 Next steps:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")

    print("\n💡 PixelTransition features:")
    print("   ✓ Pixelated dissolve effect")
    print("   ✓ Random staggered animation")
    print("   ✓ Configurable grid density")
    print("   ✓ Smooth content switching")
    print("   ✓ Design token colors")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n🎬 PixelTransition Demo Generator")
    print("   Retro-style pixel transition effects\n")

    try:
        project_path = generate_pixel_transition_demo()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
