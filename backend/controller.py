"""Main orchestration controller for Scare Box."""

import asyncio
from typing import Optional
from hardware import MicrophoneController, LightController, SpeakerController, AudioData
from state_machine import StateMachine, State, Mode, StateChangeEvent
from utils import event_logger, EventCategory
from websocket import StreamManager, manager as ws_manager
from config import config


class ScareBoxController:
    """Main controller coordinating all components."""

    def __init__(self):
        self.config = config

        # Initialize components
        self.microphone = MicrophoneController(
            sample_rate=config.audio.sample_rate,
            chunk_size=config.audio.chunk_size,
            trigger_freq_min=config.audio.trigger_frequency_min,
            trigger_freq_max=config.audio.trigger_frequency_max,
            trigger_threshold=config.audio.trigger_amplitude_threshold,
        )

        self.lights = LightController()
        self.speaker = SpeakerController()

        self.state_machine = StateMachine(
            countdown_duration=config.timing.countdown_duration,
            active_duration=config.timing.active_duration,
            reset_duration=config.timing.reset_duration,
        )

        self.event_logger = event_logger
        self.stream_manager = StreamManager(ws_manager)

        # State
        self.is_running = False
        self.ambient_task: Optional[asyncio.Task] = None
        self.light_stream_task: Optional[asyncio.Task] = None
        self.scream_delay = config.timing.scream_delay

        # Register callbacks
        self._setup_callbacks()

    def _setup_callbacks(self):
        """Setup callbacks between components."""
        # Microphone callbacks
        self.microphone.register_trigger_callback(self._on_audio_trigger)
        self.microphone.register_audio_callback(self._on_audio_data)

        # State machine callbacks
        self.state_machine.register_state_change_callback(self._on_state_change)

        # Event logger callbacks
        self.event_logger.register_callback(self._on_event)

    async def initialize(self):
        """Initialize all hardware components."""
        self.event_logger.info(EventCategory.SYSTEM, "Initializing Scare Box...")

        try:
            # Initialize microphone
            self.microphone.initialize(self.config.hardware.microphone_device)
            self.event_logger.info(EventCategory.HARDWARE, "Microphone initialized")

            # Initialize lights
            self.lights.discover_devices()
            self.lights.initialize()
            self.event_logger.info(EventCategory.HARDWARE, "Lights initialized")

            # Initialize speaker
            self.speaker.discover_and_connect(self.config.hardware.speaker_address)
            self.speaker.initialize()
            self.event_logger.info(EventCategory.HARDWARE, "Speaker initialized")

            self.event_logger.info(EventCategory.SYSTEM, "Initialization complete")

        except Exception as e:
            self.event_logger.error(EventCategory.SYSTEM, f"Initialization failed: {e}")
            raise

    async def start(self):
        """Start Scare Box operation."""
        if self.is_running:
            return

        self.is_running = True
        mode = self.state_machine.get_mode()

        self.event_logger.info(
            EventCategory.SYSTEM,
            f"Starting Scare Box in {mode.value.upper()} mode",
        )

        # Start streaming
        self.stream_manager.start_streaming()

        # Start ambient effects
        intensity = self._get_intensity_multipliers()
        self.ambient_task = asyncio.create_task(self.lights.set_ambient_pattern())
        self.speaker.play_ambient_music(intensity["volume"])

        # Start microphone listening
        await self.microphone.start_listening()

        # Start periodic light status streaming
        self.light_stream_task = asyncio.create_task(
            self.stream_manager.periodic_light_status_stream(self.lights)
        )

        self.event_logger.info(EventCategory.SYSTEM, "Scare Box started")

    async def stop(self):
        """Stop Scare Box operation."""
        if not self.is_running:
            return

        self.is_running = False

        self.event_logger.info(EventCategory.SYSTEM, "Stopping Scare Box...")

        # Stop streaming
        self.stream_manager.stop_streaming()

        # Stop microphone
        self.microphone.stop_listening()

        # Stop ambient effects
        if self.ambient_task:
            self.ambient_task.cancel()

        if self.light_stream_task:
            self.light_stream_task.cancel()

        # Stop hardware
        self.lights.shutdown()
        self.speaker.shutdown()

        self.event_logger.info(EventCategory.SYSTEM, "Scare Box stopped")

    def _on_audio_trigger(self):
        """Handle audio trigger detection."""
        if not self.state_machine.can_trigger():
            return

        self.event_logger.info(
            EventCategory.TRIGGER,
            "Audio trigger detected",
            {"type": "audio"},
        )

        asyncio.create_task(self.trigger_sequence())

    async def _on_audio_data(self, audio_data: AudioData):
        """Handle audio data updates."""
        await self.stream_manager.stream_audio_data(audio_data)

    async def _on_state_change(self, event: StateChangeEvent):
        """Handle state changes."""
        self.event_logger.info(
            EventCategory.STATE,
            f"State changed: {event.from_state.value} -> {event.to_state.value}",
        )

        await self.stream_manager.stream_state_change(event)

        # Execute hardware effects based on state
        await self._execute_state_effects(event)

    async def _execute_state_effects(self, event: StateChangeEvent):
        """Execute hardware effects for state changes."""
        intensity = self._get_intensity_multipliers()
        state = event.to_state

        if state == State.TRICK_COUNTDOWN:
            # Start glitch effects
            if event.countdown_remaining is not None:
                progress = 1.0 - (
                    event.countdown_remaining / self.config.timing.countdown_duration
                )
                await self.lights.start_glitch_effect(progress)
                self.speaker.apply_distortion(progress)

        elif state == State.TRICK_ACTIVE:
            # Execute scare
            await self.speaker.play_scare_sequence(
                volume_multiplier=intensity["volume"],
                scream_delay=self.scream_delay
            )
            self.lights.trigger_flash(intensity["brightness"])

        elif state == State.TRICK_RESET:
            # Reset to ambient
            asyncio.create_task(
                self.lights.reset_to_ambient(self.config.timing.reset_duration)
            )
            asyncio.create_task(
                self.speaker.reset_audio(self.config.timing.reset_duration)
            )

    async def _on_event(self, event):
        """Handle logged events."""
        await self.stream_manager.stream_event(event)

    async def trigger_sequence(self):
        """Manually trigger scare sequence."""
        self.event_logger.info(
            EventCategory.TRIGGER,
            "Scare sequence triggered",
            {"type": "manual"},
        )

        await self.state_machine.trigger_sequence()

    def set_mode(self, mode_str: str):
        """Set operating mode."""
        mode = Mode.CHILD if mode_str.lower() == "child" else Mode.ADULT

        self.state_machine.set_mode(mode)

        self.event_logger.info(
            EventCategory.CONFIG,
            f"Mode changed to {mode.value.upper()}",
        )

        # Update speaker volume
        intensity = self._get_intensity_multipliers()
        self.speaker.set_volume(intensity["volume"])

    def update_config(self, config_data: dict):
        """Update configuration parameters."""
        for key, value in config_data.items():
            self.event_logger.info(
                EventCategory.CONFIG,
                f"Config updated: {key} = {value}",
            )

            # Update timing
            if key == "countdown_duration":
                self.state_machine.update_timing(countdown_duration=value)
                self.config.timing.countdown_duration = value
            elif key == "active_duration":
                self.state_machine.update_timing(active_duration=value)
                self.config.timing.active_duration = value
            elif key == "reset_duration":
                self.state_machine.update_timing(reset_duration=value)
                self.config.timing.reset_duration = value
            elif key == "scream_delay":
                self.scream_delay = value
                self.config.timing.scream_delay = value

            # Update audio settings
            elif key == "trigger_frequency_min":
                self.microphone.trigger_freq_min = value
                self.config.audio.trigger_frequency_min = value
            elif key == "trigger_frequency_max":
                self.microphone.trigger_freq_max = value
                self.config.audio.trigger_frequency_max = value
            elif key == "trigger_amplitude_threshold":
                self.microphone.trigger_threshold = value
                self.config.audio.trigger_amplitude_threshold = value

        # Save config to disk
        self.config.save_to_file()

    def get_config(self) -> dict:
        """Get current configuration."""
        return {
            "mode": self.state_machine.get_mode().value,
            "audio": {
                "trigger_frequency_min": self.microphone.trigger_freq_min,
                "trigger_frequency_max": self.microphone.trigger_freq_max,
                "trigger_amplitude_threshold": self.microphone.trigger_threshold,
                "sample_rate": self.microphone.sample_rate,
            },
            "timing": {
                "countdown_duration": self.state_machine.countdown_duration,
                "active_duration": self.state_machine.active_duration,
                "reset_duration": self.state_machine.reset_duration,
                "scream_delay": self.scream_delay,
            },
        }

    def _get_intensity_multipliers(self) -> dict:
        """Get intensity multipliers for current mode."""
        mode = self.state_machine.get_mode()

        if mode == Mode.CHILD:
            return {
                "brightness": self.config.intensity.child.brightness,
                "volume": self.config.intensity.child.volume,
            }
        else:
            return {
                "brightness": self.config.intensity.adult.brightness,
                "volume": self.config.intensity.adult.volume,
            }
