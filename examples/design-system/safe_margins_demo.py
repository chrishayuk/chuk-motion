#!/usr/bin/env python3
"""
Example: Safe Margins Demo

Demonstrates platform-specific safe margins for:
- LinkedIn Feed
- Instagram Stories (9:16)
- TikTok
- YouTube
- Mobile formats

Shows how to ensure your content isn't cropped by platform UIs.
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_motion.generator.composition_builder import ComponentInstance
from chuk_motion.tokens.spacing import SPACING_TOKENS


async def create_safe_margins_demo():
    """Create a video demonstrating safe margins for different platforms."""

    import shutil

    from chuk_motion.utils.project_manager import ProjectManager

    manager = ProjectManager()
    project_name = "safe_margins_demo"

    # Clean up existing project
    project_path = manager.workspace_dir / project_name
    if project_path.exists():
        shutil.rmtree(project_path)

    # Create project (standard YouTube 16:9)
    print(f"\n📁 Creating project: {project_name}")
    manager.create_project(
        name=project_name,
        theme="tech",
        fps=30,
        width=1920,
        height=1080
    )

    print("\n🎬 Creating Safe Margins Demo Video...")
    print("=" * 70)

    # ========================================================================
    # SECTION 1: Title Card (0-5s)
    # ========================================================================
    print("\n📍 Section 1: Introduction")

    title = ComponentInstance(
        component_type="TitleScene",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "Safe Margins",
            "subtitle": "Platform-Specific Cropping Zones",
            "variant": "bold",
            "animation": "fade_zoom"
        },
        layer=0
    )
    manager.current_timeline.add_component(title, duration=5.0, track="main")

    # ========================================================================
    # SECTION 2: LinkedIn Safe Margins (5-15s)
    # ========================================================================
    print("📍 Section 2: LinkedIn Feed Margins")

    linkedin_margins = SPACING_TOKENS.safe_area['linkedin']

    linkedin_lower = ComponentInstance(
        component_type="LowerThird",
        start_frame=0,
        duration_frames=0,
        props={
            "name": "LinkedIn Feed",
            "title": f"Safe Zone: {linkedin_margins.left} horizontal, {linkedin_margins.top} vertical",
            "variant": "glass",
            "position": "bottom_left"
        },
        layer=10
    )
    manager.current_timeline.add_component(linkedin_lower, duration=8.0, track="main")

    linkedin_text = ComponentInstance(
        component_type="TextOverlay",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "⚠️ LinkedIn crops 8-24px from edges\nKeep text & graphics inside safe zone!",
            "position": "center",
            "style": "standard",
            "animation": "slide_up"
        },
        layer=15
    )
    manager.current_timeline.add_component(
        linkedin_text,
        duration=6.0,
        track="overlay",
        align_to="main",
        offset=7.0  # Start 2s after previous component (5s + 2s)
    )

    # ========================================================================
    # SECTION 3: Instagram Stories (15-25s)
    # ========================================================================
    print("📍 Section 3: Instagram Stories (9:16)")

    instagram_margins = SPACING_TOKENS.safe_area['instagram_story']

    instagram_lower = ComponentInstance(
        component_type="LowerThird",
        start_frame=0,
        duration_frames=0,
        props={
            "name": "Instagram Stories",
            "title": f"Top: {instagram_margins.top} | Bottom: {instagram_margins.bottom}",
            "variant": "animated",
            "position": "bottom_center"
        },
        layer=10
    )
    manager.current_timeline.add_component(instagram_lower, duration=8.0, track="main", gap_before=2.0)

    instagram_text = ComponentInstance(
        component_type="TextOverlay",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "📱 Stories overlay at top (100px) and bottom (120px)\nAvoid placing important content in these areas",
            "position": "center",
            "style": "glass",
            "animation": "fade_in"
        },
        layer=15
    )
    manager.current_timeline.add_component(
        instagram_text,
        duration=6.0,
        track="overlay",
        align_to="main",
        offset=17.0  # 15s + 2s
    )

    # ========================================================================
    # SECTION 4: TikTok Margins (25-35s)
    # ========================================================================
    print("📍 Section 4: TikTok Margins")

    tiktok_margins = SPACING_TOKENS.safe_area['tiktok']

    tiktok_lower = ComponentInstance(
        component_type="LowerThird",
        start_frame=0,
        duration_frames=0,
        props={
            "name": "TikTok",
            "title": f"Right side: {tiktok_margins.right} (buttons!) | Top: {tiktok_margins.top}",
            "variant": "bold",
            "position": "top_left"
        },
        layer=10
    )
    manager.current_timeline.add_component(tiktok_lower, duration=8.0, track="main", gap_before=2.0)

    tiktok_text = ComponentInstance(
        component_type="TextOverlay",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "🎵 TikTok has UI buttons on the right side\n80px right margin prevents overlap",
            "position": "center",
            "style": "standard",
            "animation": "scale_in"
        },
        layer=15
    )
    manager.current_timeline.add_component(
        tiktok_text,
        duration=6.0,
        track="overlay",
        align_to="main",
        offset=27.0  # 25s + 2s
    )

    # ========================================================================
    # SECTION 5: YouTube Long Form (35-45s)
    # ========================================================================
    print("📍 Section 5: YouTube Long Form")

    youtube_margins = SPACING_TOKENS.safe_area['youtube_long_form']

    youtube_lower = ComponentInstance(
        component_type="LowerThird",
        start_frame=0,
        duration_frames=0,
        props={
            "name": "YouTube",
            "title": f"Standard Safe Area: {youtube_margins.top} all around",
            "variant": "glass",
            "position": "bottom_right"
        },
        layer=10
    )
    manager.current_timeline.add_component(youtube_lower, duration=8.0, track="main", gap_before=2.0)

    youtube_text = ComponentInstance(
        component_type="TextOverlay",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "📺 YouTube: Simple 20px margins\nClean and professional",
            "position": "center",
            "style": "minimal",
            "animation": "blur_in"
        },
        layer=15
    )
    manager.current_timeline.add_component(
        youtube_text,
        duration=6.0,
        track="overlay",
        align_to="main",
        offset=37.0  # 35s + 2s
    )

    # ========================================================================
    # SECTION 6: All Platforms Summary (45-55s)
    # ========================================================================
    print("📍 Section 6: Platform Summary")

    summary_title = ComponentInstance(
        component_type="TitleScene",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "Platform Comparison",
            "subtitle": "7 Platform Presets Available",
            "variant": "kinetic",
            "animation": "slide_up"
        },
        layer=0
    )
    manager.current_timeline.add_component(summary_title, duration=5.0, track="main", gap_before=2.0)

    # Show stats - counter overlapping with text
    counter = ComponentInstance(
        component_type="Counter",
        start_frame=0,
        duration_frames=0,
        props={
            "start_value": 0,
            "end_value": 7,
            "prefix": "",
            "suffix": " Platforms",
            "decimals": 0,
            "animation": "count_up"
        },
        layer=10
    )
    manager.current_timeline.add_component(counter, duration=3.0, track="main")

    platform_list = ComponentInstance(
        component_type="TextOverlay",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "LinkedIn • Instagram Stories • TikTok • YouTube\nMobile Vertical • Mobile Horizontal • Instagram Square",
            "position": "center",
            "style": "glass",
            "animation": "fade_in"
        },
        layer=15
    )
    manager.current_timeline.add_component(
        platform_list,
        duration=4.5,
        track="overlay",
        align_to="main",
        offset=50.5  # Start 0.5s into the counter
    )

    # ========================================================================
    # SECTION 7: End Card (55-60s)
    # ========================================================================
    print("📍 Section 7: End Card")

    end_screen = ComponentInstance(
        component_type="EndScreen",
        start_frame=0,
        duration_frames=0,
        props={
            "cta_text": "Use Design System • Safe Margins",
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
    print("  ✓ VideoComposition.tsx")

    # Get project info
    info = manager.get_project_info()
    composition = info['composition']

    print("\n✅ Safe Margins Demo Created!")
    print("=" * 70)
    print(f"📁 Project: {project_path}")
    print(f"🎬 Duration: {composition['duration_seconds']:.1f} seconds")
    print("📐 Resolution: 1920x1080 @ 30fps")
    print("\n📱 Platform Safe Margins Covered:")
    for platform, margins in SPACING_TOKENS.safe_area.items():
        print(f"   • {platform.replace('_', ' ').title()}")
        if hasattr(margins, 'all'):
            print(f"     → {margins.all} all sides")
        else:
            top = getattr(margins, 'top', 'N/A')
            bottom = getattr(margins, 'bottom', 'N/A')
            left = getattr(margins, 'left', 'N/A')
            right = getattr(margins, 'right', 'N/A')
            print(f"     → Top: {top}, Bottom: {bottom}")
            print(f"     → Left: {left}, Right: {right}")

    print("\n🚀 To render:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")
    print("\n" + "=" * 70)

    return project_path


async def main():
    """Main example function."""
    print("\n" + "=" * 70)
    print("SAFE MARGINS DEMO")
    print("=" * 70)
    print("\nDemonstrates platform-specific safe margins:")
    print("  • LinkedIn Feed (8-24px crop zones)")
    print("  • Instagram Stories (9:16 with UI overlays)")
    print("  • TikTok (side button considerations)")
    print("  • YouTube (standard margins)")
    print("  • Mobile formats (vertical & horizontal)")
    print("\nEnsures your content is never cropped by platform UIs!")
    print("\n" + "=" * 70)

    result = await create_safe_margins_demo()

    if result:
        print("\n✨ Success! Your safe margins demo is ready to render.\n")
    else:
        print("\n❌ Something went wrong. Check the logs above.\n")


if __name__ == "__main__":
    asyncio.run(main())
