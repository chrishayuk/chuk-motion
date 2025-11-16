# Component Documentation

## Overview

This directory contains comprehensive documentation for all Remotion components in the chuk-motion generator system. Each component has its own documentation file with usage examples, props reference, and best practices.

## Quick Start

1. **Read** [COMPONENT_DESIGN.md](./COMPONENT_DESIGN.md) to understand overall architecture
2. **Browse** component categories below
3. **Refer** to individual component docs for detailed usage

## Documentation Structure

```
docs/components/
├── COMPONENT_DESIGN.md       # Architecture & design principles
├── README.md                 # This file - component index
├── overlays/                 # UI overlay components
│   ├── TitleScene.md
│   └── LowerThird.md
├── content/                  # Content display components
│   ├── CodeBlock.md
│   ├── TypingCode.md
│   ├── LineChart.md
│   └── DemoBox.md
└── layouts/                  # Container layout components
    ├── Grid.md
    ├── AsymmetricLayout.md
    └── ... (more layouts)
```

---

## Component Categories

**Total: 50 Production-Ready Components**

### 🎬 Scenes (2 components)
Full-screen scene components for titles and end cards.

| Component | Description | Template | Tests |
|-----------|-------------|----------|-------|
| **TitleScene** | Full-screen title cards with animations | `overlays/TitleScene.tsx.j2` | ✅ |
| **EndScreen** | YouTube end screens with CTAs | `overlays/EndScreen.tsx.j2` | ✅ |

### 🎨 Overlays (3 components)
Overlay components appear on top of content - perfect for labels and information displays.

| Component | Description | Template | Tests |
|-----------|-------------|----------|-------|
| **LowerThird** | Name/title overlays at screen edges | `overlays/LowerThird.tsx.j2` | ✅ |
| **TextOverlay** | Animated text emphasis | `overlays/TextOverlay.tsx.j2` | ✅ |
| **SubscribeButton** | Animated subscribe button | `overlays/SubscribeButton.tsx.j2` | ✅ |

### 📊 Charts (6 components)
Data visualization components with smooth animations.

| Component | Description | Template | Tests |
|-----------|-------------|----------|-------|
| **PieChart** | Proportions and percentages | `charts/PieChart.tsx.j2` | ✅ |
| **BarChart** | Vertical bar comparisons | `charts/BarChart.tsx.j2` | ✅ |
| **HorizontalBarChart** | Ranked horizontal bars | `charts/HorizontalBarChart.tsx.j2` | ✅ |
| **LineChart** | Trends over time | `charts/LineChart.tsx.j2` | ✅ |
| **AreaChart** | Filled area trends | `charts/AreaChart.tsx.j2` | ✅ |
| **DonutChart** | Ring chart with center stat | `charts/DonutChart.tsx.j2` | ✅ |

### 💻 Code (3 components)
Code display components with syntax highlighting.

| Component | Description | Template | Tests |
|-----------|-------------|----------|-------|
| **CodeBlock** | Syntax-highlighted code display | `code/CodeBlock.tsx.j2` | ✅ |
| **TypingCode** | Character-by-character typing animation | `code/TypingCode.tsx.j2` | ✅ |
| **CodeDiff** | Side-by-side code comparison | `code/CodeDiff.tsx.j2` | ✅ |

### 📐 Layouts (17 components)
Layout components arrange and organize other components on screen.

| Component | Description | Template | Tests |
|-----------|-------------|----------|-------|
| **Grid** | Flexible grid (1x2, 2x2, 3x3, etc.) | `layouts/Grid.tsx.j2` | ✅ |
| **AsymmetricLayout** | Main feed + stacked demos | `layouts/AsymmetricLayout.tsx.j2` | ✅ |
| **Container** | Simple wrapper container | `layouts/Container.tsx.j2` | ✅ |
| **DialogueFrame** | Split screen for conversations | `layouts/DialogueFrame.tsx.j2` | ✅ |
| **FocusStrip** | Centered host bar over background | `layouts/FocusStrip.tsx.j2` | ✅ |
| **HUDStyle** | Gaming HUD with overlays | `layouts/HUDStyle.tsx.j2` | ✅ |
| **Mosaic** | Mosaic tile arrangement | `layouts/Mosaic.tsx.j2` | ✅ |
| **OverTheShoulder** | Host + screen side-by-side | `layouts/OverTheShoulder.tsx.j2` | ✅ |
| **PerformanceMultiCam** | Multi-camera grid | `layouts/PerformanceMultiCam.tsx.j2` | ✅ |
| **PiP** | Picture-in-picture overlay | `layouts/PiP.tsx.j2` | ✅ |
| **SplitScreen** | 50/50 split (horizontal/vertical) | `layouts/SplitScreen.tsx.j2` | ✅ |
| **StackedReaction** | Vertical stack for reactions | `layouts/StackedReaction.tsx.j2` | ✅ |
| **ThreeByThreeGrid** | 3x3 grid layout | `layouts/ThreeByThreeGrid.tsx.j2` | ✅ |
| **ThreeColumnLayout** | 3-column flexible layout | `layouts/ThreeColumnLayout.tsx.j2` | ✅ |
| **ThreeRowLayout** | 3-row flexible layout | `layouts/ThreeRowLayout.tsx.j2` | ✅ |
| **Timeline** | Progress timeline with milestones | `layouts/Timeline.tsx.j2` | ✅ |
| **Vertical** | 9:16 vertical layouts (Shorts/Reels) | `layouts/Vertical.tsx.j2` | ✅ |

### 🎬 Animations (3 components)
Animation components for dynamic effects.

| Component | Description | Template | Tests |
|-----------|-------------|----------|-------|
| **Counter** | Animated number counter | `animations/Counter.tsx.j2` | ✅ |
| **LayoutEntrance** | Layout entrance animations | `animations/LayoutEntrance.tsx.j2` | ✅ |
| **PanelCascade** | Cascading panel animations | `animations/PanelCascade.tsx.j2` | ✅ |

### ✨ Text Animations (6 components)
Dynamic text effects inspired by ReactBits.

| Component | Description | Template | Tests |
|-----------|-------------|----------|-------|
| **TypewriterText** | Classic typewriter animation | `text_animations/TypewriterText.tsx.j2` | ✅ |
| **StaggerText** | Staggered reveal with spring physics | `text_animations/StaggerText.tsx.j2` | ✅ |
| **WavyText** | Continuous wave motion | `text_animations/WavyText.tsx.j2` | ✅ |
| **TrueFocus** | Word-by-word focus cycling | `text_animations/TrueFocus.tsx.j2` | ✅ |
| **DecryptedText** | Character scrambling reveal | `text_animations/DecryptedText.tsx.j2` | ✅ |
| **FuzzyText** | VHS glitch effects | `text_animations/FuzzyText.tsx.j2` | ✅ |

### 🎭 Demo Realism (4 components)
Realistic UI mockups and demonstrations (also in frames/).

| Component | Description | Template | Tests |
|-----------|-------------|----------|-------|
| **BeforeAfterSlider** | Interactive before/after comparison | `layouts/BeforeAfterSlider.tsx.j2` | ✅ |
| **BrowserFrame** | Browser window with realistic chrome | `frames/BrowserFrame.tsx.j2` | ✅ |
| **DeviceFrame** | Device mockups (phone, tablet, desktop) | `frames/DeviceFrame.tsx.j2` | ✅ |
| **Terminal** | Terminal window with command history | `frames/Terminal.tsx.j2` | ✅ |

### 📦 Content (4 components)
Content display components for various media types.

| Component | Description | Template | Tests |
|-----------|-------------|----------|-------|
| **DemoBox** | Reusable content container | `content/DemoBox.tsx.j2` | ✅ |
| **StylizedWebPage** | Stylized webpage mockup | `content/StylizedWebPage.tsx.j2` | ✅ |
| **VideoContent** | Video content placeholder | `content/VideoContent.tsx.j2` | ✅ |
| **WebPage** | Clean webpage mockup | `content/WebPage.tsx.j2` | ✅ |

### 🔄 Transitions (2 components)
Transition effects between scenes and layouts.

| Component | Description | Template | Tests |
|-----------|-------------|----------|-------|
| **LayoutTransition** | Smooth transitions between layouts | `transitions/LayoutTransition.tsx.j2` | ✅ |
| **PixelTransition** | Pixelated transition effects | `transitions/PixelTransition.tsx.j2` | ✅ |

---

## Component Design Principles

All components follow consistent design patterns. See [COMPONENT_DESIGN.md](./COMPONENT_DESIGN.md) for:

- **Timing Props** - All components use `startFrame` and `durationInFrames`
- **Props vs Templates** - When to use runtime props vs template variables
- **Children Handling** - Named props vs children arrays
- **Styling Patterns** - Absolute positioning, flexbox, grid
- **Animation Patterns** - Springs, interpolate, entrance/exit
- **Design Tokens** - Using theme colors, fonts, and motion
- **Best Practices** - Do's and don'ts for component development

---

## Common Use Cases by Video Type

### Coding Tutorials
- **TitleScene** - Episode title
- **CodeBlock** / **TypingCode** - Show code
- **AsymmetricLayout** - Editor + terminal + output
- **LowerThird** - Instructor name
- **Grid** - Code comparisons

### Educational Content
- **TitleScene** - Chapter titles
- **LineChart** - Data visualization
- **Grid** - Multi-panel comparisons
- **TimelineLayout** - Progress tracking
- **LowerThird** - Speaker credentials

### Gaming Content
- **HUDStyleLayout** - Gameplay + webcam + chat
- **PiPLayout** - Main gameplay + facecam
- **LowerThird** - Player info
- **Grid** - Multi-player views

### Reaction Videos
- **StackedReactionLayout** - Original + reactor
- **LowerThird** - Content creator info
- **TitleScene** - Video intro

### Interviews/Podcasts
- **DialogueFrameLayout** - Split screen conversation
- **LowerThird** - Guest identification
- **TitleScene** - Episode card
- **TimelineLayout** - Topic progression

---

## Testing

Every component has comprehensive test coverage:
- **950+ tests total** across all components and systems
- **98% overall coverage**
- **100% pass rate**
- Tests organized by component type
- See `tests/` for full test suite

---

## Contributing

When adding a new component:

1. **Create template** in appropriate category (`overlays/`, `content/`, `layouts/`)
2. **Write tests** following existing patterns (see `tests/templates/`)
3. **Document component** using this documentation structure
4. **Update this README** with component entry
5. **Follow design principles** from COMPONENT_DESIGN.md

### Documentation Template

Each component doc should include:

- **Overview** - Brief description and use cases
- **Props** - Required and optional props table
- **Variants** - Style/animation variants (if applicable)
- **Usage Example** - TypeScript examples
- **Scene Configuration** - Python config format
- **Design Tokens** - Theme tokens used
- **Animation Behavior** - Timing and transitions
- **Best Practices** - Do's and don'ts
- **Common Patterns** - Real-world examples
- **Testing** - Link to test file

See existing docs for examples:
- [TitleScene.md](./overlays/TitleScene.md) - Full-featured overlay
- [CodeBlock.md](./content/CodeBlock.md) - Content with variants
- [Grid.md](./layouts/Grid.md) - Layout with children array
- [AsymmetricLayout.md](./layouts/AsymmetricLayout.md) - Layout with named props

---

## Quick Reference

### All Components Require
- `startFrame: number` - When to appear
- `durationInFrames: number` - How long visible

### Content Components Accept
- Content data (code, text, data, etc.)
- Visual variant options
- Animation options

### Layout Components Accept
- Children (array or named props)
- Sizing/spacing configuration
- Border/styling options

---

## Resources

- [Component Design Principles](./COMPONENT_DESIGN.md)
- [Template Testing Guide](../../tests/templates/README_TEMPLATE_TESTS.md)
- [Theme System](../../src/chuk_motion/themes/youtube_themes.py)
- [Component Builder](../../src/chuk_motion/generator/component_builder.py)

---

**Status**: All 50 components are registered and tested. Comprehensive documentation available in the main README.

To contribute component-specific documentation, follow the patterns established in existing component docs like TitleScene.md, CodeBlock.md, and Grid.md.
