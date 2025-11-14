#!/usr/bin/env python3
"""
Animations Showcase

Demonstrates all 3 animation components with various configurations.
Shows: Counter, LayoutEntrance, PanelCascade

Usage:
    python examples/animations_showcase.py
"""
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_motion.utils.project_manager import ProjectManager
import shutil


def generate_animations_showcase():
    """Generate comprehensive showcase of all animation components."""

    project_name = "animations_showcase"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print(f"ANIMATIONS SHOWCASE")
    print(f"All 3 Animation Components")
    print(f"{'='*70}\n")

    # Create base project
    project_info = project_manager.create_project(project_name)
    project_path = Path(project_info["path"])

    print(f"✅ Created base project at: {project_path}")

    theme = "tech"
    scenes = []
    start_frame = 0
    scene_duration = 150  # 5 seconds per animation at 30fps
    title_duration = 60   # 2 seconds for title slides

    # Helper to add scene and increment start_frame
    def add_scene(scene_dict, duration=scene_duration):
        nonlocal start_frame
        scene_dict["startFrame"] = start_frame
        scene_dict["durationInFrames"] = duration
        scenes.append(scene_dict)
        start_frame += duration

    def add_animation_with_title(number, name, description, animation_scene_dict):
        """Add a title slide followed by the animation demo."""
        add_scene({
            "type": "TitleScene",
            "config": {
                "text": f"{number}. {name}",
                "subtitle": description,
                "variant": "minimal",
                "animation": "fade"
            }
        }, duration=title_duration)
        add_scene(animation_scene_dict)

    # ========================================
    # INTRODUCTION
    # ========================================
    print("\n🎬 Creating Introduction")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Animations Showcase",
            "subtitle": "3 Professional Animation Components",
            "variant": "bold",
            "animation": "fade_zoom"
        }
    }, duration=90)

    # ========================================
    # 1. COUNTER - Number animation
    # ========================================
    print("\n🔢 1. Counter - Basic")
    add_animation_with_title(
        1,
        "Counter",
        "Animated number counting",
        {
            "type": "Counter",
            "config": {
                "from": 0,
                "to": 1000,
                "duration": 4.0,
                "prefix": "$",
                "suffix": "",
                "decimals": 0,
                "font_size": 120,
                "easing": "easeOutCubic"
            }
        }
    )

    # ========================================
    # 2. COUNTER - Percentage
    # ========================================
    print("\n🔢 2. Counter - Percentage")
    add_animation_with_title(
        2,
        "Counter",
        "Percentage with suffix",
        {
            "type": "Counter",
            "config": {
                "from": 0,
                "to": 95.5,
                "duration": 3.5,
                "prefix": "",
                "suffix": "%",
                "decimals": 1,
                "font_size": 100,
                "easing": "easeInOutQuad"
            }
        }
    )

    # ========================================
    # 3. COUNTER - Revenue
    # ========================================
    print("\n🔢 3. Counter - Revenue")
    add_animation_with_title(
        3,
        "Counter",
        "Large number with decimals",
        {
            "type": "Counter",
            "config": {
                "from": 0,
                "to": 1234567.89,
                "duration": 4.5,
                "prefix": "$",
                "suffix": "",
                "decimals": 2,
                "font_size": 90,
                "easing": "easeOutExpo"
            }
        }
    )

    # ========================================
    # 4. LAYOUT ENTRANCE - Fade In
    # ========================================
    print("\n✨ 4. LayoutEntrance - Fade In")
    add_animation_with_title(
        4,
        "LayoutEntrance",
        "Fade in animation",
        {
            "type": "LayoutEntrance",
            "config": {
                "animation_type": "fade",
                "duration": 1.5,
                "delay": 0.5,
                "easing": "easeOut"
            },
            "content": {
                "type": "DemoBox",
                "config": {
                    "label": "Fade In\n\nSmooth entrance animation",
                    "color": "primary"
                }
            }
        }
    )

    # ========================================
    # 5. LAYOUT ENTRANCE - Slide From Left
    # ========================================
    print("\n✨ 5. LayoutEntrance - Slide Left")
    add_animation_with_title(
        5,
        "LayoutEntrance",
        "Slide from left",
        {
            "type": "LayoutEntrance",
            "config": {
                "animation_type": "slide_left",
                "duration": 1.0,
                "delay": 0.3,
                "easing": "easeInOut"
            },
            "content": {
                "type": "DemoBox",
                "config": {
                    "label": "Slide Left ←\n\nEnter from the left side",
                    "color": "accent"
                }
            }
        }
    )

    # ========================================
    # 6. LAYOUT ENTRANCE - Zoom
    # ========================================
    print("\n✨ 6. LayoutEntrance - Zoom")
    add_animation_with_title(
        6,
        "LayoutEntrance",
        "Zoom in from center",
        {
            "type": "LayoutEntrance",
            "config": {
                "animation_type": "zoom",
                "duration": 1.2,
                "delay": 0.2,
                "easing": "easeOutBack"
            },
            "content": {
                "type": "DemoBox",
                "config": {
                    "label": "Zoom In ⚡\n\nScale up entrance",
                    "color": "secondary"
                }
            }
        }
    )

    # ========================================
    # 7. PANEL CASCADE - Sequential reveal
    # ========================================
    print("\n🎯 7. PanelCascade - 3 Panels")
    add_animation_with_title(
        7,
        "PanelCascade",
        "Sequential panel animation",
        {
            "type": "PanelCascade",
            "config": {
                "stagger_delay": 0.3,
                "animation_duration": 0.8,
                "direction": "left_to_right"
            },
            "panels": [
                {
                    "type": "DemoBox",
                    "config": {
                        "label": "Panel 1\n\nFirst to appear",
                        "color": "primary"
                    }
                },
                {
                    "type": "DemoBox",
                    "config": {
                        "label": "Panel 2\n\nSecond",
                        "color": "accent"
                    }
                },
                {
                    "type": "DemoBox",
                    "config": {
                        "label": "Panel 3\n\nLast",
                        "color": "secondary"
                    }
                }
            ]
        }
    )

    # ========================================
    # 8. PANEL CASCADE - Top to Bottom
    # ========================================
    print("\n🎯 8. PanelCascade - Vertical")
    add_animation_with_title(
        8,
        "PanelCascade",
        "Top to bottom cascade",
        {
            "type": "PanelCascade",
            "config": {
                "stagger_delay": 0.4,
                "animation_duration": 1.0,
                "direction": "top_to_bottom"
            },
            "panels": [
                {
                    "type": "DemoBox",
                    "config": {
                        "label": "First ↓",
                        "color": "primary"
                    }
                },
                {
                    "type": "DemoBox",
                    "config": {
                        "label": "Second ↓",
                        "color": "accent"
                    }
                },
                {
                    "type": "DemoBox",
                    "config": {
                        "label": "Third ↓",
                        "color": "secondary"
                    }
                },
                {
                    "type": "DemoBox",
                    "config": {
                        "label": "Fourth ↓",
                        "color": "primary"
                    }
                }
            ]
        }
    )

    # ========================================
    # COMBINED - Counter with Layout Entrance
    # ========================================
    print("\n🎬 Creating Combined Animation")
    add_scene({
        "type": "LayoutEntrance",
        "config": {
            "animation_type": "zoom",
            "duration": 1.5,
            "delay": 0.5,
            "easing": "easeOutBack"
        },
        "content": {
            "type": "Counter",
            "config": {
                "from": 0,
                "to": 999,
                "duration": 3.0,
                "prefix": "",
                "suffix": " Users",
                "decimals": 0,
                "font_size": 80,
                "easing": "easeOutCubic"
            }
        }
    }, duration=180)

    # ========================================
    # FINAL TITLE
    # ========================================
    print("\n🎬 Creating Final Title")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Bring It To Life",
            "subtitle": "Counter • LayoutEntrance • PanelCascade",
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
    print("✅ ANIMATIONS SHOWCASE GENERATED!")
    print("="*70)
    print(f"\n📁 Project location: {project_path}")

    # Calculate stats
    total_frames = result['total_frames']
    total_duration = total_frames / 30.0

    print(f"\n⏱️  Total duration: {total_duration:.1f} seconds ({total_frames} frames @ 30fps)")
    print(f"\n📊 Showcase structure:")
    print(f"   • Introduction: 1 scene")
    print(f"   • Individual Animations: 8 × 2 scenes = 16 scenes")
    print(f"   • Combined Animation: 1 scene")
    print(f"   • Final Title: 1 scene")
    print(f"   • TOTAL: {len(scenes)} scenes")

    print(f"\n🎨 Animation Components Showcased:")
    print("   ✓ Counter - Numbers, percentages, revenue")
    print("   ✓ LayoutEntrance - Fade, slide, zoom")
    print("   ✓ PanelCascade - Sequential reveals")

    print(f"\n✨ Animation Types Demonstrated:")
    print("   • Number counting (linear, exponential)")
    print("   • Fade in transitions")
    print("   • Slide animations (left, right, top, bottom)")
    print("   • Zoom effects")
    print("   • Staggered cascades")

    print(f"\n📦 Generated {len(result['component_types'])} component types:")
    for comp_type in sorted(result['component_types']):
        print(f"   • {comp_type}")

    print(f"\n✨ Generated {len(result['component_files'])} TSX files")

    print("\n📝 Next steps:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")

    print("\n💡 This showcase demonstrates:")
    print("   ✓ All 3 professional animation components")
    print("   ✓ Multiple easing functions")
    print("   ✓ Various animation durations")
    print("   ✓ Stagger delays and timing")
    print("   ✓ Animation combinations")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n✨ Animations Showcase Generator")
    print("   Professional demonstration of all animation components\n")

    try:
        project_path = generate_animations_showcase()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
