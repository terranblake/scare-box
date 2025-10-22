"""System volume control for macOS."""

import subprocess


class VolumeController:
    """Controls macOS system volume and muting."""

    def __init__(self):
        self.original_volume = None
        self.was_muted = False

    def get_volume(self) -> float:
        """Get current system volume (0.0 to 1.0)."""
        try:
            result = subprocess.run(
                ["osascript", "-e", "output volume of (get volume settings)"],
                capture_output=True,
                text=True,
            )
            volume = int(result.stdout.strip())
            return volume / 100.0
        except Exception as e:
            print(f"Error getting volume: {e}")
            return 0.5

    def is_muted(self) -> bool:
        """Check if system is muted."""
        try:
            result = subprocess.run(
                ["osascript", "-e", "output muted of (get volume settings)"],
                capture_output=True,
                text=True,
            )
            return result.stdout.strip() == "true"
        except Exception as e:
            print(f"Error checking mute status: {e}")
            return False

    def set_volume(self, volume: float):
        """Set system volume (0.0 to 1.0)."""
        try:
            volume_percent = int(volume * 100)
            subprocess.run(
                ["osascript", "-e", f"set volume output volume {volume_percent}"],
                check=True,
            )
        except Exception as e:
            print(f"Error setting volume: {e}")

    def mute(self):
        """Mute system audio completely."""
        try:
            subprocess.run(
                ["osascript", "-e", "set volume with output muted"],
                check=True,
            )
            print("🔇 System audio MUTED")
        except Exception as e:
            print(f"Error muting: {e}")

    def unmute(self):
        """Unmute system audio."""
        try:
            subprocess.run(
                ["osascript", "-e", "set volume without output muted"],
                check=True,
            )
            print("🔊 System audio UNMUTED")
        except Exception as e:
            print(f"Error unmuting: {e}")

    def save_state(self):
        """Save current volume and mute state for later restoration."""
        self.original_volume = self.get_volume()
        self.was_muted = self.is_muted()
        print(f"Saved: volume={self.original_volume * 100:.0f}%, muted={self.was_muted}")

    def restore_state(self):
        """Restore previously saved volume and mute state."""
        if self.original_volume is not None:
            self.set_volume(self.original_volume)

            if self.was_muted:
                self.mute()
            else:
                self.unmute()

            print(f"Restored: volume={self.original_volume * 100:.0f}%, muted={self.was_muted}")
