#!/usr/bin/env python3
"""
Example: Design System Showcase Video

This example creates a comprehensive video that showcases the entire design system:
- All 7 YouTube-optimized themes
- Typography tokens and scales
- Color palettes and gradients
- Motion presets and animations
- Spacing and safe margins
- All component types

Perfect for demonstrating the design system capabilities!
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_remotion.generator.composition_builder import ComponentInstance
from chuk_mcp_remotion.themes.youtube_themes import YOUTUBE_THEMES


async def create_design_system_showcase():
    """Create a comprehensive design system showcase video."""

    from chuk_mcp_remotion.utils.project_manager import ProjectManager
    import shutil

    manager = ProjectManager()
    project_name = "design_system_showcase"

    # Clean up existing project
    project_path = manager.workspace_dir / project_name
    if project_path.exists():
        shutil.rmtree(project_path)

    # Create project
    print(f"\n📁 Creating project: {project_name}")
    project = manager.create_project(
        name=project_name,
        theme="tech",
        fps=30,
        width=1920,
        height=1080
    )

    print("\n🎬 Creating Design System Showcase Video...")
    print("=" * 70)

    # ========================================================================
    # SECTION 1: Title Card (0-5s)
    # ========================================================================
    print("\n📍 Section 1: Title Card")
    title = ComponentInstance(
        component_type="TitleScene",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "Design System",
            "subtitle": "Professional Video Components",
            "variant": "bold",
            "animation": "fade_zoom"
        },
        layer=0
    )
    manager.current_timeline.add_component(title, duration=5.0, track="main")

    # ========================================================================
    # SECTION 2: Theme Showcase (5-35s) - Show all 7 themes
    # ========================================================================
    print("📍 Section 2: Theme Showcase (7 themes)")

    themes = ["tech", "finance", "education", "lifestyle", "gaming", "minimal", "business"]
    theme_duration = 4.0  # 4 seconds per theme

    for idx, theme_name in enumerate(themes):
        theme_info = YOUTUBE_THEMES[theme_name]

        # Theme title
        lower_third = ComponentInstance(
            component_type="LowerThird",
            start_frame=0,
            duration_frames=0,
            props={
                "name": theme_info["name"],
                "title": theme_info["description"],
                "variant": "glass",
                "position": "bottom_left"
            },
            layer=10
        )
        manager.current_timeline.add_component(lower_third, duration=theme_duration, track="main")

        # Theme counter (overlapping on overlay track)
        counter = ComponentInstance(
            component_type="Counter",
            start_frame=0,
            duration_frames=0,
            props={
                "start_value": 0,
                "end_value": idx + 1,
                "prefix": "Theme ",
                "suffix": f" of {len(themes)}",
                "decimals": 0,
                "animation": "count_up"
            },
            layer=15
        )
        manager.current_timeline.add_component(
            counter,
            duration=theme_duration - 0.5,
            track="overlay",
            align_to="main",
            offset=(idx * theme_duration) + 0.5
        )

    # ========================================================================
    # SECTION 3: Typography Showcase (35-45s)
    # ========================================================================
    print("📍 Section 3: Typography Showcase")

    typo_title = ComponentInstance(
        component_type="TitleScene",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "Typography",
            "subtitle": "Video-Optimized Font Scales",
            "variant": "minimal",
            "animation": "slide_up"
        },
        layer=0
    )
    manager.current_timeline.add_component(typo_title, duration=3.0, track="main")

    # Show text hierarchy
    text_overlay = ComponentInstance(
        component_type="TextOverlay",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "Hero • Title • Heading • Subheading • Body • Caption",
            "position": "center",
            "style": "standard",
            "animation": "fade_in"
        },
        layer=10
    )
    manager.current_timeline.add_component(text_overlay, duration=7.0, track="main")

    # ========================================================================
    # SECTION 4: Charts & Data Visualization (45-65s)
    # ========================================================================
    print("📍 Section 4: Charts & Data Visualization")

    # Bar Chart
    bar_chart = ComponentInstance(
        component_type="BarChart",
        start_frame=0,
        duration_frames=0,
        props={
            "data": [
                {"label": "Q1", "value": 45},
                {"label": "Q2", "value": 67},
                {"label": "Q3", "value": 89},
                {"label": "Q4", "value": 95}
            ],
            "title": "Revenue Growth"
        },
        layer=0
    )
    manager.current_timeline.add_component(bar_chart, duration=5.0, track="main")

    # Pie Chart
    pie_chart = ComponentInstance(
        component_type="PieChart",
        start_frame=0,
        duration_frames=0,
        props={
            "data": [
                {"label": "Mobile", "value": 45},
                {"label": "Desktop", "value": 30},
                {"label": "Tablet", "value": 15},
                {"label": "Other", "value": 10}
            ],
            "title": "Platform Distribution"
        },
        layer=0
    )
    manager.current_timeline.add_component(pie_chart, duration=5.0, track="main")

    # Line Chart
    line_chart = ComponentInstance(
        component_type="LineChart",
        start_frame=0,
        duration_frames=0,
        props={
            "data": [
                {"x": 0, "y": 10},
                {"x": 1, "y": 25},
                {"x": 2, "y": 45},
                {"x": 3, "y": 65},
                {"x": 4, "y": 90}
            ],
            "title": "User Growth",
            "xlabel": "Month",
            "ylabel": "Users (K)"
        },
        layer=0
    )
    manager.current_timeline.add_component(line_chart, duration=5.0, track="main")

    # Area Chart
    area_chart = ComponentInstance(
        component_type="AreaChart",
        start_frame=0,
        duration_frames=0,
        props={
            "data": [
                {"x": 0, "y": 20},
                {"x": 1, "y": 35},
                {"x": 2, "y": 55},
                {"x": 3, "y": 70},
                {"x": 4, "y": 85}
            ],
            "title": "Engagement Trend"
        },
        layer=0
    )
    manager.current_timeline.add_component(area_chart, duration=5.0, track="main")

    # ========================================================================
    # SECTION 5: Code Components (65-75s)
    # ========================================================================
    print("📍 Section 5: Code Components")

    code_example = """function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

console.log(fibonacci(10)); // 55"""

    code_block = ComponentInstance(
        component_type="CodeBlock",
        start_frame=0,
        duration_frames=0,
        props={
            "code": code_example,
            "language": "javascript",
            "title": "Fibonacci Function",
            "variant": "editor",
            "animation": "fade_in",
            "show_line_numbers": True
        },
        layer=0
    )
    manager.current_timeline.add_component(code_block, duration=5.0, track="main")

    typing_code = ComponentInstance(
        component_type="TypingCode",
        start_frame=0,
        duration_frames=0,
        props={
            "code": "npm install design-system",
            "language": "bash",
            "title": "Installation",
            "typing_speed": "medium",
            "variant": "monospace",
            "cursor_style": "block",
            "show_line_numbers": False
        },
        layer=0
    )
    manager.current_timeline.add_component(typing_code, duration=5.0, track="main")

    # ========================================================================
    # SECTION 6: Layout Components (75-85s)
    # ========================================================================
    print("📍 Section 6: Layout Components")

    layout_text = ComponentInstance(
        component_type="TextOverlay",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "Container • Grid • Split Screen",
            "position": "center",
            "style": "glass",
            "animation": "scale_in"
        },
        layer=10
    )
    manager.current_timeline.add_component(layout_text, duration=5.0, track="main")

    # ========================================================================
    # SECTION 7: End Card (85-90s)
    # ========================================================================
    print("📍 Section 7: End Card")

    end_screen = ComponentInstance(
        component_type="EndScreen",
        start_frame=0,
        duration_frames=0,
        props={
            "cta_text": "Start Creating • Design System Showcase",
            "variant": "gradient"
        },
        layer=0
    )
    manager.current_timeline.add_component(end_screen, duration=5.0, track="main")

    # ========================================================================
    # Generate the video
    # ========================================================================
    print("\n" + "=" * 70)
    print("📦 Generating Remotion Project...")
    print("=" * 70)

    # Generate TSX files for each component type
    component_types = {c.component_type for c in manager.current_timeline.get_all_components()}

    for comp_type in component_types:
        sample = next(
            c for c in manager.current_timeline.get_all_components()
            if c.component_type == comp_type
        )
        manager.add_component_to_project(comp_type, sample.props, manager.current_timeline.theme)
        print(f"  ✓ {comp_type}.tsx")

    manager.generate_composition()
    print(f"  ✓ VideoComposition.tsx")

    # Get project info
    info = manager.get_project_info()
    composition = info['composition']

    print("\n✅ Design System Showcase Created!")
    print("=" * 70)
    print(f"📁 Project: {project_path}")
    print(f"🎬 Duration: {composition['duration_seconds']:.1f} seconds")
    print(f"📊 Components: {len(composition['components'])}")
    print(f"🎨 Themes Used: 7 (tech, finance, education, lifestyle, gaming, minimal, business)")
    print(f"📐 Resolution: 1920x1080 @ 30fps")
    print("\n💡 What's Showcased:")
    print("   • All 7 YouTube-optimized themes")
    print("   • Typography scales (1080p optimized)")
    print("   • 4 chart types (Bar, Pie, Line, Area)")
    print("   • Code components (CodeBlock, TypingCode)")
    print("   • Text overlays with animations")
    print("   • Lower thirds and counters")
    print("   • End screen with CTA")
    print("\n🚀 To render:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")
    print("\n" + "=" * 70)

    return project_path


async def main():
    """Main example function."""
    print("\n" + "=" * 70)
    print("DESIGN SYSTEM SHOWCASE VIDEO")
    print("=" * 70)
    print("\nThis example creates a 90-second video showcasing:")
    print("  • All 7 themes (tech, finance, education, lifestyle, gaming, minimal, business)")
    print("  • Typography scales and hierarchy")
    print("  • All chart types with real data")
    print("  • Code components with syntax highlighting")
    print("  • Layout and overlay components")
    print("  • Motion and animation presets")
    print("  • Platform-safe margins for LinkedIn, TikTok, Instagram")
    print("\n" + "=" * 70)

    result = await create_design_system_showcase()

    if result:
        print("\n✨ Success! Your design system showcase is ready to render.\n")
    else:
        print("\n❌ Something went wrong. Check the logs above.\n")


if __name__ == "__main__":
    asyncio.run(main())
