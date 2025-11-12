#!/usr/bin/env python3
"""
TrueFocus Text Animation Demo

Demonstrates the TrueFocus component - dramatic text animation with word-by-word focus.
Shows various configurations and use cases.

Usage:
    python examples/true_focus_demo.py
"""
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_remotion.utils.project_manager import ProjectManager
import shutil


def generate_true_focus_demo():
    """Generate a showcase of TrueFocus text animations."""

    project_name = "true_focus_demo"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print(f"TRUE FOCUS TEXT ANIMATION DEMO")
    print(f"Dramatic word-by-word focus with animated corner brackets")
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
    # SCENE 1: Introduction Title
    # ========================================
    print("\n🎬 Creating introduction...")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "TrueFocus Animation",
            "subtitle": "Dramatic Word-by-Word Text Reveals",
            "variant": "bold",
            "animation": "fade_zoom"
        }
    }, 90)  # 3 seconds

    # ========================================
    # SCENE 2: Basic Example - Center
    # ========================================
    print("🎬 Creating basic center example...")
    add_scene({
        "type": "TrueFocus",
        "config": {
            "text": "Innovation Through Excellence",
            "fontSize": "3xl",
            "fontWeight": "black",
            "wordDuration": 45,  # 1.5 seconds per word (at 30fps)
            "position": "center",
            "blurAmount": 6
        }
    }, 180)  # 6 seconds (4 words × 1.5s)

    # ========================================
    # SCENE 3: Large Text - Bottom Position
    # ========================================
    print("🎬 Creating large text bottom example...")
    add_scene({
        "type": "TrueFocus",
        "config": {
            "text": "Transform Your Vision",
            "fontSize": "4xl",
            "fontWeight": "black",
            "wordDuration": 40,  # ~1.3 seconds per word
            "position": "bottom",
            "blurAmount": 7
        }
    }, 120)  # 4 seconds

    # ========================================
    # SCENE 4: Top Position with Medium Text
    # ========================================
    print("🎬 Creating top position example...")
    add_scene({
        "type": "TrueFocus",
        "config": {
            "text": "Powered by Advanced Technology",
            "fontSize": "2xl",
            "fontWeight": "extrabold",
            "wordDuration": 30,  # 1 second per word
            "position": "top",
            "blurAmount": 5
        }
    }, 150)  # 5 seconds

    # ========================================
    # SCENE 5: Fast Cycle - Tagline
    # ========================================
    print("🎬 Creating fast cycle tagline...")
    add_scene({
        "type": "TrueFocus",
        "config": {
            "text": "Think Different Act Bold",
            "fontSize": "3xl",
            "fontWeight": "black",
            "wordDuration": 25,  # ~0.8 seconds per word (faster)
            "position": "center",
            "blurAmount": 6
        }
    }, 100)  # ~3.3 seconds

    # ========================================
    # SCENE 6: Slow Emphasis - Key Message
    # ========================================
    print("🎬 Creating slow emphasis example...")
    add_scene({
        "type": "TrueFocus",
        "config": {
            "text": "Quality Over Quantity",
            "fontSize": "3xl",
            "fontWeight": "black",
            "wordDuration": 60,  # 2 seconds per word (slower for emphasis)
            "position": "center",
            "blurAmount": 8
        }
    }, 180)  # 6 seconds

    # ========================================
    # SCENE 7: Combined with Background
    # ========================================
    print("🎬 Creating combined scene with background...")
    add_scene({
        "type": "Container",
        "config": {
            "backgroundColor": "#0A0E27",
            "padding": 40
        },
        "content": {
            "type": "TrueFocus",
            "config": {
                "text": "The Future Is Now",
                "fontSize": "4xl",
                "fontWeight": "black",
                "wordDuration": 45,
                "position": "center",
                "blurAmount": 7,
                "textColor": "#FFFFFF",
                "frameColor": "#00D9FF",
                "glowColor": "#00D9FF"
            }
        }
    }, 150)  # 5 seconds

    # ========================================
    # SCENE 8: Final Title
    # ========================================
    print("🎬 Creating final title...")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "TrueFocus",
            "subtitle": "Dramatic Text Animations",
            "variant": "glass",
            "animation": "zoom"
        }
    }, 90)  # 3 seconds

    # ========================================
    # Build the composition
    # ========================================
    print("\n🎬 Building composition...")

    result = project_manager.build_composition_from_scenes(scenes, theme="tech")

    print("\n" + "="*70)
    print("✅ TRUE FOCUS DEMO GENERATED!")
    print("="*70)
    print(f"\n📁 Project location: {project_path}")

    # Calculate stats
    total_frames = result['total_frames']
    total_duration = total_frames / 30.0

    print(f"\n⏱️  Total duration: {total_duration:.1f} seconds ({total_frames} frames @ 30fps)")
    print(f"\n📊 Demo structure:")
    print(f"   • Introduction: 1 scene")
    print(f"   • Basic Examples: 5 scenes")
    print(f"   • Combined Example: 1 scene")
    print(f"   • Final Title: 1 scene")
    print(f"   • TOTAL: {len(scenes)} scenes")

    print(f"\n🎨 TrueFocus Variations:")
    print("   ✓ Center, top, and bottom positions")
    print("   ✓ Multiple font sizes (2xl, 3xl, 4xl)")
    print("   ✓ Different cycle speeds (fast, normal, slow)")
    print("   ✓ Custom colors and glow effects")
    print("   ✓ Combined with other components")

    print(f"\n📦 Generated {len(result['component_types'])} component types:")
    for comp_type in sorted(result['component_types']):
        print(f"   • {comp_type}")

    print(f"\n✨ Generated {len(result['component_files'])} TSX files")

    print("\n📝 Next steps:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")

    print("\n💡 TrueFocus features:")
    print("   ✓ Automatic word-by-word focus cycling")
    print("   ✓ Smooth blur transitions on non-focused words")
    print("   ✓ Animated corner brackets with glow effect")
    print("   ✓ Configurable timing and positioning")
    print("   ✓ Fully design-token compliant")
    print("   ✓ Multiple font sizes and weights")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n🎬 TrueFocus Demo Generator")
    print("   Dramatic text animation showcase\n")

    try:
        project_path = generate_true_focus_demo()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
