#!/usr/bin/env python3
"""
Demo Realism Showcase

Demonstrates all the realistic UI components for product demos and presentations:
- DeviceFrame: Phone, tablet, laptop mockups
- BrowserFrame: Browser windows with different themes
- Terminal: Realistic terminal with typing animation
- CodeDiff: Side-by-side code comparison
- BeforeAfterSlider: Interactive comparison slider
"""
import asyncio
import shutil
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_motion.utils.project_manager import ProjectManager
from chuk_motion.generator.composition_builder import CompositionBuilder


async def main():
    """Generate a video showcasing all demo realism components."""
    print("\n" + "="*70)
    print("DEMO REALISM SHOWCASE")
    print("="*70)

    # Initialize project manager
    manager = ProjectManager()
    project_name = "demo_realism_showcase"

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

    print("\n📱 Step 2: Adding demo realism components...")

    # Scene 1: DeviceFrame - Phone mockup (0-5s)
    print("\n  📱 Scene 1: Phone device frame...")
    manager.current_composition.add_device_frame(
        start_time=0.5,
        duration=4.5,
        device="phone",
        orientation="portrait",
        content="Product Screenshot",
        position="center",
        scale=1.0,
        glare=True,
        shadow=True
    )

    manager.current_composition.add_text_overlay(
        text="DeviceFrame: Phone",
        start_time=0.5,
        duration=4.5,
        position="top-center"
    )

    # Scene 2: DeviceFrame - Laptop mockup (5-10s)
    print("  💻 Scene 2: Laptop device frame...")
    manager.current_composition.add_device_frame(
        start_time=5.5,
        duration=4.5,
        device="laptop",
        orientation="landscape",
        content="Dashboard Demo",
        position="center",
        scale=0.7,
        glare=True,
        shadow=True
    )

    manager.current_composition.add_text_overlay(
        text="DeviceFrame: Laptop",
        start_time=5.5,
        duration=4.5,
        position="top-center"
    )

    # Scene 3: BrowserFrame - Chrome theme (10-15s)
    print("  🌐 Scene 3: Chrome browser frame...")
    manager.current_composition.add_browser_frame(
        start_time=10.5,
        duration=4.5,
        url="https://myapp.com/dashboard",
        theme="chrome",
        tabs='[{"title": "Dashboard", "active": true}, {"title": "Analytics", "active": false}, {"title": "Settings", "active": false}]',
        content="Interactive Dashboard Content",
        position="center",
        width=1200,
        height=700,
        show_status=True,
        status_text="Loaded in 1.2s"
    )

    manager.current_composition.add_text_overlay(
        text="BrowserFrame: Chrome",
        start_time=10.5,
        duration=4.5,
        position="top-center"
    )

    # Scene 4: BrowserFrame - Safari theme (15-20s)
    print("  🧭 Scene 4: Safari browser frame...")
    manager.current_composition.add_browser_frame(
        start_time=15.5,
        duration=4.5,
        url="https://docs.example.com",
        theme="safari",
        tabs='[{"title": "Getting Started", "active": true}, {"title": "API Reference", "active": false}]',
        content="Documentation Page",
        position="center",
        width=1300,
        height=750
    )

    manager.current_composition.add_text_overlay(
        text="BrowserFrame: Safari",
        start_time=15.5,
        duration=4.5,
        position="top-center"
    )

    # Scene 5: Terminal - Typing animation (20-27s)
    print("  ⌨️  Scene 5: Terminal with typing animation...")
    manager.current_composition.add_terminal(
        start_time=20.5,
        duration=6.5,
        commands='[{"command": "npm install react-app", "output": "✓ Installed 342 packages in 8.2s", "typeOn": true}, {"command": "npm run build", "output": "Creating optimized production build...\\n✓ Build complete! Output: /dist", "typeOn": true}, {"command": "npm test", "output": "Running tests...\\n✓ All tests passed (12/12)", "typeOn": true}]',
        prompt="zsh",
        title="Terminal - Project Setup",
        theme="dracula",
        position="center",
        width=900,
        height=600,
        show_cursor=True,
        type_speed=0.04
    )

    manager.current_composition.add_text_overlay(
        text="Terminal: Dracula Theme",
        start_time=20.5,
        duration=6.5,
        position="top-center"
    )

    # Scene 6: Terminal - Different theme (27-32s)
    print("  🖥️  Scene 6: Terminal with Nord theme...")
    manager.current_composition.add_terminal(
        start_time=27.5,
        duration=4.5,
        commands='[{"command": "git status", "output": "On branch main\\nYour branch is up to date", "typeOn": true}, {"command": "git log --oneline -3", "output": "a1b2c3d feat: add new feature\\nb2c3d4e fix: resolve bug\\nc3d4e5f docs: update README", "typeOn": false}]',
        prompt="bash",
        title="Terminal - Git Commands",
        theme="nord",
        position="center",
        width=900,
        height=500,
        show_cursor=True,
        type_speed=0.05
    )

    manager.current_composition.add_text_overlay(
        text="Terminal: Nord Theme",
        start_time=27.5,
        duration=4.5,
        position="top-center"
    )

    # Scene 7: CodeDiff - Unified view (32-37s)
    print("  📝 Scene 7: Code diff - unified view...")
    manager.current_composition.add_code_diff(
        start_time=32.5,
        duration=4.5,
        lines='[{"content": "function calculateTotal(items) {", "type": "unchanged", "lineNumber": 1}, {"content": "  let total = 0;", "type": "removed", "lineNumber": 2}, {"content": "  for (let i = 0; i < items.length; i++) {", "type": "removed", "lineNumber": 3}, {"content": "    total += items[i].price;", "type": "removed", "lineNumber": 4}, {"content": "  }", "type": "removed", "lineNumber": 5}, {"content": "  return items.reduce((sum, item) => sum + item.price, 0);", "type": "added", "lineNumber": 2}, {"content": "}", "type": "unchanged", "lineNumber": 3}]',
        mode="unified",
        language="javascript",
        title="Refactor: Use Array.reduce()",
        show_line_numbers=True,
        show_heatmap=False,
        theme="dark",
        position="center",
        width=1300,
        height=600,
        animate_lines=True
    )

    manager.current_composition.add_text_overlay(
        text="CodeDiff: Unified View",
        start_time=32.5,
        duration=4.5,
        position="top-center"
    )

    # Scene 8: CodeDiff - Split view (37-42s)
    print("  🔀 Scene 8: Code diff - split view...")
    manager.current_composition.add_code_diff(
        start_time=37.5,
        duration=4.5,
        lines='[{"content": "const API_URL = \'http://localhost:3000\';", "type": "removed", "lineNumber": 1}, {"content": "const API_URL = process.env.API_URL;", "type": "added", "lineNumber": 1}, {"content": "", "type": "unchanged", "lineNumber": 2}, {"content": "async function fetchData() {", "type": "unchanged", "lineNumber": 3}, {"content": "  const response = await fetch(API_URL);", "type": "unchanged", "lineNumber": 4}, {"content": "  return response.json();", "type": "unchanged", "lineNumber": 5}, {"content": "}", "type": "unchanged", "lineNumber": 6}]',
        mode="split",
        language="javascript",
        title="Config: Use environment variables",
        left_label="Before",
        right_label="After",
        show_line_numbers=True,
        theme="github",
        position="center",
        width=1400,
        height=500,
        animate_lines=True
    )

    manager.current_composition.add_text_overlay(
        text="CodeDiff: Split View",
        start_time=37.5,
        duration=4.5,
        position="top-center"
    )

    # Scene 9: BeforeAfterSlider - Horizontal (42-47s)
    print("  ↔️  Scene 9: Before/After slider - horizontal...")
    manager.current_composition.add_before_after_slider(
        start_time=42.5,
        duration=4.5,
        before_image="https://via.placeholder.com/1200x800/3a3a3a/ffffff?text=Before:+Old+Design",
        after_image="https://via.placeholder.com/1200x800/4a90e2/ffffff?text=After:+New+Design",
        before_label="Old Design",
        after_label="New Design",
        orientation="horizontal",
        animate_slider=True,
        slider_start_position=20.0,
        slider_end_position=80.0,
        show_labels=True,
        label_position="overlay",
        handle_style="arrow",
        position="center",
        width=1200,
        height=700,
        border_radius=12
    )

    manager.current_composition.add_text_overlay(
        text="BeforeAfterSlider: Horizontal",
        start_time=42.5,
        duration=4.5,
        position="top-center"
    )

    # Scene 10: BeforeAfterSlider - Vertical (47-52s)
    print("  ↕️  Scene 10: Before/After slider - vertical...")
    manager.current_composition.add_before_after_slider(
        start_time=47.5,
        duration=4.5,
        before_image="https://via.placeholder.com/900x700/e74c3c/ffffff?text=Before",
        after_image="https://via.placeholder.com/900x700/27ae60/ffffff?text=After",
        before_label="Version 1.0",
        after_label="Version 2.0",
        orientation="vertical",
        animate_slider=True,
        slider_start_position=30.0,
        slider_end_position=70.0,
        show_labels=True,
        label_position="top",
        handle_style="circle",
        position="center",
        width=900,
        height=700,
        border_radius=16
    )

    manager.current_composition.add_text_overlay(
        text="BeforeAfterSlider: Vertical",
        start_time=47.5,
        duration=4.5,
        position="bottom-center"
    )

    # Final scene: Summary (52-57s)
    print("  🎬 Scene 11: Closing summary...")
    manager.current_composition.add_text_overlay(
        text="Demo Realism Components Complete!",
        start_time=52.5,
        duration=4.5,
        position="center"
    )

    # Build and generate
    print("\n🎬 Step 3: Generating composition files...")
    print(f"  Total duration: {manager.current_composition.get_total_duration_seconds():.1f}s ({manager.current_composition.get_total_duration_frames()} frames)")
    composition_file = manager.generate_composition()
    print(f"✓ Composition generated successfully")
    print(f"  Components: {len(manager.current_composition.components)}")

    print("\n" + "="*70)
    print("✅ DEMO COMPLETE!")
    print("="*70)
    print(f"\n📁 Project location: {manager.workspace_dir / project_name}")
    print(f"📄 Composition file: {composition_file}")
    print(f"📊 Components used: {len(manager.current_composition.components)}")
    print(f"\n💡 Component breakdown:")
    print(f"   • DeviceFrame: 2 (phone + laptop)")
    print(f"   • BrowserFrame: 2 (Chrome + Safari)")
    print(f"   • Terminal: 2 (Dracula + Nord)")
    print(f"   • CodeDiff: 2 (unified + split)")
    print(f"   • BeforeAfterSlider: 2 (horizontal + vertical)")
    print(f"   • TextOverlay: 11 (labels)")
    print("\n💡 All components support:")
    print("   • Design system integration (colors, typography, motion)")
    print("   • Multiple themes and variants")
    print("   • Smooth entrance animations")
    print("   • Flexible positioning")
    print("   • Customizable dimensions")
    print("\n🚀 To preview:")
    print(f"   cd {manager.workspace_dir / project_name}")
    print(f"   npm run dev")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
