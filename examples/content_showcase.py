#!/usr/bin/env python3
"""
Content Components Showcase

Demonstrates all 5 content components with various use cases.
Shows: ImageContent, VideoContent, StylizedWebPage, WebPage, DemoBox

NOTE: ImageContent examples use picsum.photos (free placeholder images).
      To use your own images, add them to public/ and update the src paths.

Usage:
    python examples/content_showcase.py
"""
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import shutil

from chuk_motion.utils.project_manager import ProjectManager


def generate_content_showcase():
    """Generate comprehensive showcase of all content components."""

    project_name = "content_showcase"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print("CONTENT COMPONENTS SHOWCASE")
    print("All 5 Content Display Components")
    print(f"{'='*70}\n")

    # Create base project
    project_info = project_manager.create_project(project_name)
    project_path = Path(project_info["path"])

    print(f"✅ Created base project at: {project_path}")

    theme = "tech"
    scenes = []
    start_frame = 0
    scene_duration = 150  # 5 seconds per component at 30fps
    title_duration = 60   # 2 seconds for title slides

    # Helper to add scene and increment start_frame
    def add_scene(scene_dict, duration=scene_duration):
        nonlocal start_frame
        scene_dict["startFrame"] = start_frame
        scene_dict["durationInFrames"] = duration
        scenes.append(scene_dict)
        start_frame += duration

    def add_content_with_title(number, name, description, content_scene_dict):
        """Add a title slide followed by the content demo."""
        add_scene({
            "type": "TitleScene",
            "config": {
                "text": f"{number}. {name}",
                "subtitle": description,
                "variant": "minimal",
                "animation": "fade"
            }
        }, duration=title_duration)
        add_scene(content_scene_dict)

    # ========================================
    # INTRODUCTION
    # ========================================
    print("\n🎬 Creating Introduction")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Content Showcase",
            "subtitle": "5 Professional Content Components",
            "variant": "bold",
            "animation": "fade_zoom"
        }
    }, duration=90)

    # ========================================
    # 1. DEMO BOX - Simple placeholder
    # ========================================
    print("\n📦 1. DemoBox - Primary")
    add_content_with_title(
        1,
        "DemoBox",
        "Simple labeled placeholder - primary color",
        {
            "type": "DemoBox",
            "config": {
                "label": "Primary Demo Box\n\nPerfect for prototyping\nand placeholder content",
                "color": "primary"
            }
        }
    )

    # ========================================
    # 2. DEMO BOX - Accent
    # ========================================
    print("\n📦 2. DemoBox - Accent")
    add_content_with_title(
        2,
        "DemoBox",
        "Simple labeled placeholder - accent color",
        {
            "type": "DemoBox",
            "config": {
                "label": "Accent Demo Box\n\nQuick mockups\nVisual placeholders\nDraft compositions",
                "color": "accent"
            }
        }
    )

    # ========================================
    # 3. WEB PAGE - Raw HTML
    # ========================================
    print("\n🌐 3. WebPage - HTML Content")
    add_content_with_title(
        3,
        "WebPage",
        "Display raw HTML content",
        {
            "type": "WebPage",
            "config": {
                "html": '''
<div style="padding: 60px; font-family: -apple-system, sans-serif;">
  <h1 style="font-size: 48px; margin-bottom: 20px;">Welcome to WebPage</h1>
  <p style="font-size: 20px; opacity: 0.8; margin-bottom: 30px;">
    Display any HTML content directly in your video
  </p>

  <div style="display: flex; gap: 20px; margin-top: 40px;">
    <div style="flex: 1; padding: 20px; background: rgba(59, 130, 246, 0.1); border-radius: 8px;">
      <h3>Feature 1</h3>
      <p>Custom HTML</p>
    </div>
    <div style="flex: 1; padding: 20px; background: rgba(16, 185, 129, 0.1); border-radius: 8px;">
      <h3>Feature 2</h3>
      <p>Full Styling</p>
    </div>
    <div style="flex: 1; padding: 20px; background: rgba(245, 158, 11, 0.1); border-radius: 8px;">
      <h3>Feature 3</h3>
      <p>Flexible Layout</p>
    </div>
  </div>
</div>
                ''',
                "theme": "light"
            }
        }
    )

    # ========================================
    # 4. STYLIZED WEB PAGE - Structured
    # ========================================
    print("\n🎨 4. StylizedWebPage - Light Theme")
    add_content_with_title(
        4,
        "StylizedWebPage",
        "Pre-styled web page layout - light",
        {
            "type": "StylizedWebPage",
            "config": {
                "title": "Product Documentation",
                "subtitle": "Getting Started Guide",
                "showHeader": True,
                "showSidebar": True,
                "showFooter": True,
                "headerText": "Home • Docs • API • Support",
                "sidebarItems": [
                    "Introduction",
                    "Installation",
                    "Quick Start",
                    "API Reference",
                    "Examples"
                ],
                "contentLines": [
                    "# Getting Started",
                    "",
                    "Welcome to our comprehensive documentation.",
                    "",
                    "## Installation",
                    "npm install our-package",
                    "",
                    "## Quick Example",
                    "const app = createApp();",
                    "app.start();"
                ],
                "footerText": "© 2024 Our Company",
                "theme": "light",
                "accentColor": "primary"
            }
        }
    )

    # ========================================
    # 5. STYLIZED WEB PAGE - Dark Theme
    # ========================================
    print("\n🎨 5. StylizedWebPage - Dark Theme")
    add_content_with_title(
        5,
        "StylizedWebPage",
        "Pre-styled web page layout - dark",
        {
            "type": "StylizedWebPage",
            "config": {
                "title": "Dashboard",
                "subtitle": "Analytics Overview",
                "showHeader": True,
                "showSidebar": True,
                "showFooter": False,
                "headerText": "Dashboard • Reports • Settings",
                "sidebarItems": [
                    "Overview",
                    "Users",
                    "Revenue",
                    "Traffic",
                    "Performance"
                ],
                "contentLines": [
                    "Active Users: 1,234",
                    "",
                    "Revenue Today: $5,678",
                    "",
                    "Page Views: 45,678",
                    "",
                    "Avg Session: 5m 23s"
                ],
                "theme": "dark",
                "accentColor": "accent"
            }
        }
    )

    # ========================================
    # 6. IMAGE CONTENT - Cover Fit
    # ========================================
    print("\n🖼️  6. ImageContent - Cover")
    add_content_with_title(
        6,
        "ImageContent",
        "Image display with cover fit",
        {
            "type": "ImageContent",
            "config": {
                "src": "https://picsum.photos/1920/1080",
                "fit": "cover"
            }
        }
    )

    # ========================================
    # 7. IMAGE CONTENT - Rounded with Opacity
    # ========================================
    print("\n🖼️  7. ImageContent - Styled")
    add_content_with_title(
        7,
        "ImageContent",
        "Rounded corners with semi-transparency",
        {
            "type": "ImageContent",
            "config": {
                "src": "https://picsum.photos/1200/1200",
                "fit": "contain",
                "opacity": 0.8,
                "border_radius": 30
            }
        }
    )

    # ========================================
    # 8. VIDEO CONTENT - Placeholder
    # ========================================
    print("\n🎥 8. VideoContent")
    add_content_with_title(
        8,
        "VideoContent",
        "Video playback component",
        {
            "type": "DemoBox",
            "config": {
                "label": "🎥 Video Content\n\nPlaceholder for\nvideo playback",
                "color": "secondary"
            }
        }
    )

    # ========================================
    # COMBINED LAYOUT
    # ========================================
    print("\n🎬 Creating Combined Layout")
    add_scene({
        "type": "Grid",
        "config": {
            "layout": "2x2",
            "padding": 40,
            "gap": 20,
            "border_width": 2
        },
        "children": [
            {
                "type": "ImageContent",
                "config": {
                    "src": "https://picsum.photos/800/800",
                    "fit": "cover",
                    "border_radius": 10
                }
            },
            {
                "type": "StylizedWebPage",
                "config": {
                    "title": "Web Page",
                    "showHeader": True,
                    "showSidebar": False,
                    "contentLines": ["Content here"],
                    "theme": "light"
                }
            },
            {
                "type": "WebPage",
                "config": {
                    "html": '<div style="padding: 20px; text-align: center;"><h2>Raw HTML</h2><p>Custom content</p></div>',
                    "theme": "light"
                }
            },
            {
                "type": "ImageContent",
                "config": {
                    "src": "https://picsum.photos/900/900",
                    "fit": "cover",
                    "opacity": 0.7
                }
            }
        ]
    }, duration=150)

    # ========================================
    # FINAL TITLE
    # ========================================
    print("\n🎬 Creating Final Title")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Flexible Content",
            "subtitle": "5 Components • Endless Possibilities",
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
    print("✅ CONTENT SHOWCASE GENERATED!")
    print("="*70)
    print(f"\n📁 Project location: {project_path}")

    # Calculate stats
    total_frames = result['total_frames']
    total_duration = total_frames / 30.0

    print(f"\n⏱️  Total duration: {total_duration:.1f} seconds ({total_frames} frames @ 30fps)")
    print("\n📊 Showcase structure:")
    print("   • Introduction: 1 scene")
    print("   • Individual Components: 8 × 2 scenes = 16 scenes")
    print("   • Combined Grid: 1 scene")
    print("   • Final Title: 1 scene")
    print(f"   • TOTAL: {len(scenes)} scenes")

    print("\n📦 Content Components Showcased:")
    print("   ✓ DemoBox - Quick placeholders (primary & accent)")
    print("   ✓ WebPage - Raw HTML content display")
    print("   ✓ StylizedWebPage - Pre-styled layouts (light & dark)")
    print("   ✓ ImageContent - Image display (cover, contain, opacity, border radius)")
    print("   ✓ VideoContent - Placeholder (requires actual video file)")

    print("\n🎨 Features Demonstrated:")
    print("   • Multiple color themes")
    print("   • Light and dark modes")
    print("   • Header, sidebar, footer components")
    print("   • Custom HTML content")
    print("   • Grid layouts")

    print(f"\n📦 Generated {len(result['component_types'])} component types:")
    for comp_type in sorted(result['component_types']):
        print(f"   • {comp_type}")

    print(f"\n✨ Generated {len(result['component_files'])} TSX files")

    print("\n📝 Next steps:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")

    print("\n💡 This showcase demonstrates:")
    print("   ✓ All 5 professional content components")
    print("   ✓ Different styling approaches")
    print("   ✓ Theme variations")
    print("   ✓ Layout flexibility")
    print("   ✓ HTML content rendering")
    print("   ✓ Image display with fit modes")
    print("   ✓ Image opacity and border radius")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n📦 Content Components Showcase Generator")
    print("   Professional demonstration of all content display components\n")

    try:
        generate_content_showcase()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
