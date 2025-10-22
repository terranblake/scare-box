"""WebSocket module for real-time communication."""

from .manager import ConnectionManager, manager
from .streams import StreamManager

__all__ = ["ConnectionManager", "manager", "StreamManager"]
