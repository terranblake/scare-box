#!/usr/bin/env python3
"""List available audio devices for Scare Box configuration."""

import sounddevice as sd

print("=" * 60)
print("Available Audio Input Devices")
print("=" * 60)

devices = sd.query_devices()

input_devices = []

for i, device in enumerate(devices):
    if device['max_input_channels'] > 0:
        input_devices.append((i, device))
        print(f"\n[{i}] {device['name']}")
        print(f"    Channels: {device['max_input_channels']}")
        print(f"    Sample Rate: {device['default_samplerate']} Hz")

if not input_devices:
    print("\nNo input devices found!")
else:
    print("\n" + "=" * 60)
    print("To use a specific device:")
    print("  1. Edit backend/config.yaml")
    print("  2. Set 'microphone_device' to the device name")
    print(f"  3. Example: microphone_device: \"{input_devices[0][1]['name']}\"")
    print("=" * 60)
