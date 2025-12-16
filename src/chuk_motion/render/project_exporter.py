"""
Project Exporter - Exports CompositionBuilder to a Remotion project directory.

This module handles:
1. Generating all required TSX files
2. Creating package.json, tsconfig, etc.
3. Setting up the project structure for rendering
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class RemotionProjectExporter:
    """Exports a CompositionBuilder to a complete Remotion project."""

    def __init__(self, builder, project_name: str):
        """
        Initialize the exporter.

        Args:
            builder: CompositionBuilder instance with components
            project_name: Name for the project (used for package.json, composition ID)
        """
        self.builder = builder
        self.project_name = project_name
        # Composition ID can only contain a-z, A-Z, 0-9, and -
        self.composition_id = project_name.replace("_", "-")

    def export_to_directory(self, output_dir: Path) -> dict[str, Any]:
        """
        Export the composition to a Remotion project directory.

        Args:
            output_dir: Directory to export to (will be created)

        Returns:
            Dict with export info including:
            - project_dir: Path to the project
            - composition_id: ID for rendering
            - total_frames: Total duration in frames
            - fps, width, height: Video specs
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
        self._write_package_json(output_dir)

        # Write tsconfig.json
        self._write_tsconfig(output_dir)

        # Write remotion.config.ts
        self._write_remotion_config(output_dir)

        # Write .gitignore
        with open(output_dir / ".gitignore", "w") as f:
            f.write("node_modules\nout\n*.mp4\n")

        # Generate and write VideoComposition.tsx
        composition_tsx = self.builder.generate_composition_tsx()
        with open(src_dir / "VideoComposition.tsx", "w") as f:
            f.write(composition_tsx)

        # Generate Root.tsx
        self._write_root_tsx(src_dir)

        # Generate index.ts entry point with registerRoot
        index_ts = """import { registerRoot } from 'remotion';
import { RemotionRoot } from './Root';

registerRoot(RemotionRoot);
"""
        with open(src_dir / "index.ts", "w") as f:
            f.write(index_ts)

        # Generate component TSX files using ComponentBuilder
        self._generate_component_files(components_dir)

        total_frames = self.builder.get_total_duration_frames()

        logger.info(f"Exported project to {output_dir}")

        return {
            "project_dir": str(output_dir),
            "composition_id": self.composition_id,
            "total_frames": total_frames,
            "fps": self.builder.fps,
            "width": self.builder.width,
            "height": self.builder.height,
        }

    def _write_package_json(self, output_dir: Path):
        """Write package.json with Remotion dependencies."""
        package_json = {
            "name": self.project_name,
            "version": "1.0.0",
            "description": "Remotion video project",
            "scripts": {
                "start": "remotion preview",
                "build": "remotion render",
                "upgrade": "remotion upgrade",
                "test": 'echo "No tests yet"',
            },
            "dependencies": {
                "@remotion/cli": "^4.0.0",
                "@remotion/bundler": "^4.0.0",
                "@remotion/renderer": "^4.0.0",
                "@remotion/studio": "^4.0.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "remotion": "^4.0.0",
                "prism-react-renderer": "^2.3.1",
            },
            "devDependencies": {
                "@types/react": "^18.2.0",
                "@types/node": "^20.0.0",
                "typescript": "^5.0.0",
                "prettier": "^3.0.0",
                "eslint": "^8.0.0",
            },
        }
        with open(output_dir / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)

    def _write_tsconfig(self, output_dir: Path):
        """Write tsconfig.json for TypeScript compilation."""
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
                "noEmit": True,
            },
            "include": ["src/**/*"],
            "exclude": ["node_modules"],
        }
        with open(output_dir / "tsconfig.json", "w") as f:
            json.dump(tsconfig, f, indent=2)

    def _write_remotion_config(self, output_dir: Path):
        """Write remotion.config.ts."""
        remotion_config = """import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
const cpuCores = require('os').cpus().length;
Config.setConcurrency(Math.min(Math.floor(cpuCores * 0.5), 4));
"""
        with open(output_dir / "remotion.config.ts", "w") as f:
            f.write(remotion_config)

    def _write_root_tsx(self, src_dir: Path):
        """Write Root.tsx with Composition registration."""
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

    def _generate_component_files(self, components_dir: Path):
        """Generate component TSX files using ComponentBuilder."""
        from ..generator.component_builder import ComponentBuilder

        component_builder = ComponentBuilder()

        # Get unique component types from the composition
        component_types = set()
        for comp in self.builder.components:
            component_types.add(comp.component_type)

        for comp_type in component_types:
            try:
                tsx_code = component_builder.build_component(comp_type, {}, self.builder.theme)
                output_file = components_dir / f"{comp_type}.tsx"
                with open(output_file, "w") as f:
                    f.write(tsx_code)
                logger.debug(f"Generated {comp_type}.tsx")
            except Exception as e:
                logger.warning(f"Could not generate {comp_type}: {e}")
