# chuk-motion/tests/components/test_component_helpers.py
"""Tests for component helper functions."""


class TestParseNestedComponent:
    """Tests for parse_nested_component helper function."""

    def test_parse_none(self):
        """Test parsing None returns None."""
        from chuk_motion.components.component_helpers import parse_nested_component

        result = parse_nested_component(None)
        assert result is None

    def test_parse_non_dict(self):
        """Test parsing non-dict returns value as-is."""
        from chuk_motion.components.component_helpers import parse_nested_component

        result = parse_nested_component("some string")
        assert result == "some string"

        result = parse_nested_component(42)
        assert result == 42

    def test_parse_dict_without_type(self):
        """Test parsing dict without 'type' key returns dict as-is."""
        from chuk_motion.components.component_helpers import parse_nested_component

        test_dict = {"foo": "bar", "baz": 123}
        result = parse_nested_component(test_dict)
        assert result == test_dict

    def test_parse_simple_component(self):
        """Test parsing simple component dict."""
        from chuk_motion.components.component_helpers import parse_nested_component
        from chuk_motion.generator.composition_builder import ComponentInstance

        comp_dict = {"type": "TitleScene", "config": {"text": "Hello", "variant": "bold"}}

        result = parse_nested_component(comp_dict)
        assert isinstance(result, ComponentInstance)
        assert result.component_type == "TitleScene"
        assert result.props["text"] == "Hello"
        assert result.props["variant"] == "bold"

    def test_parse_component_with_nested_component(self):
        """Test parsing component with nested component in config."""
        from chuk_motion.components.component_helpers import parse_nested_component
        from chuk_motion.generator.composition_builder import ComponentInstance

        comp_dict = {
            "type": "Container",
            "config": {"content": {"type": "TitleScene", "config": {"text": "Nested"}}},
        }

        result = parse_nested_component(comp_dict)
        assert isinstance(result, ComponentInstance)
        assert result.component_type == "Container"
        assert isinstance(result.props["content"], ComponentInstance)
        assert result.props["content"].component_type == "TitleScene"
        assert result.props["content"].props["text"] == "Nested"

    def test_parse_component_with_array_of_components(self):
        """Test parsing component with array of nested components."""
        from chuk_motion.components.component_helpers import parse_nested_component
        from chuk_motion.generator.composition_builder import ComponentInstance

        comp_dict = {
            "type": "Grid",
            "config": {
                "items": [
                    {"type": "TitleScene", "config": {"text": "Item 1"}},
                    {"type": "TitleScene", "config": {"text": "Item 2"}},
                ]
            },
        }

        result = parse_nested_component(comp_dict)
        assert isinstance(result, ComponentInstance)
        assert result.component_type == "Grid"
        assert isinstance(result.props["items"], list)
        assert len(result.props["items"]) == 2
        assert isinstance(result.props["items"][0], ComponentInstance)
        assert result.props["items"][0].props["text"] == "Item 1"
        assert isinstance(result.props["items"][1], ComponentInstance)
        assert result.props["items"][1].props["text"] == "Item 2"

    def test_parse_component_with_mixed_array(self):
        """Test parsing component with array containing both components and non-components."""
        from chuk_motion.components.component_helpers import parse_nested_component
        from chuk_motion.generator.composition_builder import ComponentInstance

        comp_dict = {
            "type": "Custom",
            "config": {
                "items": [
                    {"type": "TitleScene", "config": {"text": "Component"}},
                    "plain string",
                    42,
                    {"not": "a component"},
                ]
            },
        }

        result = parse_nested_component(comp_dict)
        assert isinstance(result, ComponentInstance)
        items = result.props["items"]
        assert len(items) == 4
        assert isinstance(items[0], ComponentInstance)
        assert items[1] == "plain string"
        assert items[2] == 42
        assert items[3] == {"not": "a component"}

    def test_parse_component_without_config(self):
        """Test parsing component with missing config key."""
        from chuk_motion.components.component_helpers import parse_nested_component
        from chuk_motion.generator.composition_builder import ComponentInstance

        comp_dict = {"type": "TitleScene"}

        result = parse_nested_component(comp_dict)
        assert isinstance(result, ComponentInstance)
        assert result.component_type == "TitleScene"
        assert result.props == {}
