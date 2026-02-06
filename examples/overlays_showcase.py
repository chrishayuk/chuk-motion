#!/usr/bin/env python3
"""
Overlays Showcase

Demonstrates all 6 overlay components with various styles and configurations.
Shows: TitleScene, TextOverlay, EndScreen, LowerThird, SubscribeButton

Usage:
    python examples/overlays_showcase.py
"""
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import shutil

from chuk_motion.utils.project_manager import ProjectManager


def generate_overlays_showcase():
    """Generate comprehensive showcase of all overlay components."""

    project_name = "overlays_showcase"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print("OVERLAYS SHOWCASE")
    print("All 6 Overlay Components")
    print(f"{'='*70}\n")

    # Create base project
    project_info = project_manager.create_project(project_name)
    project_path = Path(project_info["path"])

    print(f"✅ Created base project at: {project_path}")

    theme = "tech"
    scenes = []
    start_frame = 0
    scene_duration = 120  # 4 seconds per overlay at 30fps
    title_duration = 60   # 2 seconds for title slides

    # Helper to add scene and increment start_frame
    def add_scene(scene_dict, duration=scene_duration):
        nonlocal start_frame
        scene_dict["startFrame"] = start_frame
        scene_dict["durationInFrames"] = duration
        scenes.append(scene_dict)
        start_frame += duration

    def add_overlay_with_title(number, name, description, overlay_scene_dict):
        """Add a title slide followed by the overlay demo."""
        add_scene({
            "type": "TitleScene",
            "config": {
                "text": f"{number}. {name}",
                "subtitle": description,
                "variant": "minimal",
                "animation": "fade"
            }
        }, duration=title_duration)
        add_scene(overlay_scene_dict)

    # ========================================
    # INTRODUCTION
    # ========================================
    print("\n🎬 Creating Introduction")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Overlays Showcase",
            "subtitle": "6 Professional Overlay Components",
            "variant": "bold",
            "animation": "fade_zoom"
        }
    }, duration=90)

    # ========================================
    # 1. TITLE SCENE - Bold Variant
    # ========================================
    print("\n🎬 1. TitleScene - Bold")
    add_overlay_with_title(
        1,
        "TitleScene",
        "Bold variant for strong impact",
        {
            "type": "TitleScene",
            "config": {
                "text": "Big Announcement",
                "subtitle": "Something amazing is coming",
                "variant": "bold",
                "animation": "fade_zoom"
            }
        }
    )

    # ========================================
    # 2. TITLE SCENE - Glass Variant
    # ========================================
    print("\n🎬 2. TitleScene - Glass")
    add_overlay_with_title(
        2,
        "TitleScene",
        "Glass variant for modern look",
        {
            "type": "TitleScene",
            "config": {
                "text": "Modern Design",
                "subtitle": "Glassmorphism aesthetics",
                "variant": "glass",
                "animation": "slide"
            }
        }
    )

    # ========================================
    # 3. TITLE SCENE - Minimal Variant
    # ========================================
    print("\n🎬 3. TitleScene - Minimal")
    add_overlay_with_title(
        3,
        "TitleScene",
        "Minimal variant for subtlety",
        {
            "type": "TitleScene",
            "config": {
                "text": "Clean & Simple",
                "subtitle": "Less is more",
                "variant": "minimal",
                "animation": "fade"
            }
        }
    )

    # ========================================
    # 4. TEXT OVERLAY
    # ========================================
    print("\n💬 4. TextOverlay")
    add_overlay_with_title(
        4,
        "TextOverlay",
        "Floating text over content",
        {
            "type": "TextOverlay",
            "config": {
                "text": "This is a text overlay that appears on top of your content",
                "position": "center",
                "font_size": 48,
                "background_opacity": 0.7
            },
            "content": {
                "type": "DemoBox",
                "config": {
                    "label": "Background Content\n\nText overlays appear on top",
                    "color": "primary"
                }
            }
        }
    )

    # ========================================
    # 5. LOWER THIRD - Bottom Left
    # ========================================
    print("\n📍 5. LowerThird - Bottom Left")
    add_overlay_with_title(
        5,
        "LowerThird",
        "Name tags and context - bottom left",
        {
            "type": "LowerThird",
            "config": {
                "name": "Sarah Johnson",
                "title": "Chief Technology Officer",
                "variant": "modern",
                "position": "bottom_left"
            },
            "content": {
                "type": "DemoBox",
                "config": {
                    "label": "Interview Footage\n\n👤",
                    "color": "accent"
                }
            }
        }
    )

    # ========================================
    # 6. LOWER THIRD - Bottom Right
    # ========================================
    print("\n📍 6. LowerThird - Bottom Right")
    add_overlay_with_title(
        6,
        "LowerThird",
        "Name tags - bottom right position",
        {
            "type": "LowerThird",
            "config": {
                "name": "Alex Chen",
                "title": "Senior Software Engineer",
                "variant": "glass",
                "position": "bottom_right"
            },
            "content": {
                "type": "DemoBox",
                "config": {
                    "label": "Demo Content\n\n💻",
                    "color": "secondary"
                }
            }
        }
    )

    # ========================================
    # 7. SUBSCRIBE BUTTON
    # ========================================
    print("\n🔔 7. SubscribeButton")
    add_overlay_with_title(
        7,
        "SubscribeButton",
        "Animated call-to-action button",
        {
            "type": "SubscribeButton",
            "config": {
                "text": "Subscribe",
                "position": "bottom_right",
                "show_bell": True,
                "animate": True
            },
            "content": {
                "type": "DemoBox",
                "config": {
                    "label": "Video Content\n\nDon't forget to subscribe!",
                    "color": "primary"
                }
            }
        }
    )

    # ========================================
    # 8. END SCREEN
    # ========================================
    print("\n🎬 8. EndScreen")
    add_overlay_with_title(
        8,
        "EndScreen",
        "Professional video ending",
        {
            "type": "EndScreen",
            "config": {
                "title": "Thanks for Watching!",
                "subtitle": "Don't forget to like and subscribe",
                "show_social": True,
                "social_handles": {
                    "twitter": "@yourhandle",
                    "youtube": "YourChannel"
                }
            }
        }
    )

    # ========================================
    # COMBINED OVERLAYS SCENE
    # ========================================
    print("\n🎬 Creating Combined Overlays Scene")
    add_scene({
        "type": "LowerThird",
        "config": {
            "name": "Multiple Overlays",
            "title": "Combining different overlay types",
            "variant": "modern",
            "position": "bottom_left"
        },
        "content": {
            "type": "SubscribeButton",
            "config": {
                "text": "Subscribe",
                "position": "bottom_right",
                "show_bell": True,
                "animate": True
            },
            "content": {
                "type": "TextOverlay",
                "config": {
                    "text": "Overlays can be combined!",
                    "position": "top_center",
                    "font_size": 36,
                    "background_opacity": 0.8
                },
                "content": {
                    "type": "DemoBox",
                    "config": {
                        "label": "Base Content\n\nWith multiple overlays",
                        "color": "accent"
                    }
                }
            }
        }
    }, duration=150)

    # ========================================
    # FINAL TITLE
    # ========================================
    print("\n🎬 Creating Final Title")
    add_scene({
        "type": "EndScreen",
        "config": {
            "title": "Professional Overlays",
            "subtitle": "6 Components • Infinite Combinations",
            "show_social": False
        }
    })

    # ========================================
    # Build the composition
    # ========================================
    print("\n🎬 Building composition...")

    result = project_manager.build_composition_from_scenes(scenes, theme=theme)

    print("\n" + "="*70)
    print("✅ OVERLAYS SHOWCASE GENERATED!")
    print("="*70)
    print(f"\n📁 Project location: {project_path}")

    # Calculate stats
    total_frames = result['total_frames']
    total_duration = total_frames / 30.0

    print(f"\n⏱️  Total duration: {total_duration:.1f} seconds ({total_frames} frames @ 30fps)")
    print("\n📊 Showcase structure:")
    print("   • Introduction: 1 scene")
    print("   • Individual Overlays: 8 overlays × 2 scenes = 16 scenes")
    print("   • Combined Overlays: 1 scene")
    print("   • Final End Screen: 1 scene")
    print(f"   • TOTAL: {len(scenes)} scenes")

    print("\n🎨 Overlay Components Showcased:")
    print("   ✓ TitleScene (Bold, Glass, Minimal variants)")
    print("   ✓ TextOverlay - Floating text positioning")
    print("   ✓ LowerThird - Name tags (left & right)")
    print("   ✓ SubscribeButton - Animated CTA")
    print("   ✓ EndScreen - Video outro")

    print(f"\n📦 Generated {len(result['component_types'])} component types:")
    for comp_type in sorted(result['component_types']):
        print(f"   • {comp_type}")

    print(f"\n✨ Generated {len(result['component_files'])} TSX files")

    print("\n📝 Next steps:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")

    print("\n💡 This showcase demonstrates:")
    print("   ✓ All 6 professional overlay components")
    print("   ✓ Multiple variants and styles")
    print("   ✓ Different positioning options")
    print("   ✓ Overlay combinations and layering")
    print("   ✓ Animation effects")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n🎬 Overlays Showcase Generator")
    print("   Professional demonstration of all overlay components\n")

    try:
        generate_overlays_showcase()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
