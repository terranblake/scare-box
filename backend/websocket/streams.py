"""Data streaming handlers for WebSocket communication."""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from .manager import ConnectionManager
from hardware import AudioData
from utils import Event
from state_machine import StateChangeEvent


class StreamManager:
    """Manages real-time data streaming to WebSocket clients."""

    def __init__(self, connection_manager: ConnectionManager):
        self.manager = connection_manager
        self.is_streaming = False
        self.stream_tasks = []

    def start_streaming(self):
        """Start all data streams."""
        self.is_streaming = True

    def stop_streaming(self):
        """Stop all data streams."""
        self.is_streaming = False

    async def stream_audio_data(self, audio_data: AudioData):
        """Stream audio level data to clients."""
        if not self.is_streaming:
            return

        data = {
            "timestamp": audio_data.timestamp,
            "rms": round(audio_data.rms, 3),
            "peak": round(audio_data.peak, 3),
            "frequency_peak": round(audio_data.frequency_peak, 2),
        }

        await self.manager.broadcast_audio_level(data)

    async def stream_light_status(self, light_status: dict):
        """Stream light status data to clients."""
        if not self.is_streaming:
            return

        await self.manager.broadcast_light_status(light_status)

    async def stream_event(self, event: Event):
        """Stream event to clients."""
        if not self.is_streaming:
            return

        await self.manager.broadcast_event(event.to_dict())

    async def stream_state_change(self, state_event: StateChangeEvent):
        """Stream state change to clients."""
        if not self.is_streaming:
            return

        data = {
            "timestamp": state_event.timestamp,
            "from": state_event.from_state.value,
            "to": state_event.to_state.value,
        }

        if state_event.countdown_remaining is not None:
            data["countdown_remaining"] = round(state_event.countdown_remaining, 2)

        await self.manager.broadcast_state_change(data)

    async def send_notification(self, level: str, title: str, message: str):
        """Send notification to clients."""
        await self.manager.broadcast_notification(level, title, message)

    async def periodic_light_status_stream(self, light_controller, interval: float = 0.5):
        """Periodically stream light status."""
        while self.is_streaming:
            try:
                status = light_controller.get_status()
                await self.stream_light_status(status)
            except Exception as e:
                print(f"Error streaming light status: {e}")

            await asyncio.sleep(interval)
