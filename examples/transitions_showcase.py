#!/usr/bin/env python3
"""
Transitions Showcase

Demonstrates all 2 transition components with various effects.
Shows: LayoutTransition, PixelTransition

Usage:
    python examples/transitions_showcase.py
"""
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_motion.utils.project_manager import ProjectManager
import shutil


def generate_transitions_showcase():
    """Generate comprehensive showcase of all transition components."""

    project_name = "transitions_showcase"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print(f"TRANSITIONS SHOWCASE")
    print(f"All 2 Transition Components")
    print(f"{'='*70}\n")

    # Create base project
    project_info = project_manager.create_project(project_name)
    project_path = Path(project_info["path"])

    print(f"✅ Created base project at: {project_path}")

    theme = "tech"
    scenes = []
    start_frame = 0
    scene_duration = 150  # 5 seconds per transition at 30fps
    title_duration = 60   # 2 seconds for title slides

    # Helper to add scene and increment start_frame
    def add_scene(scene_dict, duration=scene_duration):
        nonlocal start_frame
        scene_dict["startFrame"] = start_frame
        scene_dict["durationInFrames"] = duration
        scenes.append(scene_dict)
        start_frame += duration

    def add_transition_with_title(number, name, description, transition_scene_dict):
        """Add a title slide followed by the transition demo."""
        add_scene({
            "type": "TitleScene",
            "config": {
                "text": f"{number}. {name}",
                "subtitle": description,
                "variant": "minimal",
                "animation": "fade"
            }
        }, duration=title_duration)
        add_scene(transition_scene_dict)

    # ========================================
    # INTRODUCTION
    # ========================================
    print("\n🎬 Creating Introduction")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Transitions Showcase",
            "subtitle": "2 Professional Transition Components",
            "variant": "bold",
            "animation": "fade_zoom"
        }
    }, duration=90)

    # ========================================
    # 1. LAYOUT TRANSITION - Fade
    # ========================================
    print("\n🔄 1. LayoutTransition - Fade")
    add_transition_with_title(
        1,
        "LayoutTransition",
        "Smooth fade between layouts - fade",
        {
            "type": "LayoutTransition",
            "config": {
                "transition_type": "fade",
                "duration": 1.0,
                "trigger_time": 2.0
            },
            "before": {
                "type": "DemoBox",
                "config": {
                    "label": "Before\n\nOriginal content",
                    "color": "primary"
                }
            },
            "after": {
                "type": "DemoBox",
                "config": {
                    "label": "After\n\nNew content",
                    "color": "accent"
                }
            }
        }
    )

    # ========================================
    # 2. LAYOUT TRANSITION - Slide Left
    # ========================================
    print("\n🔄 2. LayoutTransition - Slide Left")
    add_transition_with_title(
        2,
        "LayoutTransition",
        "Slide from right to left",
        {
            "type": "LayoutTransition",
            "config": {
                "transition_type": "slide_left",
                "duration": 1.2,
                "trigger_time": 2.0
            },
            "before": {
                "type": "DemoBox",
                "config": {
                    "label": "Current →\n\nSlides out left",
                    "color": "secondary"
                }
            },
            "after": {
                "type": "DemoBox",
                "config": {
                    "label": "← Next\n\nSlides in from right",
                    "color": "primary"
                }
            }
        }
    )

    # ========================================
    # 3. LAYOUT TRANSITION - Slide Right
    # ========================================
    print("\n🔄 3. LayoutTransition - Slide Right")
    add_transition_with_title(
        3,
        "LayoutTransition",
        "Slide from left to right",
        {
            "type": "LayoutTransition",
            "config": {
                "transition_type": "slide_right",
                "duration": 1.2,
                "trigger_time": 2.0
            },
            "before": {
                "type": "DemoBox",
                "config": {
                    "label": "← Current\n\nSlides out right",
                    "color": "accent"
                }
            },
            "after": {
                "type": "DemoBox",
                "config": {
                    "label": "Next →\n\nSlides in from left",
                    "color": "secondary"
                }
            }
        }
    )

    # ========================================
    # 4. LAYOUT TRANSITION - Zoom
    # ========================================
    print("\n🔄 4. LayoutTransition - Zoom")
    add_transition_with_title(
        4,
        "LayoutTransition",
        "Zoom in/out transition",
        {
            "type": "LayoutTransition",
            "config": {
                "transition_type": "zoom",
                "duration": 1.5,
                "trigger_time": 2.0
            },
            "before": {
                "type": "DemoBox",
                "config": {
                    "label": "Zoom Out\n\nShrinks away",
                    "color": "primary"
                }
            },
            "after": {
                "type": "DemoBox",
                "config": {
                    "label": "Zoom In\n\nGrows in",
                    "color": "accent"
                }
            }
        }
    )

    # ========================================
    # 5. PIXEL TRANSITION - Dissolve effect
    # ========================================
    print("\n🎨 5. PixelTransition - Dissolve")
    add_transition_with_title(
        5,
        "PixelTransition",
        "Pixelated dissolve effect",
        {
            "type": "PixelTransition",
            "config": {
                "transition_type": "dissolve",
                "duration": 1.5,
                "trigger_time": 2.0,
                "pixel_size": 20
            },
            "before": {
                "type": "DemoBox",
                "config": {
                    "label": "Scene A\n\nPixelates out",
                    "color": "primary"
                }
            },
            "after": {
                "type": "DemoBox",
                "config": {
                    "label": "Scene B\n\nPixelates in",
                    "color": "secondary"
                }
            }
        }
    )

    # ========================================
    # 6. PIXEL TRANSITION - Wipe
    # ========================================
    print("\n🎨 6. PixelTransition - Wipe")
    add_transition_with_title(
        6,
        "PixelTransition",
        "Pixelated wipe effect",
        {
            "type": "PixelTransition",
            "config": {
                "transition_type": "wipe",
                "duration": 1.8,
                "trigger_time": 2.0,
                "pixel_size": 15,
                "direction": "left_to_right"
            },
            "before": {
                "type": "DemoBox",
                "config": {
                    "label": "Old Content ▓\n\nWipes away",
                    "color": "accent"
                }
            },
            "after": {
                "type": "DemoBox",
                "config": {
                    "label": "▓ New Content\n\nWipes in",
                    "color": "primary"
                }
            }
        }
    )

    # ========================================
    # COMBINED - Transition between complex layouts
    # ========================================
    print("\n🎬 Creating Complex Transition")
    add_scene({
        "type": "LayoutTransition",
        "config": {
            "transition_type": "fade",
            "duration": 1.5,
            "trigger_time": 2.0
        },
        "before": {
            "type": "Grid",
            "config": {
                "layout": "2x2",
                "padding": 40,
                "gap": 20,
                "border_width": 2
            },
            "children": [
                {"type": "DemoBox", "config": {"label": "1", "color": "primary"}},
                {"type": "DemoBox", "config": {"label": "2", "color": "accent"}},
                {"type": "DemoBox", "config": {"label": "3", "color": "secondary"}},
                {"type": "DemoBox", "config": {"label": "4", "color": "primary"}}
            ]
        },
        "after": {
            "type": "SplitScreen",
            "config": {
                "orientation": "horizontal",
                "gap": 20,
                "divider_width": 2
            },
            "left": {
                "type": "DemoBox",
                "config": {
                    "label": "Left\n\nNew Layout",
                    "color": "accent"
                }
            },
            "right": {
                "type": "DemoBox",
                "config": {
                    "label": "Right\n\nNew Layout",
                    "color": "secondary"
                }
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
            "text": "Seamless Transitions",
            "subtitle": "LayoutTransition • PixelTransition",
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
    print("✅ TRANSITIONS SHOWCASE GENERATED!")
    print("="*70)
    print(f"\n📁 Project location: {project_path}")

    # Calculate stats
    total_frames = result['total_frames']
    total_duration = total_frames / 30.0

    print(f"\n⏱️  Total duration: {total_duration:.1f} seconds ({total_frames} frames @ 30fps)")
    print(f"\n📊 Showcase structure:")
    print(f"   • Introduction: 1 scene")
    print(f"   • Individual Transitions: 6 × 2 scenes = 12 scenes")
    print(f"   • Complex Transition: 1 scene")
    print(f"   • Final Title: 1 scene")
    print(f"   • TOTAL: {len(scenes)} scenes")

    print(f"\n🔄 Transition Components Showcased:")
    print("   ✓ LayoutTransition - Fade, slide, zoom")
    print("   ✓ PixelTransition - Dissolve, wipe")

    print(f"\n✨ Transition Types Demonstrated:")
    print("   • Fade transitions")
    print("   • Slide left/right")
    print("   • Zoom in/out")
    print("   • Pixelated dissolve")
    print("   • Pixelated wipe")
    print("   • Complex layout transitions")

    print(f"\n📦 Generated {len(result['component_types'])} component types:")
    for comp_type in sorted(result['component_types']):
        print(f"   • {comp_type}")

    print(f"\n✨ Generated {len(result['component_files'])} TSX files")

    print("\n📝 Next steps:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")

    print("\n💡 This showcase demonstrates:")
    print("   ✓ All 2 professional transition components")
    print("   ✓ Multiple transition effects")
    print("   ✓ Different durations and timing")
    print("   ✓ Transitions between simple and complex layouts")
    print("   ✓ Smooth visual effects")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n🔄 Transitions Showcase Generator")
    print("   Professional demonstration of all transition components\n")

    try:
        project_path = generate_transitions_showcase()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
