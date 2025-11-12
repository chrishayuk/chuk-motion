# Design Token Guidelines

## Purpose
This document establishes when to use design system tokens vs. hardcoded values in component templates.

## Core Principle
**Use design tokens by default. Only hardcode values when there's a specific, documented reason.**

---

## MUST Use Design Tokens

### 1. Typography
**Always use tokens for:**
- ✅ Font weights: `typography.font_weights.{thin|regular|medium|semibold|bold|extrabold|black}`
- ✅ Font sizes: `typography.font_sizes[typography.default_resolution].{xs|sm|base|lg|xl|2xl|3xl|4xl}`
- ✅ Font families: `typography.{primary_font|body_font|code_font}.fonts`
- ✅ Line heights: `typography.line_heights.{tight|snug|normal|relaxed|loose}`
- ✅ Letter spacing: `typography.letter_spacing.{tighter|tight|normal|wide|wider|widest}`

**Why:** Typography must be consistent across all components for brand coherence.

❌ **Never do this:**
```tsx
fontWeight: '600'
fontSize: '48px'
fontFamily: 'Inter, sans-serif'
```

✅ **Always do this:**
```tsx
fontWeight: '[[ typography.font_weights.semibold ]]'
fontSize: parseInt('[[ typography.font_sizes[typography.default_resolution].lg ]]')
fontFamily: "'[[ "', '".join(typography.body_font.fonts) ]]'"
```

### 2. Colors
**Always use tokens for:**
- ✅ Brand colors: `colors.primary[0-6]`, `colors.accent[0-6]`, `colors.secondary[0-6]`
- ✅ Text colors: `colors.text.{on_light|on_dark|muted}`
- ✅ Background colors: `colors.background.{light|dark|darker|glass}`
- ✅ Border colors: `colors.border.{light|medium|heavy}`

**Why:** Colors define brand identity and must support theme switching.

❌ **Never do this:**
```tsx
color: '#1A1A1A'
backgroundColor: '#FFFFFF'
borderColor: 'rgba(0,0,0,0.1)'
```

✅ **Always do this:**
```tsx
color: '[[ colors.text.on_light ]]'
backgroundColor: '[[ colors.background.light ]]'
borderColor: '[[ colors.border.light ]]'
```

**Exception:** Transparent overlays with specific opacity for component-specific effects:
```tsx
// OK for component-specific overlays
backgroundColor: 'rgba(0,0,0,0.03)'
```

### 3. Spacing (Common Values)
**Use tokens for standard spacing:**
- ✅ Padding/margin: `spacing.spacing.{xxs|xs|sm|md|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl}`
- ✅ Gaps: Same as padding/margin
- ✅ Border widths: `spacing.border_width.{thin|medium|thick|heavy}`

**Available spacing scale:**
- none: 0
- xxs: 4px
- xs: 8px
- sm: 12px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px
- 3xl: 64px
- 4xl: 80px
- 5xl: 120px
- 6xl: 160px
- 7xl: 200px

✅ **Use tokens when value matches scale:**
```tsx
padding: '[[ spacing.spacing.lg ]]'  // 24px
gap: '[[ spacing.spacing.md ]]'       // 16px
```

### 4. Border Radius
**Always use tokens for:**
- ✅ Border radius: `spacing.border_radius.{none|xs|sm|md|lg|xl|2xl|3xl|full}`

**Available border radius scale:**
- none: 0
- xs: 2px
- sm: 4px
- md: 8px
- lg: 12px
- xl: 16px
- 2xl: 24px
- 3xl: 32px
- full: 9999px

---

## MAY Hardcode (With Justification)

### 1. Component-Specific Layout Dimensions
**Acceptable to hardcode when:**
- Value is intrinsic to component's visual identity
- Value doesn't match any token in the scale
- Changing it would fundamentally change the component

**Examples:**
```tsx
// Browser window controls (macOS traffic lights)
width: '12px'  // Specific to macOS design language
height: '12px'

// Device screen aspect ratio
width: 375   // iPhone screen width
height: 812  // iPhone screen height

// Terminal cursor
width: '12px'  // Standard terminal cursor size
```

### 2. Intermediate Spacing Values
**When a value falls between token values:**
```tsx
// If you need 20px and tokens are 16px (md) and 24px (lg)
padding: '20px 24px'  // Mixed: hardcode 20px, token would be lg for 24px
// OR better: use token and document why
padding: '[[ spacing.spacing.lg ]]'  // Use 24px, slightly more spacious
```

### 3. Animation/Transition Specific Values
**OK for animation curves and durations:**
```tsx
transition: 'all 0.2s ease'  // Component-specific transition
transform: `translateY(-${currentScrollY}px)`  // Dynamic calculation
```

### 4. Mathematical Calculations
**When deriving from other values:**
```tsx
// Acceptable: Derived from component's own logic
width: `${(value / total) * 100}%`
height: chartHeight - legendHeight
```

---

## NEVER Hardcode

### 1. Brand-Critical Values
- ❌ Brand colors (must use color tokens)
- ❌ Brand fonts (must use typography tokens)
- ❌ Core spacing that appears in multiple components

### 2. Theme-Dependent Values
- ❌ Light/dark mode colors
- ❌ Text colors that should respect theme
- ❌ Background colors that should respect theme

### 3. Scalable Typography
- ❌ Any text size that should scale with resolution (1080p vs 4K)
- ❌ Font weights (must use semantic token names)

---

## Migration Strategy

### Priority Levels

**P0 - Critical (Fix Immediately):**
- Hardcoded brand colors (should use `colors.primary|accent|secondary`)
- Hardcoded font weights (should use `typography.font_weights.*`)
- Hardcoded text colors (should use `colors.text.*`)

**P1 - High (Fix Soon):**
- Common spacing values that match tokens (4px, 8px, 12px, 16px, 24px, 32px, 48px)
- Font sizes that should scale
- Border radius values that match tokens

**P2 - Medium (Fix When Touching Component):**
- Background colors that should use tokens
- Border colors that should use tokens
- Component-specific spacing that could use tokens

**P3 - Low (Document & Review):**
- Component-intrinsic dimensions (may be correct as hardcoded)
- Animation-specific values
- Mathematical calculations

### How to Fix

1. **Identify the hardcoded value**
2. **Check if a token exists** for that value or semantic meaning
3. **Replace with token reference:**
   ```tsx
   // Before
   fontWeight: '600'

   // After
   fontWeight: '[[ typography.font_weights.semibold ]]'
   ```
4. **Test the component** to ensure visual consistency
5. **Document** if you choose to keep a hardcoded value

---

## Examples

### ✅ Good Example
```tsx
<div
  style={{
    padding: '[[ spacing.spacing.lg ]]',
    backgroundColor: '[[ colors.background.light ]]',
    borderRadius: '[[ spacing.border_radius.md ]]',
    fontSize: parseInt('[[ typography.font_sizes[typography.default_resolution].base ]]'),
    fontWeight: '[[ typography.font_weights.regular ]]',
    color: '[[ colors.text.on_light ]]',
    border: `[[ spacing.border_width.thin ]] solid [[ colors.border.light ]]`,
  }}
>
```

### ❌ Bad Example
```tsx
<div
  style={{
    padding: '24px',
    backgroundColor: '#FFFFFF',
    borderRadius: '8px',
    fontSize: '40px',
    fontWeight: '400',
    color: '#1A1A1A',
    border: '1px solid rgba(0,0,0,0.1)',
  }}
>
```

### 🟡 Acceptable Mixed Example
```tsx
<div
  style={{
    // Token: Standard padding
    padding: '[[ spacing.spacing.lg ]]',
    // Token: Theme background
    backgroundColor: '[[ colors.background.light ]]',
    // Token: Standard radius
    borderRadius: '[[ spacing.border_radius.md ]]',
    // Hardcoded: Component-specific dimension
    minHeight: '120px',  // Terminal needs specific height
    // Token: Standard font
    fontFamily: "'[[ "', '".join(typography.code_font.fonts) ]]'",
    // Hardcoded: Specific overlay for this component
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  }}
>
```

---

## Token Reference Quick Guide

### Spacing
```
spacing.spacing.{xxs|xs|sm|md|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl}
spacing.border_radius.{none|xs|sm|md|lg|xl|2xl|3xl|full}
spacing.border_width.{thin|medium|thick|heavy}
```

### Typography
```
typography.font_sizes[typography.default_resolution].{xs|sm|base|lg|xl|2xl|3xl|4xl}
typography.font_weights.{thin|regular|medium|semibold|bold|extrabold|black}
typography.line_heights.{tight|snug|normal|relaxed|loose}
typography.letter_spacing.{tighter|tight|normal|wide|wider|widest}
typography.{primary_font|body_font|code_font|decorative_font}.fonts
```

### Colors
```
colors.primary[0-6]
colors.accent[0-6]
colors.secondary[0-6]
colors.text.{on_light|on_dark|muted}
colors.background.{light|dark|darker|glass}
colors.border.{light|medium|heavy}
```

---

## Enforcement

1. **Code Review:** All PRs should be checked for hardcoded values
2. **Linting:** Consider adding automated checks for common patterns
3. **Documentation:** This guide should be referenced in component README
4. **Audit:** Regular audits to identify and fix violations

## Questions?

If unsure whether to use a token or hardcode:
1. Check if a token exists for the semantic meaning
2. Ask: "Should this value be consistent across components?"
3. Ask: "Should this value respect themes?"
4. If yes to either → use a token
5. If no → document why you're hardcoding
