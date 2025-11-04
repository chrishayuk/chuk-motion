# Examples - chuk-mcp-remotion

Complete examples showcasing the design system, components, and video generation capabilities.

## 🆕 New Examples (Design System)

### 1. **design_system_showcase.py** ✨
**Comprehensive 90-second showcase of the entire design system**

Features:
- All 7 YouTube-optimized themes (tech, finance, education, lifestyle, gaming, minimal, business)
- Typography scales and hierarchy
- 4 chart types with real data (Bar, Pie, Line, Area)
- Code components with syntax highlighting
- Text overlays and animations
- Lower thirds and counters
- Professional end screen

```bash
./examples/design_system_showcase.py
```

Perfect for: Understanding the full capabilities, client presentations, portfolio pieces

---

### 2. **safe_margins_demo.py** 📱
**60-second demo of platform-specific safe margins**

Covers:
- LinkedIn Feed (8-24px safe zones)
- Instagram Stories (9:16 with UI overlays)
- TikTok (side button considerations)
- YouTube (standard margins)
- Mobile formats (vertical & horizontal)

```bash
./examples/safe_margins_demo.py
```

Perfect for: Multi-platform content, social media videos, preventing cropping

---

### 3. **explore_design_system.py** (Updated)
**Interactive exploration of design tokens and components**

Now includes:
- ✅ Spacing tokens (NEW!)
- ✅ Safe margin platforms (NEW!)
- Color palettes
- Typography tokens
- Motion presets
- Component registry

```bash
python examples/explore_design_system.py
```

Perfect for: Learning the design system, discovering components

---

## 📚 Original Examples

### **fibonacci_demo.py**
Demonstrates typing code effect with Fibonacci sequence

```bash
./examples/fibonacci_demo.py
```

---

### **multi_track_showcase.py**
Multi-track composition with various components

```bash
./examples/multi_track_showcase.py
```

---

### **ultimate_product_launch.py**
Complete product launch video with all bells and whistles

```bash
./examples/ultimate_product_launch.py
```

---

### **code_display.py**
Code syntax highlighting and display examples

```bash
./examples/code_display.py
```

---

### **data_visualization_overlay.py**
Chart overlays and data visualization

```bash
./examples/data_visualization_overlay.py
```

---

### **grid_code.py**
Grid layout examples

```bash
./examples/grid_code.py
```

---

### **comprehensive_layouts_showcase.py**
All layout components demonstrated

```bash
python examples/comprehensive_layouts_showcase.py
```

---

## 🎨 Design System Features

All new examples now leverage the complete design system:

### **Foundations**
| Category | What's Included |
|----------|----------------|
| **Colors** | 7 theme palettes with primary, accent, gradients, semantic colors |
| **Typography** | Font families (display, body, mono, decorative), sizes for 720p/1080p/4K, weights, line heights |
| **Motion** | 5 spring configs, 8 easing curves, 8 duration presets, animation templates |
| **Spacing** | Scale (xxs→5xl), safe margins (7 platforms), border radius, layout presets |

### **Platform Safe Margins**
Built-in safe zones for:
- 📱 LinkedIn Feed
- 📸 Instagram Stories & Square
- 🎵 TikTok
- 📺 YouTube
- 📱 Mobile Vertical/Horizontal

### **Components** (17 Total)
- **Charts** (6): Pie, Line, Area, Bar, HorizontalBar, Donut
- **Overlays** (5): LowerThird, TextOverlay, SubscribeButton, TitleScene, EndScreen
- **Code** (2): CodeBlock, TypingCode
- **Layouts** (3): Container, Grid, SplitScreen
- **Animations** (1): Counter

### **Themes** (7 Total)
1. **Tech** - Modern tech aesthetic (blue gradient)
2. **Finance** - Professional business (green/gold)
3. **Education** - Friendly learning (purple/orange)
4. **Lifestyle** - Warm wellness (pink/amber)
5. **Gaming** - Energetic gaming (neon purple/cyan)
6. **Minimal** - Clean modern (gray scale)
7. **Business** - Corporate professional (navy/teal)

---

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -e .
   ```

2. **Run any example:**
   ```bash
   python examples/design_system_showcase.py
   ```

3. **Navigate to generated project:**
   ```bash
   cd remotion-projects/design_system_showcase
   npm install
   npm start
   ```

4. **Render video:**
   ```bash
   npm run build
   ```

---

## 📖 Example Output

Each example generates:
- ✅ Complete Remotion project
- ✅ TypeScript components with design tokens applied
- ✅ Package.json with dependencies
- ✅ Ready-to-render video composition

Example structure:
```
remotion-projects/
  design_system_showcase/
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
Start with `explore_design_system.py` to understand available components and tokens.

### **For Client Demos:**
Use `design_system_showcase.py` to show off capabilities.

### **For Social Media:**
Check `safe_margins_demo.py` to understand platform cropping.

### **For Production:**
Study `ultimate_product_launch.py` for complex multi-track compositions.

---

## 🎯 Next Steps

1. **Explore** - Run `explore_design_system.py`
2. **Learn** - Check out `design_system_showcase.py`
3. **Create** - Build your own using the composition builder
4. **Customize** - Modify themes and tokens for your brand

---

## 📝 Documentation

- [Main README](../README.md)
- [Design System Docs](../docs/design-system.md)
- [Component Reference](../docs/components.md)
- [Theme System](../docs/themes.md)

---

**Made with ❤️ using chuk-mcp-remotion**
