"""System volume control for macOS."""

import subprocess


class VolumeController:
    """Controls macOS system volume."""

    def __init__(self):
        self.original_volume = None

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

    def save_volume(self):
        """Save current volume for later restoration."""
        self.original_volume = self.get_volume()
        print(f"Saved original volume: {self.original_volume * 100:.0f}%")

    def restore_volume(self):
        """Restore previously saved volume."""
        if self.original_volume is not None:
            self.set_volume(self.original_volume)
            print(f"Restored volume to: {self.original_volume * 100:.0f}%")

    def duck_volume(self, duck_amount: float = 0.3):
        """
        Reduce volume temporarily (duck).

        Args:
            duck_amount: How much to reduce (0.0 to 1.0).
                        0.3 = reduce to 30% of original
        """
        if self.original_volume is None:
            self.save_volume()

        ducked = self.original_volume * duck_amount
        self.set_volume(ducked)
        print(f"Ducked volume to {ducked * 100:.0f}%")
