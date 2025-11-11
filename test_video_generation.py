#!/usr/bin/env python3
"""Test script to verify VideoContent generation with nested components."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from chuk_mcp_remotion.utils.project_manager import ProjectManager
from chuk_mcp_remotion.generator.composition_builder import ComponentInstance

# Create project manager
pm = ProjectManager()

# Create test project
project_name = "test_nested_video"
pm.create_project(project_name, theme="tech", fps=30, width=1920, height=1080)

print(f"✅ Created project: {project_name}")

# Add a title scene
pm.current_timeline.add_component(
    ComponentInstance(
        component_type="TitleScene",
        start_frame=0,
        duration_frames=90,
        props={
            "text": "Test Video",
            "subtitle": "Testing nested VideoContent",
            "variant": "bold",
            "animation": "fade_zoom"
        },
        layer=0
    ),
    duration=3.0,
    track="main"
)

print("✅ Added TitleScene")

# Create nested VideoContent components
left_video = ComponentInstance(
    component_type="VideoContent",
    start_frame=0,
    duration_frames=0,
    props={
        "src": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "muted": True,
        "fit": "cover",
        "loop": True
    },
    layer=5
)

center_video = ComponentInstance(
    component_type="VideoContent",
    start_frame=0,
    duration_frames=0,
    props={
        "src": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "muted": True,
        "fit": "cover",
        "loop": True
    },
    layer=5
)

right_video = ComponentInstance(
    component_type="VideoContent",
    start_frame=0,
    duration_frames=0,
    props={
        "src": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "muted": True,
        "fit": "cover",
        "loop": True
    },
    layer=5
)

# Add ThreeColumnLayout with nested VideoContent
pm.current_timeline.add_component(
    ComponentInstance(
        component_type="ThreeColumnLayout",
        start_frame=0,
        duration_frames=0,
        props={
            "left": left_video,
            "center": center_video,
            "right": right_video,
            "left_width": 30.0,
            "center_width": 40.0,
            "right_width": 30.0,
            "gap": 16.0,
            "padding": 40.0
        },
        layer=0
    ),
    duration=10.0,
    track="main"
)

print("✅ Added ThreeColumnLayout with nested VideoContent")

# Generate the composition
try:
    composition_file = pm.generate_composition()
    print(f"✅ Generated composition: {composition_file}")

    # Check what files were created
    components_dir = Path(pm.workspace_dir) / project_name / "src" / "components"
    if components_dir.exists():
        generated_files = list(components_dir.glob("*.tsx"))
        print(f"\n📁 Generated {len(generated_files)} component files:")
        for f in generated_files:
            print(f"   - {f.name}")

        # Check specifically for VideoContent.tsx
        video_content_file = components_dir / "VideoContent.tsx"
        if video_content_file.exists():
            print("\n✅ SUCCESS: VideoContent.tsx was generated!")
        else:
            print("\n❌ FAILURE: VideoContent.tsx was NOT generated")
    else:
        print("❌ Components directory doesn't exist")

except Exception as e:
    print(f"❌ Error during generation: {e}")
    import traceback
    traceback.print_exc()
