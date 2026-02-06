#!/usr/bin/env python3
"""
Charts Showcase

Demonstrates all 6 chart components with various data sets and configurations.
Shows: PieChart, LineChart, AreaChart, DonutChart, BarChart, HorizontalBarChart

Usage:
    python examples/charts_showcase.py
"""
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import shutil

from chuk_motion.utils.project_manager import ProjectManager


def generate_charts_showcase():
    """Generate comprehensive showcase of all chart components."""

    project_name = "charts_showcase"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print("CHARTS SHOWCASE")
    print("All 6 Chart Components")
    print(f"{'='*70}\n")

    # Create base project
    project_info = project_manager.create_project(project_name)
    project_path = Path(project_info["path"])

    print(f"✅ Created base project at: {project_path}")

    theme = "tech"
    scenes = []
    start_frame = 0
    scene_duration = 150  # 5 seconds per chart at 30fps
    title_duration = 60   # 2 seconds for title slides

    # Helper to add scene and increment start_frame
    def add_scene(scene_dict, duration=scene_duration):
        nonlocal start_frame
        scene_dict["startFrame"] = start_frame
        scene_dict["durationInFrames"] = duration
        scenes.append(scene_dict)
        start_frame += duration

    def add_chart_with_title(number, name, description, chart_scene_dict):
        """Add a title slide followed by the chart demo."""
        add_scene({
            "type": "TitleScene",
            "config": {
                "text": f"{number}. {name}",
                "subtitle": description,
                "variant": "minimal",
                "animation": "fade"
            }
        }, duration=title_duration)
        add_scene(chart_scene_dict)

    # ========================================
    # INTRODUCTION
    # ========================================
    print("\n🎬 Creating Introduction")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Charts Showcase",
            "subtitle": "6 Professional Chart Components",
            "variant": "bold",
            "animation": "fade_zoom"
        }
    }, duration=90)

    # ========================================
    # 1. PIE CHART
    # ========================================
    print("\n📊 1. PieChart")
    add_chart_with_title(
        1,
        "PieChart",
        "Classic pie chart for proportions",
        {
            "type": "PieChart",
            "config": {
                "data": [
                    {"label": "Product A", "value": 35},
                    {"label": "Product B", "value": 25},
                    {"label": "Product C", "value": 20},
                    {"label": "Product D", "value": 15},
                    {"label": "Product E", "value": 5}
                ],
                "title": "Market Share by Product",
                "show_legend": True,
                "show_labels": True
            }
        }
    )

    # ========================================
    # 2. LINE CHART
    # ========================================
    print("\n📈 2. LineChart")
    add_chart_with_title(
        2,
        "LineChart",
        "Line chart for trends over time",
        {
            "type": "LineChart",
            "config": {
                "data": [
                    [1, 120],
                    [2, 150],
                    [3, 180],
                    [4, 165],
                    [5, 220],
                    [6, 280],
                    [7, 320],
                    [8, 380]
                ],
                "title": "Revenue Growth",
                "xlabel": "Month",
                "ylabel": "Revenue ($K)",
                "show_grid": True,
                "animate": True
            }
        }
    )

    # ========================================
    # 3. AREA CHART
    # ========================================
    print("\n📊 3. AreaChart")
    add_chart_with_title(
        3,
        "AreaChart",
        "Area chart for cumulative metrics",
        {
            "type": "AreaChart",
            "config": {
                "data": [
                    [1, 30],
                    [2, 45],
                    [3, 60],
                    [4, 55],
                    [5, 75],
                    [6, 90],
                    [7, 110],
                    [8, 130]
                ],
                "title": "User Growth",
                "xlabel": "Week",
                "ylabel": "Active Users (K)",
                "show_grid": True,
                "fill_opacity": 0.3
            }
        }
    )

    # ========================================
    # 4. DONUT CHART
    # ========================================
    print("\n🍩 4. DonutChart")
    add_chart_with_title(
        4,
        "DonutChart",
        "Donut chart for modern proportions",
        {
            "type": "DonutChart",
            "config": {
                "data": [
                    {"label": "Frontend", "value": 40},
                    {"label": "Backend", "value": 30},
                    {"label": "DevOps", "value": 20},
                    {"label": "Testing", "value": 10}
                ],
                "title": "Team Allocation",
                "show_legend": True,
                "show_labels": True,
                "inner_radius": 0.6
            }
        }
    )

    # ========================================
    # 5. BAR CHART
    # ========================================
    print("\n📊 5. BarChart")
    add_chart_with_title(
        5,
        "BarChart",
        "Vertical bar chart for comparisons",
        {
            "type": "BarChart",
            "config": {
                "data": [
                    {"label": "Q1", "value": 145},
                    {"label": "Q2", "value": 180},
                    {"label": "Q3", "value": 220},
                    {"label": "Q4", "value": 280}
                ],
                "title": "Quarterly Sales",
                "xlabel": "Quarter",
                "ylabel": "Sales ($K)",
                "show_grid": True,
                "bar_color": "primary"
            }
        }
    )

    # ========================================
    # 6. HORIZONTAL BAR CHART
    # ========================================
    print("\n📊 6. HorizontalBarChart")
    add_chart_with_title(
        6,
        "HorizontalBarChart",
        "Horizontal bars for rankings",
        {
            "type": "HorizontalBarChart",
            "config": {
                "data": [
                    {"label": "Feature A", "value": 95},
                    {"label": "Feature B", "value": 82},
                    {"label": "Feature C", "value": 78},
                    {"label": "Feature D", "value": 65},
                    {"label": "Feature E", "value": 54}
                ],
                "title": "Feature Adoption Rate (%)",
                "xlabel": "Adoption %",
                "ylabel": "Feature",
                "show_grid": True,
                "bar_color": "accent"
            }
        }
    )

    # ========================================
    # COMPARISON SCENE
    # ========================================
    print("\n🎬 Creating Comparison Scene")
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
                "type": "PieChart",
                "config": {
                    "data": [
                        {"label": "A", "value": 40},
                        {"label": "B", "value": 30},
                        {"label": "C", "value": 30}
                    ],
                    "title": "Pie",
                    "show_legend": False
                }
            },
            {
                "type": "DonutChart",
                "config": {
                    "data": [
                        {"label": "X", "value": 50},
                        {"label": "Y", "value": 30},
                        {"label": "Z", "value": 20}
                    ],
                    "title": "Donut",
                    "show_legend": False
                }
            },
            {
                "type": "BarChart",
                "config": {
                    "data": [
                        {"label": "Mon", "value": 45},
                        {"label": "Tue", "value": 60},
                        {"label": "Wed", "value": 55}
                    ],
                    "title": "Bar",
                    "show_grid": False
                }
            },
            {
                "type": "LineChart",
                "config": {
                    "data": [[1, 30], [2, 45], [3, 60], [4, 55]],
                    "title": "Line",
                    "show_grid": False
                }
            }
        ]
    }, duration=180)

    # ========================================
    # FINAL TITLE
    # ========================================
    print("\n🎬 Creating Final Title")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Data Visualization",
            "subtitle": "6 Chart Types • Infinite Possibilities",
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
    print("✅ CHARTS SHOWCASE GENERATED!")
    print("="*70)
    print(f"\n📁 Project location: {project_path}")

    # Calculate stats
    total_frames = result['total_frames']
    total_duration = total_frames / 30.0

    print(f"\n⏱️  Total duration: {total_duration:.1f} seconds ({total_frames} frames @ 30fps)")
    print("\n📊 Showcase structure:")
    print("   • Introduction: 1 scene")
    print("   • Individual Charts: 6 charts × 2 scenes = 12 scenes")
    print("   • Comparison Grid: 1 scene")
    print("   • Final Title: 1 scene")
    print(f"   • TOTAL: {len(scenes)} scenes")

    print("\n📈 Chart Components Showcased:")
    print("   ✓ PieChart - Market share & proportions")
    print("   ✓ LineChart - Revenue trends over time")
    print("   ✓ AreaChart - Cumulative user growth")
    print("   ✓ DonutChart - Team allocation breakdown")
    print("   ✓ BarChart - Quarterly sales comparison")
    print("   ✓ HorizontalBarChart - Feature adoption ranking")

    print(f"\n📦 Generated {len(result['component_types'])} component types:")
    for comp_type in sorted(result['component_types']):
        print(f"   • {comp_type}")

    print(f"\n✨ Generated {len(result['component_files'])} TSX files")

    print("\n📝 Next steps:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")

    print("\n💡 This showcase demonstrates:")
    print("   ✓ All 6 professional chart components")
    print("   ✓ Different data types and formats")
    print("   ✓ Various styling options")
    print("   ✓ Grid layout with multiple charts")
    print("   ✓ Animations and transitions")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n📊 Charts Showcase Generator")
    print("   Professional demonstration of all chart components\n")

    try:
        generate_charts_showcase()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
