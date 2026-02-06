#!/usr/bin/env python3
"""
End-to-End Video Rendering Example

Demonstrates the complete workflow:
1. Create a project
2. Add components (title, text effects, end screen)
3. Generate the composition files
4. Export to a Remotion project directory
5. Render to MP4 via Remotion CLI
6. Store as artifact and get presigned URL

This example shows what the MCP tools need to do for full rendering.
"""
import asyncio
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class RemotionProjectExporter:
    """Exports a CompositionBuilder to a complete Remotion project."""

    def __init__(self, builder, project_name: str):
        self.builder = builder
        self.project_name = project_name
        # Composition ID can only contain a-z, A-Z, 0-9, and -
        self.composition_id = project_name.replace("_", "-")

    def export_to_directory(self, output_dir: Path) -> dict:
        """
        Export the composition to a Remotion project directory.

        Returns:
            Dict with export info including file paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create src directory
        src_dir = output_dir / "src"
        src_dir.mkdir(exist_ok=True)

        # Create components directory
        components_dir = src_dir / "components"
        components_dir.mkdir(exist_ok=True)

        # Write package.json
        package_json = {
            "name": self.project_name,
            "version": "1.0.0",
            "description": "Remotion video project",
            "scripts": {
                "start": "remotion preview",
                "build": "remotion render",
                "upgrade": "remotion upgrade",
                "test": "echo \"No tests yet\""
            },
            "dependencies": {
                "@remotion/cli": "^4.0.0",
                "@remotion/bundler": "^4.0.0",
                "@remotion/renderer": "^4.0.0",
                "@remotion/studio": "^4.0.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "remotion": "^4.0.0",
                "prism-react-renderer": "^2.3.1"
            },
            "devDependencies": {
                "@types/react": "^18.2.0",
                "@types/node": "^20.0.0",
                "typescript": "^5.0.0",
                "prettier": "^3.0.0",
                "eslint": "^8.0.0"
            }
        }
        with open(output_dir / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)

        # Write tsconfig.json
        tsconfig = {
            "compilerOptions": {
                "target": "ES2022",
                "module": "ES2022",
                "moduleResolution": "node",
                "lib": ["DOM", "ES2022"],
                "jsx": "react-jsx",
                "strict": True,
                "esModuleInterop": True,
                "skipLibCheck": True,
                "forceConsistentCasingInFileNames": True,
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True
            },
            "include": ["src/**/*"],
            "exclude": ["node_modules"]
        }
        with open(output_dir / "tsconfig.json", "w") as f:
            json.dump(tsconfig, f, indent=2)

        # Write remotion.config.ts
        remotion_config = '''import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
const cpuCores = require('os').cpus().length;
Config.setConcurrency(Math.min(Math.floor(cpuCores * 0.5), 4));
'''
        with open(output_dir / "remotion.config.ts", "w") as f:
            f.write(remotion_config)

        # Write .gitignore
        with open(output_dir / ".gitignore", "w") as f:
            f.write("node_modules\nout\n*.mp4\n")

        # Generate and write VideoComposition.tsx
        composition_tsx = self.builder.generate_composition_tsx()
        with open(src_dir / "VideoComposition.tsx", "w") as f:
            f.write(composition_tsx)

        # Generate Root.tsx
        total_frames = self.builder.get_total_duration_frames()
        root_tsx = f'''import React from 'react';
import {{ Composition }} from 'remotion';
import {{ VideoComposition }} from './VideoComposition';

export const RemotionRoot: React.FC = () => {{
  return (
    <>
      <Composition
        id="{self.composition_id}"
        component={{VideoComposition}}
        durationInFrames={{{total_frames}}}
        fps={{{self.builder.fps}}}
        width={{{self.builder.width}}}
        height={{{self.builder.height}}}
        defaultProps={{{{
          theme: '{self.builder.theme}'
        }}}}
      />
    </>
  );
}};
'''
        with open(src_dir / "Root.tsx", "w") as f:
            f.write(root_tsx)

        # Generate index.ts entry point with registerRoot
        index_ts = '''import { registerRoot } from 'remotion';
import { RemotionRoot } from './Root';

registerRoot(RemotionRoot);
'''
        with open(src_dir / "index.ts", "w") as f:
            f.write(index_ts)

        # Generate component TSX files using ComponentBuilder
        self._generate_component_files(components_dir)

        return {
            "project_dir": str(output_dir),
            "composition_id": self.composition_id,
            "total_frames": total_frames,
            "fps": self.builder.fps,
            "width": self.builder.width,
            "height": self.builder.height,
        }

    def _generate_component_files(self, components_dir: Path):
        """Generate component TSX files using ComponentBuilder."""
        from chuk_motion.generator.component_builder import ComponentBuilder

        component_builder = ComponentBuilder()

        # Get unique component types from the composition
        component_types = set()
        for comp in self.builder.components:
            component_types.add(comp.component_type)

        for comp_type in component_types:
            try:
                tsx_code = component_builder.build_component(
                    comp_type, {}, self.builder.theme
                )
                output_file = components_dir / f"{comp_type}.tsx"
                with open(output_file, "w") as f:
                    f.write(tsx_code)
                print(f"  Created: {output_file.name}")
            except Exception as e:
                print(f"  Warning: Could not generate {comp_type}: {e}")


async def render_video(project_dir: Path, composition_id: str, output_path: Path) -> dict:
    """
    Render the video using Remotion CLI.

    Args:
        project_dir: Path to the Remotion project directory
        composition_id: The composition ID to render
        output_path: Path for the output MP4 file

    Returns:
        Dict with render result info
    """

    # Run npm install
    print("\n  Running npm install...")
    npm_install = subprocess.run(
        ["npm", "install"],
        cwd=project_dir,
        capture_output=True,
        text=True,
    )
    if npm_install.returncode != 0:
        return {
            "success": False,
            "error": f"npm install failed: {npm_install.stderr}",
        }
    print("  npm install completed")

    # Run remotion render
    print(f"\n  Rendering video to {output_path}...")
    render_cmd = [
        "npx", "remotion", "render",
        "src/index.ts",  # Entry point with registerRoot
        composition_id,
        str(output_path),
    ]

    render = subprocess.run(
        render_cmd,
        cwd=project_dir,
        capture_output=True,
        text=True,
    )

    if render.returncode != 0:
        return {
            "success": False,
            "error": f"Remotion render failed: {render.stderr}",
            "stdout": render.stdout,
        }

    # Get file info
    if output_path.exists():
        file_size = output_path.stat().st_size
        return {
            "success": True,
            "output_path": str(output_path),
            "file_size_bytes": file_size,
            "file_size_mb": round(file_size / (1024 * 1024), 2),
        }
    else:
        return {
            "success": False,
            "error": "Output file not created",
        }


async def test_render_workflow():
    """Test the complete render workflow."""
    print("\n" + "=" * 70)
    print("END-TO-END VIDEO RENDERING TEST")
    print("=" * 70)

    # Import required modules
    from chuk_motion.components import register_all_builders, register_all_renderers
    from chuk_motion.generator.composition_builder import CompositionBuilder

    # Register component builders
    register_all_builders(CompositionBuilder)
    register_all_renderers(CompositionBuilder)

    # Step 1: Create a composition builder
    print("\n--- Step 1: Create Composition Builder ---")
    builder = CompositionBuilder(fps=30, width=1920, height=1080)
    builder.theme = "tech"
    print(f"  Created builder: {builder.fps}fps, {builder.width}x{builder.height}")

    # Step 2: Add components
    print("\n--- Step 2: Add Components ---")

    # Add title scene
    builder.add_title_scene(
        text="HELLO",
        subtitle="Cool Effect",
        variant="bold",
        animation="fade_zoom",
        duration_seconds=3.0,
    )
    print("  Added: TitleScene (3.0s)")

    # Add fuzzy text
    builder.add_fuzzy_text(
        start_time=3.0,
        text="hello",
        font_size="4xl",
        glitch_intensity=12.0,
        scanline_height=2.0,
        animate=True,
        position="center",
        duration=3.0,
    )
    print("  Added: FuzzyText (3.0s)")

    # Add true focus
    builder.add_true_focus(
        start_time=6.0,
        text="hello world",
        font_size="2xl",
        font_weight="extrabold",
        word_duration=0.8,
        position="bottom",
        duration=2.0,
    )
    print("  Added: TrueFocus (2.0s)")

    # Add end screen
    builder.add_end_screen(
        cta_text="Thanks for Watching!",
        duration_seconds=3.0,
    )
    print("  Added: EndScreen (3.0s)")

    total_duration = builder.get_total_duration_seconds()
    print(f"\n  Total duration: {total_duration}s ({builder.get_total_duration_frames()} frames)")

    # Step 3: Export to Remotion project
    print("\n--- Step 3: Export to Remotion Project ---")

    # Use a temporary directory for the project
    with tempfile.TemporaryDirectory() as temp_dir:
        project_dir = Path(temp_dir) / "hello_effect_video"

        exporter = RemotionProjectExporter(builder, "hello_effect_video")
        export_result = exporter.export_to_directory(project_dir)

        print(f"  Project directory: {export_result['project_dir']}")
        print(f"  Composition ID: {export_result['composition_id']}")
        print(f"  Total frames: {export_result['total_frames']}")

        # Step 4: Render to MP4
        print("\n--- Step 4: Render to MP4 ---")
        output_path = project_dir / "out" / "video.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        render_result = await render_video(
            project_dir,
            export_result['composition_id'],
            output_path,
        )

        if render_result["success"]:
            print(f"  Output: {render_result['output_path']}")
            print(f"  Size: {render_result['file_size_mb']} MB")

            # Step 5: Simulate artifact storage (would use chuk-artifacts in production)
            print("\n--- Step 5: Store as Artifact ---")
            print("  (In production, this would upload to S3/Tigris)")
            print("  (Then generate a presigned download URL)")

            # Copy to a local output for demonstration
            final_output = Path(__file__).parent / "output" / "hello_effect_video.mp4"
            final_output.parent.mkdir(exist_ok=True)
            shutil.copy(output_path, final_output)
            print(f"  Copied to: {final_output}")
        else:
            print(f"  Error: {render_result.get('error', 'Unknown error')}")
            if render_result.get('stdout'):
                print(f"  Stdout: {render_result['stdout'][:500]}")

    # Summary
    print("\n" + "=" * 70)
    print("WORKFLOW COMPLETE")
    print("=" * 70)
    print("""
This example demonstrates:
  1. Creating a CompositionBuilder with components
  2. Exporting to a complete Remotion project
  3. Running npm install + npx remotion render
  4. Getting the rendered MP4 file

For production (in the MCP server):
  - Store the MP4 using chuk-artifacts store.store()
  - Generate presigned URL using store.presign()
  - Return the URL to the user
""")


def main():
    """Run the test."""
    asyncio.run(test_render_workflow())


if __name__ == "__main__":
    main()
