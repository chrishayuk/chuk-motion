# Component Template Testing

## Overview

This test suite ensures all component templates generate correct, type-safe TypeScript/TSX code with proper design token integration.

## Test Structure

Tests are organized **one file per template** for better maintainability:

```
tests/templates/
├── __init__.py                      # Package marker
├── conftest.py                      # Shared fixtures & helpers
├── test_component_builder.py        # ComponentBuilder tests (23 tests)
├── test_template_titlescene.py      # TitleScene template (19 tests)
├── test_template_lower_third.py     # LowerThird template (18 tests)
├── test_template_grid.py            # Grid template (17 tests)
├── test_template_codeblock.py       # (To be added)
├── test_template_typingcode.py      # (To be added)
└── ...                              # More templates
```

### Benefits of Per-Template Organization

✅ **Easy to Find**: Locate tests for a specific template quickly
✅ **Focused Testing**: Each file tests one component thoroughly
✅ **Parallel Execution**: Tests can run in parallel more efficiently
✅ **Maintainable**: Smaller files are easier to update
✅ **Clear Ownership**: Know exactly which template is being tested

## Test Coverage

### 1. ComponentBuilder Tests (3 tests)
- ✅ Builder initialization
- ✅ Jinja2 environment configuration
- ✅ Custom filters (to_camel_case, to_pascal_case)

### 2. Template Discovery Tests (4 tests)
- ✅ Finding overlay templates (TitleScene, LowerThird)
- ✅ Finding content templates (CodeBlock, TypingCode, LineChart)
- ✅ Finding layout templates (Grid, ThreeByThreeGrid, etc.)
- ✅ Error handling for nonexistent templates

### 3. TitleScene Generation Tests (6 tests)
- ✅ Basic generation with all props
- ✅ Design token injection
- ✅ All animation variants (fade_zoom, slide_up, typewriter, blur_in, fade_slide, zoom)
- ✅ All style variants (minimal, standard, bold, kinetic, glass)
- ✅ TypeScript syntax validation
- ✅ Motion token usage

### 4. LowerThird Generation Tests (4 tests)
- ✅ Basic generation
- ✅ All position variants (6 positions)
- ✅ All style variants (minimal, standard, glass, bold, animated)
- ✅ Slide animation with motion tokens

### 5. CodeBlock Generation Tests (3 tests)
- ✅ Basic generation with syntax highlighting
- ✅ All style variants (minimal, terminal, editor, glass)
- ✅ All animations (fade_in, slide_up, scale_in, blur_in)

### 6. Layout Components Tests (5 tests)
- ✅ ThreeByThreeGrid (9-cell grid)
- ✅ ThreeColumnLayout (3-column with custom widths)
- ✅ ThreeRowLayout (3-row with custom heights)
- ✅ AsymmetricLayout (main feed + demo panels)
- ✅ Grid (flexible grid layouts: 2x2, 3x3, etc.)

### 7. Content Components Tests (2 tests)
- ✅ TypingCode (animated typing effect)
- ✅ LineChart (SVG-based data visualization)

### 8. Design Token Injection Tests (3 tests)
- ✅ Color tokens properly injected from theme
- ✅ Typography tokens properly injected
- ✅ Motion tokens properly injected

### 9. TypeScript Validity Tests (4 tests)
- ✅ No unresolved template variables (`[[`, `]]`, `[%`, `%]`)
- ✅ Proper imports (React, Remotion)
- ✅ Proper TypeScript interfaces
- ✅ Valid JSX syntax (balanced tags)

### 10. Edge Cases Tests (3 tests)
- ✅ Empty config (uses defaults)
- ✅ Missing optional props
- ✅ All themes work (tech, finance, education, lifestyle, gaming, minimal, business)

### 11. Runtime Props Tests (3 tests)
- ✅ Props defined in interfaces
- ✅ Default values present
- ✅ Frame-based visibility checks

## Shared Test Utilities (`conftest.py`)

The `tests/templates/conftest.py` provides common fixtures and assertions:

### Fixtures
- `component_builder` - ComponentBuilder instance
- `theme_name` - Default theme ("tech")
- `tech_theme` - The tech theme dict
- `all_themes` - List of all theme names

### Assertion Helpers
```python
assert_valid_typescript(tsx)           # Check valid TypeScript syntax
assert_has_interface(tsx, name)        # Check TypeScript interface
assert_has_timing_props(tsx)           # Check startFrame/durationInFrames
assert_has_visibility_check(tsx)       # Check frame-based visibility
assert_design_tokens_injected(tsx)     # Check tokens are resolved
```

## Test Statistics

- **Total Template Tests**: 85
- **Total Tests (Full Suite)**: 264
- **Pass Rate**: 100%
- **Test Files**: 4 (+ more to be added)
- **Components Tested**: 3 (TitleScene, LowerThird, Grid)

## Running Tests

### Run all template tests:
```bash
uv run pytest tests/templates/ -v
```

### Run specific template tests:
```bash
uv run pytest tests/templates/test_template_titlescene.py -v
uv run pytest tests/templates/test_template_lower_third.py -v
uv run pytest tests/templates/test_template_grid.py -v
```

### Run with coverage:
```bash
uv run pytest tests/templates/ --cov=chuk_motion.generator
```

### Run tests in parallel (faster):
```bash
uv run pytest tests/templates/ -n auto
```

## What Gets Tested

### Template Rendering
- Templates render without Jinja2 errors
- All placeholders are replaced
- No syntax errors in generated code

### Design Token System
- Color tokens from themes are injected
- Typography tokens (fonts, sizes) are injected
- Motion tokens (springs, easings) are injected
- No hardcoded values in generated code

### TypeScript/TSX Validity
- Valid TypeScript interfaces
- Proper React component structure
- Correct import statements
- Balanced JSX tags
- No syntax errors

### Runtime Props
- All required props defined
- Optional props have defaults
- Frame-based timing works correctly
- Visibility checks present

### Component Variants
- All style variants generate correctly
- All animation variants work
- All layout configurations supported
- All position options available

## Key Test Assertions

### 1. Template Variable Resolution
```python
assert '[[' not in tsx  # No unresolved variables
assert ']]' not in tsx
```

### 2. Design Token Usage
```python
assert '#0066FF' in tsx  # Theme colors injected
assert 'Inter' in tsx     # Theme fonts injected
assert 'damping: 200' in tsx  # Motion config injected
```

### 3. TypeScript Structure
```python
assert 'interface TitleSceneProps' in tsx
assert 'React.FC<TitleSceneProps>' in tsx
assert 'startFrame: number' in tsx
assert 'durationInFrames: number' in tsx
```

### 4. JSX Validity
```python
open_tags = tsx.count('<div')
close_tags = tsx.count('</div>')
assert open_tags == close_tags
```

## Adding New Template Tests

When adding a new component template, create a new test file:

### 1. Create Test File

Create `tests/templates/test_template_newcomponent.py`:

```python
"""
Tests for NewComponent template generation.
"""

import pytest
from .conftest import (
    assert_valid_typescript,
    assert_has_interface,
    assert_has_timing_props,
    assert_has_visibility_check
)


class TestNewComponentBasic:
    """Basic NewComponent generation tests."""

    def test_basic_generation(self, component_builder, theme_name):
        """Test basic NewComponent generation."""
        tsx = component_builder.build_component(
            'NewComponent',
            {'prop': 'value'},
            theme_name
        )

        assert tsx is not None
        assert 'NewComponent' in tsx
        assert_valid_typescript(tsx)
        assert_has_interface(tsx, 'NewComponent')
        assert_has_timing_props(tsx)
        assert_has_visibility_check(tsx)


class TestNewComponentVariants:
    """Tests for style/animation variants."""

    @pytest.mark.parametrize('variant', ['variant1', 'variant2', 'variant3'])
    def test_variant(self, component_builder, theme_name, variant):
        """Test each variant generates correctly."""
        tsx = component_builder.build_component(
            'NewComponent',
            {'prop': 'value', 'variant': variant},
            theme_name
        )
        assert variant in tsx


class TestNewComponentDesignTokens:
    """Tests for design token integration."""

    def test_design_tokens_injected(self, component_builder, theme_name):
        """Test design tokens are properly injected."""
        tsx = component_builder.build_component(
            'NewComponent',
            {},
            theme_name
        )
        assert '[[' not in tsx  # No unresolved vars
```

### 2. Run Your New Tests

```bash
uv run pytest tests/templates/test_template_newcomponent.py -v
```

### 3. Test Checklist

For each new template, ensure you test:

- ✅ Basic generation with all props
- ✅ Minimal props (with defaults)
- ✅ All style variants
- ✅ All animation variants
- ✅ Design token injection (colors, fonts, motion)
- ✅ TypeScript validity (no syntax errors)
- ✅ Proper imports and interfaces
- ✅ Frame-based visibility
- ✅ All theme compatibility

## Benefits

1. **Confidence**: Know that templates generate valid code
2. **Regression Prevention**: Catch template breakage early
3. **Documentation**: Tests show how components should work
4. **Design Token Compliance**: Ensure theme system is used correctly
5. **Type Safety**: Verify TypeScript interfaces are correct

## CI/CD Integration

These tests run automatically in CI:
- On every commit
- Before merging PRs
- On release branches

Ensures generated code quality is maintained.
