# chuk-motion

> AI-powered video generation with Remotion - A design-system-first approach to creating professional multi-platform videos

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-compatible-green.svg)](https://github.com/anthropics/mcp)
[![Tests](https://img.shields.io/badge/tests-1471%20passing-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-86%25-brightgreen.svg)](tests/)

## Overview

`chuk-motion` is an MCP (Model Context Protocol) server that brings the power of [Remotion](https://www.remotion.dev) video generation to AI assistants like Claude. It provides a **design-system-first approach** with comprehensive design tokens, enabling AI to create professional, animated videos optimized for **YouTube, TikTok, LinkedIn, Instagram Stories**, and more.

### Key Features

- **🎨 Complete Design System**: Design tokens for colors, typography, spacing, and motion
- **📱 Multi-Platform Support**: Safe margins for LinkedIn, TikTok, Instagram, YouTube
- **🎬 51 Video Components**: Charts, code blocks, scenes, overlays, layouts, animations, text animations, transitions, and demo realism
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

### 🎬 Scenes (2 components)
- **TitleScene** - Full-screen animated titles (4 variants, 5 animations)
- **EndScreen** - YouTube end screens with CTAs (4 variants)

### 🎨 Overlays (3 components)
- **LowerThird** - Name plates (5 variants, 5 positions)
- **TextOverlay** - Animated text emphasis (5 styles, 5 animations)
- **SubscribeButton** - Animated subscribe button (5 animations)

### 💻 Code (3 components)
- **CodeBlock** - Syntax-highlighted code display (4 variants: minimal, terminal, editor, glass)
- **TypingCode** - Character-by-character typing animation (4 variants, 4 cursor styles)
- **CodeDiff** - Side-by-side code comparison with syntax highlighting

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

### 🎬 Animations (3 components)
- **Counter** - Animated number counter (4 animations: count_up, flip, slot_machine, digital)
- **LayoutEntrance** - Layout entrance animations for smooth component reveals
- **PanelCascade** - Cascading panel animations for sequential reveals

### ✨ Text Animations (6 components)
Dynamic text effects inspired by ReactBits:

- **TypewriterText** - Classic typewriter animation with optional blinking cursor
- **StaggerText** - Staggered reveal with spring physics (character or word-based)
- **WavyText** - Continuous wave motion with sine wave oscillation
- **TrueFocus** - Word-by-word focus cycling with animated corner brackets
- **DecryptedText** - Character scrambling reveal with multiple directions
- **FuzzyText** - VHS glitch effects with scanlines and RGB split

### 🎭 Demo Realism (4 components)
Realistic UI mockups and demonstrations:

- **BeforeAfterSlider** - Interactive before/after comparison slider
- **BrowserFrame** - Browser window with realistic chrome and tabs
- **DeviceFrame** - Device mockups (phone, tablet, desktop) with content
- **Terminal** - Terminal window with command history and typing

### 📦 Content (5 components)
- **DemoBox** - Reusable content container for demos
- **ImageContent** - Image display with flexible sizing (contain, cover, fill) and styling options
- **StylizedWebPage** - Stylized webpage mockup for demonstrations
- **VideoContent** - Video content placeholder with controls
- **WebPage** - Clean webpage mockup with customizable content

### 🔄 Transitions (2 components)
- **LayoutTransition** - Smooth transitions between different layouts
- **PixelTransition** - Pixelated transition effects

**Total: 51 production-ready components** - All using design tokens with comprehensive test coverage!

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+ (for Remotion)
- npm or yarn

### Install Python Package

```bash
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

# Add images
remotion_add_image_content(
    src="https://picsum.photos/1920/1080",
    fit="cover",
    duration="3s"
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

# Image layouts showcase - 17 examples (127 seconds)
python examples/image_layouts_showcase.py

# Content showcase - All 5 content components
python examples/content_showcase.py

# Fibonacci code typing demo
python examples/fibonacci_demo.py
```

All examples use the **ProjectManager API** with the track-based timeline system.

## MCP Tools Reference

### Project Management
- `remotion_create_project(name, theme, fps, width, height)` - Create new project
- `remotion_get_project_info()` - Get current project info
- `remotion_list_projects()` - List all projects

### Component Tools (50 total)

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
│   ├── async_server.py        # Async MCP server variant
│   ├── video_manager.py       # High-level video management ⭐ NEW
│   ├── tokens/                # Design tokens
│   │   ├── colors.py         # Color palettes (7 themes)
│   │   ├── typography.py     # Typography system
│   │   ├── motion.py         # Motion design
│   │   ├── spacing.py        # Spacing & safe margins
│   │   └── token_manager.py  # Token import/export
│   ├── themes/               # Theme system
│   │   └── youtube_themes.py # 7 YouTube-optimized themes
│   ├── components/           # Component library (51 components)
│   │   ├── charts/          # 6 chart components
│   │   ├── overlays/        # 3 overlay components
│   │   ├── code/            # 3 code components
│   │   ├── layouts/         # 17 layout components
│   │   ├── animations/      # 3 animation components
│   │   ├── text_animations/ # 6 text animation components
│   │   ├── frames/          # 3 frame components
│   │   ├── transitions/     # 2 transition components
│   │   └── content/         # 5 content components
│   ├── generator/            # TSX generation
│   │   ├── component_builder.py    # Jinja2 templating
│   │   ├── composition_builder.py  # Component instances
│   │   └── timeline.py            # Track-based timeline
│   ├── render/               # Video rendering ⭐ NEW
│   │   ├── project_exporter.py    # Remotion project export
│   │   └── video_renderer.py      # MP4 rendering via CLI
│   ├── rendering/            # Remotion integration
│   │   └── remotion_renderer.py   # Remotion rendering
│   ├── storage/              # Artifact storage ⭐ NEW
│   │   └── artifact_storage.py    # chuk-artifacts integration
│   ├── tools/                # MCP tools
│   │   ├── theme_tools.py         # Theme management tools
│   │   ├── token_tools.py         # Token tools
│   │   └── artifact_tools.py      # Artifact management tools
│   ├── utils/                # Utilities
│   │   ├── project_manager.py     # Project scaffolding
│   │   └── async_project_manager.py # Async project manager
│   └── models/               # Pydantic models
│       ├── artifact_models.py     # Storage models
│       └── responses.py           # Response models
├── examples/                 # Production examples
│   ├── design_system_showcase.py
│   ├── safe_margins_demo.py
│   ├── fibonacci_demo.py
│   └── explore_design_system.py
├── tests/                    # 1471 tests
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

**All checks must pass before committing!** The `make check` command runs linting, type checking, and all 1471 tests to ensure code quality.

## Recent Updates ⭐

### Video Rendering & Storage (December 2025)
- ✅ **Video Renderer**: Full Remotion CLI integration for MP4 export
- ✅ **Background Rendering**: Async job system with progress tracking
- ✅ **Artifact Storage**: Integration with chuk-artifacts for persistent storage
- ✅ **VideoManager**: High-level API for video project management
- ✅ **Project Exporter**: RemotionProjectExporter for scaffolding complete projects
- ✅ **Test Coverage**: 1471 tests passing with 86% coverage

### ImageContent Component (January 2025)
- ✅ **New ImageContent component** for displaying images in videos
- ✅ Flexible sizing modes: `cover`, `contain`, `fill`
- ✅ Styling options: opacity, border radius
- ✅ Design token integration for consistent styling
- ✅ Created comprehensive `image_layouts_showcase.py` with 17 real-world examples
- ✅ Fixed Mosaic layout to properly wrap clips in `{content: ...}` structure
- ✅ Fixed specialized layout prop keys (AsymmetricLayout, OverTheShoulder, DialogueFrame, etc.)
- ✅ Updated content_showcase.py to include ImageContent
- ✅ Total components: **51 production-ready components**

### Text Animation Components (January 2025)
- ✅ **6 new text animation components**: TypewriterText, StaggerText, WavyText, TrueFocus, DecryptedText, FuzzyText
- ✅ Created dedicated `text_animations/` folder for better organization
- ✅ Moved text animations from `overlays/` to `text_animations/`
- ✅ Inspired by [ReactBits](https://www.reactbits.dev/text-animations)
- ✅ All components use design tokens and spring physics
- ✅ Complete demo with 20 scenes (52.5 seconds)
- ✅ Total components: **51 production-ready components**

### Test Coverage Achievement (December 2025)
- ✅ **1471 passing tests** with comprehensive test suite
- ✅ **86% overall coverage** across the codebase
- ✅ **100% coverage** on video_renderer.py
- ✅ **97% coverage** on remotion_renderer.py and project_exporter.py
- ✅ **96% coverage** on theme_tools.py
- ✅ **94-95% coverage** on component_builder.py, timeline.py, theme_manager.py
- ✅ All builder.py files at 100% coverage

### Component Library Expansion (January 2025)
- ✅ **51 production-ready components** organized into 9 categories
- ✅ **17 layout components**: AsymmetricLayout, Container, DialogueFrame, FocusStrip, Grid, HUDStyle, Mosaic, OverTheShoulder, PerformanceMultiCam, PiP, SplitScreen, StackedReaction, ThreeByThreeGrid, ThreeColumnLayout, ThreeRowLayout, Timeline, Vertical
- ✅ **6 text animation components**: TypewriterText, StaggerText, WavyText, TrueFocus, DecryptedText, FuzzyText
- ✅ **6 chart components**: PieChart, BarChart, HorizontalBarChart, LineChart, AreaChart, DonutChart
- ✅ **5 content components**: DemoBox, ImageContent, StylizedWebPage, VideoContent, WebPage
- ✅ **4 demo realism components**: BeforeAfterSlider, BrowserFrame, DeviceFrame, Terminal
- ✅ **3 frame components**: BrowserFrame, DeviceFrame, Terminal
- ✅ **3 animation components**: Counter, LayoutEntrance, PanelCascade
- ✅ **3 code components**: CodeBlock, TypingCode, CodeDiff
- ✅ **3 overlay components**: LowerThird, TextOverlay, SubscribeButton
- ✅ **2 scene components**: TitleScene, EndScreen
- ✅ **2 transition components**: LayoutTransition, PixelTransition

### Design System Integration (January 2025)
- ✅ Created comprehensive spacing tokens with 7 platform safe margins
- ✅ Applied design tokens to ALL 51 components (100% coverage)
- ✅ Fixed Jinja2 template rendering for token context
- ✅ Updated all themes with spacing tokens
- ✅ Fixed Pydantic v2 compatibility issues

### Time String Support (January 2025)
- ✅ Support for time strings: "1s", "500ms", "1m"
- ✅ Fixed `gap_before` string concatenation bug
- ✅ Updated all 51 MCP tools to accept time strings
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

### Phase 3: Rendering ✅ COMPLETE
- ✅ Remotion render integration with video_renderer
- ✅ Export to MP4 via Remotion CLI
- ✅ Background rendering with job status tracking
- ✅ Progress monitoring during renders
- ✅ RemotionProjectExporter for project scaffolding

### Phase 4: Storage & Artifacts ✅ COMPLETE
- ✅ ArtifactStorageManager with chuk-artifacts integration
- ✅ Project storage (WORKSPACE namespaces)
- ✅ Render storage (BLOB namespaces)
- ✅ Asset management for media files
- ✅ Checkpoint/versioning support
- ✅ VideoManager for high-level video operations

### Phase 5: Advanced Features
- 🔲 Custom theme builder
- 🔲 Animation timeline editor
- 🔲 Audio sync
- 🔲 Auto-captioning
- 🔲 Light/dark mode switching
- 🔲 Cloud rendering integration

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `make lint && make format && make typecheck`
5. Submit a pull request

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Links

- **Related Projects**:
  - chuk-mcp-server - Zero-config MCP framework
  - chuk-mcp-pptx - PowerPoint MCP server
  - [Remotion](https://www.remotion.dev) - React-based video generation
