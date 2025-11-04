#!/usr/bin/env python3
"""
Example: Explore the Remotion design system

This example demonstrates how to explore available components,
themes, and design tokens programmatically.
"""
import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_remotion import (
    COLOR_TOKENS,
    TYPOGRAPHY_TOKENS,
    MOTION_TOKENS,
    SPACING_TOKENS,
    COMPONENT_REGISTRY,
    YOUTUBE_THEMES
)


async def explore_components():
    """Explore available video components."""
    print("\n" + "="*70)
    print("AVAILABLE VIDEO COMPONENTS")
    print("="*70)

    # Group components by category
    by_category = {}
    for name, component in COMPONENT_REGISTRY.items():
        category = component.get("category", "other")
        if category not in by_category:
            by_category[category] = []
        by_category[category].append((name, component))

    # Display each category
    for category, components in sorted(by_category.items()):
        print(f"\n📁 {category.upper()}")
        print("-" * 70)
        for name, component in components:
            desc = component.get("description", "No description")
            print(f"  • {name}: {desc}")

            # Show variants if available
            variants = component.get("variants", {})
            if variants:
                variant_list = ", ".join(variants.keys())
                print(f"    Variants: {variant_list}")


async def explore_themes():
    """Explore available themes."""
    print("\n" + "="*70)
    print("AVAILABLE THEMES")
    print("="*70)

    for theme_name, theme in YOUTUBE_THEMES.items():
        print(f"\n🎨 {theme['name'].upper()}")
        print("-" * 70)
        print(f"  Description: {theme['description']}")

        # Show colors
        colors = theme['colors']
        primary = colors['primary'][0] if isinstance(colors['primary'], list) else colors['primary']
        accent = colors['accent'][0] if isinstance(colors['accent'], list) else colors['accent']
        print(f"  Colors: Primary {primary}, Accent {accent}")

        # Show use cases
        use_cases = theme.get('use_cases', [])
        if use_cases:
            print(f"  Use Cases: {', '.join(use_cases[:3])}")


async def explore_tokens():
    """Explore design tokens."""
    print("\n" + "="*70)
    print("DESIGN TOKENS")
    print("="*70)

    # Color tokens
    print(f"\n🎨 Colors: {len(COLOR_TOKENS)} themes")
    print(f"  Themes: {', '.join(COLOR_TOKENS.keys())}")

    # Typography tokens
    print(f"\n📝 Typography:")
    font_families = TYPOGRAPHY_TOKENS['font_families']
    print(f"  Font Families: {', '.join(font_families.keys())}")

    # Motion tokens
    print(f"\n⚡ Motion:")
    springs = MOTION_TOKENS['spring_configs']
    easings = MOTION_TOKENS['easing_curves']
    durations = MOTION_TOKENS['durations']
    print(f"  Spring Configs: {len(springs)}")
    print(f"  Easing Curves: {len(easings)}")
    print(f"  Duration Presets: {len(durations)}")

    # Spacing tokens
    print(f"\n📏 Spacing:")
    spacing = SPACING_TOKENS['spacing']
    safe_margins = SPACING_TOKENS['safe_margins']
    print(f"  Spacing Scale: {len(spacing)} steps ({', '.join(list(spacing.keys())[:5])}...)")
    print(f"  Safe Margins: {len(safe_margins)} platforms ({', '.join(list(safe_margins.keys())[:3])}...)")
    print(f"  Border Radius: {len(SPACING_TOKENS['border_radius'])} variants")
    print(f"  Layout Presets: {len(SPACING_TOKENS['layout_widths'])} widths, {len(SPACING_TOKENS['layout_heights'])} heights")


async def show_component_example():
    """Show a detailed component example."""
    print("\n" + "="*70)
    print("COMPONENT EXAMPLE: LowerThird")
    print("="*70)

    lower_third = COMPONENT_REGISTRY.get("LowerThird")
    if lower_third:
        print(f"\nDescription: {lower_third['description']}")
        print(f"Category: {lower_third['category']}")

        print("\nVariants:")
        for variant, desc in lower_third['variants'].items():
            print(f"  • {variant}: {desc}")

        print("\nPositions:")
        for position, desc in lower_third['positions'].items():
            print(f"  • {position}: {desc}")

        print("\nExample Usage:")
        example = lower_third['example']
        print(json.dumps(example, indent=2))


async def main():
    """Main example function."""
    print("\n" + "="*70)
    print("CHUK-MCP-REMOTION DESIGN SYSTEM EXPLORER")
    print("="*70)

    # Explore different aspects
    await explore_components()
    await explore_themes()
    await explore_tokens()
    await show_component_example()

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"  Total Components: {len(COMPONENT_REGISTRY)}")
    print(f"  Total Themes: {len(YOUTUBE_THEMES)}")
    print(f"  Color Palettes: {len(COLOR_TOKENS)}")
    print(f"  Spring Configs: {len(MOTION_TOKENS['spring_configs'])}")
    print(f"  Easing Curves: {len(MOTION_TOKENS['easing_curves'])}")
    print(f"  Spacing Tokens: {len(SPACING_TOKENS)} categories")
    print(f"  Safe Margin Platforms: {len(SPACING_TOKENS['safe_margins'])}")
    print("\n" + "="*70)
    print("\n✨ Ready to create amazing videos with AI!")
    print("📱 Now with platform-specific safe margins for LinkedIn, TikTok, Instagram & more!\n")


if __name__ == "__main__":
    asyncio.run(main())
