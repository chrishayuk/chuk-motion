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

    # Get composition builder
    composition = manager.current_composition

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

    # Create ComponentInstance objects for each code snippet
    children = []
    for idx, snippet in enumerate(code_snippets):
        print(f"  {idx + 1}. {snippet['title']:<16} - {snippet['description']}")

        child = composition.create_code_block_instance(
            code=snippet['code'],
            language=snippet['language'],
            title=snippet['title'],
            start_frame=0,  # Will be managed by Grid
            duration_frames=300,  # 10 seconds
            variant="minimal",  # Compact variant
            animation="fade_in",
            show_line_numbers=False  # No line numbers for compact display
        )
        children.append(child)

    print()
    print("📊 Step 3: Creating 3x3 grid layout...")

    # Add grid with all 9 snippets
    composition.add_grid(
        child_components=children,
        start_time=0.5,
        duration=9.5,
        layout="3x3",
        gap=20,  # Increased gap for better separation
        padding=40
    )

    print("✓ Grid created with 3x3 layout")
    print(f"  Total snippets: {len(children)}")
    print(f"  Grid gap: 20px")
    print(f"  Padding: 40px")
    print()

    print("⚙️  Step 4: Generating TSX components...")

    # Generate Grid component
    grid_tsx = manager.component_builder.build_component("Grid", {}, composition.theme)
    grid_file = Path(project['path']) / "src" / "components" / "Grid.tsx"
    grid_file.write_text(grid_tsx)
    print("✓ Generated: Grid.tsx")

    # Generate CodeBlock component
    code_block_tsx = manager.component_builder.build_component("CodeBlock", {}, composition.theme)
    code_block_file = Path(project['path']) / "src" / "components" / "CodeBlock.tsx"
    code_block_file.write_text(code_block_tsx)
    print("✓ Generated: CodeBlock.tsx")

    print()
    print("📝 Step 5: Generating VideoComposition.tsx...")

    # Generate composition
    composition_path = manager.generate_composition()
    print(f"✓ Generated: VideoComposition.tsx")

    print()
    print("=" * 70)
    print("🎉 3x3 CODE GRID GENERATED!")
    print("=" * 70)
    print()
    print(f"Project location: {project['path']}")
    print()
    print("✨ Features:")
    print("  • 3x3 grid layout with 9 code snippets")
    print("  • Syntax highlighting for JavaScript and Python")
    print("  • Compact minimal variant for dense display")
    print("  • Showcases: Functions, OOP, Async, React, Generators")
    print("  • Design system tokens for consistent spacing")
    print()
    print("Next steps:")
    print()
    print("1. Install dependencies:")
    print(f"   cd {project['path']}")
    print("   npm install")
    print()
    print("2. Preview in Remotion Studio:")
    print("   npm start")
    print()
    print("3. Render video:")
    print("   npx remotion render src/index.ts code-grid out/grid.mp4")
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
    print("✨ Your 3x3 code grid is ready!")
    print()


if __name__ == "__main__":
    asyncio.run(main())
