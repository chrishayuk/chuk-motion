#!/usr/bin/env python3
"""
Code Display Example

Demonstrates both static and animated typing code components
for technical tutorials and coding videos.
"""
import asyncio
import shutil
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_motion.generator.composition_builder import CompositionBuilder
from chuk_motion.utils.project_manager import ProjectManager


async def main():
    """Generate a video with code display examples."""
    print("\n" + "="*70)
    print("CODE DISPLAY EXAMPLE")
    print("="*70)

    # Initialize project manager
    manager = ProjectManager()
    project_name = "code_tutorial"

    # Clean up existing project if it exists
    project_path = manager.workspace_dir / project_name
    if project_path.exists():
        print(f"\n🔄 Removing existing project: {project_name}")
        shutil.rmtree(project_path)

    # Step 1: Create project
    print(f"\n💻 Step 1: Creating {project_name} project...")
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

    # Initialize composition
    manager.current_composition = CompositionBuilder(
        fps=30,
        width=1920,
        height=1080,
        transparent=False
    )
    manager.current_composition.theme = "tech"

    print("\n  🎨 Using dark background for code display")

    # Step 2: Add examples
    print("\n📝 Step 2: Adding code examples...")

    # Example 1: Static code block - Quick reference
    static_code_1 = """const fibonacci = (n) => {
  if (n <= 1) return n;
  return fibonacci(n-1) + fibonacci(n-2);
};

console.log(fibonacci(10));"""

    manager.current_composition.add_code_block(
        code=static_code_1,
        language="javascript",
        title="fibonacci.js",
        start_time=0.5,
        duration=4.0,
        variant="editor",
        animation="slide_up",
        show_line_numbers=True
    )
    print("✓ Example #1: Static Fibonacci (editor style)")
    print("  Animation: slide_up")
    print("  Duration: 4.0s")

    # Example 2: Typing code - Shows the process
    typing_code_1 = """function isPrime(num) {
  if (num <= 1) return false;

  for (let i = 2; i < num; i++) {
    if (num % i === 0) {
      return false;
    }
  }

  return true;
}"""

    manager.current_composition.add_typing_code(
        code=typing_code_1,
        language="javascript",
        title="isPrime.js",
        start_time=5.0,
        duration=8.0,
        variant="editor",
        cursor_style="line",
        typing_speed="normal",
        show_line_numbers=True
    )
    print("\n✓ Example #2: Typing isPrime function")
    print("  Animation: character-by-character typing")
    print("  Typing speed: normal")
    print("  Duration: 8.0s")

    # Example 3: Terminal variant with command
    terminal_code = """$ npm install remotion
+ remotion@4.0.358
added 247 packages in 12s

$ npm run dev
> dev
> remotion studio

Server running at http://localhost:3000"""

    manager.current_composition.add_code_block(
        code=terminal_code,
        language="bash",
        title="",
        start_time=14.0,
        duration=4.0,
        variant="terminal",
        animation="fade_in",
        show_line_numbers=False
    )
    print("\n✓ Example #3: Terminal commands")
    print("  Variant: terminal (no line numbers)")
    print("  Duration: 4.0s")

    # Example 4: Hacker-style typing
    hacker_code = """async function hack() {
  const target = await connect();
  const data = await infiltrate(target);
  return decrypt(data);
}"""

    manager.current_composition.add_typing_code(
        code=hacker_code,
        language="javascript",
        title="",
        start_time=19.0,
        duration=6.0,
        variant="hacker",
        cursor_style="block",
        typing_speed="fast",
        show_line_numbers=False
    )
    print("\n✓ Example #4: Hacker-style typing")
    print("  Variant: hacker (green glow)")
    print("  Typing speed: fast")
    print("  Duration: 6.0s")

    # Example 5: Python code with glass effect
    python_code = """def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)"""

    manager.current_composition.add_code_block(
        code=python_code,
        language="python",
        title="merge_sort.py",
        start_time=26.0,
        duration=5.0,
        variant="glass",
        animation="scale_in",
        show_line_numbers=True
    )
    print("\n✓ Example #5: Python with glass effect")
    print("  Variant: glass (glassmorphism)")
    print("  Animation: scale_in")
    print("  Duration: 5.0s")

    # Step 3: Get composition info
    print("\n📊 Step 3: Composition summary...")
    info = manager.get_project_info()
    composition = info['composition']

    print(f"  Total duration: {composition['duration_seconds']:.1f} seconds")
    print(f"  Total frames: {composition['duration_frames']}")
    print(f"  Components: {len(composition['components'])}")

    print("\n  Timeline:")
    for comp in composition['components']:
        comp_type = comp['type']
        start = comp['start_time']
        end = comp['start_time'] + comp['duration']
        variant = comp['props'].get('variant', 'N/A')
        title = comp['props'].get('title', 'untitled')

        if comp_type == "CodeBlock":
            print(f"    📄 CodeBlock ({variant}): {start:.1f}s - {end:.1f}s | {title}")
        elif comp_type == "TypingCode":
            speed = comp['props'].get('typing_speed', 'normal')
            print(f"    ⌨️  TypingCode ({speed}): {start:.1f}s - {end:.1f}s | {title}")

    # Step 4: Generate TSX files
    print("\n⚙️  Step 4: Generating TSX components...")

    # Generate CodeBlock component if present
    if any(c.component_type == "CodeBlock" for c in manager.current_composition.components):
        code_component = next(
            c for c in manager.current_composition.components
            if c.component_type == "CodeBlock"
        )
        code_file = manager.add_component_to_project(
            "CodeBlock",
            code_component.props,
            manager.current_composition.theme
        )
        print(f"✓ Generated: {Path(code_file).name}")

    # Generate TypingCode component if present
    if any(c.component_type == "TypingCode" for c in manager.current_composition.components):
        typing_component = next(
            c for c in manager.current_composition.components
            if c.component_type == "TypingCode"
        )
        typing_file = manager.add_component_to_project(
            "TypingCode",
            typing_component.props,
            manager.current_composition.theme
        )
        print(f"✓ Generated: {Path(typing_file).name}")

    # Generate main composition
    print("\n📝 Step 5: Generating VideoComposition.tsx...")
    composition_file = manager.generate_composition()
    print(f"✓ Generated: {Path(composition_file).name}")

    # Step 5: Show next steps
    print("\n" + "="*70)
    print("🎉 CODE TUTORIAL VIDEO GENERATED!")
    print("="*70)

    print(f"\nProject location: {project['path']}")

    print("\n✨ Key Features:")
    print("  • Static code blocks with animations")
    print("  • Character-by-character typing effect")
    print("  • Multiple variants: editor, terminal, hacker, glass")
    print("  • Blinking cursor for typing animations")
    print("  • Line numbers and syntax theming")
    print("  • Monospace fonts from design system")

    print("\nNext steps:")
    print("\n1. Install dependencies:")
    print(f"   cd {project['path']}")
    print("   npm install")

    print("\n2. Preview in Remotion Studio:")
    print("   npm start")

    print("\n3. Render video:")
    print("   npx remotion render src/index.ts code-tutorial out/tutorial.mp4")

    print("\n💡 Use Cases:")
    print("  • Coding tutorials")
    print("  • Programming courses")
    print("  • Tech explainer videos")
    print("  • Live coding demonstrations")
    print("  • Algorithm visualizations")
    print("  • Command line tutorials")

    print("\n🎨 Variants:")
    print("  • editor:   IDE-style with window buttons")
    print("  • terminal: Command-line interface look")
    print("  • glass:    Glassmorphism with blur")
    print("  • hacker:   Matrix-style green glow")
    print("  • minimal:  Clean and simple")

    print("\n" + "="*70)
    print("\n✨ Your code tutorial video is ready!\n")


if __name__ == "__main__":
    asyncio.run(main())
