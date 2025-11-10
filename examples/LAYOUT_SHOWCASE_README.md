# Layout Showcase

Comprehensive demonstration of all 17 layout components in the system.

## What's Included

The `layout_showcase.py` script generates a complete video showcasing every layout:

### Core Layouts (7)
1. **Container** - Basic wrapper/frame with borders
2. **Grid** - Multi-layout grid system (3x3 example)
3. **SplitScreen** - Two-pane split layout
4. **ThreeByThreeGrid** - Perfect 3x3 grid (9 cells)
5. **ThreeColumnLayout** - Sidebar + Main + Sidebar
6. **ThreeRowLayout** - Header + Main + Footer
7. **AsymmetricLayout** - Main feed (2/3) + stacked panels (1/3)

### Specialized Layouts (10)
8. **PiP** - Picture-in-Picture with overlay
9. **Vertical** - 9:16 mobile-optimized layout
10. **DialogueFrame** - Conversation/interview layout
11. **StackedReaction** - Reaction video style
12. **FocusStrip** - Focused banner/strip overlay
13. **OverTheShoulder** - Screen recording perspective
14. **HUDStyle** - Heads-up display with corner overlays
15. **Timeline** - Progress/milestone timeline overlay
16. **PerformanceMultiCam** - Multi-camera performance view
17. **Mosaic** - Irregular collage layout

## Usage

### Generate the Showcase

```bash
# From the repository root
python examples/layout_showcase.py
```

This will:
1. Create a new project called `layout_showcase`
2. Generate 19 scenes (title + 17 layouts + outro)
3. Each layout gets 5 seconds of screen time
4. Total duration: ~95 seconds

### Build the Video

```bash
# Navigate to the generated project
cd workspace/layout_showcase

# Install dependencies (first time only)
npm install

# Build the video
npm run build

# The video will be in the `out` directory
```

## What Each Scene Shows

Each layout scene demonstrates:
- **Layout structure** - How the layout divides the screen
- **Content areas** - Using colored DemoBox components
- **Borders & spacing** - Design token usage
- **Practical application** - Real-world use case

## Customization

You can modify the showcase script to:

### Change Scene Duration
```python
scene_duration = 150  # 5 seconds at 30fps
# Change to 90 for 3 seconds, 180 for 6 seconds, etc.
```

### Change Theme
```python
theme = "tech"  # Options: tech, finance, creative, minimal
```

### Add More Content
Each scene uses `create_demo_box()` helpers. You can replace with:
- Text components
- Code blocks
- Charts
- Custom components

### Example: Custom Content
```python
# Instead of DemoBox
create_demo_box("Label", "primary")

# Use real components
{
    "type": "CodeBlock",
    "config": {
        "code": "console.log('Hello')",
        "language": "javascript",
    }
}
```

## Output Structure

```
workspace/layout_showcase/
├── src/
│   ├── Root.tsx          # Main composition
│   └── theme/            # Generated theme
├── public/
├── package.json
└── remotion.config.ts
```

## Features Demonstrated

### Design Token Integration
All layouts use design tokens:
```typescript
padding = parseInt('[[ spacing.spacing.xl ]]')     // 32px
gap = parseInt('[[ spacing.spacing.md ]]')         // 16px
border_radius = parseInt('[[ spacing.border_radius.md ]]')  // 8px
```

### Responsive Design
- Vertical layout optimized for 9:16 (mobile)
- Other layouts optimized for 16:9 (desktop/YouTube)

### Composition Builder Pattern
All layouts follow the modular component pattern:
- Pydantic models for type safety
- Builder methods for composition
- MCP tools for AI agent integration
- TSX templates with token support

## Tips for Best Results

1. **Preview First**: Use `npm start` to preview before building
2. **Adjust Timing**: Modify scene_duration for longer/shorter demos
3. **Theme Consistency**: Stick with one theme for cohesive look
4. **High Quality**: Build with `--quality=high` for best output

## Related Examples

- `comprehensive_layouts_showcase.py` - Original layouts demo
- `design_system_showcase.py` - Design token showcase
- `multi_track_showcase.py` - Track system demo
- `demo_realism_showcase.py` - Realistic UI components

## Troubleshooting

### Import Errors
```bash
# Ensure you're running from repository root
python examples/layout_showcase.py
# NOT: cd examples && python layout_showcase.py
```

### Missing Components
If you get component errors, ensure all layouts are properly registered:
```python
# Check layouts/__init__.py exports all 17 layouts
```

### Build Failures
```bash
# Clean and rebuild
cd workspace/layout_showcase
rm -rf node_modules package-lock.json
npm install
npm run build
```

## Next Steps

After viewing the showcase:
1. Study the layouts that fit your use case
2. Check layout-specific documentation in `src/chuk_mcp_remotion/components/layouts/`
3. Use layouts in your own projects via MCP tools or composition builder
4. Customize layouts by modifying props

## Contributing

Found issues or have improvements? Submit a PR with:
- New layout examples
- Better demo content
- Additional use case scenarios
- Documentation improvements
