"""USB-C Microphone controller for audio input and trigger detection."""

import asyncio
import numpy as np
from typing import Callable, List, Optional
import sounddevice as sd
from dataclasses import dataclass


@dataclass
class AudioData:
    """Audio analysis data."""
    timestamp: float
    rms: float
    peak: float
    frequency_peak: float
    triggered: bool


class MicrophoneController:
    """Controls USB-C microphone for audio input and trigger detection."""

    def __init__(
        self,
        sample_rate: int = 44100,
        chunk_size: int = 1024,
        trigger_freq_min: float = 800.0,
        trigger_freq_max: float = 1200.0,
        trigger_threshold: float = 0.3,
    ):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.trigger_freq_min = trigger_freq_min
        self.trigger_freq_max = trigger_freq_max
        self.trigger_threshold = trigger_threshold

        self.device_id: Optional[int] = None
        self.stream: Optional[sd.InputStream] = None
        self.is_listening = False

        self.trigger_callbacks: List[Callable] = []
        self.audio_callbacks: List[Callable[[AudioData], None]] = []

    def initialize(self, device_name: Optional[str] = None):
        """Initialize microphone device."""
        devices = sd.query_devices()

        if device_name:
            # Find specific device
            for i, device in enumerate(devices):
                if device_name.lower() in device["name"].lower():
                    self.device_id = i
                    break
        else:
            # Use default input device
            self.device_id = sd.default.device[0]

        if self.device_id is None:
            raise RuntimeError("Microphone device not found")

        device_info = sd.query_devices(self.device_id)
        print(f"Microphone: {device_info['name']}")

    async def start_listening(self):
        """Start listening to microphone input."""
        # Close any existing stream first
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except:
                pass
            self.stream = None
            self.is_listening = False

        if self.is_listening:
            return

        self.is_listening = True
        loop = asyncio.get_event_loop()

        def audio_callback(indata, frames, time_info, status):
            """Process audio chunk in callback."""
            if status:
                print(f"Audio status: {status}")

            audio_data = indata[:, 0]  # Mono
            analysis = self._analyze_audio(audio_data)

            # Notify listeners
            for callback in self.audio_callbacks:
                # Handle both sync and async callbacks
                result = callback(analysis)
                if asyncio.iscoroutine(result):
                    # Run coroutine in the main event loop (cross-thread)
                    asyncio.run_coroutine_threadsafe(result, loop)

            # Check for trigger
            if analysis.triggered:
                for callback in self.trigger_callbacks:
                    callback()

        self.stream = sd.InputStream(
            device=self.device_id,
            channels=1,
            samplerate=self.sample_rate,
            blocksize=self.chunk_size,
            callback=audio_callback,
        )
        self.stream.start()

    def stop_listening(self):
        """Stop listening to microphone input."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.is_listening = False

    def _analyze_audio(self, audio_data: np.ndarray) -> AudioData:
        """Analyze audio chunk using FFT."""
        import time

        # Calculate RMS (loudness)
        rms = float(np.sqrt(np.mean(audio_data**2)))

        # Calculate peak
        peak = float(np.max(np.abs(audio_data)))

        # Perform FFT
        fft = np.fft.rfft(audio_data)
        magnitude = np.abs(fft)
        freqs = np.fft.rfftfreq(len(audio_data), 1 / self.sample_rate)

        # Find peak frequency
        peak_idx = np.argmax(magnitude)
        frequency_peak = float(freqs[peak_idx])

        # Check if trigger frequency detected
        in_trigger_range = (
            self.trigger_freq_min <= frequency_peak <= self.trigger_freq_max
        )
        above_threshold = rms >= self.trigger_threshold
        triggered = in_trigger_range and above_threshold

        return AudioData(
            timestamp=time.time(),
            rms=rms,
            peak=peak,
            frequency_peak=frequency_peak,
            triggered=triggered,
        )

    def register_trigger_callback(self, callback: Callable):
        """Register callback for trigger events."""
        self.trigger_callbacks.append(callback)

    def register_audio_callback(self, callback: Callable[[AudioData], None]):
        """Register callback for audio data updates."""
        self.audio_callbacks.append(callback)

    def get_status(self) -> dict:
        """Get current microphone status."""
        return {
            "connected": self.device_id is not None,
            "listening": self.is_listening,
            "device_id": self.device_id,
            "sample_rate": self.sample_rate,
        }
