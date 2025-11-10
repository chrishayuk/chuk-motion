#!/usr/bin/env python3
"""
Interactive Design System Explorer

Browse themes, components, and design tokens interactively without rendering videos.
"""
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_remotion import (
    COLOR_TOKENS,
    TYPOGRAPHY_TOKENS,
    MOTION_TOKENS,
    COMPONENT_REGISTRY,
    YOUTUBE_THEMES
)


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)


def print_section(text: str):
    """Print a section header."""
    print(f"\n{'─' * 70}")
    print(f"  {text}")
    print('─' * 70)


def explore_themes():
    """Interactive theme explorer."""
    print_header("THEME EXPLORER")

    while True:
        print("\nAvailable Themes:")
        theme_list = list(YOUTUBE_THEMES.keys())
        for idx, theme_name in enumerate(theme_list, 1):
            theme = YOUTUBE_THEMES[theme_name]
            print(f"  {idx}. {theme.name} - {theme.description}")

        print("\n  0. Back to main menu")

        choice = input("\nSelect a theme (0-{}): ".format(len(theme_list)))

        if choice == "0":
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(theme_list):
                show_theme_details(theme_list[idx])
        except (ValueError, IndexError):
            print("❌ Invalid choice")


def show_theme_details(theme_name: str):
    """Show detailed information about a theme."""
    theme = YOUTUBE_THEMES[theme_name]
    colors = theme.colors

    print_section(f"THEME: {theme.name.upper()}")
    print(f"\n{theme.description}")

    print("\n📊 Color Palette:")
    print(f"  Primary:    {colors.primary[0]}")
    print(f"  Accent:     {colors.accent[0]}")
    print(f"  Gradient:   {colors.gradient[:50]}...")

    print("\n🎨 Background:")
    background_dict = colors.background.model_dump()
    for key, value in background_dict.items():
        print(f"  {key:12} {value}")

    print("\n✍️  Text Colors:")
    text_dict = colors.text.model_dump()
    for key, value in text_dict.items():
        print(f"  {key:12} {value}")

    print("\n💡 Use Cases:")
    for use_case in theme.use_cases[:5]:
        print(f"  • {use_case}")

    input("\nPress Enter to continue...")


def explore_components():
    """Interactive component explorer."""
    print_header("COMPONENT LIBRARY")

    # Group by category
    by_category = {}
    for name, comp in COMPONENT_REGISTRY.items():
        cat = comp.get('category', 'other')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append((name, comp))

    while True:
        print("\nComponent Categories:")
        categories = list(by_category.keys())
        for idx, cat in enumerate(categories, 1):
            count = len(by_category[cat])
            print(f"  {idx}. {cat.upper()} ({count} components)")

        print("\n  0. Back to main menu")

        choice = input("\nSelect a category (0-{}): ".format(len(categories)))

        if choice == "0":
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(categories):
                show_category_components(categories[idx], by_category[categories[idx]])
        except (ValueError, IndexError):
            print("❌ Invalid choice")


def show_category_components(category: str, components: list):
    """Show components in a category."""
    print_section(f"CATEGORY: {category.upper()}")

    while True:
        print(f"\nComponents in {category}:")
        for idx, (name, comp) in enumerate(components, 1):
            print(f"  {idx}. {name} - {comp['description'][:50]}...")

        print("\n  0. Back to categories")

        choice = input("\nSelect a component (0-{}): ".format(len(components)))

        if choice == "0":
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(components):
                show_component_details(components[idx][0], components[idx][1])
        except (ValueError, IndexError):
            print("❌ Invalid choice")


def show_component_details(name: str, component: dict):
    """Show detailed component information."""
    print_section(f"COMPONENT: {name}")

    print(f"\n📝 {component['description']}")
    print(f"\n📁 Category: {component['category']}")

    if 'variants' in component:
        print("\n🎨 Variants:")
        for variant, desc in component['variants'].items():
            print(f"  • {variant:15} {desc}")

    if 'animations' in component:
        print("\n✨ Animations:")
        for anim, desc in component['animations'].items():
            print(f"  • {anim:15} {desc}")

    if 'positions' in component:
        print("\n📍 Positions:")
        for pos, desc in component['positions'].items():
            print(f"  • {pos:15} {desc}")

    print("\n📋 Schema:")
    schema = component.get('schema', {})
    for prop, details in schema.items():
        required = " (required)" if details.get('required') else ""
        default = f" = {details.get('default')}" if 'default' in details else ""
        print(f"  • {prop}{required}{default}")
        print(f"    {details.get('description', '')}")

    print("\n💡 Example:")
    import json
    example = component.get('example', {})
    for key, value in example.items():
        print(f"  {key}: {json.dumps(value)}")

    input("\nPress Enter to continue...")


def explore_tokens():
    """Explore design tokens."""
    print_header("DESIGN TOKENS")

    menu = {
        "1": ("Colors", show_color_tokens),
        "2": ("Typography", show_typography_tokens),
        "3": ("Motion", show_motion_tokens),
    }

    while True:
        print("\nToken Categories:")
        print("  1. Colors (palettes, gradients)")
        print("  2. Typography (fonts, sizes, weights)")
        print("  3. Motion (springs, easings, durations)")
        print("\n  0. Back to main menu")

        choice = input("\nSelect a category (0-3): ")

        if choice == "0":
            break

        if choice in menu:
            menu[choice][1]()
        else:
            print("❌ Invalid choice")


def show_color_tokens():
    """Show color token details."""
    print_section("COLOR TOKENS")

    for theme_name, theme_colors in COLOR_TOKENS.items():
        print(f"\n🎨 {theme_name.upper()}")
        print(f"   Primary: {theme_colors['primary']}")
        print(f"   Accent:  {theme_colors['accent']}")

    input("\nPress Enter to continue...")


def show_typography_tokens():
    """Show typography token details."""
    print_section("TYPOGRAPHY TOKENS")

    print("\n📝 Font Families:")
    font_families = TYPOGRAPHY_TOKENS.font_families.model_dump()
    for name, family in font_families.items():
        print(f"  • {name:12} {family['fonts'][0]}")

    print("\n📏 Font Sizes (1080p):")
    sizes = TYPOGRAPHY_TOKENS.font_sizes.video_1080p.model_dump()
    for size, value in sizes.items():
        print(f"  • {size:8} {value}")

    print("\n⚖️  Font Weights:")
    font_weights = TYPOGRAPHY_TOKENS.font_weights.model_dump()
    for name, value in font_weights.items():
        print(f"  • {name:12} {value}")

    input("\nPress Enter to continue...")


def show_motion_tokens():
    """Show motion token details."""
    print_section("MOTION TOKENS")

    print("\n⚡ Spring Configs:")
    for name, config in MOTION_TOKENS.spring_configs.items():
        print(f"  • {name:10} {config['description']}")

    print("\n📈 Easing Curves:")
    for name, curve in MOTION_TOKENS.easing.items():
        print(f"  • {name:20} {curve['description']}")

    print("\n⏱️  Duration Presets:")
    for name, duration in MOTION_TOKENS.duration.items():
        print(f"  • {name:12} {duration['seconds']}s ({duration['frames']} frames)")

    input("\nPress Enter to continue...")


def main():
    """Main interactive menu."""
    print_header("REMOTION DESIGN SYSTEM EXPLORER")
    print("\nExplore themes, components, and design tokens")
    print("No video rendering required!")

    menu = {
        "1": ("Themes", explore_themes),
        "2": ("Components", explore_components),
        "3": ("Design Tokens", explore_tokens),
    }

    while True:
        print("\n" + "─" * 70)
        print("Main Menu:")
        print("  1. 🎨 Themes (7 YouTube-optimized themes)")
        print("  2. 🎬 Components (7 video components with variants)")
        print("  3. 🎯 Design Tokens (colors, typography, motion)")
        print("\n  0. Exit")

        choice = input("\nYour choice (0-3): ")

        if choice == "0":
            print("\n✨ Thanks for exploring! Build amazing videos with chuk-mcp-remotion!\n")
            break

        if choice in menu:
            menu[choice][1]()
        else:
            print("❌ Invalid choice, please try again")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✨ Goodbye!\n")
        sys.exit(0)
