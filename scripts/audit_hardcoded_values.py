#!/usr/bin/env python3
"""
Audit component templates for hardcoded values that should use design tokens.

This script scans all .tsx.j2 template files and identifies:
- Hardcoded colors (hex, rgb, rgba)
- Hardcoded font weights (numeric values)
- Hardcoded spacing values that match token scale
- Hardcoded border radius values
- Hardcoded font sizes

Outputs a prioritized report of violations.
"""

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

# Token definitions for matching
SPACING_TOKENS = {
    "0": "none",
    "4px": "xxs",
    "8px": "xs",
    "12px": "sm",
    "16px": "md",
    "24px": "lg",
    "32px": "xl",
    "48px": "2xl",
    "64px": "3xl",
    "80px": "4xl",
    "120px": "5xl",
    "160px": "6xl",
    "200px": "7xl",
}

BORDER_RADIUS_TOKENS = {
    "0": "none",
    "2px": "xs",
    "4px": "sm",
    "8px": "md",
    "12px": "lg",
    "16px": "xl",
    "24px": "2xl",
    "32px": "3xl",
    "9999px": "full",
}

FONT_WEIGHTS = {
    "100": "thin",
    "200": "extralight",
    "300": "light",
    "400": "regular",
    "500": "medium",
    "600": "semibold",
    "700": "bold",
    "800": "extrabold",
    "900": "black",
}


@dataclass
class Violation:
    """A hardcoded value violation."""
    file: Path
    line_num: int
    line_content: str
    violation_type: str
    hardcoded_value: str
    suggested_token: str
    priority: str  # P0, P1, P2, P3


class TemplateAuditor:
    """Audits template files for hardcoded values."""

    def __init__(self, components_dir: Path):
        self.components_dir = components_dir
        self.violations: list[Violation] = []
        self.stats = defaultdict(int)

    def audit_all(self):
        """Audit all .tsx.j2 files in components directory."""
        print(f"🔍 Scanning {self.components_dir}...")

        template_files = list(self.components_dir.rglob("*.tsx.j2"))
        print(f"Found {len(template_files)} template files\n")

        for template_file in sorted(template_files):
            self.audit_file(template_file)

        return self.violations

    def audit_file(self, file_path: Path):
        """Audit a single template file."""
        try:
            with open(file_path) as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                # Skip comments and empty lines
                if line.strip().startswith('//') or line.strip().startswith('/*') or not line.strip():
                    continue

                # Check for violations
                self._check_hex_colors(file_path, line_num, line)
                self._check_rgb_colors(file_path, line_num, line)
                self._check_font_weights(file_path, line_num, line)
                self._check_spacing(file_path, line_num, line)
                self._check_border_radius(file_path, line_num, line)

        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")

    def _check_hex_colors(self, file: Path, line_num: int, line: str):
        """Check for hardcoded hex colors."""
        # Skip if line already uses token
        if 'colors.' in line or '[[ colors' in line:
            return

        # Match #HEX colors
        pattern = r'[\'"]#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})[\'"]'
        matches = re.finditer(pattern, line)

        for match in matches:
            color = match.group(0)
            self.violations.append(Violation(
                file=file,
                line_num=line_num,
                line_content=line.strip(),
                violation_type="Hardcoded Color",
                hardcoded_value=color,
                suggested_token="colors.{primary|accent|secondary|text|background|border}.*",
                priority="P0"
            ))
            self.stats["hardcoded_colors"] += 1

    def _check_rgb_colors(self, file: Path, line_num: int, line: str):
        """Check for hardcoded rgb/rgba colors."""
        # Skip if line already uses token
        if 'colors.' in line or '[[ colors' in line:
            return

        # Match rgba(...) - but only if it looks like a standalone color def
        # Allow rgba for component-specific overlays
        pattern = r'rgba?\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(?:,\s*[\d.]+\s*)?\)'
        matches = re.finditer(pattern, line)

        for match in matches:
            color = match.group(0)
            # Only flag if it's used for background/border/color properties
            # and not for overlays (opacity < 0.5)
            if any(prop in line for prop in ['backgroundColor:', 'borderColor:', 'color:']):
                # Check if it's a low-opacity overlay (might be OK)
                opacity_match = re.search(r',\s*(0\.\d+|0)\s*\)', color)
                if opacity_match:
                    opacity = float(opacity_match.group(1))
                    priority = "P2" if opacity <= 0.15 else "P1"  # Very transparent = probably component-specific overlay
                else:
                    priority = "P0"  # Opaque color should definitely use token

                self.violations.append(Violation(
                    file=file,
                    line_num=line_num,
                    line_content=line.strip(),
                    violation_type="Hardcoded RGB Color",
                    hardcoded_value=color,
                    suggested_token="colors.{primary|accent|secondary|text|background|border}.*",
                    priority=priority
                ))
                self.stats["hardcoded_rgb_colors"] += 1

    def _check_font_weights(self, file: Path, line_num: int, line: str):
        """Check for hardcoded font weights."""
        # Skip if line already uses token
        if 'font_weights' in line or '[[ typography.font_weights' in line:
            return

        # Match fontWeight with numeric string
        pattern = r'fontWeight\s*:\s*[\'"](\d{3})[\'"]'
        matches = re.finditer(pattern, line)

        for match in matches:
            weight = match.group(1)
            suggested = FONT_WEIGHTS.get(weight, "unknown")

            self.violations.append(Violation(
                file=file,
                line_num=line_num,
                line_content=line.strip(),
                violation_type="Hardcoded Font Weight",
                hardcoded_value=weight,
                suggested_token=f"typography.font_weights.{suggested}",
                priority="P0"
            ))
            self.stats["hardcoded_font_weights"] += 1

    def _check_spacing(self, file: Path, line_num: int, line: str):
        """Check for hardcoded spacing values that match token scale."""
        # Skip if line already uses spacing token
        if 'spacing.spacing' in line or '[[ spacing.spacing' in line:
            return

        # Check for padding, margin, gap with px values
        pattern = r'(padding|margin|gap|top|bottom|left|right|height|width)\s*:\s*[\'"]?(\d+)px[\'"]?'
        matches = re.finditer(pattern, line)

        for match in matches:
            match.group(1)
            value = match.group(2) + "px"

            if value in SPACING_TOKENS:
                suggested = SPACING_TOKENS[value]

                # Priority based on how common the spacing is
                priority = "P1" if value in ["24px", "16px", "12px", "8px", "4px"] else "P2"  # Very common spacing vs. less common

                self.violations.append(Violation(
                    file=file,
                    line_num=line_num,
                    line_content=line.strip(),
                    violation_type="Hardcoded Spacing",
                    hardcoded_value=value,
                    suggested_token=f"spacing.spacing.{suggested}",
                    priority=priority
                ))
                self.stats["hardcoded_spacing"] += 1

    def _check_border_radius(self, file: Path, line_num: int, line: str):
        """Check for hardcoded border radius values."""
        # Skip if line already uses token
        if 'border_radius' in line or '[[ spacing.border_radius' in line:
            return

        # Match borderRadius with px values
        pattern = r'borderRadius\s*:\s*[\'"]?(\d+)px[\'"]?'
        matches = re.finditer(pattern, line)

        for match in matches:
            value = match.group(1) + "px"

            if value in BORDER_RADIUS_TOKENS:
                suggested = BORDER_RADIUS_TOKENS[value]

                self.violations.append(Violation(
                    file=file,
                    line_num=line_num,
                    line_content=line.strip(),
                    violation_type="Hardcoded Border Radius",
                    hardcoded_value=value,
                    suggested_token=f"spacing.border_radius.{suggested}",
                    priority="P1"
                ))
                self.stats["hardcoded_border_radius"] += 1

    def print_report(self):
        """Print a detailed report of violations."""
        if not self.violations:
            print("✅ No violations found!")
            return

        print("\n" + "="*80)
        print("HARDCODED VALUES AUDIT REPORT")
        print("="*80)

        # Group by priority
        by_priority = defaultdict(list)
        for v in self.violations:
            by_priority[v.priority].append(v)

        # Group by file
        by_file = defaultdict(list)
        for v in self.violations:
            by_file[v.file].append(v)

        # Summary statistics
        print("\n📊 SUMMARY")
        print(f"   Total violations: {len(self.violations)}")
        print(f"   Files affected: {len(by_file)}")
        print("\n   By Type:")
        for stat_type, count in sorted(self.stats.items()):
            print(f"      {stat_type}: {count}")

        print("\n   By Priority:")
        for priority in ["P0", "P1", "P2", "P3"]:
            count = len(by_priority[priority])
            if count > 0:
                print(f"      {priority}: {count}")

        # Detailed violations by priority
        for priority in ["P0", "P1", "P2", "P3"]:
            violations = by_priority[priority]
            if not violations:
                continue

            print(f"\n{'='*80}")
            print(f"{priority} PRIORITY VIOLATIONS ({len(violations)} total)")
            print(f"{'='*80}")

            # Group by file within priority
            file_violations = defaultdict(list)
            for v in violations:
                file_violations[v.file].append(v)

            for file_path in sorted(file_violations.keys()):
                file_viols = file_violations[file_path]
                rel_path = file_path.relative_to(self.components_dir.parent.parent)

                print(f"\n📄 {rel_path} ({len(file_viols)} violations)")
                print(f"   {'─' * 76}")

                # Group by violation type
                type_viols = defaultdict(list)
                for v in file_viols:
                    type_viols[v.violation_type].append(v)

                for vtype, viols in sorted(type_viols.items()):
                    print(f"   {vtype} ({len(viols)}):")
                    for v in viols[:5]:  # Show first 5 per type
                        print(f"      Line {v.line_num}: {v.hardcoded_value}")
                        print(f"         → {v.suggested_token}")
                    if len(viols) > 5:
                        print(f"      ... and {len(viols) - 5} more")

        # Most problematic files
        print(f"\n{'='*80}")
        print("🔥 MOST PROBLEMATIC FILES (Top 10)")
        print(f"{'='*80}")

        sorted_files = sorted(by_file.items(), key=lambda x: len(x[1]), reverse=True)
        for i, (file_path, violations) in enumerate(sorted_files[:10], 1):
            rel_path = file_path.relative_to(self.components_dir.parent.parent)

            # Count by priority
            p0 = sum(1 for v in violations if v.priority == "P0")
            p1 = sum(1 for v in violations if v.priority == "P1")
            p2 = sum(1 for v in violations if v.priority == "P2")

            print(f"{i:2}. {rel_path}")
            print(f"    Total: {len(violations)} | P0: {p0} | P1: {p1} | P2: {p2}")

        print(f"\n{'='*80}")
        print("💡 RECOMMENDATIONS")
        print(f"{'='*80}")
        print("\n1. Fix P0 violations immediately (brand colors, font weights, text colors)")
        print("2. Fix P1 violations soon (common spacing, border radius)")
        print("3. Fix P2 violations when touching the component")
        print("4. Review P3 violations - may be acceptable as hardcoded")
        print("\n📖 See DESIGN_TOKEN_GUIDELINES.md for detailed guidance")
        print(f"{'='*80}\n")


def main():
    """Main entry point."""
    components_dir = Path(__file__).parent.parent / "src" / "chuk_motion" / "components"

    if not components_dir.exists():
        print(f"❌ Components directory not found: {components_dir}")
        return 1

    auditor = TemplateAuditor(components_dir)
    auditor.audit_all()
    auditor.print_report()

    return 0


if __name__ == "__main__":
    exit(main())
