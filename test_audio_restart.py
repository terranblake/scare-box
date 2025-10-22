#!/usr/bin/env python3
"""Test audio playback after stop/start cycle."""

import pygame
import time
from pathlib import Path

audio_dir = Path(__file__).parent / "backend" / "audio"

print("=== Initial setup ===")
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
print("Mixer initialized")

boo_sound = pygame.mixer.Sound(str(audio_dir / "boo.wav"))
happy_sound = pygame.mixer.Sound(str(audio_dir / "happy_halloween.wav"))
print(f"BOO loaded: {boo_sound.get_length():.2f}s")
print(f"Happy Halloween loaded: {happy_sound.get_length():.2f}s")

print("\n=== Playing BOO ===")
boo_sound.play()
time.sleep(1)

print("\n=== Playing Happy Halloween ===")
happy_sound.play()
time.sleep(2)

print("\n=== Simulating stop (quit mixer) ===")
pygame.mixer.quit()
print("Mixer quit")

time.sleep(1)

print("\n=== Simulating start (reinit mixer) ===")
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
print("Mixer reinitialized")

boo_sound = pygame.mixer.Sound(str(audio_dir / "boo.wav"))
happy_sound = pygame.mixer.Sound(str(audio_dir / "happy_halloween.wav"))
print(f"BOO reloaded: {boo_sound.get_length():.2f}s")
print(f"Happy Halloween reloaded: {happy_sound.get_length():.2f}s")

print("\n=== Playing BOO after restart ===")
boo_sound.set_volume(1.0)
boo_sound.play()
while pygame.mixer.get_busy():
    time.sleep(0.1)
print("BOO finished")

print("\n=== Playing Happy Halloween after restart ===")
happy_sound.set_volume(1.0)
happy_sound.play()
while pygame.mixer.get_busy():
    time.sleep(0.1)
print("Happy Halloween finished")

print("\n=== Test complete ===")
pygame.mixer.quit()
