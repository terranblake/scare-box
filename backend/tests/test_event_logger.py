"""Tests for event logger."""

import pytest
from backend.utils.event_logger import EventLogger, EventLevel, EventCategory


def test_event_logger_initialization():
    """Test event logger initializes correctly."""
    logger = EventLogger(max_events=10)

    assert len(logger.events) == 0


def test_event_logger_logging():
    """Test basic logging functionality."""
    logger = EventLogger()

    logger.info(EventCategory.SYSTEM, "Test message")
    logger.warning(EventCategory.HARDWARE, "Warning message")
    logger.error(EventCategory.CONFIG, "Error message")

    assert len(logger.events) == 3

    events = logger.get_events()
    assert events[0].level == EventLevel.INFO
    assert events[1].level == EventLevel.WARNING
    assert events[2].level == EventLevel.ERROR


def test_event_logger_filtering():
    """Test event filtering."""
    logger = EventLogger()

    logger.info(EventCategory.SYSTEM, "System event")
    logger.warning(EventCategory.HARDWARE, "Hardware warning")
    logger.error(EventCategory.TRIGGER, "Trigger error")

    # Filter by level
    warnings = logger.get_events(level=EventLevel.WARNING)
    assert len(warnings) == 1
    assert warnings[0].message == "Hardware warning"

    # Filter by category
    system_events = logger.get_events(category=EventCategory.SYSTEM)
    assert len(system_events) == 1
    assert system_events[0].message == "System event"


def test_event_logger_limit():
    """Test event limit functionality."""
    logger = EventLogger(max_events=5)

    # Add more than max
    for i in range(10):
        logger.info(EventCategory.SYSTEM, f"Message {i}")

    # Should only keep last 5
    assert len(logger.events) == 5

    events = logger.get_events()
    assert events[-1].message == "Message 9"


def test_event_logger_callbacks():
    """Test event callbacks."""
    logger = EventLogger()

    callback_events = []

    def callback(event):
        callback_events.append(event)

    logger.register_callback(callback)

    logger.info(EventCategory.SYSTEM, "Test event")

    assert len(callback_events) == 1
    assert callback_events[0].message == "Test event"


def test_event_logger_stats():
    """Test event statistics."""
    logger = EventLogger()

    logger.info(EventCategory.SYSTEM, "Info 1")
    logger.info(EventCategory.SYSTEM, "Info 2")
    logger.warning(EventCategory.HARDWARE, "Warning 1")
    logger.error(EventCategory.TRIGGER, "Error 1")

    stats = logger.get_stats()

    assert stats["total_events"] == 4
    assert stats["by_level"]["info"] == 2
    assert stats["by_level"]["warning"] == 1
    assert stats["by_level"]["error"] == 1
    assert stats["by_category"]["system"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
