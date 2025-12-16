"""Tests for RemotionProjectExporter."""

import json
import tempfile
from pathlib import Path

from chuk_motion.generator.composition_builder import ComponentInstance, CompositionBuilder
from chuk_motion.render.project_exporter import RemotionProjectExporter


class TestRemotionProjectExporterInitialization:
    """Test RemotionProjectExporter initialization."""

    def test_initialization(self):
        """Test exporter initialization."""
        builder = CompositionBuilder()
        exporter = RemotionProjectExporter(builder, "test_project")

        assert exporter.builder == builder
        assert exporter.project_name == "test_project"
        assert exporter.composition_id == "test-project"

    def test_composition_id_sanitization(self):
        """Test that composition ID replaces underscores with dashes."""
        builder = CompositionBuilder()
        exporter = RemotionProjectExporter(builder, "my_test_project_name")

        assert exporter.composition_id == "my-test-project-name"


class TestRemotionProjectExporterExport:
    """Test export functionality."""

    def test_export_creates_directory_structure(self):
        """Test that export creates required directories."""
        builder = CompositionBuilder(fps=30, width=1920, height=1080)

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "project"
            exporter = RemotionProjectExporter(builder, "test")

            exporter.export_to_directory(output_dir)

            # Check directories
            assert output_dir.exists()
            assert (output_dir / "src").exists()
            assert (output_dir / "src" / "components").exists()

    def test_export_creates_package_json(self):
        """Test that export creates package.json."""
        builder = CompositionBuilder()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "project"
            exporter = RemotionProjectExporter(builder, "test_project")

            exporter.export_to_directory(output_dir)

            package_json_path = output_dir / "package.json"
            assert package_json_path.exists()

            with open(package_json_path) as f:
                package_json = json.load(f)

            assert package_json["name"] == "test_project"
            assert "remotion" in package_json["dependencies"]
            assert "react" in package_json["dependencies"]

    def test_export_creates_tsconfig(self):
        """Test that export creates tsconfig.json."""
        builder = CompositionBuilder()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "project"
            exporter = RemotionProjectExporter(builder, "test")

            exporter.export_to_directory(output_dir)

            tsconfig_path = output_dir / "tsconfig.json"
            assert tsconfig_path.exists()

            with open(tsconfig_path) as f:
                tsconfig = json.load(f)

            assert "compilerOptions" in tsconfig
            assert tsconfig["compilerOptions"]["jsx"] == "react-jsx"

    def test_export_creates_remotion_config(self):
        """Test that export creates remotion.config.ts."""
        builder = CompositionBuilder()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "project"
            exporter = RemotionProjectExporter(builder, "test")

            exporter.export_to_directory(output_dir)

            config_path = output_dir / "remotion.config.ts"
            assert config_path.exists()

            content = config_path.read_text()
            assert "Config" in content
            assert "setVideoImageFormat" in content

    def test_export_creates_gitignore(self):
        """Test that export creates .gitignore."""
        builder = CompositionBuilder()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "project"
            exporter = RemotionProjectExporter(builder, "test")

            exporter.export_to_directory(output_dir)

            gitignore_path = output_dir / ".gitignore"
            assert gitignore_path.exists()

            content = gitignore_path.read_text()
            assert "node_modules" in content

    def test_export_creates_video_composition_tsx(self):
        """Test that export creates VideoComposition.tsx."""
        builder = CompositionBuilder()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "project"
            exporter = RemotionProjectExporter(builder, "test")

            exporter.export_to_directory(output_dir)

            tsx_path = output_dir / "src" / "VideoComposition.tsx"
            assert tsx_path.exists()

            content = tsx_path.read_text()
            assert "VideoComposition" in content
            assert "React" in content

    def test_export_creates_root_tsx(self):
        """Test that export creates Root.tsx."""
        builder = CompositionBuilder(fps=30, width=1920, height=1080)
        builder.theme = "tech"
        builder.components.append(
            ComponentInstance(
                component_type="TitleScene",
                start_frame=0,
                duration_frames=90,
            )
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "project"
            exporter = RemotionProjectExporter(builder, "test")

            exporter.export_to_directory(output_dir)

            root_tsx_path = output_dir / "src" / "Root.tsx"
            assert root_tsx_path.exists()

            content = root_tsx_path.read_text()
            assert "RemotionRoot" in content
            assert "Composition" in content
            assert 'id="test"' in content
            assert "durationInFrames={90}" in content
            assert "fps={30}" in content
            assert "width={1920}" in content
            assert "height={1080}" in content
            assert "theme: 'tech'" in content

    def test_export_creates_index_ts(self):
        """Test that export creates index.ts."""
        builder = CompositionBuilder()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "project"
            exporter = RemotionProjectExporter(builder, "test")

            exporter.export_to_directory(output_dir)

            index_path = output_dir / "src" / "index.ts"
            assert index_path.exists()

            content = index_path.read_text()
            assert "registerRoot" in content
            assert "RemotionRoot" in content

    def test_export_returns_info(self):
        """Test that export returns project info."""
        builder = CompositionBuilder(fps=30, width=1920, height=1080)
        builder.components.append(
            ComponentInstance(
                component_type="TitleScene",
                start_frame=0,
                duration_frames=90,
            )
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "project"
            exporter = RemotionProjectExporter(builder, "test_project")

            result = exporter.export_to_directory(output_dir)

            assert result["project_dir"] == str(output_dir)
            assert result["composition_id"] == "test-project"
            assert result["total_frames"] == 90
            assert result["fps"] == 30
            assert result["width"] == 1920
            assert result["height"] == 1080


class TestRemotionProjectExporterPrivateMethods:
    """Test private methods of RemotionProjectExporter."""

    def test_write_package_json(self):
        """Test _write_package_json method."""
        builder = CompositionBuilder()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            exporter = RemotionProjectExporter(builder, "my_project")

            exporter._write_package_json(output_dir)

            package_json_path = output_dir / "package.json"
            assert package_json_path.exists()

            with open(package_json_path) as f:
                data = json.load(f)

            assert data["name"] == "my_project"
            assert "@remotion/cli" in data["dependencies"]
            assert "typescript" in data["devDependencies"]

    def test_write_tsconfig(self):
        """Test _write_tsconfig method."""
        builder = CompositionBuilder()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            exporter = RemotionProjectExporter(builder, "test")

            exporter._write_tsconfig(output_dir)

            tsconfig_path = output_dir / "tsconfig.json"
            assert tsconfig_path.exists()

            with open(tsconfig_path) as f:
                data = json.load(f)

            assert data["compilerOptions"]["target"] == "ES2022"
            assert data["compilerOptions"]["strict"] is True

    def test_write_remotion_config(self):
        """Test _write_remotion_config method."""
        builder = CompositionBuilder()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            exporter = RemotionProjectExporter(builder, "test")

            exporter._write_remotion_config(output_dir)

            config_path = output_dir / "remotion.config.ts"
            assert config_path.exists()

            content = config_path.read_text()
            assert "Config" in content
            assert "setOverwriteOutput" in content

    def test_write_root_tsx(self):
        """Test _write_root_tsx method."""
        builder = CompositionBuilder(fps=60, width=1280, height=720)
        builder.theme = "finance"
        builder.components.append(
            ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=120)
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = Path(temp_dir) / "src"
            src_dir.mkdir()
            exporter = RemotionProjectExporter(builder, "my_video")

            exporter._write_root_tsx(src_dir)

            root_tsx_path = src_dir / "Root.tsx"
            assert root_tsx_path.exists()

            content = root_tsx_path.read_text()
            assert "my-video" in content  # composition_id
            assert "durationInFrames={120}" in content
            assert "fps={60}" in content
            assert "width={1280}" in content
            assert "height={720}" in content
            assert "theme: 'finance'" in content

    def test_generate_component_files(self):
        """Test _generate_component_files method."""
        builder = CompositionBuilder()
        builder.theme = "tech"
        builder.components.append(
            ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90)
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            components_dir = Path(temp_dir)
            exporter = RemotionProjectExporter(builder, "test")

            exporter._generate_component_files(components_dir)

            # TitleScene should be generated
            titlescene_path = components_dir / "TitleScene.tsx"
            assert titlescene_path.exists()


class TestRemotionProjectExporterWithComponents:
    """Test exporter with various component types."""

    def test_export_with_multiple_components(self):
        """Test export with multiple component types."""
        builder = CompositionBuilder()
        builder.components.extend(
            [
                ComponentInstance(component_type="TitleScene", start_frame=0, duration_frames=90),
                ComponentInstance(component_type="LowerThird", start_frame=90, duration_frames=60),
            ]
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "project"
            exporter = RemotionProjectExporter(builder, "test")

            result = exporter.export_to_directory(output_dir)

            # Check component files
            components_dir = output_dir / "src" / "components"
            assert (components_dir / "TitleScene.tsx").exists()
            assert (components_dir / "LowerThird.tsx").exists()

            # Check total frames
            assert result["total_frames"] == 150  # 90 + 60

    def test_export_empty_composition(self):
        """Test export with empty composition."""
        builder = CompositionBuilder()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "project"
            exporter = RemotionProjectExporter(builder, "test")

            result = exporter.export_to_directory(output_dir)

            assert result["total_frames"] == 0
