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

    # BrowserFrame showing landing page with real HTML
    add_scene({
        "type": "BrowserFrame",
        "config": {
            "url": "https://example.com",
            "browser_type": "chrome",
            "show_controls": True,
            "theme": "light"
        },
        "content": {
            "type": "WebPage",
            "config": {
                "html": '''
<div style="max-width: 1200px; margin: 0 auto; text-align: center; padding: 60px 20px;">
  <h1 style="font-size: 56px; margin-bottom: 20px;">Welcome to Example.com</h1>
  <p style="font-size: 24px; opacity: 0.8; margin-bottom: 40px;">Modern Web Solutions for Your Business</p>
  <button style="font-size: 18px; padding: 16px 32px;">Get Started →</button>

  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-top: 80px; text-align: left;">
    <div style="padding: 30px; background: rgba(0,0,0,0.03); border-radius: 12px;">
      <h3 style="margin-bottom: 12px;">🚀 Fast</h3>
      <p>Lightning-fast performance that scales with your needs.</p>
    </div>
    <div style="padding: 30px; background: rgba(0,0,0,0.03); border-radius: 12px;">
      <h3 style="margin-bottom: 12px;">🔒 Secure</h3>
      <p>Enterprise-grade security built into every layer.</p>
    </div>
    <div style="padding: 30px; background: rgba(0,0,0,0.03); border-radius: 12px;">
      <h3 style="margin-bottom: 12px;">💎 Reliable</h3>
      <p>99.9% uptime with automatic failover protection.</p>
    </div>
  </div>
</div>
                ''',
                "theme": "light"
            }
        }
    })

    # BrowserFrame showing code editor/IDE
    add_scene({
        "type": "BrowserFrame",
        "config": {
            "url": "localhost:3000/editor",
            "browser_type": "arc",
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

    # BrowserFrame showing documentation site with StylizedWebPage
    add_scene({
        "type": "BrowserFrame",
        "config": {
            "url": "docs.example.com/api",
            "browser_type": "chrome",
            "show_controls": True,
            "theme": "light"
        },
        "content": {
            "type": "StylizedWebPage",
            "config": {
                "title": "API Docs",
                "subtitle": "Complete API Reference",
                "showHeader": True,
                "showSidebar": True,
                "showFooter": False,
                "headerText": "Getting Started • API • Examples",
                "sidebarItems": ["Authentication", "Users", "Posts", "Comments"],
                "contentLines": [
                    "GET /api/users - List all users",
                    "",
                    "POST /api/auth - Authenticate user",
                    "",
                    "DELETE /api/sessions - End session",
                    "",
                    "PUT /api/users/:id - Update user"
                ],
                "theme": "light",
                "accentColor": "primary"
            }
        }
    })

    # ========================================
    # DEVICE FRAMES
    # ========================================
    print("\n🎬 Device Frame Examples")

    # DeviceFrame - iPhone with video player
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
                "label": "▶ Now Playing\n\nTutorial Video\n00:42 / 05:30\n\n━━━━●────",
                "color": "primary"
            }
        }
    })

    # DeviceFrame - iPad with app interface
    add_scene({
        "type": "DeviceFrame",
        "config": {
            "device_type": "ipad",
            "orientation": "landscape",
            "show_notch": False
        },
        "content": {
            "type": "DemoBox",
            "config": {
                "label": "📱 Mobile Dashboard\n\nUsers: 1,234\nRevenue: $56.7K\nActive: 892\n\nView Analytics →",
                "color": "accent"
            }
        }
    })

    # DeviceFrame - Android with streaming app
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
                "label": "🎬 Video Library\n\nRecommended\n━━━━━━━━\nTrending\n━━━━━━━━\nSubscriptions",
                "color": "secondary"
            }
        }
    })

    # ========================================
    # TERMINAL FRAMES
    # ========================================
    print("\n🎬 Terminal Examples")

    # Terminal showing npm commands
    add_scene({
        "type": "Terminal",
        "config": {
            "title": "bash - npm",
            "theme": "dark",
            "show_header": True
        },
        "content": {
            "type": "DemoBox",
            "config": {
                "label": "$ npm install remotion\n+ remotion@4.0.0\nadded 245 packages in 12s\n\n$ npm start\nServer running on localhost:3000 ✓",
                "color": "primary"
            }
        }
    })

    # Terminal showing git workflow
    add_scene({
        "type": "Terminal",
        "config": {
            "title": "zsh - git",
            "theme": "dracula",
            "show_header": True
        },
        "content": {
            "type": "DemoBox",
            "config": {
                "label": "❯ git status\nOn branch main\nChanges not staged\n\n❯ git add .\n\n❯ git commit -m \"Update\"\n[main a1b2c3d] Update\n3 files changed, 42 insertions(+)",
                "color": "accent"
            }
        }
    })

    # Terminal showing docker commands
    add_scene({
        "type": "Terminal",
        "config": {
            "title": "bash - docker",
            "theme": "monokai",
            "show_header": True
        },
        "content": {
            "type": "DemoBox",
            "config": {
                "label": "$ docker ps\nCONTAINER ID  IMAGE   STATUS\nf3a2b1c4d5e6  nginx   Up 2h\n\n$ docker logs f3a2b1c4d5e6\nServer started ✓\nListening on port 80",
                "color": "secondary"
            }
        }
    })

    # ========================================
    # COMBINED LAYOUTS
    # ========================================
    print("\n🎬 Combined Frame Layouts")

    # SplitScreen with Browser and Terminal showing dev workflow
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
                "theme": "light"
            },
            "content": {
                "type": "DemoBox",
                "config": {
                    "label": "🚀 Live Preview\n\nApp Running\nHot Reload: ON\n\nlocalhost:3000",
                    "color": "accent"
                }
            }
        },
        "right": {
            "type": "Terminal",
            "config": {
                "title": "bash - dev server",
                "theme": "dark",
                "show_header": True
            },
            "content": {
                "type": "DemoBox",
                "config": {
                    "label": "$ npm run dev\n\nVITE ready in 543ms\n\nLocal: http://localhost:3000\nNetwork: use --host",
                    "color": "primary"
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
                        "label": "iPhone\nPortrait",
                        "color": "primary"
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
                        "label": "iPad\nLandscape",
                        "color": "accent"
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
                        "label": "Android\nPortrait",
                        "color": "secondary"
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
                        "label": "Desktop\nBrowser",
                        "color": "primary"
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
