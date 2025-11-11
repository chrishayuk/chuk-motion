#!/usr/bin/env python3
"""
Frames Showcase

Demonstrates the three frame components: BrowserFrame, DeviceFrame, and Terminal.
Shows them with various content types and configurations.

Usage:
    python examples/frames_showcase.py
"""
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_remotion.utils.project_manager import ProjectManager
import shutil


def generate_frames_showcase():
    """Generate stunning showcase of frame components."""

    project_name = "frames_showcase"
    project_manager = ProjectManager()

    # Clean up existing project
    project_path_obj = project_manager.workspace_dir / project_name
    if project_path_obj.exists():
        print(f"🔄 Removing existing project: {project_path_obj}")
        shutil.rmtree(project_path_obj)

    print(f"\n{'='*70}")
    print(f"FRAMES SHOWCASE")
    print(f"BrowserFrame • DeviceFrame • Terminal")
    print(f"{'='*70}\n")

    # Create base project
    project_info = project_manager.create_project(project_name)
    project_path = Path(project_info["path"])

    print(f"✅ Created base project at: {project_path}")

    theme = "tech"
    scenes = []
    start_frame = 0
    scene_duration = 120  # 4 seconds per scene at 30fps

    # Helper to add scene and increment start_frame
    def add_scene(scene_dict, duration=scene_duration):
        nonlocal start_frame
        scene_dict["startFrame"] = start_frame
        scene_dict["durationInFrames"] = duration
        scenes.append(scene_dict)
        start_frame += duration

    # ========================================
    # INTRODUCTION
    # ========================================
    print("\n🎬 Creating Introduction")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Frames Showcase",
            "subtitle": "Professional Frame Components",
            "variant": "bold",
            "animation": "fade_zoom"
        }
    })

    # ========================================
    # BROWSER FRAMES
    # ========================================
    print("\n🎬 Browser Frame Examples")

    # BrowserFrame with CodeBlock
    add_scene({
        "type": "BrowserFrame",
        "config": {
            "url": "https://example.com/code",
            "browser_type": "chrome",
            "show_controls": True,
            "theme": "dark"
        },
        "content": {
            "type": "CodeBlock",
            "config": {
                "code": '''function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

console.log(fibonacci(10));''',
                "language": "javascript",
                "theme": "dark",
                "show_line_numbers": True,
                "highlight_lines": [2, 3]
            }
        }
    })

    # BrowserFrame with TypingCode animation
    add_scene({
        "type": "BrowserFrame",
        "config": {
            "url": "localhost:3000",
            "browser_type": "safari",
            "show_controls": True,
            "theme": "light"
        },
        "content": {
            "type": "TypingCode",
            "config": {
                "code": '''import React from 'react';

export const App = () => {
  return <h1>Hello World!</h1>;
};''',
                "language": "typescript",
                "theme": "light",
                "typing_speed": 2
            }
        }
    }, duration=150)

    # BrowserFrame with CodeBlock
    add_scene({
        "type": "BrowserFrame",
        "config": {
            "url": "docs.example.com",
            "browser_type": "firefox",
            "show_controls": True,
            "theme": "dark"
        },
        "content": {
            "type": "CodeBlock",
            "config": {
                "code": '''# Getting Started

This documentation guides you through
the basics of using our API.

Visit: docs.example.com''',
                "language": "markdown",
                "theme": "dark",
                "show_line_numbers": False
            }
        }
    })

    # ========================================
    # DEVICE FRAMES
    # ========================================
    print("\n🎬 Device Frame Examples")

    # DeviceFrame - iPhone with content
    add_scene({
        "type": "DeviceFrame",
        "config": {
            "device_type": "iphone",
            "orientation": "portrait",
            "show_notch": True
        },
        "content": {
            "type": "DemoBox",
            "config": {
                "text": "Mobile App\n\nDesigned for iOS",
                "font_size": 32,
                "line_height": 1.5,
                "alignment": "center"
            }
        }
    })

    # DeviceFrame - iPad landscape
    add_scene({
        "type": "DeviceFrame",
        "config": {
            "device_type": "ipad",
            "orientation": "landscape",
            "show_notch": False
        },
        "content": {
            "type": "CodeBlock",
            "config": {
                "code": '''class DataManager {
  async fetchData() {
    const response = await fetch('/api/data');
    return response.json();
  }
}''',
                "language": "typescript",
                "theme": "dark",
                "show_line_numbers": True
            }
        }
    })

    # DeviceFrame - Android phone
    add_scene({
        "type": "DeviceFrame",
        "config": {
            "device_type": "android",
            "orientation": "portrait",
            "show_notch": False
        },
        "content": {
            "type": "DemoBox",
            "config": {
                "text": "Cross-Platform\n\nWorks on Android too!",
                "font_size": 28,
                "line_height": 1.5,
                "alignment": "center"
            }
        }
    })

    # ========================================
    # TERMINAL FRAMES
    # ========================================
    print("\n🎬 Terminal Examples")

    # Terminal with simple command
    add_scene({
        "type": "Terminal",
        "config": {
            "title": "bash",
            "theme": "dark",
            "show_header": True
        },
        "content": {
            "type": "CodeBlock",
            "config": {
                "code": '''$ npm install remotion
+ remotion@4.0.0
added 245 packages in 12s

$ npm start
Server running on http://localhost:3000''',
                "language": "bash",
                "theme": "dark",
                "show_line_numbers": False
            }
        }
    })

    # Terminal with typing animation
    add_scene({
        "type": "Terminal",
        "config": {
            "title": "zsh",
            "theme": "dark",
            "show_header": True
        },
        "content": {
            "type": "TypingCode",
            "config": {
                "code": '''$ git clone https://github.com/user/repo.git
Cloning into 'repo'...
remote: Counting objects: 100%
Receiving objects: 100% (1234/1234)

$ cd repo && npm install''',
                "language": "bash",
                "theme": "dark",
                "typing_speed": 3
            }
        }
    }, duration=150)

    # Terminal with Python code
    add_scene({
        "type": "Terminal",
        "config": {
            "title": "python",
            "theme": "dark",
            "show_header": True
        },
        "content": {
            "type": "CodeBlock",
            "config": {
                "code": '''>>> def greet(name):
...     return f"Hello, {name}!"
...
>>> greet("World")
'Hello, World!'
>>> exit()''',
                "language": "python",
                "theme": "dark",
                "show_line_numbers": False
            }
        }
    })

    # ========================================
    # COMBINED LAYOUTS
    # ========================================
    print("\n🎬 Combined Frame Layouts")

    # SplitScreen with Browser and Terminal
    add_scene({
        "type": "SplitScreen",
        "config": {
            "orientation": "horizontal",
            "gap": 20,
            "divider_width": 2
        },
        "left": {
            "type": "BrowserFrame",
            "config": {
                "url": "localhost:3000",
                "browser_type": "chrome",
                "show_controls": True,
                "theme": "dark"
            },
            "content": {
                "type": "DemoBox",
                "config": {
                    "text": "Live Preview\n\nYour app is running",
                    "font_size": 28,
                    "alignment": "center"
                }
            }
        },
        "right": {
            "type": "Terminal",
            "config": {
                "title": "npm",
                "theme": "dark",
                "show_header": True
            },
            "content": {
                "type": "CodeBlock",
                "config": {
                    "code": '''$ npm run dev

> dev
> vite

  VITE ready in 543 ms

  Local:   http://localhost:3000
  Network: use --host to expose''',
                    "language": "bash",
                    "theme": "dark",
                    "show_line_numbers": False
                }
            }
        }
    })

    # Grid with multiple device frames
    add_scene({
        "type": "Grid",
        "config": {
            "layout": "2x2",
            "padding": 40,
            "gap": 20,
            "border_width": 2
        },
        "children": [
            {
                "type": "DeviceFrame",
                "config": {
                    "device_type": "iphone",
                    "orientation": "portrait",
                    "show_notch": True
                },
                "content": {
                    "type": "DemoBox",
                    "config": {
                        "text": "iPhone\nPortrait",
                        "font_size": 24,
                        "alignment": "center"
                    }
                }
            },
            {
                "type": "DeviceFrame",
                "config": {
                    "device_type": "ipad",
                    "orientation": "landscape",
                    "show_notch": False
                },
                "content": {
                    "type": "DemoBox",
                    "config": {
                        "text": "iPad\nLandscape",
                        "font_size": 24,
                        "alignment": "center"
                    }
                }
            },
            {
                "type": "DeviceFrame",
                "config": {
                    "device_type": "android",
                    "orientation": "portrait",
                    "show_notch": False
                },
                "content": {
                    "type": "DemoBox",
                    "config": {
                        "text": "Android\nPortrait",
                        "font_size": 24,
                        "alignment": "center"
                    }
                }
            },
            {
                "type": "BrowserFrame",
                "config": {
                    "url": "responsive.design",
                    "browser_type": "chrome",
                    "show_controls": True,
                    "theme": "dark"
                },
                "content": {
                    "type": "DemoBox",
                    "config": {
                        "text": "Desktop\nBrowser",
                        "font_size": 24,
                        "alignment": "center"
                    }
                }
            }
        ]
    })

    # ========================================
    # FINAL TITLE
    # ========================================
    print("\n🎬 Creating Final Title")
    add_scene({
        "type": "TitleScene",
        "config": {
            "text": "Professional Frames",
            "subtitle": "Browser • Device • Terminal",
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
    print("✅ FRAMES SHOWCASE GENERATED!")
    print("="*70)
    print(f"\n📁 Project location: {project_path}")

    # Calculate stats
    total_frames = result['total_frames']
    total_duration = total_frames / 30.0

    print(f"\n⏱️  Total duration: {total_duration:.1f} seconds ({total_frames} frames @ 30fps)")
    print(f"\n📊 Showcase structure:")
    print(f"   • Introduction: 1 scene")
    print(f"   • Browser Frames: 3 scenes")
    print(f"   • Device Frames: 3 scenes")
    print(f"   • Terminal Frames: 3 scenes")
    print(f"   • Combined Layouts: 2 scenes")
    print(f"   • Final Title: 1 scene")
    print(f"   • TOTAL: {len(scenes)} scenes")

    print(f"\n🎨 Frame Components Showcased:")
    print("   ✓ BrowserFrame (Chrome, Safari, Firefox)")
    print("   ✓ DeviceFrame (iPhone, iPad, Android)")
    print("   ✓ Terminal (bash, zsh, python)")

    print(f"\n📦 Generated {len(result['component_types'])} component types:")
    for comp_type in sorted(result['component_types']):
        print(f"   • {comp_type}")

    print(f"\n✨ Generated {len(result['component_files'])} TSX files")

    print("\n📝 Next steps:")
    print(f"   cd {project_path}")
    print("   npm install")
    print("   npm start")

    print("\n💡 This showcase demonstrates:")
    print("   ✓ All three professional frame components")
    print("   ✓ Various browser types and themes")
    print("   ✓ Multiple device types and orientations")
    print("   ✓ Terminal frames with different shells")
    print("   ✓ Frames combined with content components")
    print("   ✓ Complex layouts using frames")

    print("\n" + "="*70)

    return project_path


def main():
    """Main entry point."""
    print("\n🎬 Frames Showcase Generator")
    print("   Professional demonstration of frame components\n")

    try:
        project_path = generate_frames_showcase()
        print("✨ Generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
