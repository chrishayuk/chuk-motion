# chuk-motion

> AI-powered video generation with Remotion - A design-system-first approach to creating professional multi-platform videos

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-compatible-green.svg)](https://github.com/anthropics/mcp)
[![Tests](https://img.shields.io/badge/tests-950%20passing-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen.svg)](tests/)

## Overview

`chuk-motion` is an MCP (Model Context Protocol) server that brings the power of [Remotion](https://www.remotion.dev) video generation to AI assistants like Claude. It provides a **design-system-first approach** with comprehensive design tokens, enabling AI to create professional, animated videos optimized for **YouTube, TikTok, LinkedIn, Instagram Stories**, and more.

### Key Features

- **🎨 Complete Design System**: Design tokens for colors, typography, spacing, and motion
- **📱 Multi-Platform Support**: Safe margins for LinkedIn, TikTok, Instagram, YouTube
- **🎬 43+ Video Components**: Charts, code blocks, overlays, layouts, animations, text animations, and demo realism
- **🎨 7 Built-in Themes**: Tech, Finance, Education, Lifestyle, Gaming, Minimal, Business
- **⚡ Track-Based Timeline**: Professional multi-track composition system
- **🤖 LLM-Friendly**: Discoverable components with detailed schemas
- **📊 Data Visualization**: Animated charts (Pie, Bar, Line, Area, Donut, Horizontal Bar)
- **💻 Code Display**: Syntax-highlighted code blocks with typing animations

## Design System

### Four Token Categories

1. **Colors** (`tokens/colors.py`)
   - 7 theme palettes optimized for video
   - Dark/light mode support (`on_dark`, `on_light`)
   - Background variants (dark, light, glass)
   - Semantic colors (success, warning, error, info)

2. **Typography** (`tokens/typography.py`)
   - Font scales for 720p, 1080p, 4K
   - Primary and code font stacks
   - Font weights, line heights, letter spacing
   - Video-optimized readability

3. **Spacing** (`tokens/spacing.py`) ⭐ NEW
   - 10-step spacing scale (4px - 120px)
   - **7 platform safe margins**: LinkedIn, Instagram Stories/Square, TikTok, YouTube, Mobile
   - Border radius tokens
   - Layout width tokens

4. **Motion** (`tokens/motion.py`)
   - Spring configurations for animations
   - Easing curves (ease-out, ease-in-out, bounce)
   - Duration presets (fast, normal, slow)

### Platform Safe Margins

Ensure your content isn't cropped by platform UIs:

| Platform | Top | Bottom | Left | Right | Notes |
|----------|-----|--------|------|-------|-------|
| **LinkedIn Feed** | 40px | 40px | 24px | 24px | Recommended 8-24px safe zone |
| **Instagram Stories** | 100px | 120px | 24px | 24px | UI overlays at top/bottom |
| **TikTok** | 100px | 180px | 24px | **80px** | Side buttons on right |
| **YouTube** | 20px | 20px | 20px | 20px | Standard margins |
| **Mobile Vertical** | 80px | 100px | - | - | 9:16 format |
| **Mobile Horizontal** | - | - | 24px | 24px | 16:9 format |
| **Instagram Square** | 32px (all sides) | - | - | - | 1:1 format |

## Component Library

### 📊 Charts (6 components)
All charts support design tokens and smooth animations:

- **PieChart** - Proportions and percentages
- **BarChart** - Vertical bar comparisons
- **HorizontalBarChart** - Ranked horizontal bars with top 3 highlighting
- **LineChart** - Trends over time
- **AreaChart** - Filled area trends
- **DonutChart** - Ring chart with center stat

### 🎨 Overlays (5 components)
- **TitleScene** - Full-screen animated titles (4 variants, 5 animations)
- **EndScreen** - YouTube end screens with CTAs (4 variants)
- **LowerThird** - Name plates (5 variants, 5 positions)
- **TextOverlay** - Animated text emphasis (5 styles, 5 animations)
- **SubscribeButton** - Animated subscribe button (5 animations)

### 💻 Code (2 components)
- **CodeBlock** - Syntax-highlighted code display (4 variants: minimal, terminal, editor, glass)
- **TypingCode** - Character-by-character typing animation (4 variants, 4 cursor styles)

### 📐 Layouts (17 components)
Professional video layouts for multi-platform content:

- **AsymmetricLayout** - Main feed (2/3) + stacked demo panels (1/3)
- **Container** - Content container with optional borders and backgrounds
- **DialogueFrame** - Conversation-style layout with speaker/audience
- **FocusStrip** - Main content with focus strip overlay
- **Grid** - Flexible grid layouts (8 types: 1x2, 2x1, 2x2, 3x2, 2x3, 3x3, 4x2, 2x4)
- **HUDStyle** - HUD-style overlay layout (4 corners + center)
- **Mosaic** - Multi-clip mosaic grid layout
- **OverTheShoulder** - Presenter with screen content
- **PerformanceMultiCam** - Primary camera + up to 4 secondary cameras
- **PiP** - Picture-in-picture with positioning
- **SplitScreen** - Side-by-side or top/bottom splits (4 divider styles)
- **StackedReaction** - Content with stacked reactions
- **ThreeByThreeGrid** - 3x3 grid layout for multiple items
- **ThreeColumnLayout** - Three-column layout
- **ThreeRowLayout** - Three-row layout
- **Timeline** - Timeline-based event display
- **Vertical** - Two-panel vertical split

### 🎬 Animations (1 component)
- **Counter** - Animated number counter (4 animations: count_up, flip, slot_machine, digital)

### ✨ Text Animations (6 components)
Dynamic text effects inspired by ReactBits:

- **TypewriterText** - Classic typewriter animation with optional blinking cursor
- **StaggerText** - Staggered reveal with spring physics (character or word-based)
- **WavyText** - Continuous wave motion with sine wave oscillation
- **TrueFocus** - Word-by-word focus cycling with animated corner brackets
- **DecryptedText** - Character scrambling reveal with multiple directions
- **FuzzyText** - VHS glitch effects with scanlines and RGB split

### 🎭 Demo Realism (5 components)
Realistic UI mockups and demonstrations:

- **BeforeAfterSlider** - Interactive before/after comparison slider
- **BrowserFrame** - Browser window with realistic chrome and tabs
- **CodeDiff** - Side-by-side code comparison with syntax highlighting
- **DeviceFrame** - Device mockups (phone, tablet, desktop) with content
- **Terminal** - Terminal window with command history and typing

### 📦 Content (1 component)
- **DemoBox** - Reusable content container for demos

**Total: 43 production-ready components** - All using design tokens with 100% test coverage!

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+ (for Remotion)
- npm or yarn

### Install Python Package

```bash
# Clone the repository
git clone https://github.com/chrishayuk/chuk-motion.git
cd chuk-motion

# Install dependencies with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

### Install Remotion

```bash
# Remotion is installed per-project automatically
# The MCP server handles this when generating projects
```

## Quick Start

### 1. Start the MCP Server

**STDIO Mode** (for Claude Desktop):
```bash
python -m chuk_motion.server stdio
```

**HTTP Mode** (for testing/development):
```bash
python -m chuk_motion.server http --port 8000
```

### 2. Create a Project

```python
# Via MCP tools
remotion_create_project(
    name="my_video",
    theme="tech",
    fps=30,
    width=1920,
    height=1080
)
```

### 3. Add Components

```python
# Add a title scene
remotion_add_title_scene(
    text="Welcome to AI Videos",
    subtitle="Created with Design Tokens",
    variant="bold",
    animation="fade_zoom",
    duration="3s"
)

# Add a chart with safe margins
remotion_add_pie_chart(
    data='[{"label": "AI", "value": 40}, {"label": "ML", "value": 30}]',
    title="Technology Distribution",
    duration="4s",
    gap_before="1s"  # Time strings supported!
)

# Add code with typing animation
remotion_add_typing_code(
    code="console.log('Hello, World!');",
    language="javascript",
    title="Example Code",
    typing_speed="medium",
    duration="5s"
)
```

### 4. Render the Video

```bash
cd remotion-projects/my_video
npm install
npm start  # Preview in browser
npm run build  # Render to MP4
```

## Examples

The `examples/` directory contains production-ready demos:

### Design System Showcases

```bash
# Complete design system showcase (90 seconds)
python examples/design_system_showcase.py

# Platform safe margins demo (60 seconds)
python examples/safe_margins_demo.py

# Explore all design tokens
python examples/explore_design_system.py
```

### Component Showcases

```bash
# Complete text animations showcase (52.5 seconds)
python examples/all_text_animations_demo.py

# Fibonacci code typing demo
python examples/fibonacci_demo.py
```

All examples use the **ProjectManager API** with the track-based timeline system.

## MCP Tools Reference

### Project Management
- `remotion_create_project(name, theme, fps, width, height)` - Create new project
- `remotion_get_project_info()` - Get current project info
- `remotion_list_projects()` - List all projects

### Component Tools (43 total)

#### Charts
- `remotion_add_pie_chart(data, title, duration, track, gap_before)`
- `remotion_add_bar_chart(data, title, duration, track, gap_before)`
- `remotion_add_horizontal_bar_chart(data, title, duration, track, gap_before)`
- `remotion_add_line_chart(data, title, xlabel, ylabel, duration, track, gap_before)`
- `remotion_add_area_chart(data, title, duration, track, gap_before)`
- `remotion_add_donut_chart(data, title, duration, track, gap_before)`

#### Overlays
- `remotion_add_title_scene(text, subtitle, variant, animation, duration, track, gap_before)`
- `remotion_add_end_screen(cta_text, variant, duration, track, gap_before)`
- `remotion_add_lower_third(name, title, variant, position, duration, track, gap_before)`
- `remotion_add_text_overlay(text, style, animation, position, duration, track, gap_before)`
- `remotion_add_subscribe_button(animation, position, duration, track, gap_before)`

#### Code
- `remotion_add_code_block(code, language, title, variant, animation, show_line_numbers, duration, track, gap_before)`
- `remotion_add_typing_code(code, language, title, variant, cursor_style, typing_speed, show_line_numbers, duration, track, gap_before)`

#### Layouts
- `remotion_add_grid(children, layout, duration, track, gap_before)`
- `remotion_add_container(content, border, duration, track, gap_before)`
- `remotion_add_split_screen(left, right, variant, duration, track, gap_before)`

#### Animations
- `remotion_add_counter(start_value, end_value, prefix, suffix, decimals, animation, duration, track, gap_before)`

#### Text Animations
- `remotion_add_typewriter_text(text, font_size, font_weight, text_color, cursor_color, show_cursor, type_speed, position, align, duration, track, gap_before)`
- `remotion_add_stagger_text(text, font_size, font_weight, text_color, stagger_by, stagger_delay, animation_type, position, align, duration, track, gap_before)`
- `remotion_add_wavy_text(text, font_size, font_weight, text_color, wave_amplitude, wave_speed, wave_frequency, position, align, duration, track, gap_before)`
- `remotion_add_true_focus(text, font_size, font_weight, text_color, word_duration, position, duration, track, gap_before)`
- `remotion_add_decrypted_text(text, font_size, font_weight, text_color, reveal_direction, scramble_speed, position, duration, track, gap_before)`
- `remotion_add_fuzzy_text(text, font_size, font_weight, text_color, glitch_intensity, animate, position, duration, track, gap_before)`

### Discovery Tools
- `remotion_list_components(category)` - List available components
- `remotion_search_components(query)` - Search components
- `remotion_get_component_schema(name)` - Get component details
- `remotion_list_themes()` - List available themes
- `remotion_get_theme_info(name)` - Get theme details

### Token Tools
- `remotion_list_color_tokens()` - Color palettes
- `remotion_list_typography_tokens()` - Typography system
- `remotion_list_motion_tokens()` - Motion design
- `remotion_list_spacing_tokens()` ⭐ NEW - Spacing and safe margins

### Info Tools
- `remotion_get_info()` - Server information and statistics

## Time String Format ⭐ NEW

All duration and timing parameters support flexible time strings:

```python
# String formats
duration="2s"       # 2 seconds
duration="500ms"    # 500 milliseconds
duration="1.5s"     # 1.5 seconds
duration="1m"       # 1 minute (60 seconds)
gap_before="1s"     # 1 second gap
gap_before="250ms"  # 250ms gap

# Float format still works
duration=2.0
gap_before=0.5
```

## Track-Based Timeline System

The timeline uses a professional multi-track approach:

```python
# Main track: Sequential auto-stacking
remotion_add_title_scene(...)  # Starts at 0s
remotion_add_pie_chart(...)    # Auto-stacks after title
remotion_add_bar_chart(...)    # Auto-stacks after pie chart

# Overlay track: Layers on top
remotion_add_text_overlay(..., track="overlay", align_to="main", offset=5.0)

# Background track: Behind main content
remotion_add_background(..., track="background")
```

**Default Tracks:**
- `main` (layer 0) - Primary content, auto-stacks with 0.5s gap
- `overlay` (layer 10) - Text overlays, UI elements
- `background` (layer -10) - Background media

## Themes

### Tech Theme
Modern tech aesthetic with blue/cyan palette
- **Colors**: Primary blue (#0066FF), Accent cyan (#00D9FF)
- **Use Cases**: Tech reviews, coding tutorials, software demos

### Finance Theme
Professional finance with green/gold
- **Colors**: Primary green (#00C853), Accent gold (#FFD600)
- **Use Cases**: Stock analysis, investing advice, business news

### Education Theme
Friendly education with purple/orange
- **Colors**: Primary purple (#7C4DFF), Accent orange (#FF6E40)
- **Use Cases**: Educational content, explainers, courses

### Gaming Theme
High-energy gaming with neon accents
- **Colors**: Neon green (#00E676), Neon purple (#E040FB)
- **Use Cases**: Gaming videos, esports, stream overlays

### Minimal Theme
Clean monochrome aesthetic
- **Colors**: Grayscale with subtle accents
- **Use Cases**: Professional content, documentaries

### Lifestyle Theme
Warm lifestyle with coral/pink
- **Colors**: Pink (#FF6B9D), Coral (#FFB74D)
- **Use Cases**: Vlogs, lifestyle, wellness, travel

### Business Theme
Professional business with navy/teal
- **Colors**: Navy (#1565C0), Teal (#00ACC1)
- **Use Cases**: Corporate videos, presentations, B2B

## Configuration for Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "remotion": {
      "command": "python",
      "args": ["-m", "chuk_motion.server", "stdio"],
      "env": {
        "MCP_STDIO": "1"
      }
    }
  }
}
```

## Development

### Project Structure

```
chuk-motion/
├── src/chuk_motion/
│   ├── server.py              # Main MCP server
│   ├── tokens/                # Design tokens ⭐
│   │   ├── colors.py         # Color palettes (7 themes)
│   │   ├── typography.py     # Typography system
│   │   ├── motion.py         # Motion design
│   │   ├── spacing.py        # Spacing & safe margins ⭐ NEW
│   │   └── token_manager.py  # Token import/export
│   ├── themes/               # Theme system
│   │   └── youtube_themes.py # 7 YouTube-optimized themes
│   ├── components/           # Component library ⭐
│   │   ├── charts/          # 6 chart components
│   │   ├── overlays/        # 5 overlay components
│   │   ├── code/            # 2 code components
│   │   ├── layouts/         # 17 layout components ⭐
│   │   ├── animations/      # 1 animation component
│   │   ├── text-animations/ # 6 text animation components ⭐
│   │   ├── frames/          # Frame components
│   │   ├── demo_realism/    # 5 demo realism components ⭐
│   │   └── content/         # 1 content component
│   ├── generator/            # TSX generation
│   │   ├── component_builder.py    # Jinja2 templating
│   │   ├── composition_builder.py  # Component instances
│   │   └── timeline.py            # Track-based timeline ⭐
│   ├── utils/                # Utilities
│   │   └── project_manager.py     # Project scaffolding ⭐
│   └── models.py             # Pydantic models
├── examples/                 # Production examples ⭐
│   ├── design_system_showcase.py
│   ├── safe_margins_demo.py
│   ├── fibonacci_demo.py
│   └── explore_design_system.py
├── tests/                    # Tests
├── remotion-templates/       # Base Remotion templates
└── remotion-projects/        # Generated projects (gitignored)
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov
```

### Code Quality

```bash
# Run all checks (linting, type checking, tests)
make check

# Individual checks
make lint       # Ruff linting
make format     # Ruff formatting
make typecheck  # MyPy type checking
make test       # Run all tests
```

**All checks must pass before committing!** The `make check` command runs linting, type checking, and all 950 tests to ensure code quality.

## Recent Updates ⭐

### Text Animation Components (January 2025)
- ✅ **6 new text animation components**: TypewriterText, StaggerText, WavyText, TrueFocus, DecryptedText, FuzzyText
- ✅ Created dedicated `text-animations/` folder for better organization
- ✅ Moved text animations from `overlays/` to `text-animations/`
- ✅ Inspired by [ReactBits](https://www.reactbits.dev/text-animations)
- ✅ All components use design tokens and spring physics
- ✅ Complete demo with 20 scenes (52.5 seconds)
- ✅ Total components: **43 production-ready components**

### Test Coverage Achievement (January 2025)
- ✅ **100% test coverage** on all 17 layout component tools
- ✅ **98% coverage** on token_manager.py (improved from 81%)
- ✅ **950 passing tests** with comprehensive test suite
- ✅ Added JSON parsing error tests to all layout tools
- ✅ Removed 67 legacy tests, replaced with modular tests
- ✅ All builder.py files at 100% coverage

### Component Library Expansion (January 2025)
- ✅ **17 layout components** (up from 3): AsymmetricLayout, Container, DialogueFrame, FocusStrip, Grid, HUDStyle, Mosaic, OverTheShoulder, PerformanceMultiCam, PiP, SplitScreen, StackedReaction, ThreeByThreeGrid, ThreeColumnLayout, ThreeRowLayout, Timeline, Vertical
- ✅ **6 text animation components**: TypewriterText, StaggerText, WavyText, TrueFocus, DecryptedText, FuzzyText
- ✅ **5 demo realism components**: BeforeAfterSlider, BrowserFrame, CodeDiff, DeviceFrame, Terminal
- ✅ **1 content component**: DemoBox
- ✅ Total: **43 production-ready components**

### Design System Integration (January 2025)
- ✅ Created comprehensive spacing tokens with 7 platform safe margins
- ✅ Applied design tokens to ALL 43 components (100% coverage)
- ✅ Fixed Jinja2 template rendering for token context
- ✅ Updated all themes with spacing tokens
- ✅ Fixed Pydantic v2 compatibility issues

### Time String Support (January 2025)
- ✅ Support for time strings: "1s", "500ms", "1m"
- ✅ Fixed `gap_before` string concatenation bug
- ✅ Updated all 43 MCP tools to accept time strings
- ✅ Enhanced `seconds_to_frames()` with format parsing

### Example Files (January 2025)
- ✅ Fixed ProjectManager API usage in all examples
- ✅ Created design system showcase demo (90s)
- ✅ Created platform safe margins demo (60s)
- ✅ Created text animations showcase demo (52.5s)
- ✅ Fixed EndScreen thumbnail handling

## Roadmap

### Phase 1: Foundation ✅ COMPLETE
- ✅ Design token system (colors, typography, motion, spacing)
- ✅ Component registry with 17 components
- ✅ 7 YouTube-optimized themes
- ✅ Discovery tools for LLMs
- ✅ Track-based timeline system
- ✅ Platform safe margin support

### Phase 2: Generation ✅ COMPLETE
- ✅ TSX component generation with Jinja2
- ✅ Remotion project scaffolding
- ✅ Composition builder with ComponentInstance
- ✅ ProjectManager API
- ✅ Time string parsing ("1s", "500ms")

### Phase 3: Rendering 🚧 IN PROGRESS
- 🔲 Remotion render integration
- 🔲 Export to MP4/WebM
- 🔲 Thumbnail generation
- 🔲 Preview generation

### Phase 4: Advanced Features
- 🔲 Custom theme builder
- 🔲 Animation timeline editor
- 🔲 Audio sync
- 🔲 Asset management
- 🔲 Auto-captioning
- 🔲 Light/dark mode switching

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `make lint && make format && make typecheck`
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- **GitHub**: https://github.com/chrishayuk/chuk-motion
- **Related Projects**:
  - [chuk-mcp-server](https://github.com/chrishayuk/chuk-mcp-server) - Zero-config MCP framework
  - [chuk-mcp-pptx](https://github.com/chrishayuk/chuk-mcp-pptx) - PowerPoint MCP server
  - [Remotion](https://www.remotion.dev) - React-based video generation

## Author

**Chris Hay** - [@chrishayuk](https://github.com/chrishayuk)

---

Built with ❤️ using [chuk-mcp-server](https://github.com/chrishayuk/chuk-mcp-server) and [Remotion](https://www.remotion.dev)
