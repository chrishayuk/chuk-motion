#!/usr/bin/env python3
"""
Token System Showcase
=====================

Comprehensive demonstration of the chuk-motion token system.

This example showcases:
- Typography tokens (font families, sizes, weights, text styles)
- Color tokens (themes, gradients, semantic colors)
- Motion tokens (durations, easings, springs, enter/exit transitions)
- Spacing tokens (spacing scale, safe areas, border tokens)
- Platform-specific optimizations
- Token export/import functionality

Usage:
    python examples/tokens_showcase.py
"""

import asyncio

from chuk_virtual_fs import AsyncVirtualFileSystem

from chuk_motion.tokens.brand import get_brand_pack
from chuk_motion.tokens.captions import CAPTION_STYLES, get_caption_style
from chuk_motion.tokens.colors import COLOR_TOKENS
from chuk_motion.tokens.motion import MOTION_TOKENS
from chuk_motion.tokens.spacing import SPACING_TOKENS
from chuk_motion.tokens.token_manager import TokenManager
from chuk_motion.tokens.typography import TYPOGRAPHY_TOKENS


async def main():
    """Showcase the complete token system."""
    print("=" * 80)
    print("TOKEN SYSTEM SHOWCASE")
    print("=" * 80)
    print()

    # Initialize VFS and token manager
    vfs = AsyncVirtualFileSystem()
    token_manager = TokenManager(vfs)

    # ========================================================================
    # TYPOGRAPHY TOKENS
    # ========================================================================
    print("1. TYPOGRAPHY TOKENS")
    print("-" * 80)

    print("\nFont Families:")
    for family_key in ["display", "body", "mono", "decorative"]:
        family = getattr(TYPOGRAPHY_TOKENS.font_families, family_key)
        print(f"  {family.name}: {', '.join(family.fonts[:2])}")
        print(f"    Usage: {family.usage}")

    print("\nFont Sizes (1080p):")
    sizes_1080p = TYPOGRAPHY_TOKENS.font_sizes.video_1080p
    for size_name in ["xs", "sm", "base", "lg", "xl", "xxl", "xxxl", "xxxxl"]:
        size = getattr(sizes_1080p, size_name)
        print(f"  {size_name}: {size}")

    print("\nText Styles:")
    for style_name in ["hero_title", "title", "heading", "body", "caption"]:
        style = getattr(TYPOGRAPHY_TOKENS.text_styles, style_name)
        print(f"  {style.name}:")
        print(f"    Font Size: {style.fontSize}")
        print(f"    Font Weight: {style.fontWeight}")
        print(f"    Line Height: {style.lineHeight}")

    # ========================================================================
    # COLOR TOKENS
    # ========================================================================
    print("\n2. COLOR TOKENS")
    print("-" * 80)

    print("\nAvailable Themes:")
    for theme_key in ["tech", "finance", "education", "lifestyle", "gaming", "minimal", "business"]:
        theme_data = getattr(COLOR_TOKENS, theme_key)
        print(f"  {theme_data.name}: {theme_data.description}")
        print(f"    Primary: {theme_data.primary[0]}")
        print(f"    Accent: {theme_data.accent[0]}")

    print("\nTech Theme Color Palette:")
    tech_theme = COLOR_TOKENS.tech
    print(f"  Primary Scale: {' → '.join(tech_theme.primary)}")
    print(f"  Accent Scale: {' → '.join(tech_theme.accent)}")
    print(f"  Gradient: {tech_theme.gradient}")

    print("\nSemantic Colors (Tech Theme):")
    semantic_dict = tech_theme.semantic.model_dump()
    for key, value in semantic_dict.items():
        print(f"  {key.title()}: {value}")

    # ========================================================================
    # MOTION TOKENS
    # ========================================================================
    print("\n3. MOTION TOKENS")
    print("-" * 80)

    print("\nDuration Presets:")
    duration_names = ["instant", "ultra_fast", "fast", "normal", "medium", "slow"]
    for duration_name in duration_names:
        duration = MOTION_TOKENS.duration[duration_name]
        print(
            f"  {duration.description}: {duration.ms}ms ({duration.frames_30fps} frames @ 30fps)"
        )

    print("\nEasing Curves:")
    easing_names = [
        "linear",
        "ease_out",
        "ease_in",
        "ease_out_back",
        "ease_out_expo",
        "bounce",
    ]
    for easing_name in easing_names:
        easing = MOTION_TOKENS.easing[easing_name]
        print(f"  {easing.description}:")
        print(f"    CSS: {easing.css}")
        print(f"    Usage: {easing.usage}")

    print("\nSpring Configurations:")
    spring_names = ["gentle", "smooth", "bouncy", "snappy", "stiff"]
    for spring_name in spring_names:
        spring = MOTION_TOKENS.spring_configs[spring_name]
        config = spring.config
        print(f"  {spring.feel}:")
        print(
            f"    Damping: {config.damping}, Stiffness: {config.stiffness}, Mass: {config.mass}"
        )
        print(f"    Usage: {spring.usage}")

    print("\nEnter Transitions:")
    enter_names = [
        "fade_in",
        "fade_up",
        "slide_in_left",
        "scale_in",
        "zoom_in",
        "bounce_in",
    ]
    for enter_name in enter_names:
        transition = MOTION_TOKENS.enter[enter_name]
        print(f"  {transition.description}")
        print(f"    Default Duration: {transition.default_duration}")
        print(f"    Default Easing: {transition.default_easing}")

    print("\nExit Transitions:")
    exit_names = ["fade_out", "fade_out_down", "slide_out_left", "scale_out", "zoom_out"]
    for exit_name in exit_names:
        transition = MOTION_TOKENS.exit[exit_name]
        print(f"  {transition.description}")

    print("\nTempo Presets:")
    tempo_names = ["sprint", "fast", "medium", "slow", "cinematic"]
    for tempo_name in tempo_names:
        tempo = MOTION_TOKENS.tempo[tempo_name]
        print(f"  {tempo.feel}:")
        print(f"    Beat Duration: {tempo.beat_duration}s")
        print(f"    Scene Change Interval: {tempo.scene_change_interval}s")
        print(f"    Cuts Per Minute: {tempo.cuts_per_minute}")

    print("\nPlatform Timing Optimizations:")
    platform_names = [
        "youtube_long_form",
        "youtube_shorts",
        "tiktok",
        "instagram_reel",
        "linkedin",
    ]
    for platform_name in platform_names:
        platform = MOTION_TOKENS.platform_timing[platform_name]
        print(f"  {platform.description}:")
        print(f"    Hook Duration: {platform.hook_duration}s")
        print(f"    Scene Change: every {platform.scene_change_interval}s")
        print(f"    Recommended Tempo: {platform.recommended_tempo}")

    # ========================================================================
    # SPACING TOKENS
    # ========================================================================
    print("\n4. SPACING TOKENS")
    print("-" * 80)

    print("\nSpacing Scale:")
    spacing_names = ["none", "xxs", "xs", "sm", "md", "lg", "xl", "2xl", "3xl"]
    for spacing_name in spacing_names:
        spacing = SPACING_TOKENS.spacing[spacing_name]
        print(f"  {spacing_name}: {spacing}")

    print("\nSafe Areas (Platform-Specific):")
    safe_area_platforms = [
        "desktop",
        "mobile",
        "youtube_shorts",
        "tiktok",
        "instagram_reel",
    ]
    for platform_name in safe_area_platforms:
        safe_area = SPACING_TOKENS.safe_area[platform_name]
        print(f"  {safe_area.description}:")
        print(
            f"    Margins - Top: {safe_area.top}px, Bottom: {safe_area.bottom}px, "
            f"Left: {safe_area.left}px, Right: {safe_area.right}px"
        )
        print(f"    Aspect Ratio: {safe_area.aspect_ratio}")
        if safe_area.ui_overlays:
            print(f"    UI Overlays: {', '.join(safe_area.ui_overlays[:2])}...")

    print("\nBorder Radius:")
    radius_names = ["none", "xs", "sm", "md", "lg", "xl", "2xl", "3xl", "full"]
    for radius_name in radius_names:
        radius = SPACING_TOKENS.border_radius[radius_name]
        print(f"  {radius_name}: {radius}")

    # ========================================================================
    # BRAND PACKS
    # ========================================================================
    print("\n5. BRAND PACKS")
    print("-" * 80)

    print("\nAvailable Brand Packs:")
    for pack_key in ["default", "tech_startup", "enterprise", "creator", "education"]:
        pack = get_brand_pack(pack_key)
        print(f"  {pack.display_name}: {pack.description}")
        print(f"    Default Motion: {pack.motion.default_spring} spring")
        print(f"    Default Tempo: {pack.motion.default_tempo}")

    # ========================================================================
    # CAPTION STYLES
    # ========================================================================
    print("\n6. CAPTION STYLES")
    print("-" * 80)

    print("\nAvailable Caption Styles:")
    for style_key in ["burst", "precise", "headline", "minimal", "neon", "classic"]:
        style = get_caption_style(style_key)
        print(f"  {style.display_name}: {style.description}")
        print(f"    Display Mode: {style.display_mode}")
        print(f"    Recommended Tempo: {style.recommended_tempo}")

    # ========================================================================
    # TOKEN EXPORT/IMPORT
    # ========================================================================
    print("\n7. TOKEN EXPORT/IMPORT")
    print("-" * 80)

    print("\nExporting tokens...")

    # Export all token types
    try:
        typo_file = await token_manager.export_typography_tokens("showcase_typography.json")
        print(f"  ✓ Typography tokens exported to: {typo_file}")

        color_file = await token_manager.export_color_tokens(
            "showcase_colors.json", theme_name="tech"
        )
        print(f"  ✓ Color tokens (tech theme) exported to: {color_file}")

        motion_file = await token_manager.export_motion_tokens("showcase_motion.json")
        print(f"  ✓ Motion tokens exported to: {motion_file}")

        spacing_file = await token_manager.export_spacing_tokens("showcase_spacing.json")
        print(f"  ✓ Spacing tokens exported to: {spacing_file}")

        # Export all at once
        all_files = await token_manager.export_all_tokens("showcase_all_tokens")
        print(f"\n  ✓ All tokens exported to directory: showcase_all_tokens/")
        for token_type, file_path in all_files.items():
            print(f"    - {token_type}: {file_path}")

    except Exception as e:
        print(f"  ✗ Error exporting tokens: {e}")

    # ========================================================================
    # TOKEN USAGE EXAMPLES
    # ========================================================================
    print("\n8. PRACTICAL USAGE EXAMPLES")
    print("-" * 80)

    print("\nExample 1: Building a component with tokens")
    print("```python")
    print("# Get theme colors")
    print('tech_primary = COLOR_TOKENS.tech.primary[0]')
    print()
    print("# Get typography")
    print("title_style = TYPOGRAPHY_TOKENS.text_styles.hero_title")
    print('font_size = TYPOGRAPHY_TOKENS.font_sizes.video_1080p.xl  # "64px"')
    print()
    print("# Get motion")
    print("spring_config = MOTION_TOKENS.spring_configs.bouncy.config")
    print("fade_in_preset = MOTION_TOKENS.enter.fade_in")
    print("```")

    print("\nExample 2: Platform-specific video generation")
    print("```python")
    print("# TikTok video")
    print("platform = MOTION_TOKENS.platform_timing.tiktok")
    print("safe_area = SPACING_TOKENS.safe_area.tiktok")
    print("caption_style = get_caption_style('burst')")
    print()
    print("# Use platform recommendations")
    print("tempo = MOTION_TOKENS.tempo[platform.recommended_tempo]")
    print("hook_duration = platform.hook_duration  # 1.5s for TikTok")
    print("```")

    print("\nExample 3: Custom theme with brand pack")
    print("```python")
    print("from chuk_motion.tokens.brand import merge_brand_pack")
    print()
    print('custom_brand = merge_brand_pack("tech_startup", {')
    print('    "logo": {"url": "client-logo.png"},')
    print('    "colors": {"primary": ["#FF6B6B", "#EE5A6F"]},')
    print('    "motion": {"default_spring": "bouncy"},')
    print("})")
    print("```")

    # ========================================================================
    # PYDANTIC MODEL USAGE
    # ========================================================================
    print("\n9. PYDANTIC MODEL USAGE")
    print("-" * 80)

    print("\nAccessing tokens as Pydantic models:")
    print("```python")
    print("# Access as attributes")
    print('duration = MOTION_TOKENS.duration["normal"]')
    print(f"# duration.ms = {MOTION_TOKENS.duration['normal'].ms}")
    print(f"# duration.frames_30fps = {MOTION_TOKENS.duration['normal'].frames_30fps}")
    print()
    print("# Nested properties")
    print('damping = MOTION_TOKENS.spring_configs["smooth"].config.damping')
    print(f"# damping = {MOTION_TOKENS.spring_configs['smooth'].config.damping}")
    print()
    print("# Convert to dict for JSON serialization")
    print('duration_dict = MOTION_TOKENS.duration["normal"].model_dump()')
    print()
    print("# Convert entire model")
    print("all_motion = MOTION_TOKENS.model_dump()")
    print("```")

    # Cleanup
    await vfs.close()

    print()
    print("=" * 80)
    print("SHOWCASE COMPLETE")
    print("=" * 80)
    print()
    print("For more details, see:")
    print("  - docs/tokens.md - Comprehensive token documentation")
    print("  - src/chuk_motion/tokens/ - Token source files")
    print()


if __name__ == "__main__":
    asyncio.run(main())
