#!/usr/bin/env python3
"""Validation script to test backend components without hardware."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from backend.state_machine import StateMachine, State, Mode
from backend.utils.event_logger import EventLogger, EventCategory
from backend.websocket.manager import ConnectionManager
from backend.config import Config


async def validate_state_machine():
    """Validate state machine functionality."""
    print("\n" + "=" * 60)
    print("Testing State Machine")
    print("=" * 60)

    sm = StateMachine(
        countdown_duration=0.5,
        active_duration=0.2,
        reset_duration=0.3,
    )

    print(f"✓ Initial state: {sm.get_state().value}")
    print(f"✓ Initial mode: {sm.get_mode().value}")

    # Test mode switching
    sm.set_mode(Mode.ADULT)
    assert sm.get_mode() == Mode.ADULT
    print("✓ Mode switching works")

    # Test state transitions
    states_seen = []

    def track_states(event):
        states_seen.append(event.to_state)
        print(f"  State transition: {event.from_state.value} -> {event.to_state.value}")

    sm.register_state_change_callback(track_states)

    print("\n  Triggering sequence...")
    await sm.trigger_sequence()

    # Wait for completion
    await asyncio.sleep(1.5)

    assert State.TRICK_COUNTDOWN in states_seen
    assert State.TRICK_ACTIVE in states_seen
    assert State.TRICK_RESET in states_seen
    assert sm.get_state() == State.NON_TRICK

    print("✓ Full sequence completed successfully")


def validate_event_logger():
    """Validate event logger functionality."""
    print("\n" + "=" * 60)
    print("Testing Event Logger")
    print("=" * 60)

    logger = EventLogger()

    # Test logging
    logger.info(EventCategory.SYSTEM, "System initialized")
    logger.warning(EventCategory.HARDWARE, "Device not found")
    logger.error(EventCategory.TRIGGER, "Trigger failed")

    events = logger.get_events()
    assert len(events) == 3
    print(f"✓ Logged {len(events)} events")

    # Test filtering
    system_events = logger.get_events(category=EventCategory.SYSTEM)
    assert len(system_events) == 1
    print("✓ Event filtering works")

    # Test stats
    stats = logger.get_stats()
    assert stats["total_events"] == 3
    print(f"✓ Statistics: {stats}")

    # Test callbacks
    callback_count = [0]

    def count_events(event):
        callback_count[0] += 1

    logger.register_callback(count_events)
    logger.info(EventCategory.SYSTEM, "New event")

    assert callback_count[0] == 1
    print("✓ Callbacks work")


def validate_config():
    """Validate configuration loading."""
    print("\n" + "=" * 60)
    print("Testing Configuration")
    print("=" * 60)

    config = Config.load_from_file("config.yaml")

    print(f"✓ Mode: {config.mode}")
    print(f"✓ Sample rate: {config.audio.sample_rate}")
    print(f"✓ Countdown duration: {config.timing.countdown_duration}")
    print(f"✓ Server port: {config.server.port}")

    assert config.mode in ["child", "adult"]
    assert config.audio.sample_rate > 0
    assert config.timing.countdown_duration > 0

    print("✓ Configuration loaded successfully")


async def validate_websocket_manager():
    """Validate WebSocket manager."""
    print("\n" + "=" * 60)
    print("Testing WebSocket Manager")
    print("=" * 60)

    manager = ConnectionManager()

    assert manager.get_connection_count() == 0
    print("✓ Manager initialized")

    # Test broadcasting (no connections)
    await manager.broadcast({"type": "test", "data": "hello"})
    print("✓ Broadcasting works (no connections)")

    print("✓ WebSocket manager ready")


async def main():
    """Run all validation tests."""
    print("\n")
    print("🎃" * 30)
    print("SCARE BOX BACKEND VALIDATION")
    print("🎃" * 30)

    try:
        # Run tests
        validate_config()
        validate_event_logger()
        await validate_state_machine()
        await validate_websocket_manager()

        print("\n" + "=" * 60)
        print("✅ ALL VALIDATION TESTS PASSED")
        print("=" * 60)
        print("\nThe backend is ready for integration!")
        print("\nNext steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run tests: pytest")
        print("  3. Start server: uvicorn main:app --reload")
        print("\n")

        return 0

    except AssertionError as e:
        print("\n" + "=" * 60)
        print("❌ VALIDATION FAILED")
        print("=" * 60)
        print(f"\nError: {e}\n")
        return 1

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ UNEXPECTED ERROR")
        print("=" * 60)
        print(f"\nError: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))
