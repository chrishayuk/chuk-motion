#!/usr/bin/env python3
"""
Layout Animations Showcase

Demonstrates the three new layout animation components:
1. LayoutTransition - Scene-to-scene layout transitions
2. LayoutEntrance - Universal entrance animations for any layout
3. PanelCascade - Staggered panel entrance animations

Run this to generate a comprehensive showcase video demonstrating
all animation variants with proper motion token integration.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_motion.utils.project_manager import ProjectManager
from chuk_motion.generator.composition_builder import ComponentInstance
import shutil


async def main():
    """Generate layout animations showcase video."""

    # ============================================================================
    # 1. CREATE PROJECT
    # ============================================================================
    print("🎬 Creating Layout Animations Showcase project...")

    manager = ProjectManager()
    project_name = "layout_animations_showcase"

    # Clean up existing project
    project_path = manager.workspace_dir / project_name
    if project_path.exists():
        shutil.rmtree(project_path)

    # Create project
    project = manager.create_project(
        name=project_name,
        theme="tech",
        fps=30,
        width=1920,
        height=1080
    )
    print(f"✅ Project created: {project_name}")

    # ============================================================================
    # 2. LAYOUT ENTRANCE SHOWCASE - DRAMATIC FULL-SCREEN EXAMPLES
    # ============================================================================
    print("\n🎭 Section 1: LayoutEntrance Showcase")

    # Example 1: Large hero code block with fade_in (0-4s)
    hero_code = ComponentInstance(
        component_type="CodeBlock",
        start_frame=0,
        duration_frames=0,
        props={
            "code": """// Welcome to Layout Animations
const showcase = {
  entrance: "Smooth fade transitions",
  cascade: "Staggered panel reveals",
  transition: "Scene-to-scene morphing"
};

// Token-first motion design
animate(showcase, {
  duration: motion.duration.medium,
  easing: motion.easing.ease_out_expo
});""",
            "language": "javascript",
            "title": "Layout Animations Demo",
            "variant": "editor",
        },
        layer=0
    )

    entrance1 = ComponentInstance(
        component_type="LayoutEntrance",
        start_frame=0,
        duration_frames=0,
        props={
            "content": hero_code,
            "entranceType": "fade_in",
            "entranceDelay": 0.0
        },
        layer=0
    )
    manager.current_timeline.add_component(entrance1, duration=4.0, track="main")

    # Example 2: Large full-screen code with blur_in (4-8s)
    large_code = ComponentInstance(
        component_type="CodeBlock",
        start_frame=0,
        duration_frames=0,
        props={
            "code": """// Cinematic blur entrance
function createMagic() {
  return (
    <LayoutEntrance entranceType="blur_in">
      <YourContent />
    </LayoutEntrance>
  );
}

// Smooth, professional, effortless
// That's the power of motion tokens ✨""",
            "language": "typescript",
            "title": "Blur In Animation",
            "variant": "editor",
        },
        layer=0
    )

    entrance2 = ComponentInstance(
        component_type="LayoutEntrance",
        start_frame=0,
        duration_frames=0,
        props={
            "content": large_code,
            "entranceType": "blur_in",
            "entranceDelay": 0.0
        },
        layer=0
    )
    manager.current_timeline.add_component(entrance2, duration=4.0, track="main")

    # Example 3: Large 2x2 grid with zoom_in (8-12s)
    large_grid = ComponentInstance(
        component_type="Grid",
        start_frame=0,
        duration_frames=0,
        props={
            "layout": "2x2",
            "items": [
                ComponentInstance("CodeBlock", 0, 0, {
                    "code": "// Fade In\nopacity: 0 → 1",
                    "language": "javascript",
                    "title": "Smooth Entry"
                }, 0),
                ComponentInstance("CodeBlock", 0, 0, {
                    "code": "// Scale Pop\nscale: 0.9 → 1.0",
                    "language": "javascript",
                    "title": "Bouncy Feel"
                }, 0),
                ComponentInstance("CodeBlock", 0, 0, {
                    "code": "// Slide Up\ntranslateY: 30 → 0",
                    "language": "javascript",
                    "title": "Directional"
                }, 0),
                ComponentInstance("CodeBlock", 0, 0, {
                    "code": "// Blur In\nblur: 20px → 0",
                    "language": "javascript",
                    "title": "Cinematic"
                }, 0),
            ]
        },
        layer=0
    )

    entrance3 = ComponentInstance(
        component_type="LayoutEntrance",
        start_frame=0,
        duration_frames=0,
        props={
            "content": large_grid,
            "entranceType": "zoom_in",
            "entranceDelay": 0.0
        },
        layer=0
    )
    manager.current_timeline.add_component(entrance3, duration=4.0, track="main")

    print("  ✓ Added 3 dramatic LayoutEntrance examples")

    # ============================================================================
    # 3. PANEL CASCADE SHOWCASE - DRAMATIC STAGGERED REVEALS
    # ============================================================================
    print("\n✨ Section 2: PanelCascade Showcase")

    # Large 3x2 grid with from_center cascade (12-16s)
    cascade1 = ComponentInstance(
        component_type="PanelCascade",
        start_frame=0,
        duration_frames=0,
        props={
            "items": [
                ComponentInstance("CodeBlock", 0, 0, {
                    "code": "// Center Panel\nstagger: 0ms",
                    "language": "javascript",
                    "title": "Origin"
                }, 0),
                ComponentInstance("CodeBlock", 0, 0, {
                    "code": "// Ring 1\nstagger: 80ms",
                    "language": "javascript",
                    "title": "Layer 1"
                }, 0),
                ComponentInstance("CodeBlock", 0, 0, {
                    "code": "// Ring 1\nstagger: 80ms",
                    "language": "javascript",
                    "title": "Layer 1"
                }, 0),
                ComponentInstance("CodeBlock", 0, 0, {
                    "code": "// Ring 2\nstagger: 160ms",
                    "language": "javascript",
                    "title": "Layer 2"
                }, 0),
                ComponentInstance("CodeBlock", 0, 0, {
                    "code": "// Ring 2\nstagger: 160ms",
                    "language": "javascript",
                    "title": "Layer 2"
                }, 0),
                ComponentInstance("CodeBlock", 0, 0, {
                    "code": "// Ring 2\nstagger: 160ms",
                    "language": "javascript",
                    "title": "Layer 2"
                }, 0),
            ],
            "cascadeType": "from_center",
            "staggerDelay": 0.08
        },
        layer=0
    )
    manager.current_timeline.add_component(cascade1, duration=4.0, track="main")

    # Large 2x3 grid with wave cascade (16-20s)
    cascade2 = ComponentInstance(
        component_type="PanelCascade",
        start_frame=0,
        duration_frames=0,
        props={
            "items": [
                ComponentInstance("CodeBlock", 0, 0, {
                    "code": f"// Wave {i+1}\nconst animate = () => {{\n  return cascade({i})\n}}",
                    "language": "javascript",
                    "title": f"Panel {i+1}"
                }, 0)
                for i in range(6)
            ],
            "cascadeType": "wave",
            "staggerDelay": 0.1
        },
        layer=0
    )
    manager.current_timeline.add_component(cascade2, duration=4.0, track="main")

    print("  ✓ Added 2 dramatic PanelCascade examples")

    # ============================================================================
    # 4. LAYOUT TRANSITION SHOWCASE - CINEMATIC SCENE CHANGES
    # ============================================================================
    print("\n📐 Section 3: LayoutTransition Showcase")

    # Scene 1: Hero message
    first_scene = ComponentInstance(
        component_type="CodeBlock",
        start_frame=0,
        duration_frames=0,
        props={
            "code": """// Scene 1: The Problem
function traditionalAnimation() {
  // Complex frame-by-frame logic
  const frames = 60;
  for (let i = 0; i < frames; i++) {
    updateOpacity(i / frames);
    updatePosition(i);
    updateScale(i);
    render();
  }
}

// Tedious, error-prone, hard to maintain""",
            "language": "javascript",
            "title": "Traditional Approach",
            "variant": "editor",
        },
        layer=0
    )

    # Scene 2: The solution
    second_scene = ComponentInstance(
        component_type="CodeBlock",
        start_frame=0,
        duration_frames=0,
        props={
            "code": """// Scene 2: The Solution
<LayoutTransition
  transitionType="crossfade"
  transitionDuration={30}
>
  <FirstScene />
  <SecondScene />
</LayoutTransition>

// Declarative, smooth, token-driven
// Professional results, zero complexity ✨""",
            "language": "typescript",
            "title": "Modern Approach",
            "variant": "editor",
        },
        layer=0
    )

    # Dramatic crossfade transition (20-26s)
    transition1 = ComponentInstance(
        component_type="LayoutTransition",
        start_frame=0,
        duration_frames=0,
        props={
            "firstContent": first_scene,
            "secondContent": second_scene,
            "transitionType": "crossfade",
            "transitionStart": 60,  # 2 seconds in
            "transitionDuration": 45  # 1.5 second transition
        },
        layer=0
    )
    manager.current_timeline.add_component(transition1, duration=6.0, track="main")

    print("  ✓ Added cinematic LayoutTransition example")

    # ============================================================================
    # 5. GENERATE COMPOSITION
    # ============================================================================
    print("\n🎬 Generating composition...")
    composition_path = manager.generate_composition()
    print(f"✅ Composition generated: {composition_path}")

    # ============================================================================
    # 6. SUMMARY
    # ============================================================================
    print("\n✅ DRAMATIC showcase created!")
    print(f"\n📊 Timeline Summary:")
    print(f"   Duration: {manager.current_timeline.get_total_duration_seconds():.1f}s")
    print(f"   Components: {len(manager.current_timeline.get_all_components())}")
    print("\n💡 Motion Token Usage:")
    print("  • Durations: normal, medium, slow")
    print("  • Easings: ease_out_expo, ease_out_quint, ease_out_back")
    print("  • Springs: smooth, bouncy")
    print("\n🎯 What to see:")
    print("  • 0-4s: Hero code block with smooth fade")
    print("  • 4-8s: Full-screen code with cinematic blur")
    print("  • 8-12s: Large 2x2 grid zooming in")
    print("  • 12-16s: 6-panel from-center cascade")
    print("  • 16-20s: 6-panel wave cascade")
    print("  • 20-26s: Cinematic scene transition")
    print(f"\n📁 Project: {project_path}")
    print("🚀 Run: cd remotion-projects/layout_animations_showcase && npm start")
    print("\n✨ Much more dramatic and visually impressive!")


if __name__ == "__main__":
    asyncio.run(main())
