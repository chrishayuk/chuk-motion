# chuk-mcp-remotion/src/chuk_mcp_remotion/tokens/motion.py
"""
Motion token system for Remotion video design system.

Comprehensive motion system including:
- Duration tokens (instant to ultra_slow with frame conversions)
- Easing curves (15+ cubic bezier presets)
- Spring configurations (gentle to explosive)
- Enter/exit transitions (fade, slide, scale, etc.)
- Tempo/rhythm tokens (sprint to cinematic)
- Platform-specific timing (hook durations, scene change intervals)

Critical for consistent, platform-optimized motion design across components.
"""

from typing import Any
from pydantic import BaseModel, Field


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class DurationConfig(BaseModel):
    """Duration configuration with multiple time representations."""
    ms: int = Field(..., description="Duration in milliseconds")
    frames_30fps: int = Field(..., description="Duration in frames at 30 FPS")
    frames_60fps: int = Field(..., description="Duration in frames at 60 FPS")
    seconds: float = Field(..., description="Duration in seconds")
    css: str = Field(..., description="CSS-compatible duration string")
    description: str = Field(..., description="Human-readable description")


class EasingConfig(BaseModel):
    """Easing curve configuration."""
    curve: list[float] = Field(..., description="Cubic bezier curve [x1, y1, x2, y2]")
    css: str = Field(..., description="CSS-compatible easing function")
    description: str = Field(..., description="Human-readable description")
    usage: str = Field(..., description="When to use this easing")


class RemotionSpringConfig(BaseModel):
    """Remotion spring physics configuration."""
    damping: float = Field(..., description="Damping coefficient")
    mass: float = Field(..., description="Mass of the spring")
    stiffness: float = Field(..., description="Stiffness of the spring")
    overshootClamping: bool = Field(..., description="Whether to clamp overshoot")


class SpringConfig(BaseModel):
    """Spring animation configuration."""
    config: RemotionSpringConfig = Field(..., description="Remotion spring config")
    description: str = Field(..., description="Human-readable description")
    feel: str = Field(..., description="How the animation feels")
    usage: str = Field(..., description="When to use this spring")


class TransitionProperties(BaseModel):
    """Properties for a transition animation."""
    from_value: Any = Field(..., alias="from", description="Starting value")
    to: Any = Field(..., description="Ending value")

    class Config:
        populate_by_name = True


class EnterTransition(BaseModel):
    """Enter transition configuration."""
    properties: dict[str, TransitionProperties] = Field(..., description="Animated properties")
    description: str = Field(..., description="Human-readable description")
    usage: str = Field(..., description="When to use this transition")
    default_duration: str = Field(..., description="Recommended duration token")
    default_easing: str = Field(..., description="Recommended easing token")


class ExitTransition(BaseModel):
    """Exit transition configuration."""
    properties: dict[str, TransitionProperties] = Field(..., description="Animated properties")
    description: str = Field(..., description="Human-readable description")
    usage: str = Field(..., description="When to use this transition")
    default_duration: str = Field(..., description="Recommended duration token")
    default_easing: str = Field(..., description="Recommended easing token")


class TempoConfig(BaseModel):
    """Tempo/rhythm configuration for narrative pacing."""
    beat_duration: float = Field(..., description="Duration of one 'beat' in seconds")
    frames_30fps: int = Field(..., description="Frames per beat at 30 FPS")
    frames_60fps: int = Field(..., description="Frames per beat at 60 FPS")
    caption_duration: float = Field(..., description="Recommended caption display duration")
    scene_change_interval: float = Field(..., description="Recommended scene change interval")
    cuts_per_minute: int = Field(..., description="Average cuts per minute")
    description: str = Field(..., description="Human-readable description")
    feel: str = Field(..., description="How the pacing feels")
    usage: str = Field(..., description="When to use this tempo")


class CTATiming(BaseModel):
    """Call-to-action timing configuration."""
    first_cta: float = Field(..., description="Time for first CTA in seconds")
    final_cta: float = Field(..., description="Time for final CTA (negative = from end)")
    mid_roll_cta: float | None = Field(None, description="Optional mid-roll CTA timing")


class PlatformTimingConfig(BaseModel):
    """Platform-specific timing configuration."""
    hook_duration: float = Field(..., description="Duration of opening hook in seconds")
    scene_change_interval: float = Field(..., description="Average scene change interval")
    caption_display_duration: float = Field(..., description="Recommended caption duration")
    cta_timing: CTATiming = Field(..., description="Call-to-action timing")
    attention_span: str = Field(..., description="Platform attention span characteristic")
    recommended_tempo: str = Field(..., description="Recommended tempo token")
    description: str = Field(..., description="Human-readable description")


class MotionTokens(BaseModel):
    """Complete motion token system."""
    duration: dict[str, DurationConfig]
    easing: dict[str, EasingConfig]
    spring_configs: dict[str, SpringConfig]
    enter: dict[str, EnterTransition]
    exit: dict[str, ExitTransition]
    tempo: dict[str, TempoConfig]
    platform_timing: dict[str, PlatformTimingConfig]


# ============================================================================
# MOTION TOKENS DATA
# ============================================================================

MOTION_TOKENS = MotionTokens(
    # ============================================================================
    # DURATION TOKENS
    # ============================================================================
    duration={
        "instant": DurationConfig(
            ms=0,
            frames_30fps=0,
            frames_60fps=0,
            seconds=0.0,
            css="0s",
            description="Instant (no animation)",
        ),
        "ultra_fast": DurationConfig(
            ms=100,
            frames_30fps=3,
            frames_60fps=6,
            seconds=0.1,
            css="0.1s",
            description="Ultra fast motion",
        ),
        "fast": DurationConfig(
            ms=200,
            frames_30fps=6,
            frames_60fps=12,
            seconds=0.2,
            css="0.2s",
            description="Fast motion",
        ),
        "normal": DurationConfig(
            ms=350,
            frames_30fps=11,
            frames_60fps=21,
            seconds=0.35,
            css="0.35s",
            description="Normal motion (default)",
        ),
        "medium": DurationConfig(
            ms=500,
            frames_30fps=15,
            frames_60fps=30,
            seconds=0.5,
            css="0.5s",
            description="Medium motion",
        ),
        "slow": DurationConfig(
            ms=700,
            frames_30fps=21,
            frames_60fps=42,
            seconds=0.7,
            css="0.7s",
            description="Slow motion",
        ),
        "slower": DurationConfig(
            ms=1000,
            frames_30fps=30,
            frames_60fps=60,
            seconds=1.0,
            css="1.0s",
            description="Slower motion",
        ),
        "ultra_slow": DurationConfig(
            ms=1500,
            frames_30fps=45,
            frames_60fps=90,
            seconds=1.5,
            css="1.5s",
            description="Ultra slow motion",
        ),
    },
    # ============================================================================
    # EASING CURVES
    # ============================================================================
    easing={
        "linear": EasingConfig(
            curve=[0.0, 0.0, 1.0, 1.0],
            css="linear",
            description="No easing, constant speed",
            usage="Use for continuous loops, loading spinners",
        ),
        "ease_in_out": EasingConfig(
            curve=[0.42, 0.0, 0.58, 1.0],
            css="ease-in-out",
            description="Starts slow, accelerates, decelerates",
            usage="Default for most transitions",
        ),
        "ease_out": EasingConfig(
            curve=[0.0, 0.0, 0.58, 1.0],
            css="ease-out",
            description="Starts fast, decelerates",
            usage="Enter transitions, appearing elements",
        ),
        "ease_in": EasingConfig(
            curve=[0.42, 0.0, 1.0, 1.0],
            css="ease-in",
            description="Starts slow, accelerates",
            usage="Exit transitions, disappearing elements",
        ),
        "ease_out_back": EasingConfig(
            curve=[0.34, 1.56, 0.64, 1.0],
            css="cubic-bezier(0.34, 1.56, 0.64, 1)",
            description="Overshoots slightly then settles",
            usage="Playful entrances, bounce effects",
        ),
        "ease_out_expo": EasingConfig(
            curve=[0.16, 1.0, 0.3, 1.0],
            css="cubic-bezier(0.16, 1, 0.3, 1)",
            description="Exponential deceleration",
            usage="Snappy UI responses, quick slides",
        ),
        "ease_out_quint": EasingConfig(
            curve=[0.22, 1.0, 0.36, 1.0],
            css="cubic-bezier(0.22, 1, 0.36, 1)",
            description="Smooth, elegant deceleration",
            usage="Refined transitions, elegant slides",
        ),
        "ease_out_cubic": EasingConfig(
            curve=[0.33, 1.0, 0.68, 1.0],
            css="cubic-bezier(0.33, 1, 0.68, 1)",
            description="Moderate deceleration",
            usage="General purpose, balanced feel",
        ),
        "ease_in_cubic": EasingConfig(
            curve=[0.32, 0.0, 0.67, 0.0],
            css="cubic-bezier(0.32, 0, 0.67, 0)",
            description="Moderate acceleration",
            usage="Exit animations, dismissals",
        ),
        "ease_in_out_quart": EasingConfig(
            curve=[0.76, 0.0, 0.24, 1.0],
            css="cubic-bezier(0.76, 0, 0.24, 1)",
            description="Strong acceleration and deceleration",
            usage="Dramatic transitions, scene changes",
        ),
        "ease_in_out_back": EasingConfig(
            curve=[0.68, -0.55, 0.27, 1.55],
            css="cubic-bezier(0.68, -0.55, 0.27, 1.55)",
            description="Anticipates before moving, overshoots",
            usage="Playful, energetic transitions",
        ),
        "ease_out_circ": EasingConfig(
            curve=[0.08, 0.82, 0.17, 1.0],
            css="cubic-bezier(0.08, 0.82, 0.17, 1)",
            description="Circular deceleration",
            usage="Smooth, rounded motion",
        ),
        "bounce": EasingConfig(
            curve=[0.68, -0.55, 0.27, 1.55],
            css="cubic-bezier(0.68, -0.55, 0.27, 1.55)",
            description="Bounces at the end",
            usage="Fun, playful emphasis",
        ),
        "elastic": EasingConfig(
            curve=[0.68, -0.55, 0.27, 1.55],
            css="cubic-bezier(0.68, -0.55, 0.27, 1.55)",
            description="Elastic spring effect",
            usage="Attention-grabbing, cartoonish",
        ),
        "anticipate": EasingConfig(
            curve=[0.68, -0.55, 0.27, 1.55],
            css="cubic-bezier(0.68, -0.55, 0.27, 1.55)",
            description="Pulls back before moving forward",
            usage="Dramatic reveals, scene transitions",
        ),
    },
    # ============================================================================
    # SPRING CONFIGURATIONS
    # ============================================================================
    spring_configs={
        "gentle": SpringConfig(
            config=RemotionSpringConfig(damping=100, mass=1.0, stiffness=100, overshootClamping=False),
            description="Smooth, gradual spring with minimal overshoot",
            feel="Calm, refined, elegant",
            usage="Subtle UI transitions, professional content",
        ),
        "smooth": SpringConfig(
            config=RemotionSpringConfig(damping=50, mass=1.0, stiffness=120, overshootClamping=False),
            description="Balanced spring animation (default)",
            feel="Natural, pleasant, general-purpose",
            usage="Most transitions, default choice",
        ),
        "bouncy": SpringConfig(
            config=RemotionSpringConfig(damping=30, mass=1.0, stiffness=150, overshootClamping=False),
            description="Playful spring with noticeable bounce",
            feel="Fun, energetic, playful",
            usage="Playful UI, creator content, emphasizing actions",
        ),
        "snappy": SpringConfig(
            config=RemotionSpringConfig(damping=80, mass=0.5, stiffness=200, overshootClamping=False),
            description="Quick, responsive spring",
            feel="Fast, responsive, modern",
            usage="UI responses, button presses, snappy interactions",
        ),
        "wobbly": SpringConfig(
            config=RemotionSpringConfig(damping=20, mass=1.2, stiffness=100, overshootClamping=False),
            description="Exaggerated wobble spring",
            feel="Cartoonish, attention-grabbing, silly",
            usage="Comedic emphasis, playful reveals",
        ),
        "stiff": SpringConfig(
            config=RemotionSpringConfig(damping=150, mass=1.0, stiffness=300, overshootClamping=True),
            description="Very stiff, minimal bounce",
            feel="Precise, controlled, mechanical",
            usage="Precise UI movements, technical content",
        ),
        "explosive": SpringConfig(
            config=RemotionSpringConfig(damping=10, mass=0.8, stiffness=250, overshootClamping=False),
            description="Dramatic, high-energy spring",
            feel="Explosive, dramatic, intense",
            usage="Hero moments, dramatic reveals, climactic scenes",
        ),
    },
    # ============================================================================
    # ENTER TRANSITIONS
    # ============================================================================
    enter={
        "fade_in": EnterTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 0, "to": 1}),
            },
            description="Simple fade in",
            usage="Subtle entrances, text, overlays",
            default_duration="normal",
            default_easing="ease_out",
        ),
        "fade_up": EnterTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 0, "to": 1}),
                "translateY": TransitionProperties(**{"from": 30, "to": 0}),
            },
            description="Fade in while sliding up",
            usage="Content blocks, cards, sections",
            default_duration="medium",
            default_easing="ease_out_expo",
        ),
        "fade_down": EnterTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 0, "to": 1}),
                "translateY": TransitionProperties(**{"from": -30, "to": 0}),
            },
            description="Fade in while sliding down",
            usage="Dropdown content, notifications",
            default_duration="medium",
            default_easing="ease_out_expo",
        ),
        "scale_in": EnterTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 0, "to": 1}),
                "scale": TransitionProperties(**{"from": 0.8, "to": 1}),
            },
            description="Fade in while scaling up",
            usage="Modals, popups, emphasis",
            default_duration="medium",
            default_easing="ease_out_back",
        ),
        "zoom_in": EnterTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 0, "to": 1}),
                "scale": TransitionProperties(**{"from": 0, "to": 1}),
            },
            description="Zoom from 0% to 100%",
            usage="Dramatic entrances, hero elements",
            default_duration="medium",
            default_easing="ease_out_expo",
        ),
        "slide_in_left": EnterTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 0, "to": 1}),
                "translateX": TransitionProperties(**{"from": -100, "to": 0}),
            },
            description="Slide in from left",
            usage="Side panels, nav menus",
            default_duration="medium",
            default_easing="ease_out_expo",
        ),
        "slide_in_right": EnterTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 0, "to": 1}),
                "translateX": TransitionProperties(**{"from": 100, "to": 0}),
            },
            description="Slide in from right",
            usage="Side panels, nav menus",
            default_duration="medium",
            default_easing="ease_out_expo",
        ),
        "bounce_in": EnterTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 0, "to": 1}),
                "scale": TransitionProperties(**{"from": 0.3, "to": 1}),
            },
            description="Bounce in with overshoot",
            usage="Playful emphasis, notifications",
            default_duration="medium",
            default_easing="ease_out_back",
        ),
        "rotate_in": EnterTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 0, "to": 1}),
                "rotate": TransitionProperties(**{"from": -180, "to": 0}),
            },
            description="Rotate in from -180deg",
            usage="Playful transitions, icons",
            default_duration="medium",
            default_easing="ease_out_back",
        ),
        "blur_in": EnterTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 0, "to": 1}),
                "blur": TransitionProperties(**{"from": 20, "to": 0}),
            },
            description="Fade in from blurred",
            usage="Backgrounds, hero images",
            default_duration="slow",
            default_easing="ease_out",
        ),
    },
    # ============================================================================
    # EXIT TRANSITIONS
    # ============================================================================
    exit={
        "fade_out": ExitTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 1, "to": 0}),
            },
            description="Simple fade out",
            usage="Subtle exits, dismissals",
            default_duration="normal",
            default_easing="ease_in",
        ),
        "fade_out_down": ExitTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 1, "to": 0}),
                "translateY": TransitionProperties(**{"from": 0, "to": 30}),
            },
            description="Fade out while sliding down",
            usage="Content blocks, cards",
            default_duration="medium",
            default_easing="ease_in_cubic",
        ),
        "fade_out_up": ExitTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 1, "to": 0}),
                "translateY": TransitionProperties(**{"from": 0, "to": -30}),
            },
            description="Fade out while sliding up",
            usage="Notifications, toasts",
            default_duration="medium",
            default_easing="ease_in_cubic",
        ),
        "scale_out": ExitTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 1, "to": 0}),
                "scale": TransitionProperties(**{"from": 1, "to": 0.8}),
            },
            description="Fade out while scaling down",
            usage="Modals, popups",
            default_duration="medium",
            default_easing="ease_in_cubic",
        ),
        "zoom_out": ExitTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 1, "to": 0}),
                "scale": TransitionProperties(**{"from": 1, "to": 0}),
            },
            description="Zoom from 100% to 0%",
            usage="Dramatic exits",
            default_duration="medium",
            default_easing="ease_in_cubic",
        ),
        "slide_out_left": ExitTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 1, "to": 0}),
                "translateX": TransitionProperties(**{"from": 0, "to": -100}),
            },
            description="Slide out to left",
            usage="Side panels, dismissals",
            default_duration="medium",
            default_easing="ease_in_cubic",
        ),
        "slide_out_right": ExitTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 1, "to": 0}),
                "translateX": TransitionProperties(**{"from": 0, "to": 100}),
            },
            description="Slide out to right",
            usage="Side panels, dismissals",
            default_duration="medium",
            default_easing="ease_in_cubic",
        ),
        "blur_out": ExitTransition(
            properties={
                "opacity": TransitionProperties(**{"from": 1, "to": 0}),
                "blur": TransitionProperties(**{"from": 0, "to": 20}),
            },
            description="Fade out to blurred",
            usage="Backgrounds, scene transitions",
            default_duration="slow",
            default_easing="ease_in",
        ),
    },
    # ============================================================================
    # TEMPO / RHYTHM TOKENS
    # ============================================================================
    tempo={
        "sprint": TempoConfig(
            beat_duration=1.0,
            frames_30fps=30,
            frames_60fps=60,
            caption_duration=0.8,
            scene_change_interval=2.0,
            cuts_per_minute=45,
            description="Ultra-fast pacing for maximum retention",
            feel="Frenetic, intense, rapid-fire",
            usage="TikTok, Shorts, attention-grabbing content",
        ),
        "fast": TempoConfig(
            beat_duration=1.5,
            frames_30fps=45,
            frames_60fps=90,
            caption_duration=1.2,
            scene_change_interval=3.0,
            cuts_per_minute=30,
            description="Fast pacing for energetic content",
            feel="Energetic, dynamic, engaging",
            usage="Short-form content, energetic tutorials",
        ),
        "medium": TempoConfig(
            beat_duration=2.0,
            frames_30fps=60,
            frames_60fps=120,
            caption_duration=1.8,
            scene_change_interval=4.5,
            cuts_per_minute=20,
            description="Balanced pacing (default)",
            feel="Comfortable, natural, conversational",
            usage="Most content types, general tutorials",
        ),
        "slow": TempoConfig(
            beat_duration=3.0,
            frames_30fps=90,
            frames_60fps=180,
            caption_duration=2.5,
            scene_change_interval=6.0,
            cuts_per_minute=12,
            description="Deliberate pacing for clarity",
            feel="Thoughtful, clear, educational",
            usage="Technical content, presentations, explanations",
        ),
        "cinematic": TempoConfig(
            beat_duration=4.0,
            frames_30fps=120,
            frames_60fps=240,
            caption_duration=3.5,
            scene_change_interval=8.0,
            cuts_per_minute=8,
            description="Slow, cinematic pacing",
            feel="Atmospheric, dramatic, contemplative",
            usage="Storytelling, documentaries, cinematic content",
        ),
    },
    # ============================================================================
    # PLATFORM-SPECIFIC TIMING
    # ============================================================================
    platform_timing={
        "tiktok": PlatformTimingConfig(
            hook_duration=1.5,
            scene_change_interval=2.0,
            caption_display_duration=0.8,
            cta_timing=CTATiming(
                first_cta=3.0,
                final_cta=-2.0,
            ),
            attention_span="ultra_short",
            recommended_tempo="sprint",
            description="TikTok algorithm-optimized timing",
        ),
        "youtube_shorts": PlatformTimingConfig(
            hook_duration=2.0,
            scene_change_interval=3.0,
            caption_display_duration=1.0,
            cta_timing=CTATiming(
                first_cta=5.0,
                final_cta=-3.0,
            ),
            attention_span="short",
            recommended_tempo="fast",
            description="YouTube Shorts optimized timing",
        ),
        "instagram_reel": PlatformTimingConfig(
            hook_duration=2.0,
            scene_change_interval=3.5,
            caption_display_duration=1.2,
            cta_timing=CTATiming(
                first_cta=5.0,
                final_cta=-3.0,
            ),
            attention_span="short",
            recommended_tempo="fast",
            description="Instagram Reels optimized timing",
        ),
        "youtube_long_form": PlatformTimingConfig(
            hook_duration=3.0,
            scene_change_interval=5.0,
            caption_display_duration=2.0,
            cta_timing=CTATiming(
                first_cta=15.0,
                mid_roll_cta=180.0,
                final_cta=-10.0,
            ),
            attention_span="medium",
            recommended_tempo="medium",
            description="YouTube long-form optimized timing",
        ),
        "linkedin": PlatformTimingConfig(
            hook_duration=2.5,
            scene_change_interval=4.0,
            caption_display_duration=2.0,
            cta_timing=CTATiming(
                first_cta=10.0,
                final_cta=-5.0,
            ),
            attention_span="medium",
            recommended_tempo="medium",
            description="LinkedIn feed optimized timing",
        ),
        "presentation": PlatformTimingConfig(
            hook_duration=4.0,
            scene_change_interval=6.0,
            caption_display_duration=3.0,
            cta_timing=CTATiming(
                first_cta=20.0,
                final_cta=-10.0,
            ),
            attention_span="long",
            recommended_tempo="slow",
            description="Presentation/educational optimized timing",
        ),
    },
)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_duration(name: str) -> DurationConfig:
    """Get a duration config by name, fallback to 'normal' if not found."""
    return MOTION_TOKENS.duration.get(name, MOTION_TOKENS.duration["normal"])


def get_easing(name: str) -> EasingConfig:
    """Get an easing config by name, fallback to 'ease_out' if not found."""
    return MOTION_TOKENS.easing.get(name, MOTION_TOKENS.easing["ease_out"])


def get_spring(name: str) -> SpringConfig:
    """Get a spring config by name, fallback to 'smooth' if not found."""
    return MOTION_TOKENS.spring_configs.get(name, MOTION_TOKENS.spring_configs["smooth"])


def get_enter_transition(name: str) -> EnterTransition:
    """Get an enter transition by name, fallback to 'fade_in' if not found."""
    return MOTION_TOKENS.enter.get(name, MOTION_TOKENS.enter["fade_in"])


def get_exit_transition(name: str) -> ExitTransition:
    """Get an exit transition by name, fallback to 'fade_out' if not found."""
    return MOTION_TOKENS.exit.get(name, MOTION_TOKENS.exit["fade_out"])


def get_tempo(name: str) -> TempoConfig:
    """Get a tempo config by name, fallback to 'medium' if not found."""
    return MOTION_TOKENS.tempo.get(name, MOTION_TOKENS.tempo["medium"])


def get_platform_timing(platform: str) -> PlatformTimingConfig:
    """Get platform timing config by name, fallback to 'youtube_long_form' if not found."""
    return MOTION_TOKENS.platform_timing.get(
        platform, MOTION_TOKENS.platform_timing["youtube_long_form"]
    )


def list_durations() -> list[str]:
    """List all available duration token names."""
    return list(MOTION_TOKENS.duration.keys())


def list_easings() -> list[str]:
    """List all available easing token names."""
    return list(MOTION_TOKENS.easing.keys())


def list_springs() -> list[str]:
    """List all available spring config names."""
    return list(MOTION_TOKENS.spring_configs.keys())


def list_enter_transitions() -> list[str]:
    """List all available enter transition names."""
    return list(MOTION_TOKENS.enter.keys())


def list_exit_transitions() -> list[str]:
    """List all available exit transition names."""
    return list(MOTION_TOKENS.exit.keys())


def list_tempos() -> list[str]:
    """List all available tempo names."""
    return list(MOTION_TOKENS.tempo.keys())


def list_platforms() -> list[str]:
    """List all available platform timing configs."""
    return list(MOTION_TOKENS.platform_timing.keys())
