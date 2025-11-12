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

### 🎬 Overlays
Overlay components appear on top of content - perfect for titles, labels, and information displays.

| Component | Description | Documentation | Template | Tests |
|-----------|-------------|---------------|----------|-------|
| **TitleScene** | Full-screen title cards with animations | [📖 Docs](./overlays/TitleScene.md) | `overlays/TitleScene.tsx.j2` | `tests/templates/overlays/test_titlescene.py` |
| **LowerThird** | Name/title overlays at screen edges | [📖 Docs](./overlays/LowerThird.md) | `overlays/LowerThird.tsx.j2` | `tests/templates/overlays/test_lowerthird.py` |

---

### 📄 Content
Content components display primary visual information like code, charts, and visualizations.

| Component | Description | Documentation | Template | Tests |
|-----------|-------------|---------------|----------|-------|
| **CodeBlock** | Syntax-highlighted code display | [📖 Docs](./content/CodeBlock.md) | `content/CodeBlock.tsx.j2` | `tests/templates/content/test_codeblock.py` |
| **TypingCode** | Animated typing effect for code | [📖 Docs](./content/TypingCode.md) | `content/TypingCode.tsx.j2` | `tests/templates/content/test_typingcode.py` |
| **LineChart** | SVG-based data visualization | [📖 Docs](./content/LineChart.md) | `content/LineChart.tsx.j2` | `tests/templates/content/test_linechart.py` |
| **DemoBox** | Simple colored placeholder boxes | [📖 Docs](./content/DemoBox.md) | `content/DemoBox.tsx.j2` | `tests/templates/content/test_demobox.py` |

---

### 📐 Layouts
Layout components arrange and organize other components on screen.

#### Grid Layouts

| Component | Description | Documentation | Template | Tests |
|-----------|-------------|---------------|----------|-------|
| **Grid** | Flexible grid (1x2, 2x2, 3x3, etc.) | [📖 Docs](./layouts/Grid.md) | `layouts/Grid.tsx.j2` | `tests/templates/layouts/test_grid.py` |
| **ThreeByThreeGrid** | 3x3 grid layout | *To be documented* | `layouts/ThreeByThreeGrid.tsx.j2` | `tests/templates/layouts/test_threebythreegrid.py` |
| **ThreeColumnLayout** | 3-column flexible layout | *To be documented* | `layouts/ThreeColumnLayout.tsx.j2` | `tests/templates/layouts/test_threecolumnlayout.py` |
| **ThreeRowLayout** | 3-row flexible layout | *To be documented* | `layouts/ThreeRowLayout.tsx.j2` | `tests/templates/layouts/test_threerowlayout.py` |

#### Asymmetric Layouts

| Component | Description | Documentation | Template | Tests |
|-----------|-------------|---------------|----------|-------|
| **AsymmetricLayout** | Main feed + stacked demos | [📖 Docs](./layouts/AsymmetricLayout.md) | `layouts/AsymmetricLayout.tsx.j2` | `tests/templates/layouts/test_asymmetriclayout.py` |
| **SplitScreen** | 50/50 split (horizontal/vertical) | *To be documented* | `layouts/SplitScreen.tsx.j2` | `tests/templates/layouts/test_splitscreen.py` |
| **PiPLayout** | Picture-in-picture overlay | *To be documented* | `layouts/PiPLayout.tsx.j2` | `tests/templates/layouts/test_piplayout.py` |

#### Specialized Layouts

| Component | Description | Documentation | Template | Tests |
|-----------|-------------|---------------|----------|-------|
| **VerticalLayout** | 9:16 vertical layouts (Shorts/Reels) | *To be documented* | `layouts/VerticalLayout.tsx.j2` | `tests/templates/layouts/test_verticallayout.py` |
| **DialogueFrameLayout** | Split screen for conversations | *To be documented* | `layouts/DialogueFrameLayout.tsx.j2` | `tests/templates/layouts/test_dialogueframelayout.py` |
| **FocusStripLayout** | Centered host bar over background | *To be documented* | `layouts/FocusStripLayout.tsx.j2` | `tests/templates/layouts/test_focusstriplayout.py` |
| **OverTheShoulderLayout** | Host + screen side-by-side | *To be documented* | `layouts/OverTheShoulderLayout.tsx.j2` | `tests/templates/layouts/test_overtheshoulderlayout.py` |
| **TimelineLayout** | Progress timeline with milestones | *To be documented* | `layouts/TimelineLayout.tsx.j2` | `tests/templates/layouts/test_timelinelayout.py` |
| **StackedReactionLayout** | Vertical stack for reactions | *To be documented* | `layouts/StackedReactionLayout.tsx.j2` | `tests/templates/layouts/test_stackedreactionlayout.py` |
| **PerformanceMultiCamLayout** | 2x2 multi-camera grid | *To be documented* | `layouts/PerformanceMultiCamLayout.tsx.j2` | `tests/templates/layouts/test_performancemulticamlayout.py` |
| **HUDStyleLayout** | Gaming HUD with overlays | *To be documented* | `layouts/HUDStyleLayout.tsx.j2` | `tests/templates/layouts/test_hudstylelayout.py` |
| **MosaicLayout** | Mosaic tile arrangement | *To be documented* | `layouts/MosaicLayout.tsx.j2` | `tests/templates/layouts/test_mosaiclayout.py` |
| **Container** | Simple wrapper container | *To be documented* | `layouts/Container.tsx.j2` | `tests/templates/layouts/test_container.py` |

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
- **225 tests total** across all components
- **100% pass rate**
- Tests organized by component type
- See `tests/templates/` for full test suite

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

**Status**: 8 components fully documented, 15 components pending documentation

To contribute missing documentation, follow the patterns established in existing component docs.
