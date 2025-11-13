#!/usr/bin/env python3
"""
Fibonacci Code Typing Demo - Track-Based Timeline

This example creates the Fibonacci typing demo using the new track-based system.
Shows how easy it is to create educational coding videos with auto-stacking.
"""
import asyncio
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_motion.utils.project_manager import ProjectManager
from chuk_motion.generator.composition_builder import ComponentInstance


async def main():
    """Generate Fibonacci code typing demo."""
    print("\n" + "="*70)
    print("FIBONACCI CODE TYPING DEMO - Track-Based Timeline")
    print("="*70)

    manager = ProjectManager()
    project_name = "fibonacci_typing_demo"

    # Clean up
    project_path = manager.workspace_dir / project_name
    if project_path.exists():
        shutil.rmtree(project_path)

    # Create project
    print(f"\n📁 Creating project...")
    project = manager.create_project(
        name=project_name,
        theme="tech",
        fps=30,
        width=1920,
        height=1080
    )

    # Main track: Sequential code scenes
    print("\n🎬 Building main track (sequential code scenes)...")

    # 1. Title scene (0s - 3s)
    print("  • Title scene")
    title = ComponentInstance(
        component_type="TitleScene",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "Fibonacci Code Typing Demo",
            "subtitle": "Python — step-by-step typing",
            "variant": "default",
            "animation": "glow"
        },
        layer=0
    )
    manager.current_timeline.add_component(title, duration=3.0, track="main")

    # 2. Typing code (3.5s - 15.5s) - 12 seconds with 0.5s gap
    print("  • Typing code animation")
    typing_code = ComponentInstance(
        component_type="TypingCode",
        start_frame=0,
        duration_frames=0,
        props={
            "code": """# Fibonacci (iterative generator)
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

if __name__ == "__main__":
    n = 10
    print("First", n, "Fibonacci numbers:")
    for num in fibonacci(n):
        print(num, end=" ")
    print()
""",
            "language": "python",
            "title": "Fibonacci in Python",
            "variant": "monospace",
            "cursor_style": "block",
            "typing_speed": "medium",
            "show_line_numbers": True
        },
        layer=0
    )
    manager.current_timeline.add_component(typing_code, duration=12.0, track="main", gap_before=0.5)

    # 3. Static code block (20.5s - 26.5s) - alternative approach
    print("  • Alternative implementation")
    code_block = ComponentInstance(
        component_type="CodeBlock",
        start_frame=0,
        duration_frames=0,
        props={
            "code": """# Alternative: simple recursive (inefficient)
from functools import lru_cache

@lru_cache(None)
def fib_rec(n):
    if n < 2:
        return n
    return fib_rec(n-1) + fib_rec(n-2)

print()
""",
            "language": "python",
            "title": "Recursive (with memoization)",
            "variant": "monospace",
            "animation": "slide_up",
            "show_line_numbers": True
        },
        layer=0
    )
    # Add with explicit timing (not auto-stacking) to create a gap
    manager.current_timeline.add_component(
        code_block,
        duration=6.0,
        track="main",
        start_frame=manager.current_timeline.seconds_to_frames(20.5)
    )

    # 4. End screen (26.5s - 34.5s)
    print("  • End screen")
    end_screen = ComponentInstance(
        component_type="EndScreen",
        start_frame=0,
        duration_frames=0,
        props={
            "cta_text": "Try it yourself — link in description",
            "variant": "gradient"  # gradient variant handles missing thumbnail gracefully
        },
        layer=0
    )
    manager.current_timeline.add_component(end_screen, duration=8.0, track="main", gap_before=0)

    # Overlay track: Explanatory text
    print("\n💬 Adding overlay track (explanations)...")

    # Text overlay during typing code
    print("  • Explanation caption")
    text_overlay = ComponentInstance(
        component_type="TextOverlay",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "Explanation: iterative generator is memory-efficient",
            "style": "caption",
            "animation": "fade_in",
            "position": "bottom_left"
        },
        layer=10
    )
    manager.current_timeline.add_component(
        text_overlay,
        duration=4.0,
        track="overlay",
        align_to="main",
        offset=16.0  # Shows after typing finishes
    )

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    info = manager.get_project_info()
    composition = info['composition']

    print(f"\nTotal duration: {composition['duration_seconds']:.1f} seconds")
    print(f"Total components: {len(composition['components'])}")

    print("\nTimeline:")
    for comp in sorted(composition['components'], key=lambda c: c['start_time']):
        print(f"  {comp['start_time']:>5.1f}s - {comp['start_time'] + comp['duration']:>5.1f}s │ "
              f"L{comp['layer']:>2} │ {comp['type']}")

    # Generate files
    print("\n⚙️  Generating files...")
    component_types = {c.component_type for c in manager.current_timeline.get_all_components()}

    for comp_type in component_types:
        sample = next(
            c for c in manager.current_timeline.get_all_components()
            if c.component_type == comp_type
        )
        manager.add_component_to_project(comp_type, sample.props, manager.current_timeline.theme)
        print(f"  ✓ {comp_type}.tsx")

    manager.generate_composition()
    print(f"  ✓ VideoComposition.tsx")

    # Next steps
    print("\n" + "="*70)
    print("🎉 FIBONACCI DEMO GENERATED!")
    print("="*70)

    print(f"\n📁 {project['path']}")
    print("\nNext steps:")
    print(f"  cd {project['path']}")
    print("  npm install && npm start")
    print("\n✨ Track-based timeline made this super easy!\n")


if __name__ == "__main__":
    asyncio.run(main())
