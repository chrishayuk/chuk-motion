# Examples - chuk-motion

Complete examples showcasing all components organized by category.

## 🎯 Component Showcases (NEW!)

**Each category has a dedicated showcase demonstrating all components of that type.**

### 📊 Charts Showcase
**All 6 chart components with various data visualizations**

```bash
python examples/charts_showcase.py
```

**Includes:**
- PieChart - Market share & proportions
- LineChart - Revenue trends over time
- AreaChart - Cumulative user growth
- DonutChart - Team allocation breakdown
- BarChart - Quarterly sales comparison
- HorizontalBarChart - Feature adoption ranking

Perfect for: Data presentations, analytics videos, business reports

---

### 🎬 Overlays Showcase
**All 6 overlay components with different styles and positions**

```bash
python examples/overlays_showcase.py
```

**Includes:**
- TitleScene (Bold, Glass, Minimal variants)
- TextOverlay - Floating text positioning
- LowerThird - Name tags (left & right positions)
- SubscribeButton - Animated call-to-action
- EndScreen - Professional video outro

Perfect for: YouTube videos, interviews, educational content

---

### 💻 Code Showcase
**All 3 code display components with multiple languages**

```bash
python examples/code_showcase.py
```

**Includes:**
- CodeBlock - Static code display (Python, JavaScript, TypeScript)
- TypingCode - Animated typing effect
- CodeDiff - Git-style diffs and refactoring

Perfect for: Tech tutorials, coding demos, documentation videos

---

### 📦 Content Showcase
**All 4 content components with various use cases**

```bash
python examples/content_showcase.py
```

**Includes:**
- DemoBox - Quick placeholders (primary & accent colors)
- WebPage - Raw HTML content display
- StylizedWebPage - Pre-styled layouts (light & dark themes)
- VideoContent - Video playback (shown as placeholder)

Perfect for: Website demos, app showcases, prototyping

---

### 🖼️ Frames Showcase
**All 3 frame components with various browser/device types**

```bash
python examples/frames_showcase.py
```

**Includes:**
- BrowserFrame (Chrome, Arc, Safari, Firefox)
- DeviceFrame (iPhone, iPad, Android)
- Terminal (bash, zsh, various themes)

Perfect for: Product demos, app tutorials, development videos

---

### ✨ Animations Showcase
**All 3 animation components with different effects**

```bash
python examples/animations_showcase.py
```

**Includes:**
- Counter - Number counting (revenue, percentages, metrics)
- LayoutEntrance - Fade, slide, zoom entrances
- PanelCascade - Sequential panel reveals

Perfect for: Engaging intros, data reveals, sequential storytelling

---

### 🔄 Transitions Showcase
**All 2 transition components with various effects**

```bash
python examples/transitions_showcase.py
```

**Includes:**
- LayoutTransition - Fade, slide (left/right), zoom
- PixelTransition - Dissolve, wipe effects

Perfect for: Scene changes, smooth visual flow, creative effects

---

### 📐 Layouts Showcase
**All 18+ layout components demonstrated**

```bash
python examples/layouts_showcase.py
```

**Includes:**
- Container, Grid, ThreeColumnLayout, ThreeRowLayout
- SplitScreen, Mosaic, Timeline, Vertical
- AsymmetricLayout, BeforeAfterSlider, DialogueFrame
- FocusStrip, HUDStyle, OverTheShoulder
- PerformanceMultiCam, PiP, StackedReaction
- ThreeByThreeGrid

Perfect for: Complex compositions, multi-panel layouts, creative arrangements

---

## 🎨 Design System Examples

### **design_system_showcase.py** ✨
**Comprehensive 90-second showcase of the entire design system**

```bash
python examples/design-system/design_system_showcase.py
```

Features:
- All 7 YouTube-optimized themes
- Typography scales and hierarchy
- Charts, code components, overlays
- Complete design token demonstration

Perfect for: Understanding capabilities, client presentations

---

### **safe_margins_demo.py** 📱
**60-second demo of platform-specific safe margins**

```bash
python examples/design-system/safe_margins_demo.py
```

Covers LinkedIn, Instagram, TikTok, YouTube, and mobile formats.

Perfect for: Multi-platform content, preventing cropping

---

### **explore_design_system.py**
**Interactive exploration of design tokens and components**

```bash
python examples/design-system/explore_design_system.py
```

Perfect for: Learning the design system, discovering components

---

## 📚 Additional Examples

### Complete Compositions

#### **ultimate_product_launch.py**
Complete product launch video with all components

```bash
python examples/complete/ultimate_product_launch.py
```

---

#### **multi_track_showcase.py**
Multi-track composition examples

```bash
python examples/complete/multi_track_showcase.py
```

---

### Basics

#### **fibonacci_demo.py**
Typing code effect demonstration

```bash
python examples/basics/fibonacci_demo.py
```

---

#### **code_display.py**
Code syntax highlighting examples

```bash
python examples/basics/code_display.py
```

---

## 🎯 Component Categories Summary

| Category | Count | Components |
|----------|-------|------------|
| **Charts** | 6 | PieChart, LineChart, AreaChart, DonutChart, BarChart, HorizontalBarChart |
| **Overlays** | 6 | TitleScene, TextOverlay, EndScreen, LowerThird, SubscribeButton |
| **Code** | 3 | CodeBlock, TypingCode, CodeDiff |
| **Content** | 4 | VideoContent, StylizedWebPage, WebPage, DemoBox |
| **Frames** | 3 | BrowserFrame, DeviceFrame, Terminal |
| **Animations** | 3 | Counter, LayoutEntrance, PanelCascade |
| **Transitions** | 2 | LayoutTransition, PixelTransition |
| **Layouts** | 18+ | Grid, SplitScreen, Mosaic, Timeline, and many more |

**Total: 45+ Professional Components**

---

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -e .
   ```

2. **Run any showcase:**
   ```bash
   python examples/charts_showcase.py
   ```

3. **Navigate to generated project:**
   ```bash
   cd remotion-projects/charts_showcase
   npm install
   npm start
   ```

4. **Render video:**
   ```bash
   npm run build
   ```

---

## 📖 Example Output

Each showcase generates:
- ✅ Complete Remotion project
- ✅ TypeScript components with design tokens
- ✅ Package.json with dependencies
- ✅ Ready-to-render video composition

Example structure:
```
remotion-projects/
  charts_showcase/
    ├── src/
    │   ├── components/        # Generated components
    │   ├── VideoComposition.tsx
    │   └── Root.tsx
    ├── package.json
    └── remotion.config.ts
```

---

## 💡 Tips

### **For Learning:**
Start with category showcases (charts, overlays, etc.) to understand each component type.

### **For Quick Reference:**
Each showcase is organized by component category for easy navigation.

### **For Client Demos:**
Use `design_system_showcase.py` to show off complete capabilities.

### **For Social Media:**
Check `safe_margins_demo.py` to understand platform cropping.

### **For Production:**
Study `ultimate_product_launch.py` for complex multi-track compositions.

---

## 🎨 Design System Features

All examples leverage the complete design system:

### **Foundations**
| Category | What's Included |
|----------|----------------|
| **Colors** | 7 theme palettes with primary, accent, gradients, semantic colors |
| **Typography** | Font families (display, body, mono), sizes for 720p/1080p/4K, weights |
| **Motion** | 5 spring configs, 8 easing curves, 8 duration presets, animation templates |
| **Spacing** | Scale (xxs→5xl), safe margins (7 platforms), border radius |

### **Platform Safe Margins**
Built-in safe zones for:
- 📱 LinkedIn Feed (8-24px safe zones)
- 📸 Instagram Stories & Square (9:16 with UI overlays)
- 🎵 TikTok (side button considerations)
- 📺 YouTube (standard margins)
- 📱 Mobile Vertical/Horizontal

### **Themes** (7 Total)
1. **Tech** - Modern tech aesthetic (blue gradient)
2. **Finance** - Professional business (green/gold)
3. **Education** - Friendly learning (purple/orange)
4. **Lifestyle** - Warm wellness (pink/amber)
5. **Gaming** - Energetic gaming (neon purple/cyan)
6. **Minimal** - Clean modern (gray scale)
7. **Business** - Corporate professional (navy/teal)

---

## 🎯 Next Steps

1. **Explore by Category** - Run showcases for components you need
2. **Learn** - Check out `design_system_showcase.py`
3. **Create** - Build your own using the composition builder
4. **Customize** - Modify themes and tokens for your brand

---

## 📝 Documentation

- [Main README](../README.md)
- [Component Builder Guide](../COMPONENT_BUILDER_GUIDE.md)
- Design system documentation (coming soon)

---

**Made with ❤️ using chuk-motion**
