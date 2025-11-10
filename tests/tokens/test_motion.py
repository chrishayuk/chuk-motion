# tests/tokens/test_motion.py
"""
Comprehensive tests for motion token system.
"""

import pytest
from pydantic import ValidationError

from chuk_mcp_remotion.tokens.motion import (
    MOTION_TOKENS,
    CTATiming,
    DurationConfig,
    EasingConfig,
    EnterTransition,
    ExitTransition,
    MotionTokens,
    PlatformTimingConfig,
    RemotionSpringConfig,
    SpringConfig,
    TempoConfig,
    TransitionProperties,
    get_duration,
    get_easing,
    get_enter_transition,
    get_exit_transition,
    get_platform_timing,
    get_spring,
    get_tempo,
    list_durations,
    list_easings,
    list_enter_transitions,
    list_exit_transitions,
    list_platforms,
    list_springs,
    list_tempos,
)


class TestPydanticModels:
    """Test all Pydantic models are properly defined."""

    def test_duration_config_model(self):
        """Test DurationConfig model validation."""
        duration = DurationConfig(
            ms=350,
            frames_30fps=11,
            frames_60fps=21,
            seconds=0.35,
            css="0.35s",
            description="Test duration",
        )
        assert duration.ms == 350
        assert duration.frames_30fps == 11
        assert duration.seconds == 0.35

    def test_duration_config_validation_error(self):
        """Test DurationConfig validation fails with invalid data."""
        with pytest.raises(ValidationError):
            DurationConfig(ms="invalid", frames_30fps=11, frames_60fps=21)

    def test_easing_config_model(self):
        """Test EasingConfig model validation."""
        easing = EasingConfig(
            curve=[0.42, 0.0, 0.58, 1.0],
            css="ease-in-out",
            description="Test easing",
            usage="Test usage",
        )
        assert len(easing.curve) == 4
        assert easing.css == "ease-in-out"

    def test_remotion_spring_config_model(self):
        """Test RemotionSpringConfig model validation."""
        spring = RemotionSpringConfig(
            damping=100.0, mass=1.0, stiffness=100.0, overshootClamping=False
        )
        assert spring.damping == 100.0
        assert spring.mass == 1.0
        assert spring.stiffness == 100.0
        assert spring.overshootClamping is False

    def test_spring_config_model(self):
        """Test SpringConfig with nested RemotionSpringConfig."""
        config = RemotionSpringConfig(
            damping=50.0, mass=1.0, stiffness=120.0, overshootClamping=False
        )
        spring = SpringConfig(
            config=config,
            description="Smooth spring",
            feel="Natural",
            usage="General purpose",
        )
        assert spring.config.damping == 50.0
        assert spring.feel == "Natural"

    def test_transition_properties_model(self):
        """Test TransitionProperties with alias support."""
        props = TransitionProperties(**{"from": 0, "to": 1})
        assert props.from_value == 0
        assert props.to == 1

    def test_enter_transition_model(self):
        """Test EnterTransition model."""
        transition = EnterTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 0, "to": 1}),
            },
            description="Fade in",
            usage="Subtle entrances",
            default_duration="normal",
            default_easing="ease_out",
        )
        assert "opacity" in transition.properties
        assert transition.default_duration == "normal"

    def test_cta_timing_model(self):
        """Test CTATiming model."""
        cta = CTATiming(first_cta=5.0, final_cta=-3.0, mid_roll_cta=180.0)
        assert cta.first_cta == 5.0
        assert cta.final_cta == -3.0
        assert cta.mid_roll_cta == 180.0

    def test_cta_timing_optional_field(self):
        """Test CTATiming with optional mid_roll_cta."""
        cta = CTATiming(first_cta=5.0, final_cta=-3.0)
        assert cta.mid_roll_cta is None

    def test_platform_timing_config_model(self):
        """Test PlatformTimingConfig with CTATiming."""
        timing = PlatformTimingConfig(
            hook_duration=2.0,
            scene_change_interval=3.0,
            caption_display_duration=1.0,
            cta_timing=CTATiming(first_cta=5.0, final_cta=-3.0),
            attention_span="short",
            recommended_tempo="fast",
            description="Test timing",
        )
        assert timing.hook_duration == 2.0
        assert timing.cta_timing.first_cta == 5.0


class TestMotionTokensStructure:
    """Test MOTION_TOKENS structure and completeness."""

    def test_motion_tokens_is_pydantic_model(self):
        """Test that MOTION_TOKENS is a Pydantic model instance."""
        assert isinstance(MOTION_TOKENS, MotionTokens)

    def test_all_duration_tokens_present(self):
        """Test all expected duration tokens exist."""
        expected_durations = [
            "instant",
            "ultra_fast",
            "fast",
            "normal",
            "medium",
            "slow",
            "slower",
            "ultra_slow",
        ]
        for duration in expected_durations:
            assert duration in MOTION_TOKENS.duration, f"Duration '{duration}' not found"
            assert isinstance(MOTION_TOKENS.duration[duration], DurationConfig)

    def test_duration_frame_calculations(self):
        """Test duration frame calculations are correct."""
        normal = MOTION_TOKENS.duration["normal"]
        assert normal.ms == 350
        assert normal.frames_30fps == 11  # 350ms / 33.33ms per frame ≈ 11
        assert normal.frames_60fps == 21  # 350ms / 16.67ms per frame ≈ 21
        assert normal.seconds == 0.35

    def test_all_easing_tokens_present(self):
        """Test all expected easing tokens exist."""
        expected_easings = [
            "linear",
            "ease_in_out",
            "ease_out",
            "ease_in",
            "ease_out_back",
            "ease_out_expo",
        ]
        for easing in expected_easings:
            assert easing in MOTION_TOKENS.easing, f"Easing '{easing}' not found"
            assert isinstance(MOTION_TOKENS.easing[easing], EasingConfig)

    def test_easing_curve_format(self):
        """Test easing curves have correct format."""
        for easing_name, easing in MOTION_TOKENS.easing.items():
            assert len(easing.curve) == 4, f"Easing '{easing_name}' curve should have 4 values"
            assert all(isinstance(v, (int, float)) for v in easing.curve), (
                f"Easing '{easing_name}' curve values should be numeric"
            )

    def test_all_spring_configs_present(self):
        """Test all expected spring configs exist."""
        expected_springs = ["gentle", "smooth", "bouncy", "snappy", "wobbly", "stiff", "explosive"]
        for spring in expected_springs:
            assert spring in MOTION_TOKENS.spring_configs, f"Spring '{spring}' not found"
            assert isinstance(MOTION_TOKENS.spring_configs[spring], SpringConfig)

    def test_spring_config_structure(self):
        """Test spring configs have proper structure."""
        smooth = MOTION_TOKENS.spring_configs["smooth"]
        assert isinstance(smooth.config, RemotionSpringConfig)
        assert smooth.config.damping > 0
        assert smooth.config.mass > 0
        assert smooth.config.stiffness > 0
        assert isinstance(smooth.config.overshootClamping, bool)

    def test_all_enter_transitions_present(self):
        """Test all expected enter transitions exist."""
        expected_enters = [
            "fade_in",
            "fade_up",
            "fade_down",
            "scale_in",
            "zoom_in",
            "slide_in_left",
            "slide_in_right",
            "bounce_in",
            "rotate_in",
            "blur_in",
        ]
        for enter in expected_enters:
            assert enter in MOTION_TOKENS.enter, f"Enter transition '{enter}' not found"
            assert isinstance(MOTION_TOKENS.enter[enter], EnterTransition)

    def test_all_exit_transitions_present(self):
        """Test all expected exit transitions exist."""
        expected_exits = [
            "fade_out",
            "fade_out_down",
            "fade_out_up",
            "scale_out",
            "zoom_out",
            "slide_out_left",
            "slide_out_right",
            "blur_out",
        ]
        for exit_trans in expected_exits:
            assert exit_trans in MOTION_TOKENS.exit, f"Exit transition '{exit_trans}' not found"
            assert isinstance(MOTION_TOKENS.exit[exit_trans], ExitTransition)

    def test_all_tempo_tokens_present(self):
        """Test all expected tempo tokens exist."""
        expected_tempos = ["sprint", "fast", "medium", "slow", "cinematic"]
        for tempo in expected_tempos:
            assert tempo in MOTION_TOKENS.tempo, f"Tempo '{tempo}' not found"
            assert isinstance(MOTION_TOKENS.tempo[tempo], TempoConfig)

    def test_tempo_beat_calculations(self):
        """Test tempo beat calculations are consistent."""
        for tempo_name, tempo in MOTION_TOKENS.tempo.items():
            # Verify frame calculations match beat duration
            expected_30fps = int(tempo.beat_duration * 30)
            expected_60fps = int(tempo.beat_duration * 60)
            assert tempo.frames_30fps == expected_30fps, (
                f"Tempo '{tempo_name}' 30fps frames mismatch"
            )
            assert tempo.frames_60fps == expected_60fps, (
                f"Tempo '{tempo_name}' 60fps frames mismatch"
            )

    def test_all_platform_timings_present(self):
        """Test all expected platform timings exist."""
        expected_platforms = [
            "tiktok",
            "youtube_shorts",
            "instagram_reel",
            "youtube_long_form",
            "linkedin",
            "presentation",
        ]
        for platform in expected_platforms:
            assert platform in MOTION_TOKENS.platform_timing, f"Platform '{platform}' not found"
            assert isinstance(MOTION_TOKENS.platform_timing[platform], PlatformTimingConfig)

    def test_platform_timing_cta_structure(self):
        """Test platform timing CTA timing is properly structured."""
        for platform, timing in MOTION_TOKENS.platform_timing.items():
            assert isinstance(timing.cta_timing, CTATiming)
            assert timing.cta_timing.first_cta > 0, (
                f"Platform '{platform}' first_cta should be positive"
            )
            assert timing.cta_timing.final_cta < 0, (
                f"Platform '{platform}' final_cta should be negative"
            )


class TestUtilityFunctions:
    """Test all utility functions."""

    def test_get_duration(self):
        """Test get_duration utility function."""
        duration = get_duration("normal")
        assert isinstance(duration, DurationConfig)
        assert duration.ms == 350

    def test_get_duration_fallback(self):
        """Test get_duration falls back to 'normal' for unknown durations."""
        duration = get_duration("unknown_duration")
        assert duration.ms == 350  # Should return 'normal'

    def test_get_easing(self):
        """Test get_easing utility function."""
        easing = get_easing("ease_out")
        assert isinstance(easing, EasingConfig)
        assert easing.css == "ease-out"

    def test_get_easing_fallback(self):
        """Test get_easing falls back to 'ease_out' for unknown easings."""
        easing = get_easing("unknown_easing")
        assert easing.css == "ease-out"

    def test_get_spring(self):
        """Test get_spring utility function."""
        spring = get_spring("smooth")
        assert isinstance(spring, SpringConfig)
        assert spring.config.damping == 50

    def test_get_spring_fallback(self):
        """Test get_spring falls back to 'smooth' for unknown springs."""
        spring = get_spring("unknown_spring")
        assert spring.config.damping == 50

    def test_get_enter_transition(self):
        """Test get_enter_transition utility function."""
        transition = get_enter_transition("fade_in")
        assert isinstance(transition, EnterTransition)
        assert "opacity" in transition.properties

    def test_get_exit_transition(self):
        """Test get_exit_transition utility function."""
        transition = get_exit_transition("fade_out")
        assert isinstance(transition, ExitTransition)
        assert "opacity" in transition.properties

    def test_get_tempo(self):
        """Test get_tempo utility function."""
        tempo = get_tempo("medium")
        assert isinstance(tempo, TempoConfig)
        assert tempo.beat_duration == 2.0

    def test_get_platform_timing(self):
        """Test get_platform_timing utility function."""
        timing = get_platform_timing("tiktok")
        assert isinstance(timing, PlatformTimingConfig)
        assert timing.attention_span == "ultra_short"

    def test_list_durations(self):
        """Test list_durations returns all duration names."""
        durations = list_durations()
        assert isinstance(durations, list)
        assert "normal" in durations
        assert "fast" in durations
        assert len(durations) == 8

    def test_list_easings(self):
        """Test list_easings returns all easing names."""
        easings = list_easings()
        assert isinstance(easings, list)
        assert "ease_out" in easings
        assert len(easings) >= 10

    def test_list_springs(self):
        """Test list_springs returns all spring config names."""
        springs = list_springs()
        assert isinstance(springs, list)
        assert "smooth" in springs
        assert len(springs) == 7

    def test_list_enter_transitions(self):
        """Test list_enter_transitions returns all enter transition names."""
        enters = list_enter_transitions()
        assert isinstance(enters, list)
        assert "fade_in" in enters
        assert len(enters) == 10

    def test_list_exit_transitions(self):
        """Test list_exit_transitions returns all exit transition names."""
        exits = list_exit_transitions()
        assert isinstance(exits, list)
        assert "fade_out" in exits
        assert len(exits) == 8

    def test_list_tempos(self):
        """Test list_tempos returns all tempo names."""
        tempos = list_tempos()
        assert isinstance(tempos, list)
        assert "medium" in tempos
        assert len(tempos) == 5

    def test_list_platforms(self):
        """Test list_platforms returns all platform names."""
        platforms = list_platforms()
        assert isinstance(platforms, list)
        assert "tiktok" in platforms
        assert "youtube_long_form" in platforms
        assert len(platforms) == 6


class TestTokenConsistency:
    """Test consistency across motion tokens."""

    def test_transition_durations_reference_valid_tokens(self):
        """Test that transitions reference valid duration tokens."""
        for enter_name, enter in MOTION_TOKENS.enter.items():
            assert enter.default_duration in MOTION_TOKENS.duration, (
                f"Enter '{enter_name}' references invalid duration '{enter.default_duration}'"
            )

        for exit_name, exit_trans in MOTION_TOKENS.exit.items():
            assert exit_trans.default_duration in MOTION_TOKENS.duration, (
                f"Exit '{exit_name}' references invalid duration '{exit_trans.default_duration}'"
            )

    def test_transition_easings_reference_valid_tokens(self):
        """Test that transitions reference valid easing tokens."""
        for enter_name, enter in MOTION_TOKENS.enter.items():
            assert enter.default_easing in MOTION_TOKENS.easing, (
                f"Enter '{enter_name}' references invalid easing '{enter.default_easing}'"
            )

        for exit_name, exit_trans in MOTION_TOKENS.exit.items():
            assert exit_trans.default_easing in MOTION_TOKENS.easing, (
                f"Exit '{exit_name}' references invalid easing '{exit_trans.default_easing}'"
            )

    def test_platform_tempo_references_valid_tokens(self):
        """Test that platform timings reference valid tempo tokens."""
        for platform, timing in MOTION_TOKENS.platform_timing.items():
            assert timing.recommended_tempo in MOTION_TOKENS.tempo, (
                f"Platform '{platform}' references invalid tempo '{timing.recommended_tempo}'"
            )

    def test_tempo_progression(self):
        """Test that tempos have logical progression."""
        sprint = MOTION_TOKENS.tempo["sprint"]
        fast = MOTION_TOKENS.tempo["fast"]
        medium = MOTION_TOKENS.tempo["medium"]
        slow = MOTION_TOKENS.tempo["slow"]
        cinematic = MOTION_TOKENS.tempo["cinematic"]

        # Beat durations should increase
        assert sprint.beat_duration < fast.beat_duration
        assert fast.beat_duration < medium.beat_duration
        assert medium.beat_duration < slow.beat_duration
        assert slow.beat_duration < cinematic.beat_duration

        # Cuts per minute should decrease
        assert sprint.cuts_per_minute > fast.cuts_per_minute
        assert fast.cuts_per_minute > medium.cuts_per_minute
        assert medium.cuts_per_minute > slow.cuts_per_minute
