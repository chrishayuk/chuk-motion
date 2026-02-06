#!/usr/bin/env python3
"""
Code Components Showcase

Demonstrates all 3 code display components with various programming languages.
Shows: CodeBlock, TypingCode, CodeDiff

Usage:
    python examples/code_showcase.py
"""
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import shutil

from chuk_motion.utils.project_manager import ProjectManager


def generate_code_showcase():
    """Generate comprehensive showcase of all code components."""

    project_name = "code_showcase"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print("CODE COMPONENTS SHOWCASE")
    print("All 3 Code Display Components")
    print(f"{'='*70}\n")

    # Create base project
    project_info = project_manager.create_project(project_name)
    project_path = Path(project_info["path"])

    print(f"✅ Created base project at: {project_path}")

    theme = "tech"
    scenes = []
    start_frame = 0
    scene_duration = 150  # 5 seconds per component at 30fps
    title_duration = 60   # 2 seconds for title slides

    # Helper to add scene and increment start_frame
    def add_scene(scene_dict, duration=scene_duration):
        nonlocal start_frame
        scene_dict["startFrame"] = start_frame
        scene_dict["durationInFrames"] = duration
        scenes.append(scene_dict)
        start_frame += duration

    def add_code_with_title(number, name, description, code_scene_dict):
        """Add a title slide followed by the code demo."""
        add_scene({
            "type": "TitleScene",
            "config": {
                "text": f"{number}. {name}",
                "subtitle": description,
                "variant": "minimal",
                "animation": "fade"
            }
        }, duration=title_duration)
        add_scene(code_scene_dict)

    # ========================================
    # INTRODUCTION
    # ========================================
    print("\n🎬 Creating Introduction")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Code Showcase",
            "subtitle": "3 Professional Code Display Components",
            "variant": "bold",
            "animation": "fade_zoom"
        }
    }, duration=90)

    # ========================================
    # 1. CODE BLOCK - Python
    # ========================================
    print("\n💻 1. CodeBlock - Python")
    add_code_with_title(
        1,
        "CodeBlock",
        "Static code display - Python",
        {
            "type": "CodeBlock",
            "config": {
                "code": '''def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Example usage
result = fibonacci(10)
print(f"The 10th Fibonacci number is: {result}")''',
                "language": "python",
                "theme": "dark",
                "show_line_numbers": True,
                "highlight_lines": [3, 4, 5]
            }
        }
    )

    # ========================================
    # 2. CODE BLOCK - JavaScript
    # ========================================
    print("\n💻 2. CodeBlock - JavaScript")
    add_code_with_title(
        2,
        "CodeBlock",
        "Static code display - JavaScript",
        {
            "type": "CodeBlock",
            "config": {
                "code": '''// React component example
const Button = ({ onClick, children }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={isHovered ? 'hovered' : ''}
    >
      {children}
    </button>
  );
};''',
                "language": "javascript",
                "theme": "dark",
                "show_line_numbers": True,
                "highlight_lines": [2, 3, 6, 7, 8]
            }
        }
    )

    # ========================================
    # 3. CODE BLOCK - TypeScript
    # ========================================
    print("\n💻 3. CodeBlock - TypeScript")
    add_code_with_title(
        3,
        "CodeBlock",
        "Static code display - TypeScript",
        {
            "type": "CodeBlock",
            "config": {
                "code": '''interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return await response.json();
}''',
                "language": "typescript",
                "theme": "dark",
                "show_line_numbers": True,
                "highlight_lines": [1, 2, 3, 4, 5]
            }
        }
    )

    # ========================================
    # 4. TYPING CODE - Animated typing effect
    # ========================================
    print("\n⌨️  4. TypingCode - Animated")
    add_code_with_title(
        4,
        "TypingCode",
        "Animated typing effect",
        {
            "type": "TypingCode",
            "config": {
                "code": '''const express = require('express');
const app = express();

app.get('/api/hello', (req, res) => {
  res.json({ message: 'Hello, World!' });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});''',
                "language": "javascript",
                "theme": "dark",
                "typing_speed": 50,
                "show_cursor": True,
                "show_line_numbers": True
            }
        }
    )

    # ========================================
    # 5. CODE DIFF - Before/After
    # ========================================
    print("\n🔄 5. CodeDiff - Git style diff")
    add_code_with_title(
        5,
        "CodeDiff",
        "Show code changes git-style",
        {
            "type": "CodeDiff",
            "config": {
                "before": '''function calculateTotal(items) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i].price;
  }
  return total;
}''',
                "after": '''function calculateTotal(items) {
  return items.reduce((total, item) => {
    return total + item.price;
  }, 0);
}''',
                "language": "javascript",
                "theme": "dark",
                "show_line_numbers": True,
                "highlight_changes": True
            }
        }
    )

    # ========================================
    # 6. CODE DIFF - Refactoring example
    # ========================================
    print("\n🔄 6. CodeDiff - Refactoring")
    add_code_with_title(
        6,
        "CodeDiff",
        "Refactoring improvement",
        {
            "type": "CodeDiff",
            "config": {
                "before": '''# Old implementation
def get_user_data(user_id):
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = " + str(user_id))
    result = cursor.fetchone()
    conn.close()
    return result''',
                "after": '''# Improved implementation
def get_user_data(user_id: int) -> dict:
    with db.connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        return cursor.fetchone()''',
                "language": "python",
                "theme": "dark",
                "show_line_numbers": True,
                "highlight_changes": True
            }
        }
    )

    # ========================================
    # COMBINED LAYOUT - Side by Side
    # ========================================
    print("\n🎬 Creating Combined Layout")
    add_scene({
        "type": "SplitScreen",
        "config": {
            "orientation": "horizontal",
            "gap": 20,
            "divider_width": 2
        },
        "left": {
            "type": "CodeBlock",
            "config": {
                "code": '''# Python
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))''',
                "language": "python",
                "theme": "dark",
                "show_line_numbers": True
            }
        },
        "right": {
            "type": "CodeBlock",
            "config": {
                "code": '''// JavaScript
function greet(name) {
  return `Hello, ${name}!`;
}

console.log(greet("World"));''',
                "language": "javascript",
                "theme": "dark",
                "show_line_numbers": True
            }
        }
    }, duration=150)

    # ========================================
    # FINAL TITLE
    # ========================================
    print("\n🎬 Creating Final Title")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Code Made Beautiful",
            "subtitle": "CodeBlock • TypingCode • CodeDiff",
            "variant": "glass",
            "animation": "zoom"
        }
    })

    # ========================================
    # Build the composition
    # ========================================
    print("\n🎬 Building composition...")

    result = project_manager.build_composition_from_scenes(scenes, theme=theme)

    print("\n" + "="*70)
    print("✅ CODE SHOWCASE GENERATED!")
    print("="*70)
    print(f"\n📁 Project location: {project_path}")

    # Calculate stats
    total_frames = result['total_frames']
    total_duration = total_frames / 30.0

    print(f"\n⏱️  Total duration: {total_duration:.1f} seconds ({total_frames} frames @ 30fps)")
    print("\n📊 Showcase structure:")
    print("   • Introduction: 1 scene")
    print("   • Individual Components: 6 × 2 scenes = 12 scenes")
    print("   • Combined Layout: 1 scene")
    print("   • Final Title: 1 scene")
    print(f"   • TOTAL: {len(scenes)} scenes")

    print("\n💻 Code Components Showcased:")
    print("   ✓ CodeBlock - Static code display (Python, JS, TS)")
    print("   ✓ TypingCode - Animated typing effect")
    print("   ✓ CodeDiff - Git-style diffs and refactoring")

    print("\n🎨 Languages Demonstrated:")
    print("   • Python")
    print("   • JavaScript")
    print("   • TypeScript")

    print(f"\n📦 Generated {len(result['component_types'])} component types:")
    for comp_type in sorted(result['component_types']):
        print(f"   • {comp_type}")

    print(f"\n✨ Generated {len(result['component_files'])} TSX files")

    print("\n📝 Next steps:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")

    print("\n💡 This showcase demonstrates:")
    print("   ✓ All 3 professional code components")
    print("   ✓ Multiple programming languages")
    print("   ✓ Syntax highlighting")
    print("   ✓ Line numbers and highlighting")
    print("   ✓ Animated typing effects")
    print("   ✓ Before/after code comparisons")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n💻 Code Components Showcase Generator")
    print("   Professional demonstration of all code display components\n")

    try:
        generate_code_showcase()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
