# chuk-motion/tests/components/test_base.py
"""Tests for base component models."""

from pathlib import Path

import pytest
from pydantic import ValidationError


class TestComponentMetadata:
    """Tests for ComponentMetadata model."""

    def test_component_metadata_creation(self):
        """Test creating ComponentMetadata instance."""
        from chuk_motion.components.base import ComponentMetadata

        metadata = ComponentMetadata(
            name="TestComponent", description="A test component", category="test"
        )

        assert metadata.name == "TestComponent"
        assert metadata.description == "A test component"
        assert metadata.category == "test"

    def test_component_metadata_forbids_extra_fields(self):
        """Test that ComponentMetadata rejects extra fields."""
        from chuk_motion.components.base import ComponentMetadata

        with pytest.raises(ValidationError):
            ComponentMetadata(
                name="Test", description="Test", category="test", extra_field="not allowed"
            )


class TestComponentInfo:
    """Tests for ComponentInfo model."""

    def test_component_info_basic(self):
        """Test creating ComponentInfo with minimal fields."""
        from chuk_motion.components.base import ComponentInfo, ComponentMetadata

        metadata = ComponentMetadata(name="TestComponent", description="Test", category="test")

        info = ComponentInfo(metadata=metadata)

        assert info.metadata == metadata
        assert info.template_path is None
        assert info.register_tool is None
        assert info.add_to_composition is None
        assert info.directory_name is None

    def test_component_info_all_fields(self):
        """Test creating ComponentInfo with all fields."""
        from chuk_motion.components.base import ComponentInfo, ComponentMetadata

        metadata = ComponentMetadata(name="TestComponent", description="Test", category="test")

        def mock_register_tool():
            pass

        def mock_add_to_composition():
            pass

        template_path = Path("/tmp/template.tsx.j2")

        info = ComponentInfo(
            metadata=metadata,
            template_path=template_path,
            register_tool=mock_register_tool,
            add_to_composition=mock_add_to_composition,
            directory_name="overlays",
        )

        assert info.metadata == metadata
        assert info.template_path == template_path
        assert info.register_tool == mock_register_tool
        assert info.add_to_composition == mock_add_to_composition
        assert info.directory_name == "overlays"

    def test_component_info_name_property(self):
        """Test ComponentInfo.name property."""
        from chuk_motion.components.base import ComponentInfo, ComponentMetadata

        metadata = ComponentMetadata(name="MyComponent", description="Test", category="test")

        info = ComponentInfo(metadata=metadata)

        # Test the name property (line 37)
        assert info.name == "MyComponent"
        assert info.name == info.metadata.name

    def test_component_info_category_property(self):
        """Test ComponentInfo.category property."""
        from chuk_motion.components.base import ComponentInfo, ComponentMetadata

        metadata = ComponentMetadata(name="Test", description="Test", category="overlay")

        info = ComponentInfo(metadata=metadata)

        # Test the category property (line 42)
        assert info.category == "overlay"
        assert info.category == info.metadata.category

    def test_component_info_forbids_extra_fields(self):
        """Test that ComponentInfo rejects extra fields."""
        from chuk_motion.components.base import ComponentInfo, ComponentMetadata

        metadata = ComponentMetadata(name="Test", description="Test", category="test")

        with pytest.raises(ValidationError):
            ComponentInfo(metadata=metadata, extra_field="not allowed")
