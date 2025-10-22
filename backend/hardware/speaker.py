"""Bluetooth speaker controller for audio output."""

import asyncio
import pygame
from typing import Optional
from pathlib import Path


class SpeakerController:
    """Controls Bluetooth speaker for audio playback."""

    def __init__(self):
        self.is_connected = False
        self.current_volume = 0.5
        self.is_playing = False
        self.distortion_level = 0.0

    def discover_and_connect(self, device_address: Optional[str] = None):
        """Discover and connect to Bluetooth speaker."""
        # In production, this would use bleak for Bluetooth
        # For now, we'll use pygame mixer which works with system audio
        print("Connecting to audio output...")
        self.is_connected = True

    def initialize(self):
        """Initialize audio playback system."""
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        print("Audio system initialized")

        # Create placeholder audio files if they don't exist
        self._ensure_audio_files()

    def _ensure_audio_files(self):
        """Ensure placeholder audio files exist."""
        audio_dir = Path("backend/audio")
        audio_dir.mkdir(exist_ok=True)

        # Note: In production, add actual audio files here
        self.ambient_music = None
        self.boo_sound = None

    def play_ambient_music(self, volume_multiplier: float = 1.0):
        """Play looping Halloween ambient music."""
        volume = self.current_volume * volume_multiplier
        pygame.mixer.music.set_volume(volume)

        # In production, load and play actual ambient music
        # pygame.mixer.music.load("backend/audio/ambient.mp3")
        # pygame.mixer.music.play(-1)  # Loop indefinitely

        self.is_playing = True
        print(f"Ambient music playing at volume {volume:.2f}")

    def apply_distortion(self, intensity: float = 0.0):
        """Apply audio distortion effect."""
        self.distortion_level = intensity

        # Reduce volume as distortion increases
        distorted_volume = self.current_volume * (1 - intensity * 0.5)
        pygame.mixer.music.set_volume(distorted_volume)

        # In production, apply real-time pitch shifting and distortion
        # This would require additional audio processing libraries

    def play_scare_sequence(self, volume_multiplier: float = 1.0):
        """Play the scare audio sequence."""
        # Stop ambient music
        pygame.mixer.music.stop()

        # Brief silence
        import time
        time.sleep(0.3)

        # In production, play actual BOO sound effect
        # boo_sound = pygame.mixer.Sound("backend/audio/boo.wav")
        # boo_sound.set_volume(volume_multiplier)
        # boo_sound.play()

        print(f"BOO! 🎃 HAPPY HALLOWEEN!")

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
        pygame.mixer.music.set_volume(self.current_volume)

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
