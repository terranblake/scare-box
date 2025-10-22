"""Bluetooth speaker controller for audio output."""

import asyncio
import pygame
from typing import Optional
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.volume_control import VolumeController


class SpeakerController:
    """Controls Bluetooth speaker for audio playback."""

    def __init__(self):
        self.is_connected = False
        self.current_volume = 0.5
        self.is_playing = False
        self.distortion_level = 0.0
        self.audio_dir = None
        self.boo_sound = None
        self.happy_halloween_sound = None
        self.volume_controller = VolumeController()

    def discover_and_connect(self, device_address: Optional[str] = None):
        """
        Discover and connect to Bluetooth speaker.

        Note: Audio will play through system default output device.
        Make sure your Bluetooth speaker is set as the system default
        in macOS System Settings > Sound > Output.
        """
        print("Audio output will use system default speaker")
        print("Ensure Bluetooth speaker is connected and set as default output")
        self.is_connected = True

    def initialize(self):
        """Initialize audio playback system."""
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        print("Audio system initialized")

        # Load audio files
        self._load_audio_files()

    def _load_audio_files(self):
        """Load scare audio files."""
        self.audio_dir = Path(__file__).parent.parent / "audio"
        self.audio_dir.mkdir(exist_ok=True)

        # Try to load BOO sound
        boo_path = self.audio_dir / "boo.wav"
        if boo_path.exists():
            self.boo_sound = pygame.mixer.Sound(str(boo_path))
            print(f"  ✓ Loaded: {boo_path.name}")
        else:
            print(f"  ✗ Missing: {boo_path}")
            print(f"    Place your BOO sound at: {boo_path}")

        # Try to load Happy Halloween sound
        halloween_path = self.audio_dir / "happy_halloween.wav"
        if halloween_path.exists():
            self.happy_halloween_sound = pygame.mixer.Sound(str(halloween_path))
            print(f"  ✓ Loaded: {halloween_path.name}")
        else:
            print(f"  ✗ Missing: {halloween_path}")
            print(f"    Place your Happy Halloween sound at: {halloween_path}")

    def play_ambient_music(self, volume_multiplier: float = 1.0):
        """
        User controls ambient music externally (Soundcloud, Spotify, etc).
        This is just a placeholder - your music plays through the same speaker.
        """
        self.is_playing = True
        print(f"Ready - Play your ambient music on the laptop (Soundcloud/Spotify/etc)")
        print(f"  It will route through your Bluetooth speaker (if set as default)")
        print(f"  Scare sounds will interrupt when triggered")

    def apply_distortion(self, intensity: float = 0.0):
        """
        Distortion effect during countdown.
        Note: This doesn't affect your external music, only system volume.
        """
        self.distortion_level = intensity
        # Could potentially lower system volume here if needed
        # For now, just track the distortion level

    async def play_scare_sequence(self, volume_multiplier: float = 1.0, scream_delay: float = 2.0):
        """
        Play the scare audio sequence.

        Sequence:
        1. Duck (lower) your ambient music volume
        2. Play BOO sound (now audible over your music)
        3. Delay for screams
        4. Play HAPPY HALLOWEEN
        5. Restore your music volume
        """
        if not self.boo_sound or not self.happy_halloween_sound:
            print("⚠️  Missing audio files! Printing instead:")
            print("BOO! 💀")
            await asyncio.sleep(scream_delay)  # Delay for screams
            print("HAPPY HALLOWEEN! 🎃")
            return

        # Save current audio state and MUTE your music completely
        print("Muting ambient music...")
        self.volume_controller.save_state()
        self.volume_controller.mute()

        await asyncio.sleep(0.2)  # Brief moment for mute to take effect

        print("Playing BOO sound...")
        # Play BOO sound (your music is now SILENT)
        self.boo_sound.set_volume(volume_multiplier)
        self.boo_sound.play()

        # Wait for BOO to finish
        while pygame.mixer.get_busy():
            await asyncio.sleep(0.1)

        print(f"Pausing {scream_delay}s for screams...")
        # Delay for screams/reactions (music still muted)
        await asyncio.sleep(scream_delay)

        print("Playing Happy Halloween...")
        # Play Happy Halloween (music still muted)
        self.happy_halloween_sound.set_volume(volume_multiplier)
        self.happy_halloween_sound.play()

        # Wait for Happy Halloween to finish
        while pygame.mixer.get_busy():
            await asyncio.sleep(0.1)

        # Restore original audio state (unmute your music)
        print("Unmuting ambient music...")
        self.volume_controller.restore_state()

        print("Scare sequence complete - your ambient music continues")

    async def reset_audio(self, duration: float = 5.0):
        """Gradually return to normal ambient music."""
        steps = int(duration * 10)
        step_delay = duration / steps

        for i in range(steps):
            progress = i / steps
            self.apply_distortion(intensity=1.0 - progress)
            await asyncio.sleep(step_delay)

        # Resume ambient music
        self.apply_distortion(0.0)
        self.play_ambient_music()

    def set_volume(self, volume: float):
        """Set speaker volume (0.0 to 1.0)."""
        self.current_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.current_volume)
        except pygame.error:
            # Mixer not initialized - expected during testing
            pass

    def shutdown(self):
        """Stop playback and cleanup."""
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.is_playing = False
        print("Audio system shutdown")

    def get_status(self) -> dict:
        """Get current speaker status."""
        return {
            "connected": self.is_connected,
            "playing": self.is_playing,
            "volume": self.current_volume,
            "distortion": self.distortion_level,
        }
