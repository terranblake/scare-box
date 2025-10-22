#!/usr/bin/env python3
"""Direct test of audio playback."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import asyncio
from backend.hardware.speaker import SpeakerController

async def test_audio():
    speaker = SpeakerController()
    speaker.discover_and_connect()
    speaker.initialize()

    print("\n" + "="*60)
    print("Testing audio playback...")
    print("="*60 + "\n")

    await speaker.play_scare_sequence(volume_multiplier=1.0, scream_delay=2.0)

    print("\n" + "="*60)
    print("Test complete!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_audio())
