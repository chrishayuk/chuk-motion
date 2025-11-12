# Layout Components Migration Status

## ✅ Completed Layouts (9 total)

### Core Layouts (6)
1. **Container** ✅ (existing)
   - Basic wrapper/frame
   - Location: `src/chuk_motion/components/layouts/Container/`

2. **Grid** ✅ (existing)
   - Multi-layout grid system (1x2, 2x1, 2x2, 3x2, 2x3, 3x3, 4x2, 2x4)
   - Location: `src/chuk_motion/components/layouts/Grid/`

3. **SplitScreen** ✅ (existing)
   - Two-pane split
   - Location: `src/chuk_motion/components/layouts/SplitScreen/`

4. **ThreeByThreeGrid** ✅ NEW
   - Perfect 3x3 grid (9 cells)
   - Location: `src/chuk_motion/components/layouts/ThreeByThreeGrid/`

5. **ThreeColumnLayout** ✅ NEW
   - Sidebar + Main + Sidebar arrangements with configurable widths
   - Props: `left`, `center`, `right`, `left_width`, `center_width`, `right_width`
   - Location: `src/chuk_motion/components/layouts/ThreeColumnLayout/`

6. **ThreeRowLayout** ✅ NEW
   - Header + Main + Footer arrangements with configurable heights
   - Props: `top`, `middle`, `bottom`, `top_height`, `middle_height`, `bottom_height`
   - Location: `src/chuk_motion/components/layouts/ThreeRowLayout/`

### Specialized Layouts (3)
7. **AsymmetricLayout** ✅ NEW
   - Main feed (2/3) + two demo panels (1/3 stacked)
   - Perfect for tutorials
   - Props: `main`, `top_side`, `bottom_side`, `layout` (main-left/main-right), `main_ratio`
   - Location: `src/chuk_motion/components/layouts/AsymmetricLayout/`

8. **PiP (Picture-in-Picture)** ✅ NEW
   - Webcam overlay with positions (bottom-right, bottom-left, top-right, top-left)
   - Props: `main_content`, `pip_content`, `position`, `overlay_size`, `margin`
   - Location: `src/chuk_motion/components/layouts/PiP/`

9. **Layouts exported in __init__.py** ✅ UPDATED
   - Location: `src/chuk_motion/components/layouts/__init__.py`

## 🚧 Remaining Layouts to Migrate (8 total)

### High Priority
1. **Vertical**
   - 9:16 optimized for Shorts/TikTok/Reels
   - Layouts: top-bottom, caption-content, content-caption, split-vertical
   - Test file: `tests/templates/layouts/test_verticallayout.py`

2. **DialogueFrame**
   - For conversation/dialogue scenes
   - Test file: `tests/templates/layouts/test_dialogueframelayout.py`

3. **Timeline**
   - Progress/timeline overlay with milestones and progress indicators
   - Test file: `tests/templates/layouts/test_timelinelayout.py`

### Medium Priority
4. **OverTheShoulder**
   - Looking over someone's shoulder perspective
   - Test file: `tests/templates/layouts/test_overtheshoulderlayout.py`

5. **StackedReaction**
   - Reaction video style with stacked feeds
   - Test file: `tests/templates/layouts/test_stackedreactionlayout.py`

6. **HUDStyle**
   - Heads-up display style with overlay elements
   - Test file: `tests/templates/layouts/test_hudstylelayout.py`

7. **PerformanceMultiCam**
   - Multi-camera performance view
   - Test file: `tests/templates/layouts/test_performancemulticamlayout.py`

8. **FocusStrip**
   - Focused strip/banner layout
   - Test file: `tests/templates/layouts/test_focusstriplayout.py`

### Low Priority (Complex)
9. **Mosaic**
   - Irregular collage with layered clips
   - Styles: hero-corners, stacked, spotlight
   - Test file: `tests/templates/layouts/test_mosaiclayout.py`

## 📋 Next Steps

### To Complete a Layout:
For each remaining layout, follow this pattern (see `LAYOUT_MIGRATION_GUIDE.md` for details):

1. **Read the test file** in `tests/templates/layouts/test_{layoutname}.py` to understand:
   - Required props
   - Layout behavior
   - Expected variants

2. **Create directory structure**:
   ```bash
   mkdir -p src/chuk_motion/components/layouts/{LayoutName}
   ```

3. **Create 5 required files**:
   - `schema.py` - Pydantic models and metadata
   - `builder.py` - Composition builder method
   - `tool.py` - MCP tool registration
   - `template.tsx.j2` - React/Remotion template with tokens
   - `__init__.py` - Component exports

4. **Use existing layouts as templates**:
   - ThreeColumnLayout - for multi-column layouts
   - ThreeRowLayout - for multi-row layouts
   - AsymmetricLayout - for complex nested layouts
   - PiP - for overlay/positioning layouts

5. **Key requirements**:
   - ✅ Use design tokens in templates (`[[ spacing.spacing.xl ]]`, etc.)
   - ✅ Include timing props (`start_time`, `duration`)
   - ✅ Include standard props (`gap`, `padding`, `border_width`, etc.)
   - ✅ Handle JSON parsing in tool.py
   - ✅ Use ComponentInstance pattern
   - ✅ Return LayoutComponentResponse from tools

6. **Update exports**:
   - Add new layout to `src/chuk_motion/components/layouts/__init__.py`

7. **Register tools** (if not auto-registered):
   - Check tool registration system
   - May need to add to tool registry

## 🎯 Quick Reference

### Common Props Pattern
```python
# Schema
gap: float | None = Field(20, description="Gap between elements (pixels)")
padding: float | None = Field(40, description="Padding around layout (pixels)")
start_time: float = Field(description="When to show (seconds)")
duration: float | None = Field(5.0, description="How long to show (seconds)")

# Template (use tokens!)
padding = parseInt('[[ spacing.spacing.xl ]]')  // 32px
gap = parseInt('[[ spacing.spacing.md ]]')      // 16px
border_radius = parseInt('[[ spacing.border_radius.md ]]')  // 8px
```

### File Locations
- **Layouts**: `src/chuk_motion/components/layouts/{LayoutName}/`
- **Tests**: `tests/templates/layouts/test_{layoutname}.py`
- **Test fixtures**: `tests/components/layouts/{LayoutName}/test_{layoutname}.py` (create these)
- **Migration guide**: `LAYOUT_MIGRATION_GUIDE.md`

## 📊 Progress Summary
- **Total layouts needed**: 17
- **Completed**: 9 (53%)
- **Remaining**: 8 (47%)
- **Core layouts complete**: 6/7 (86%)
- **Specialized layouts complete**: 3/10 (30%)

## 🎉 What's Working
All completed layouts now:
- ✅ Follow the new modular structure
- ✅ Use Pydantic models for type safety
- ✅ Have MCP tools for AI agent integration
- ✅ Use design token system
- ✅ Include proper builder methods
- ✅ Are exported from layouts __init__.py
- ✅ Have React/Remotion templates with proper timing

You can now use these layouts in your compositions!
