"""Tests for state machine."""

import pytest
import asyncio
from backend.state_machine import StateMachine, State, Mode


@pytest.mark.asyncio
async def test_state_machine_initialization():
    """Test state machine initializes correctly."""
    sm = StateMachine()

    assert sm.get_state() == State.NON_TRICK
    assert sm.get_mode() == Mode.CHILD
    assert sm.can_trigger() is True


@pytest.mark.asyncio
async def test_state_machine_mode_switching():
    """Test mode switching."""
    sm = StateMachine()

    sm.set_mode(Mode.ADULT)
    assert sm.get_mode() == Mode.ADULT

    sm.set_mode(Mode.CHILD)
    assert sm.get_mode() == Mode.CHILD


@pytest.mark.asyncio
async def test_state_machine_trigger_sequence():
    """Test full scare sequence."""
    sm = StateMachine(
        countdown_duration=0.1,
        active_duration=0.05,
        reset_duration=0.05,
    )

    states_seen = []

    def on_state_change(event):
        states_seen.append(event.to_state)

    sm.register_state_change_callback(on_state_change)

    # Trigger sequence
    await sm.trigger_sequence()

    # Wait for completion
    await asyncio.sleep(0.3)

    # Should have seen all states
    assert State.TRICK_COUNTDOWN in states_seen
    assert State.TRICK_ACTIVE in states_seen
    assert State.TRICK_RESET in states_seen
    assert State.NON_TRICK in states_seen

    # Should be back to NON_TRICK
    assert sm.get_state() == State.NON_TRICK


@pytest.mark.asyncio
async def test_state_machine_cannot_trigger_during_sequence():
    """Test that trigger is blocked during sequence."""
    sm = StateMachine(
        countdown_duration=0.2,
        active_duration=0.1,
        reset_duration=0.1,
    )

    # Start sequence
    await sm.trigger_sequence()

    # Immediately check - should not be able to trigger
    await asyncio.sleep(0.05)
    assert sm.can_trigger() is False

    # Wait for completion
    await asyncio.sleep(0.5)

    # Now should be able to trigger again
    assert sm.can_trigger() is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
