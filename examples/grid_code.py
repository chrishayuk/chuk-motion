"""
Grid Code Example - Demonstrates 3x3 grid layout with code snippets.

This example showcases:
- Grid layout with 9 code blocks (3x3)
- Multiple programming languages
- Syntax highlighting
- Compact code snippets
- Design system integration
"""
import asyncio
import shutil
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_remotion.utils.project_manager import ProjectManager
from chuk_mcp_remotion.generator.composition_builder import ComponentInstance


async def main():
    """Generate a 3x3 grid of code snippets."""

    print("=" * 70)
    print("GRID CODE EXAMPLE - 3x3 CODE SNIPPETS")
    print("=" * 70)
    print()

    # Create project
    manager = ProjectManager()
    project_name = "code_grid"

    # Clean up existing project if it exists
    project_path = manager.workspace_dir / project_name
    if project_path.exists():
        print(f"🔄 Removing existing project: {project_name}")
        shutil.rmtree(project_path)

    print(f"📦 Step 1: Creating {project_name} project...")
    project = manager.create_project(
        name=project_name,
        theme="tech",
        fps=30,
        width=1920,
        height=1080
    )
    print(f"✓ Project created: {project['name']}")
    print(f"  Theme: {project['theme']}")
    print(f"  Resolution: {project['resolution']}")
    print()

    print("🎨 Step 2: Creating 9 code snippets...")
    print()

    # Define 9 compact code snippets showcasing different languages/concepts
    # Shorter versions optimized for 3x3 grid display with proper indentation
    code_snippets = [
        {
            "code": "const sum = (a, b) =>\n  a + b;\n\nsum(5, 3); // 8",
            "language": "javascript",
            "title": "sum.js",
            "description": "Arrow function"
        },
        {
            "code": "def fib(n):\n  if n <= 1:\n    return n\n  a = fib(n-1)\n  b = fib(n-2)\n  return a + b",
            "language": "python",
            "title": "fib.py",
            "description": "Recursion"
        },
        {
            "code": "function isPrime(n) {\n  for (let i=2; i<n; i++) {\n    if (n % i === 0) {\n      return false;\n    }\n  }\n  return n > 1;\n}",
            "language": "javascript",
            "title": "prime.js",
            "description": "Prime check"
        },
        {
            "code": "const reverse = str =>\n  str.split('')\n     .reverse()\n     .join('');",
            "language": "javascript",
            "title": "reverse.js",
            "description": "String reversal"
        },
        {
            "code": "class Circle:\n  def __init__(self, r):\n    self.radius = r\n  \n  def area(self):\n    pi = 3.14\n    return pi * \n           self.radius ** 2",
            "language": "python",
            "title": "circle.py",
            "description": "OOP class"
        },
        {
            "code": "function* count() {\n  let i = 0;\n  while (true) {\n    yield i++;\n  }\n}",
            "language": "javascript",
            "title": "generator.js",
            "description": "Generator"
        },
        {
            "code": "const debounce = (fn, ms) => {\n  let timer;\n  return (...args) => {\n    clearTimeout(timer);\n    timer = setTimeout(\n      () => fn(...args),\n      ms\n    );\n  };\n};",
            "language": "javascript",
            "title": "debounce.js",
            "description": "Debounce"
        },
        {
            "code": "function Counter() {\n  const [n, setN] = \n        useState(0);\n  \n  return (\n    <button \n      onClick={() => \n        setN(n + 1)}>\n      {n}\n    </button>\n  );\n}",
            "language": "javascript",
            "title": "Counter.tsx",
            "description": "React Hook"
        },
        {
            "code": "async function get(url) {\n  try {\n    const res = \n          await fetch(url);\n    return await \n           res.json();\n  } catch (err) {\n    console.error(err);\n  }\n}",
            "language": "javascript",
            "title": "fetch.js",
            "description": "Async/await"
        }
    ]

    # Add title card
    title = ComponentInstance(
        component_type="TitleScene",
        start_frame=0,
        duration_frames=0,
        props={
            "text": "Code Grid",
            "subtitle": "9 Code Snippets in 3x3 Layout",
            "variant": "bold",
            "animation": "fade_zoom"
        },
        layer=0
    )
    manager.current_timeline.add_component(title, duration=3.0, track="main")

    print("✓ Title card added")
    print()
    print("📊 Step 3: Creating code block components...")

    # Create individual code block components
    for idx, snippet in enumerate(code_snippets):
        print(f"  {idx + 1}. {snippet['title']:<16} - {snippet['description']}")

        code_block = ComponentInstance(
            component_type="CodeBlock",
            start_frame=0,
            duration_frames=0,
            props={
                "code": snippet['code'],
                "language": snippet['language'],
                "title": snippet['title'],
                "variant": "minimal",
                "animation": "fade_in",
                "show_line_numbers": False
            },
            layer=0
        )
        # Add each code block sequentially with a short duration
        manager.current_timeline.add_component(code_block, duration=3.0, track="main", gap_before=0.2)

    print()
    print("✓ All 9 code blocks added")
    print(f"  Total snippets: {len(code_snippets)}")
    print()

    # Add end screen
    end_screen = ComponentInstance(
        component_type="EndScreen",
        start_frame=0,
        duration_frames=0,
        props={
            "cta_text": "Explore More Code Examples",
            "variant": "gradient"
        },
        layer=0
    )
    manager.current_timeline.add_component(end_screen, duration=3.0, track="main", gap_before=0.5)
    print("✓ End screen added")

    print()
    print("⚙️  Step 4: Generating TSX components...")

    # Generate TSX files for each component type
    component_types = {c.component_type for c in manager.current_timeline.get_all_components()}

    for comp_type in component_types:
        sample = next(
            c for c in manager.current_timeline.get_all_components()
            if c.component_type == comp_type
        )
        manager.add_component_to_project(comp_type, sample.props, manager.current_timeline.theme)
        print(f"  ✓ {comp_type}.tsx")

    print()
    print("📝 Step 5: Generating VideoComposition.tsx...")

    # Generate composition
    manager.generate_composition()
    print(f"  ✓ VideoComposition.tsx")

    # Get project info
    info = manager.get_project_info()
    composition = info['composition']

    print()
    print("=" * 70)
    print("🎉 CODE GRID GENERATED!")
    print("=" * 70)
    print()
    print(f"📁 Project: {project_path}")
    print(f"🎬 Duration: {composition['duration_seconds']:.1f} seconds")
    print(f"📊 Components: {len(composition['components'])}")
    print(f"📐 Resolution: 1920x1080 @ 30fps")
    print()
    print("✨ Features:")
    print("  • 9 code snippets across multiple languages")
    print("  • Syntax highlighting for JavaScript and Python")
    print("  • Compact minimal variant for clean display")
    print("  • Showcases: Functions, OOP, Async, React, Generators")
    print("  • Design system tokens for consistent styling")
    print()
    print("🚀 To render:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")
    print()
    print("💡 Use Cases:")
    print("  • Programming language comparisons")
    print("  • Code pattern collections")
    print("  • Algorithm showcases")
    print("  • Cheat sheet videos")
    print("  • Portfolio showcases")
    print()
    print("=" * 70)
    print()
    print("✨ Your code grid is ready!")
    print()


if __name__ == "__main__":
    asyncio.run(main())
