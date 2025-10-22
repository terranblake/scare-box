"""WebSocket connection manager for real-time communication."""

from fastapi import WebSocket
from typing import List, Dict, Any
import json
import asyncio


class ConnectionManager:
    """Manages WebSocket connections and broadcasting."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"WebSocket client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"WebSocket client disconnected. Total: {len(self.active_connections)}")

    async def send_personal(self, message: Dict[str, Any], websocket: WebSocket):
        """Send message to specific client."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending to client: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients."""
        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                disconnected.append(connection)

        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

    async def broadcast_audio_level(self, audio_data: Dict[str, Any]):
        """Broadcast audio level data."""
        message = {
            "type": "audio_level",
            "data": audio_data,
        }
        await self.broadcast(message)

    async def broadcast_light_status(self, light_data: Dict[str, Any]):
        """Broadcast light status data."""
        message = {
            "type": "light_status",
            "data": light_data,
        }
        await self.broadcast(message)

    async def broadcast_event(self, event_data: Dict[str, Any]):
        """Broadcast event data."""
        message = {
            "type": "event",
            "data": event_data,
        }
        await self.broadcast(message)

    async def broadcast_state_change(self, state_data: Dict[str, Any]):
        """Broadcast state change data."""
        message = {
            "type": "state_change",
            "data": state_data,
        }
        await self.broadcast(message)

    async def broadcast_notification(
        self,
        level: str,
        title: str,
        message: str,
    ):
        """Broadcast notification."""
        import time

        notification = {
            "type": "notification",
            "data": {
                "timestamp": time.time(),
                "level": level,
                "title": title,
                "message": message,
            },
        }
        await self.broadcast(notification)

    def get_connection_count(self) -> int:
        """Get number of active connections."""
        return len(self.active_connections)


# Global connection manager instance
manager = ConnectionManager()
