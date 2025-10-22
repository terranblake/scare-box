"""Event logging and tracking system."""

import time
from typing import List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from collections import deque


class EventLevel(Enum):
    """Event severity levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class EventCategory(Enum):
    """Event categories."""
    SYSTEM = "system"
    TRIGGER = "trigger"
    STATE = "state"
    HARDWARE = "hardware"
    CONFIG = "config"


@dataclass
class Event:
    """Event data structure."""
    timestamp: float
    level: EventLevel
    category: EventCategory
    message: str
    details: Optional[dict] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "timestamp": self.timestamp,
            "level": self.level.value,
            "category": self.category.value,
            "message": self.message,
            "details": self.details or {},
        }


class EventLogger:
    """Centralized event logging and tracking."""

    def __init__(self, max_events: int = 1000):
        self.events: deque[Event] = deque(maxlen=max_events)
        self.callbacks: List[Callable[[Event], None]] = []

    def log(
        self,
        level: EventLevel,
        category: EventCategory,
        message: str,
        details: Optional[dict] = None,
    ):
        """Log an event."""
        event = Event(
            timestamp=time.time(),
            level=level,
            category=category,
            message=message,
            details=details,
        )

        self.events.append(event)

        # Print to console
        print(f"[{level.value.upper()}] {category.value}: {message}")

        # Notify callbacks
        for callback in self.callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in event callback: {e}")

    def info(self, category: EventCategory, message: str, details: Optional[dict] = None):
        """Log info event."""
        self.log(EventLevel.INFO, category, message, details)

    def warning(self, category: EventCategory, message: str, details: Optional[dict] = None):
        """Log warning event."""
        self.log(EventLevel.WARNING, category, message, details)

    def error(self, category: EventCategory, message: str, details: Optional[dict] = None):
        """Log error event."""
        self.log(EventLevel.ERROR, category, message, details)

    def debug(self, category: EventCategory, message: str, details: Optional[dict] = None):
        """Log debug event."""
        self.log(EventLevel.DEBUG, category, message, details)

    def get_events(
        self,
        limit: Optional[int] = None,
        level: Optional[EventLevel] = None,
        category: Optional[EventCategory] = None,
    ) -> List[Event]:
        """Get events with optional filtering."""
        events = list(self.events)

        if level:
            events = [e for e in events if e.level == level]

        if category:
            events = [e for e in events if e.category == category]

        if limit:
            events = events[-limit:]

        return events

    def get_stats(self) -> dict:
        """Get event statistics."""
        total = len(self.events)
        by_level = {}
        by_category = {}

        for event in self.events:
            by_level[event.level.value] = by_level.get(event.level.value, 0) + 1
            by_category[event.category.value] = by_category.get(event.category.value, 0) + 1

        return {
            "total_events": total,
            "by_level": by_level,
            "by_category": by_category,
        }

    def register_callback(self, callback: Callable[[Event], None]):
        """Register callback for new events."""
        self.callbacks.append(callback)

    def clear(self):
        """Clear all events."""
        self.events.clear()


# Global event logger instance
event_logger = EventLogger()
