"""LIFX Light Bar controller for addressable LED lighting."""

import asyncio
from typing import List, Optional, Tuple
from lifxlan import LifxLAN, Light
import random
import time


class LightController:
    """Controls LIFX Light Bars over WiFi/LAN."""

    def __init__(self):
        self.lifx = LifxLAN()
        self.devices: List[Light] = []
        self.is_running = False
        self.current_task: Optional[asyncio.Task] = None

    def discover_devices(self, timeout: int = 5) -> int:
        """Discover LIFX devices on network."""
        print("Discovering LIFX devices...")
        self.devices = self.lifx.get_lights()
        print(f"Found {len(self.devices)} LIFX device(s)")
        for device in self.devices:
            print(f"  - {device.get_label()}")
        return len(self.devices)

    def initialize(self):
        """Initialize connection to all LIFX devices."""
        if not self.devices:
            print("No LIFX devices found. Running in simulation mode.")
            return

        for device in self.devices:
            device.set_power(True)

    async def set_ambient_pattern(self):
        """Set calming, Halloween-themed ambient pattern."""
        if not self.devices:
            return

        # Turn on all lights first
        for device in self.devices:
            device.set_power(True)

        # Halloween colors: Orange, Purple, Green
        colors = [
            (30, 65535, 32768, 3500),   # Orange
            (270, 65535, 32768, 3500),  # Purple
            (120, 65535, 32768, 3500),  # Green
        ]

        self.is_running = True

        while self.is_running:
            for device in self.devices:
                color = random.choice(colors)
                device.set_color(color, duration=2000)

            await asyncio.sleep(3)

    async def start_glitch_effect(self, intensity: float = 0.0):
        """Apply glitching effect with increasing intensity."""
        if not self.devices:
            return

        # Increase glitch frequency with intensity
        delay = max(0.05, 0.5 - (intensity * 0.4))

        for device in self.devices:
            # Random brightness flicker
            brightness = int(32768 * (1 - intensity * 0.5 + random.random() * intensity))

            # Random color shift
            hue = random.randint(0, 65535)
            saturation = int(65535 * (0.8 + random.random() * 0.2))

            device.set_color((hue, saturation, brightness, 3500), duration=50)

        await asyncio.sleep(delay)

    def trigger_flash(self, brightness_multiplier: float = 1.0):
        """Execute bright flash effect."""
        if not self.devices:
            return

        brightness = int(65535 * brightness_multiplier)

        for device in self.devices:
            # Bright white flash
            device.set_color((0, 0, brightness, 9000), duration=100)

    async def reset_to_ambient(self, duration: float = 5.0):
        """Gradually return to ambient pattern."""
        # Transition back to ambient over duration
        steps = int(duration * 10)
        step_delay = duration / steps

        for i in range(steps):
            progress = i / steps
            await self.start_glitch_effect(intensity=1.0 - progress)
            await asyncio.sleep(step_delay)

        # Resume ambient pattern
        if self.current_task:
            self.current_task.cancel()
        self.current_task = asyncio.create_task(self.set_ambient_pattern())

    def shutdown(self):
        """Turn off all lights."""
        self.is_running = False
        if self.current_task:
            self.current_task.cancel()

        for device in self.devices:
            device.set_power(False)

    def get_status(self) -> dict:
        """Get current light status."""
        if not self.devices:
            return {
                "connected": False,
                "devices": [],
            }

        device_status = []
        for device in self.devices:
            try:
                color = device.get_color()
                power = device.get_power()

                device_status.append({
                    "id": str(device.get_mac_addr()),
                    "name": device.get_label(),
                    "power": power > 0,
                    "brightness": color[2] / 65535,
                    "color": {
                        "hue": color[0],
                        "saturation": color[1],
                    },
                })
            except Exception as e:
                print(f"Error getting device status: {e}")

        return {
            "connected": True,
            "device_count": len(self.devices),
            "devices": device_status,
        }
