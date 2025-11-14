#!/usr/bin/env python3
"""
Generate Static HTML Previews

Creates an HTML page showcasing all themes and components
for easy visual exploration without rendering videos.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_motion import COLOR_TOKENS, COMPONENT_REGISTRY, YOUTUBE_THEMES


def generate_theme_preview_html() -> str:
    """Generate HTML preview of all themes."""
    html_parts = []

    html_parts.append("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Remotion Design System Preview</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0a0e1a;
            color: #ffffff;
            padding: 40px 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { font-size: 48px; margin-bottom: 20px; text-align: center; }
        .subtitle { text-align: center; color: #8b92a4; margin-bottom: 60px; font-size: 18px; }

        .section { margin-bottom: 80px; }
        .section-title {
            font-size: 32px;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #1e2535;
        }

        .theme-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
        }

        .theme-card {
            background: #1a1f2e;
            border-radius: 12px;
            padding: 25px;
            border: 1px solid #2a3142;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .theme-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }

        .theme-name {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .theme-desc {
            color: #8b92a4;
            font-size: 14px;
            margin-bottom: 20px;
            line-height: 1.5;
        }

        .color-swatches {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }

        .color-swatch {
            width: 60px;
            height: 60px;
            border-radius: 8px;
            border: 2px solid rgba(255, 255, 255, 0.1);
        }

        .gradient-preview {
            height: 80px;
            border-radius: 8px;
            margin-bottom: 15px;
        }

        .use-cases {
            list-style: none;
            margin-top: 15px;
        }

        .use-cases li {
            padding: 6px 0;
            color: #a0a8b8;
            font-size: 13px;
        }

        .use-cases li:before {
            content: "→ ";
            color: #00d9ff;
            font-weight: bold;
        }

        .component-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
        }

        .component-card {
            background: #1a1f2e;
            border-radius: 12px;
            padding: 25px;
            border: 1px solid #2a3142;
        }

        .component-name {
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 8px;
            color: #00d9ff;
        }

        .component-category {
            display: inline-block;
            padding: 4px 12px;
            background: rgba(0, 217, 255, 0.1);
            color: #00d9ff;
            border-radius: 4px;
            font-size: 11px;
            text-transform: uppercase;
            margin-bottom: 12px;
            font-weight: 600;
        }

        .component-desc {
            color: #8b92a4;
            font-size: 14px;
            margin-bottom: 15px;
            line-height: 1.5;
        }

        .variants {
            margin-top: 15px;
        }

        .variants-title {
            font-size: 13px;
            color: #a0a8b8;
            margin-bottom: 8px;
            text-transform: uppercase;
            font-weight: 600;
        }

        .variant-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .variant-tag {
            padding: 6px 12px;
            background: #2a3142;
            border-radius: 6px;
            font-size: 12px;
            color: #ffffff;
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 60px;
            margin: 60px 0;
            padding: 40px;
            background: linear-gradient(135deg, #1a1f2e 0%, #0f1419 100%);
            border-radius: 12px;
        }

        .stat {
            text-align: center;
        }

        .stat-number {
            font-size: 48px;
            font-weight: 900;
            background: linear-gradient(135deg, #0066FF 0%, #00D9FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .stat-label {
            color: #8b92a4;
            font-size: 14px;
            margin-top: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 Remotion Design System</h1>
        <p class="subtitle">Explore themes, components, and design tokens for AI-powered video generation</p>

        <div class="stats">
            <div class="stat">
                <div class="stat-number">7</div>
                <div class="stat-label">Themes</div>
            </div>
            <div class="stat">
                <div class="stat-number">7</div>
                <div class="stat-label">Components</div>
            </div>
            <div class="stat">
                <div class="stat-number">20+</div>
                <div class="stat-label">Variants</div>
            </div>
        </div>
""")

    # Generate theme previews
    html_parts.append('<div class="section"><h2 class="section-title">🎨 YouTube Themes</h2><div class="theme-grid">')

    for theme_name, theme in YOUTUBE_THEMES.items():
        colors = theme.colors
        primary = colors.primary[0] if isinstance(colors.primary, list) else colors.primary
        accent = colors.accent[0] if isinstance(colors.accent, list) else colors.accent

        use_cases_html = "\n".join(
            f'<li>{uc}</li>' for uc in theme.use_cases[:4]
        )

        html_parts.append(f'''
        <div class="theme-card">
            <div class="theme-name">{theme.name}</div>
            <div class="theme-desc">{theme.description}</div>
            <div class="color-swatches">
                <div class="color-swatch" style="background: {primary};" title="Primary"></div>
                <div class="color-swatch" style="background: {accent};" title="Accent"></div>
            </div>
            <div class="gradient-preview" style="background: {colors.gradient};"></div>
            <ul class="use-cases">
                {use_cases_html}
            </ul>
        </div>
        ''')

    html_parts.append('</div></div>')

    # Generate component previews
    html_parts.append('<div class="section"><h2 class="section-title">🎬 Component Library</h2><div class="component-grid">')

    for comp_name, component in COMPONENT_REGISTRY.items():
        variants = component.get('variants', {})
        animations = component.get('animations', {})

        variant_tags = "\n".join(
            f'<span class="variant-tag">{v}</span>' for v in list(variants.keys())[:5]
        )

        animation_tags = "\n".join(
            f'<span class="variant-tag">✨ {a}</span>' for a in list(animations.keys())[:5]
        )

        html_parts.append(f'''
        <div class="component-card">
            <div class="component-category">{component['category']}</div>
            <div class="component-name">{comp_name}</div>
            <div class="component-desc">{component['description']}</div>

            {f'<div class="variants"><div class="variants-title">Variants</div><div class="variant-tags">{variant_tags}</div></div>' if variants else ''}
            {f'<div class="variants"><div class="variants-title">Animations</div><div class="variant-tags">{animation_tags}</div></div>' if animations else ''}
        </div>
        ''')

    html_parts.append('</div></div>')

    html_parts.append("""
        <div style="text-align: center; margin-top: 80px; padding: 40px; color: #8b92a4;">
            <p>Built with ❤️ using <strong>chuk-motion</strong></p>
            <p style="margin-top: 10px;">AI-powered video generation for YouTube</p>
        </div>
    </div>
</body>
</html>
""")

    return "\n".join(html_parts)


def main():
    """Generate and save the preview HTML."""
    print("Generating design system preview...")

    html = generate_theme_preview_html()

    output_path = Path("design-system-preview.html")
    output_path.write_text(html)

    print(f"\n✅ Preview generated: {output_path.absolute()}")
    print(f"\n📂 Open in browser: file://{output_path.absolute()}")
    print("\n💡 Tip: You can also run:")
    print(f"   open {output_path.name}  # macOS")
    print(f"   xdg-open {output_path.name}  # Linux")
    print(f"   start {output_path.name}  # Windows")


if __name__ == "__main__":
    main()
