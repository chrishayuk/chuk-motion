"""
Async Project Manager - Creates and manages Remotion projects using chuk-artifacts.

This is the async-native replacement for the synchronous ProjectManager,
using ArtifactStorageManager for all storage operations.
"""

import logging
from pathlib import Path
from typing import Any

from jinja2 import Template

from ..generator.component_builder import ComponentBuilder
from ..generator.composition_builder import ComponentInstance
from ..generator.timeline import Timeline
from ..models.artifact_models import (
    ProjectInfo,
    ProviderType,
    StorageScope,
)
from ..storage import ArtifactStorageManager

logger = logging.getLogger(__name__)


class AsyncProjectManager:
    """
    Async-native project manager using chuk-artifacts for storage.

    All methods are async and use ArtifactStorageManager for persistence.
    """

    def __init__(
        self,
        provider_type: ProviderType = ProviderType.FILESYSTEM,
        provider_config: dict[str, Any] | None = None,
    ):
        """
        Initialize async project manager.

        Args:
            provider_type: Storage provider backend (default: FILESYSTEM)
            provider_config: Provider-specific configuration
        """
        self.storage = ArtifactStorageManager(
            provider_type=provider_type, provider_config=provider_config or {}
        )
        self.component_builder = ComponentBuilder()

        # Current project state (namespace ID)
        self.current_project_id: str | None = None
        self.current_timeline: Timeline | None = None
        self.current_composition = None

    async def initialize(self) -> None:
        """Initialize the storage manager."""
        await self.storage.initialize()
        logger.info("AsyncProjectManager initialized")

    async def cleanup(self) -> None:
        """Cleanup the storage manager."""
        await self.storage.cleanup()
        logger.info("AsyncProjectManager cleaned up")

    async def create_project(
        self,
        name: str,
        theme: str = "tech",
        fps: int = 30,
        width: int = 1920,
        height: int = 1080,
        scope: StorageScope = StorageScope.USER,
        user_id: str | None = None,
    ) -> ProjectInfo:
        """
        Create a new Remotion project.

        Args:
            name: Project name
            theme: Theme to use
            fps: Frames per second
            width: Video width
            height: Video height
            scope: Storage scope (SESSION, USER, SANDBOX)
            user_id: User ID (required for USER scope)

        Returns:
            ProjectInfo with namespace and metadata
        """
        # Create project via artifact storage
        project_info = await self.storage.create_project(
            project_name=name,
            theme=theme,
            fps=fps,
            width=width,
            height=height,
            scope=scope,
            user_id=user_id,
        )

        # Set as current project
        self.current_project_id = project_info.namespace_info.namespace_id

        # Create timeline (track-based system)
        self.current_timeline = Timeline(fps=fps, width=width, height=height, theme=theme)

        # Get VFS and create project structure
        vfs = await self.storage.get_project_vfs(self.current_project_id)

        # Create directories
        await vfs.mkdir("/src")
        await vfs.mkdir("/src/components")

        # Copy template files
        template_dir = Path(__file__).parent.parent.parent.parent / "remotion-templates"

        # Copy package.json
        await self._copy_template_async(
            vfs, template_dir / "package.json", "/package.json", {"project_name": name}
        )

        # Copy config files
        await self._copy_file_async(vfs, template_dir / "remotion.config.ts", "/remotion.config.ts")
        await self._copy_file_async(vfs, template_dir / "tsconfig.json", "/tsconfig.json")
        await self._copy_file_async(vfs, template_dir / ".gitignore", "/.gitignore")

        # Copy source files
        composition_id = name.replace("_", "-")

        await self._copy_template_async(
            vfs,
            template_dir / "src" / "Root.tsx",
            "/src/Root.tsx",
            {
                "composition_id": composition_id,
                "duration_in_frames": 300,
                "fps": fps,
                "width": width,
                "height": height,
                "theme": theme,
            },
        )

        await self._copy_file_async(vfs, template_dir / "src" / "index.ts", "/src/index.ts")

        logger.info(f"Created project: {name} ({project_info.namespace_info.namespace_id})")

        return project_info

    async def _copy_file_async(self, vfs, src: Path, dest: str) -> None:
        """Copy a file to VFS."""
        if not src.exists():
            await vfs.write_file(dest, b"")
            return

        content = src.read_bytes()
        await vfs.write_file(dest, content)

    async def _copy_template_async(
        self, vfs, src: Path, dest: str, variables: dict[str, Any]
    ) -> None:
        """Copy a template file and replace variables."""
        if not src.exists():
            await vfs.write_file(dest, b"")
            return

        content = src.read_text()
        template = Template(
            content,
            variable_start_string="[[",
            variable_end_string="]]",
            block_start_string="[%",
            block_end_string="%]",
        )
        rendered = template.render(**variables)
        await vfs.write_file(dest, rendered.encode())

    async def add_component_to_project(
        self, component_type: str, config: dict, theme: str = "tech"
    ) -> str:
        """
        Generate and add a component to the current project.

        Args:
            component_type: Type of component
            config: Component configuration
            theme: Theme to use

        Returns:
            Path to generated component file
        """
        if not self.current_project_id:
            raise ValueError("No active project. Create a project first.")

        # Generate component code
        tsx_code = self.component_builder.build_component(component_type, config, theme)

        # Write component file
        vfs = await self.storage.get_project_vfs(self.current_project_id)
        component_path = f"/src/components/{component_type}.tsx"
        await vfs.write_file(component_path, tsx_code.encode())

        return component_path

    async def generate_composition(self) -> str:
        """
        Generate the complete video composition from the timeline.

        Returns:
            Path to generated VideoComposition.tsx file
        """
        if not self.current_project_id:
            raise ValueError("No active project")

        # Support both Timeline and CompositionBuilder
        if (
            self.current_composition
            and hasattr(self.current_composition, "components")
            and self.current_composition.components
        ):
            builder = self.current_composition
        elif self.current_timeline:
            builder = self.current_timeline
        else:
            raise ValueError("No timeline or composition created")

        composition_tsx = builder.generate_composition_tsx()
        duration_frames = builder.get_total_duration_frames()

        # Ensure minimum duration
        if duration_frames == 0:
            duration_frames = 300

        fps = builder.fps
        width = builder.width
        height = builder.height
        theme = getattr(builder, "theme", "tech")

        # Get VFS
        vfs = await self.storage.get_project_vfs(self.current_project_id)

        # Generate component TSX files
        if hasattr(builder, "get_all_components"):
            all_components = builder.get_all_components()
            component_types = self._find_all_component_types_recursive(all_components)
        elif hasattr(builder, "components"):
            component_types = builder._find_all_component_types(builder.components)  # type: ignore
        else:
            component_types = set()

        for component_type in component_types:
            try:
                tsx_code = self.component_builder.build_component(component_type, {}, theme)
                component_path = f"/src/components/{component_type}.tsx"
                await vfs.write_file(component_path, tsx_code.encode())
                logger.debug(f"Generated {component_type}.tsx")
            except Exception as e:
                logger.warning(f"Could not generate {component_type}: {e}")

        # Write composition file
        await vfs.write_file("/src/VideoComposition.tsx", composition_tsx.encode())

        # Get current project info
        project_info = await self.storage.get_project(self.current_project_id)

        # Update Root.tsx
        composition_id = project_info.metadata.project_name.replace("_", "-")
        template_dir = Path(__file__).parent.parent.parent.parent / "remotion-templates"

        await self._copy_template_async(
            vfs,
            template_dir / "src" / "Root.tsx",
            "/src/Root.tsx",
            {
                "composition_id": composition_id,
                "duration_in_frames": duration_frames,
                "fps": fps,
                "width": width,
                "height": height,
                "theme": theme,
            },
        )

        # Update project metadata with duration and component count
        metadata = project_info.metadata
        metadata.total_duration_seconds = duration_frames / fps
        metadata.component_count = len(component_types)
        await self.storage.update_project_metadata(self.current_project_id, metadata)

        return "/src/VideoComposition.tsx"

    def _find_all_component_types_recursive(self, components: list) -> set:
        """Recursively find all component types including nested children."""
        types = set()

        def collect_types(comp):
            types.add(comp.component_type)

            for _key, value in comp.props.items():
                if isinstance(value, ComponentInstance):
                    collect_types(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, ComponentInstance):
                            collect_types(item)

        for comp in components:
            collect_types(comp)

        return types

    async def get_project_info(self) -> dict:
        """Get information about the current project."""
        if not self.current_project_id:
            return {"error": "No active project"}

        if not self.current_timeline:
            return {"error": "No timeline"}

        project_info = await self.storage.get_project(self.current_project_id)

        return {
            "name": project_info.metadata.project_name,
            "namespace_id": self.current_project_id,
            "composition": self.current_timeline.to_dict(),
        }

    async def list_projects(
        self, scope: StorageScope | None = None, user_id: str | None = None
    ) -> list[ProjectInfo]:
        """List all projects."""
        return await self.storage.list_projects(scope=scope, user_id=user_id)

    async def create_checkpoint(self, name: str, description: str | None = None):
        """Create a checkpoint of the current project."""
        if not self.current_project_id:
            raise ValueError("No active project")

        return await self.storage.create_checkpoint(
            self.current_project_id, name=name, description=description
        )

    async def restore_checkpoint(self, checkpoint_id: str) -> None:
        """Restore the current project from a checkpoint."""
        if not self.current_project_id:
            raise ValueError("No active project")

        await self.storage.restore_checkpoint(self.current_project_id, checkpoint_id)
