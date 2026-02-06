#!/usr/bin/env python3
"""
Image Content & Layouts Showcase

Demonstrates ImageContent component combined with various layouts.
Shows real-world use cases for images in different layout compositions.

NOTE: This example uses picsum.photos (free placeholder images) for demonstration.
      To use your own images:
      1. Add images to the project's public/ folder after generation
      2. Replace the URLs with local file paths (e.g., "my-image.jpg")

Usage:
    python examples/image_layouts_showcase.py
"""
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import shutil

from chuk_motion.utils.project_manager import ProjectManager


def create_image_content(src, **kwargs):
    """Helper to create an ImageContent component."""
    config = {"src": src}
    config.update(kwargs)
    return {"type": "ImageContent", "config": config}


def create_demo_box(label, color="primary"):
    """Helper to create a demo box component."""
    return {"type": "DemoBox", "config": {"label": label, "color": color}}


def generate_image_layouts_showcase():
    """Generate comprehensive showcase of ImageContent with layouts."""

    project_name = "image_layouts_showcase"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print("IMAGE CONTENT & LAYOUTS SHOWCASE")
    print("ImageContent Component + Layout Compositions")
    print(f"{'='*70}\n")

    # Create base project
    project_info = project_manager.create_project(project_name)
    project_path = Path(project_info["path"])

    print(f"✅ Created base project at: {project_path}")

    theme = "tech"
    scenes = []
    start_frame = 0
    scene_duration = 150  # 5 seconds per scene at 30fps
    title_duration = 60   # 2 seconds for title slides

    # Helper to add scene and increment start_frame
    def add_scene(scene_dict, duration=scene_duration):
        nonlocal start_frame
        scene_dict["startFrame"] = start_frame
        scene_dict["durationInFrames"] = duration
        scenes.append(scene_dict)
        start_frame += duration

    def add_demo_with_title(number, name, description, demo_scene_dict):
        """Add a title slide followed by the demo."""
        add_scene({
            "type": "TitleScene",
            "config": {
                "text": f"{number}. {name}",
                "subtitle": description,
                "variant": "minimal",
                "animation": "fade"
            }
        }, duration=title_duration)
        add_scene(demo_scene_dict)

    # ========================================
    # INTRODUCTION
    # ========================================
    print("\n🎬 Creating Introduction")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Image Layouts",
            "subtitle": "ImageContent Component Showcase",
            "variant": "bold",
            "animation": "fade_zoom"
        }
    }, duration=90)

    # ========================================
    # 1. BASIC IMAGE CONTENT - Cover Fit
    # ========================================
    print("\n🖼️  1. Basic ImageContent - Cover")
    add_demo_with_title(
        1,
        "Basic Image",
        "Full-screen image with cover fit",
        create_image_content(
            "https://picsum.photos/1920/1080",
            fit="cover"
        )
    )

    # ========================================
    # 2. IMAGE CONTENT - Contain Fit
    # ========================================
    print("\n🖼️  2. ImageContent - Contain")
    add_demo_with_title(
        2,
        "Contained Image",
        "Image fitted within bounds",
        create_image_content(
            "https://picsum.photos/1200/1200",
            fit="contain"
        )
    )

    # ========================================
    # 3. IMAGE WITH OPACITY
    # ========================================
    print("\n🖼️  3. Image with Opacity")
    add_demo_with_title(
        3,
        "Semi-Transparent",
        "Image overlay with 50% opacity",
        create_image_content(
            "https://picsum.photos/1920/1080?random=1",
            fit="cover",
            opacity=0.5
        )
    )

    # ========================================
    # 4. ROUNDED IMAGE
    # ========================================
    print("\n🖼️  4. Rounded Corners")
    add_demo_with_title(
        4,
        "Border Radius",
        "Image with 30px rounded corners",
        create_image_content(
            "https://picsum.photos/1200/1200?random=2",
            fit="cover",
            border_radius=30
        )
    )

    # ========================================
    # 5. GRID LAYOUT - Image Gallery
    # ========================================
    print("\n🎨 5. Grid Layout - Photo Gallery")
    add_demo_with_title(
        5,
        "Photo Gallery",
        "2x2 grid of images",
        {
            "type": "Grid",
            "config": {
                "layout": "2x2",
                "padding": 40,
                "gap": 20,
                "border_width": 2
            },
            "children": [
                create_image_content("https://picsum.photos/800/800?random=3", fit="cover"),
                create_image_content("https://picsum.photos/800/800?random=4", fit="cover"),
                create_image_content("https://picsum.photos/800/800?random=5", fit="cover"),
                create_image_content("https://picsum.photos/800/800?random=6", fit="cover")
            ]
        }
    )

    # ========================================
    # 6. SPLIT SCREEN - Before/After
    # ========================================
    print("\n🎨 6. Split Screen - Before/After")
    add_demo_with_title(
        6,
        "Before/After",
        "Split screen image comparison",
        {
            "type": "SplitScreen",
            "config": {
                "orientation": "vertical",
                "split_position": 50,
                "show_divider": True,
                "divider_width": 4
            },
            "children": [
                create_image_content("https://picsum.photos/960/1080?random=7", fit="cover"),
                create_image_content("https://picsum.photos/960/1080?random=8", fit="cover")
            ]
        }
    )

    # ========================================
    # 7. THREE COLUMN LAYOUT - Product Showcase
    # ========================================
    print("\n🎨 7. Three Column - Product Showcase")
    add_demo_with_title(
        7,
        "Product Showcase",
        "Three product images side-by-side",
        {
            "type": "ThreeColumnLayout",
            "config": {
                "column_ratios": [1, 1, 1],
                "gap": 30,
                "padding": 40
            },
            "children": [
                create_image_content("https://picsum.photos/600/900?random=9", fit="contain"),
                create_image_content("https://picsum.photos/600/900?random=10", fit="contain"),
                create_image_content("https://picsum.photos/600/900?random=11", fit="contain")
            ]
        }
    )

    # ========================================
    # 8. CONTAINER - Centered Image
    # ========================================
    print("\n🎨 8. Container - Centered")
    add_demo_with_title(
        8,
        "Centered Image",
        "Image in centered container with padding",
        {
            "type": "Container",
            "config": {
                "padding": 100,
                "border_width": 3,
                "border_radius": 20,
                "background_opacity": 0.1
            },
            "children": [
                create_image_content("https://picsum.photos/800/600?random=12", fit="contain")
            ]
        }
    )

    # ========================================
    # 9. PICTURE-IN-PICTURE
    # ========================================
    print("\n🎨 9. Picture-in-Picture")
    add_demo_with_title(
        9,
        "PiP Layout",
        "Small image overlay on larger image",
        {
            "type": "PiP",
            "config": {
                "pip_size": 25,
                "pip_position": "bottom-right",
                "padding": 30,
                "corner_radius": 15
            },
            "children": [
                create_image_content("https://picsum.photos/1920/1080?random=13", fit="cover"),
                create_image_content("https://picsum.photos/600/400?random=14", fit="cover")
            ]
        }
    )

    # ========================================
    # 10. ASYMMETRIC LAYOUT - Hero Section
    # ========================================
    print("\n🎨 10. Asymmetric - Hero Section")
    add_demo_with_title(
        10,
        "Hero Section",
        "Large image + content area",
        {
            "type": "AsymmetricLayout",
            "config": {
                "orientation": "horizontal",
                "main_ratio": 60,
                "padding": 40,
                "gap": 30
            },
            "children": [
                create_image_content("https://picsum.photos/1200/900?random=15", fit="cover"),
                create_demo_box("Hero Content\n\nTitle\nSubtitle\nCTA Button", "accent")
            ]
        }
    )

    # ========================================
    # 11. THREE ROW LAYOUT - Feature Stack
    # ========================================
    print("\n🎨 11. Three Row - Feature Stack")
    add_demo_with_title(
        11,
        "Feature Stack",
        "Stacked feature images",
        {
            "type": "ThreeRowLayout",
            "config": {
                "row_ratios": [1, 1, 1],
                "gap": 20,
                "padding": 30
            },
            "children": [
                create_image_content("https://picsum.photos/1920/400?random=16", fit="cover", border_radius=10),
                create_image_content("https://picsum.photos/1920/400?random=17", fit="cover", border_radius=10),
                create_image_content("https://picsum.photos/1920/400?random=18", fit="cover", border_radius=10)
            ]
        }
    )

    # ========================================
    # 12. MOSAIC - Image Collage
    # ========================================
    print("\n🎨 12. Mosaic - Image Collage")
    add_demo_with_title(
        12,
        "Image Collage",
        "Mosaic layout with mixed images",
        {
            "type": "Mosaic",
            "config": {
                "padding": 50,
                "gap": 15
            },
            "children": [
                create_image_content("https://picsum.photos/900/600?random=19", fit="cover"),
                create_image_content("https://picsum.photos/900/600?random=20", fit="cover"),
                create_image_content("https://picsum.photos/900/600?random=21", fit="cover"),
                create_image_content("https://picsum.photos/900/600?random=22", fit="cover")
            ]
        }
    )

    # ========================================
    # 13. BROWSER FRAME - Screenshot
    # ========================================
    print("\n🖼️  13. Browser Frame - Screenshot")
    add_demo_with_title(
        13,
        "Browser Screenshot",
        "Website screenshot in browser frame",
        {
            "type": "BrowserFrame",
            "config": {
                "url": "https://example.com",
                "theme": "light",
                "show_url": True,
                "show_controls": True
            },
            "children": [
                create_image_content("https://picsum.photos/1400/900?random=23", fit="cover")
            ]
        }
    )

    # ========================================
    # 14. DEVICE FRAME - Mobile Screenshot
    # ========================================
    print("\n📱 14. Device Frame - Mobile")
    add_demo_with_title(
        14,
        "Mobile Screenshot",
        "App screenshot in phone frame",
        {
            "type": "DeviceFrame",
            "config": {
                "device": "phone",
                "orientation": "portrait",
                "scale": 1.0,
                "glare": True,
                "shadow": True,
                "position": "center"
            },
            "children": [
                create_image_content("https://picsum.photos/375/812?random=24", fit="cover")
            ]
        }
    )

    # ========================================
    # 15. OVERLAYS - Image with Text
    # ========================================
    print("\n🎨 15. Text Overlay on Image")
    add_demo_with_title(
        15,
        "Text Overlay",
        "Image background with text overlay",
        {
            "type": "Container",
            "config": {
                "padding": 0,
                "border_width": 0
            },
            "children": [
                create_image_content("https://picsum.photos/1920/1080?random=25", fit="cover"),
                {
                    "type": "TextOverlay",
                    "config": {
                        "text": "Beautiful Imagery",
                        "position": "bottom-left",
                        "background_opacity": 0.7,
                        "padding": 30
                    }
                }
            ]
        }
    )

    # ========================================
    # 16. TIMELINE - Image Progression
    # ========================================
    print("\n🎨 16. Timeline - Image Progression")
    add_demo_with_title(
        16,
        "Progress Timeline",
        "Images showing progression over time",
        {
            "type": "Timeline",
            "config": {
                "orientation": "horizontal",
                "padding": 40
            },
            "children": [
                create_image_content("https://picsum.photos/800/600?random=26", fit="contain")
            ]
        }
    )

    # ========================================
    # 17. COMPLEX COMPOSITION
    # ========================================
    print("\n🎨 17. Complex Composition")
    add_demo_with_title(
        17,
        "Complex Layout",
        "Multi-layer image composition",
        {
            "type": "Grid",
            "config": {
                "layout": "2x2",
                "padding": 30,
                "gap": 15,
                "border_width": 2
            },
            "children": [
                # Top-left: Rounded image
                create_image_content("https://picsum.photos/800/600?random=29", fit="cover", border_radius=20),
                # Top-right: Container with image
                {
                    "type": "Container",
                    "config": {
                        "padding": 20,
                        "border_width": 0,
                        "background_opacity": 0.05
                    },
                    "children": [
                        create_image_content("https://picsum.photos/700/700?random=30", fit="contain")
                    ]
                },
                # Bottom-left: Semi-transparent
                create_image_content("https://picsum.photos/800/600?random=31", fit="cover", opacity=0.7),
                # Bottom-right: Split images
                {
                    "type": "SplitScreen",
                    "config": {
                        "orientation": "horizontal",
                        "split_position": 50,
                        "show_divider": False
                    },
                    "children": [
                        create_image_content("https://picsum.photos/400/600?random=32", fit="cover"),
                        create_image_content("https://picsum.photos/400/600?random=33", fit="cover")
                    ]
                }
            ]
        }
    )

    # ========================================
    # FINAL SUMMARY
    # ========================================
    print("\n🎬 Creating Final Summary")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Image Layouts",
            "subtitle": "17 Examples • Endless Possibilities",
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
    print("✅ IMAGE LAYOUTS SHOWCASE GENERATED!")
    print("="*70)
    print(f"\n📁 Project location: {project_path}")

    # Calculate stats
    total_frames = result['total_frames']
    total_duration = total_frames / 30.0

    print(f"\n⏱️  Total duration: {total_duration:.1f} seconds ({total_frames} frames @ 30fps)")
    print("\n📊 Showcase structure:")
    print("   • Introduction: 1 scene")
    print("   • Image Demos: 17 × 2 scenes = 34 scenes")
    print("   • Final Summary: 1 scene")
    print(f"   • TOTAL: {len(scenes)} scenes")

    print("\n🖼️  Image Content Features:")
    print("   ✓ Cover, Contain, Fill fit modes")
    print("   ✓ Opacity control (0.0 - 1.0)")
    print("   ✓ Border radius (rounded corners)")
    print("   ✓ Local files & remote URLs")

    print("\n🎨 Layouts Demonstrated:")
    print("   ✓ Grid - Photo galleries")
    print("   ✓ SplitScreen - Before/after comparisons")
    print("   ✓ ThreeColumnLayout - Product showcases")
    print("   ✓ Container - Centered images")
    print("   ✓ PiP - Picture-in-picture overlays")
    print("   ✓ AsymmetricLayout - Hero sections")
    print("   ✓ ThreeRowLayout - Feature stacks")
    print("   ✓ Mosaic - Image collages")
    print("   ✓ BrowserFrame - Screenshots")
    print("   ✓ DeviceFrame - Mobile mockups")
    print("   ✓ TextOverlay - Image + text")
    print("   ✓ Timeline - Image progressions")

    print(f"\n📦 Generated {len(result['component_types'])} component types:")
    for comp_type in sorted(result['component_types']):
        print(f"   • {comp_type}")

    print(f"\n✨ Generated {len(result['component_files'])} TSX files")

    print("\n💡 Real-World Use Cases:")
    print("   • Product photography galleries")
    print("   • Before/after transformations")
    print("   • App/website screenshots")
    print("   • Brand/logo displays")
    print("   • Feature visualizations")
    print("   • Social media content")
    print("   • Marketing materials")
    print("   • Portfolio presentations")

    print("\n📝 Next steps:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")
    print("\n   📸 Images: Using picsum.photos placeholder service")
    print("   💡 To use your own images:")
    print("      1. Add images to {project_path}/public/")
    print("      2. Update src paths in composition (e.g., 'my-image.jpg')")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n🖼️  Image Content & Layouts Showcase Generator")
    print("   Comprehensive examples of ImageContent with various layouts\n")

    try:
        generate_image_layouts_showcase()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
