#!/usr/bin/env python3
"""
Complete Text Animations Demo

Demonstrates all 6 text animation components:
- TypewriterText: Classic typing with cursor
- StaggerText: Staggered reveal with spring physics
- WavyText: Continuous wave motion
- TrueFocus: Word-by-word focus with brackets
- DecryptedText: Character scrambling reveal
- FuzzyText: VHS glitch effects

Usage:
    python examples/all_text_animations_demo.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import shutil

from chuk_motion.utils.project_manager import ProjectManager


def generate_all_text_animations_demo():
    """Generate a comprehensive showcase of all text animation components."""

    project_name = "all_text_animations_demo"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print("ALL TEXT ANIMATIONS DEMO")
    print("Complete showcase of 6 text animation components")
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
    # INTRO TITLE
    # ========================================
    print("\n🎬 Creating intro...")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Text Animations",
            "subtitle": "6 Dynamic Effects",
            "variant": "glass",
            "animation": "fade"
        }
    }, 60)  # 2 seconds

    # ========================================
    # SECTION 1: TypewriterText
    # ========================================
    print("🎬 Creating TypewriterText examples...")

    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "TypewriterText",
            "subtitle": "Classic Typing Effect",
            "variant": "minimal",
            "animation": "fade"
        }
    }, 45)

    add_scene({
        "type": "TypewriterText",
        "config": {
            "text": "Hello, World!",
            "fontSize": "3xl",
            "typeSpeed": 3.0,
            "showCursor": True,
            "position": "center"
        }
    }, 90)

    add_scene({
        "type": "TypewriterText",
        "config": {
            "text": "Code is poetry.",
            "fontSize": "2xl",
            "typeSpeed": 4.0,
            "position": "left",
            "align": "left"
        }
    }, 75)

    # ========================================
    # SECTION 2: StaggerText
    # ========================================
    print("🎬 Creating StaggerText examples...")

    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "StaggerText",
            "subtitle": "Smooth Reveal Animation",
            "variant": "minimal",
            "animation": "fade"
        }
    }, 45)

    add_scene({
        "type": "StaggerText",
        "config": {
            "text": "WELCOME",
            "fontSize": "4xl",
            "staggerBy": "char",
            "staggerDelay": 2.0,
            "animationType": "slide-up",
            "align": "center"
        }
    }, 90)

    add_scene({
        "type": "StaggerText",
        "config": {
            "text": "Key Points To Remember",
            "fontSize": "3xl",
            "staggerBy": "word",
            "staggerDelay": 3.0,
            "animationType": "fade",
            "align": "center"
        }
    }, 120)

    # ========================================
    # SECTION 3: WavyText
    # ========================================
    print("🎬 Creating WavyText examples...")

    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "WavyText",
            "subtitle": "Fun Wave Motion",
            "variant": "minimal",
            "animation": "fade"
        }
    }, 45)

    add_scene({
        "type": "WavyText",
        "config": {
            "text": "MUSIC",
            "fontSize": "4xl",
            "waveAmplitude": 25.0,
            "waveSpeed": 1.5,
            "waveFrequency": 0.3,
            "align": "center"
        }
    }, 90)

    add_scene({
        "type": "WavyText",
        "config": {
            "text": "Creative Content",
            "fontSize": "3xl",
            "waveAmplitude": 15.0,
            "waveSpeed": 1.0,
            "waveFrequency": 0.4,
            "align": "center"
        }
    }, 90)

    # ========================================
    # SECTION 4: TrueFocus
    # ========================================
    print("🎬 Creating TrueFocus examples...")

    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "TrueFocus",
            "subtitle": "Word-by-Word Focus",
            "variant": "minimal",
            "animation": "fade"
        }
    }, 45)

    add_scene({
        "type": "TrueFocus",
        "config": {
            "text": "Innovation Through Excellence",
            "fontSize": "3xl",
            "fontWeight": "black",
            "wordDuration": 1.5,
            "position": "center"
        }
    }, 120)

    add_scene({
        "type": "TrueFocus",
        "config": {
            "text": "Quality Matters Most",
            "fontSize": "4xl",
            "wordDuration": 1.0,
            "position": "center"
        }
    }, 90)

    # ========================================
    # SECTION 5: DecryptedText
    # ========================================
    print("🎬 Creating DecryptedText examples...")

    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "DecryptedText",
            "subtitle": "Character Scrambling",
            "variant": "minimal",
            "animation": "fade"
        }
    }, 45)

    add_scene({
        "type": "DecryptedText",
        "config": {
            "text": "Access Granted",
            "fontSize": "4xl",
            "revealDirection": "start",
            "scrambleSpeed": 3.0,
            "position": "center"
        }
    }, 90)

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
    }, 120)

    # ========================================
    # SECTION 6: FuzzyText
    # ========================================
    print("🎬 Creating FuzzyText examples...")

    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "FuzzyText",
            "subtitle": "VHS Glitch Effects",
            "variant": "minimal",
            "animation": "fade"
        }
    }, 45)

    add_scene({
        "type": "FuzzyText",
        "config": {
            "text": "GLITCH EFFECT",
            "fontSize": "4xl",
            "glitchIntensity": 8.0,
            "animate": True,
            "position": "center"
        }
    }, 90)

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
    }, 90)

    # ========================================
    # OUTRO
    # ========================================
    print("🎬 Creating outro...")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Text Animations",
            "subtitle": "6 Components Ready",
            "variant": "bold",
            "animation": "fade"
        }
    }, 90)

    # ========================================
    # Build the composition
    # ========================================
    print("\n🎬 Building composition...")

    result = project_manager.build_composition_from_scenes(scenes, theme="tech")

    print("\n" + "="*70)
    print("✅ ALL TEXT ANIMATIONS DEMO GENERATED!")
    print("="*70)
    print(f"\n📁 Project location: {project_path}")

    total_frames = result['total_frames']
    total_duration = total_frames / 30.0

    print(f"\n⏱️  Total duration: {total_duration:.1f} seconds ({total_frames} frames @ 30fps)")
    print("\n📊 Demo structure:")
    print("   • TypewriterText: 2 examples")
    print("   • StaggerText: 2 examples")
    print("   • WavyText: 2 examples")
    print("   • TrueFocus: 2 examples")
    print("   • DecryptedText: 2 examples")
    print("   • FuzzyText: 2 examples")
    print(f"   • TOTAL: {len(scenes)} scenes")

    print("\n🎨 All Text Animation Components:")
    print("   ✓ TypewriterText - Classic typing with cursor")
    print("   ✓ StaggerText - Staggered reveal with spring")
    print("   ✓ WavyText - Continuous wave motion")
    print("   ✓ TrueFocus - Word-by-word focus")
    print("   ✓ DecryptedText - Character scrambling")
    print("   ✓ FuzzyText - VHS glitch effects")

    print(f"\n📦 Generated {len(result['component_types'])} component types:")
    for comp_type in sorted(result['component_types']):
        print(f"   • {comp_type}")

    print(f"\n✨ Generated {len(result['component_files'])} TSX files")

    print("\n📝 Next steps:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")

    print("\n💡 Component locations:")
    print("   src/chuk_motion/components/text-animations/")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n🎬 All Text Animations Demo Generator")
    print("   Complete showcase of 6 text animation components\n")

    try:
        generate_all_text_animations_demo()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
