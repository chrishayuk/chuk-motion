#!/usr/bin/env python3
"""
DecryptedText and FuzzyText Demo

Demonstrates the DecryptedText and FuzzyText components - animated text effects
with character scrambling and glitch aesthetics.

Usage:
    python examples/text_animations_demo.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_motion.utils.project_manager import ProjectManager
import shutil


def generate_text_animations_demo():
    """Generate a showcase of DecryptedText and FuzzyText effects."""

    project_name = "text_animations_demo"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print(f"TEXT ANIMATIONS DEMO")
    print(f"DecryptedText & FuzzyText showcase")
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
    # SECTION 1: DecryptedText Examples
    # ========================================

    # Title card for DecryptedText
    print("\n🎬 Creating DecryptedText examples...")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "DecryptedText",
            "subtitle": "Character Scrambling Animation",
            "variant": "glass",
            "animation": "fade"
        }
    }, 60)  # 2 seconds

    # Example 1: Start-to-end reveal
    add_scene({
        "type": "DecryptedText",
        "config": {
            "text": "Access Granted",
            "fontSize": "4xl",
            "revealDirection": "start",
            "scrambleSpeed": 3.0,
            "position": "center"
        }
    }, 90)  # 3 seconds

    # Example 2: Center-out reveal
    add_scene({
        "type": "DecryptedText",
        "config": {
            "text": "System Initialized",
            "fontSize": "3xl",
            "fontWeight": "extrabold",
            "revealDirection": "center",
            "scrambleSpeed": 4.0,
            "position": "center"
        }
    }, 120)  # 4 seconds

    # Example 3: End-to-start reveal
    add_scene({
        "type": "DecryptedText",
        "config": {
            "text": "Decoding Complete",
            "fontSize": "3xl",
            "revealDirection": "end",
            "scrambleSpeed": 2.5,
            "position": "center"
        }
    }, 90)  # 3 seconds

    # Example 4: Fast reveal at top
    add_scene({
        "type": "DecryptedText",
        "config": {
            "text": "Authenticated",
            "fontSize": "2xl",
            "revealDirection": "start",
            "scrambleSpeed": 6.0,
            "position": "top"
        }
    }, 60)  # 2 seconds

    # ========================================
    # SECTION 2: FuzzyText Examples
    # ========================================

    # Title card for FuzzyText
    print("🎬 Creating FuzzyText examples...")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "FuzzyText",
            "subtitle": "VHS Glitch Effects",
            "variant": "bold",
            "animation": "fade"
        }
    }, 60)  # 2 seconds

    # Example 5: Basic animated glitch
    add_scene({
        "type": "FuzzyText",
        "config": {
            "text": "GLITCH EFFECT",
            "fontSize": "4xl",
            "glitchIntensity": 8.0,
            "animate": True,
            "position": "center"
        }
    }, 90)  # 3 seconds

    # Example 6: Static VHS aesthetic
    add_scene({
        "type": "FuzzyText",
        "config": {
            "text": "VHS Aesthetic",
            "fontSize": "3xl",
            "glitchIntensity": 3.0,
            "scanlineHeight": 1.5,
            "animate": False,
            "position": "center"
        }
    }, 90)  # 3 seconds

    # Example 7: High-intensity cyberpunk
    add_scene({
        "type": "FuzzyText",
        "config": {
            "text": "SYSTEM ERROR",
            "fontSize": "4xl",
            "fontWeight": "extrabold",
            "glitchIntensity": 15.0,
            "animate": True,
            "position": "center"
        }
    }, 90)  # 3 seconds

    # Example 8: Subtle scanlines at bottom
    add_scene({
        "type": "FuzzyText",
        "config": {
            "text": "Transmission",
            "fontSize": "2xl",
            "glitchIntensity": 4.0,
            "scanlineHeight": 2.5,
            "animate": True,
            "position": "bottom"
        }
    }, 90)  # 3 seconds

    # ========================================
    # SECTION 3: Combined Effects
    # ========================================

    # Title card for combined
    print("🎬 Creating combined examples...")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Combined",
            "subtitle": "Multiple Effects Together",
            "variant": "kinetic",
            "animation": "fade"
        }
    }, 60)  # 2 seconds

    # Example 9: DecryptedText with fast reveal
    add_scene({
        "type": "DecryptedText",
        "config": {
            "text": "Target Acquired",
            "fontSize": "3xl",
            "fontWeight": "black",
            "revealDirection": "center",
            "scrambleSpeed": 5.0,
            "position": "top"
        }
    }, 60)  # 2 seconds

    # Example 10: FuzzyText with medium glitch
    add_scene({
        "type": "FuzzyText",
        "config": {
            "text": "Connection Lost",
            "fontSize": "2xl",
            "glitchIntensity": 10.0,
            "animate": True,
            "position": "bottom"
        }
    }, 90)  # 3 seconds

    # ========================================
    # Build the composition
    # ========================================
    print("\n🎬 Building composition...")

    result = project_manager.build_composition_from_scenes(scenes, theme="tech")

    print("\n" + "="*70)
    print("✅ TEXT ANIMATIONS DEMO GENERATED!")
    print("="*70)
    print(f"\n📁 Project location: {project_path}")

    total_frames = result['total_frames']
    total_duration = total_frames / 30.0

    print(f"\n⏱️  Total duration: {total_duration:.1f} seconds ({total_frames} frames @ 30fps)")
    print(f"\n📊 Demo structure:")
    print(f"   • DecryptedText examples: 4 scenes")
    print(f"   • FuzzyText examples: 4 scenes")
    print(f"   • Combined examples: 2 scenes")
    print(f"   • TOTAL: {len(scenes)} scenes")

    print(f"\n🎨 Text Animation Features:")
    print("   ✓ Character scrambling reveals")
    print("   ✓ VHS scanline effects")
    print("   ✓ RGB split glitches")
    print("   ✓ Multiple reveal directions")
    print("   ✓ Configurable intensity")

    print(f"\n📦 Generated {len(result['component_types'])} component types:")
    for comp_type in sorted(result['component_types']):
        print(f"   • {comp_type}")

    print(f"\n✨ Generated {len(result['component_files'])} TSX files")

    print("\n📝 Next steps:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")

    print("\n💡 Use cases:")
    print("   • Hacker/tech aesthetics")
    print("   • System messages")
    print("   • Retro VHS effects")
    print("   • Cyberpunk themes")
    print("   • Dramatic reveals")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n🎬 Text Animations Demo Generator")
    print("   DecryptedText & FuzzyText showcase\n")

    try:
        project_path = generate_text_animations_demo()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
