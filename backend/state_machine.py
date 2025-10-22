"""State machine for scare sequence orchestration."""

import asyncio
from enum import Enum
from typing import Optional, Callable, List
from dataclasses import dataclass
import time


class State(Enum):
    """System operational states."""
    NON_TRICK = "non_trick"
    TRICK_COUNTDOWN = "trick_countdown"
    TRICK_ACTIVE = "trick_active"
    TRICK_RESET = "trick_reset"


class Mode(Enum):
    """Operating modes."""
    CHILD = "child"
    ADULT = "adult"


@dataclass
class StateChangeEvent:
    """State change event data."""
    timestamp: float
    from_state: State
    to_state: State
    countdown_remaining: Optional[float] = None


class StateMachine:
    """Manages state transitions and scare sequence timing."""

    def __init__(
        self,
        countdown_duration: float = 3.0,
        active_duration: float = 4.0,
        reset_duration: float = 5.0,
    ):
        self.countdown_duration = countdown_duration
        self.active_duration = active_duration
        self.reset_duration = reset_duration

        self.current_state = State.NON_TRICK
        self.current_mode = Mode.CHILD

        self.is_running = False
        self.sequence_task: Optional[asyncio.Task] = None

        self.state_change_callbacks: List[Callable[[StateChangeEvent], None]] = []

    def set_mode(self, mode: Mode):
        """Set operating mode."""
        self.current_mode = mode

    def get_state(self) -> State:
        """Get current state."""
        return self.current_state

    def get_mode(self) -> Mode:
        """Get current mode."""
        return self.current_mode

    def can_trigger(self) -> bool:
        """Check if trigger is allowed in current state."""
        return self.current_state == State.NON_TRICK

    async def trigger_sequence(self):
        """Trigger scare sequence if allowed."""
        if not self.can_trigger():
            print(f"Cannot trigger in state: {self.current_state.value}")
            return

        if self.sequence_task and not self.sequence_task.done():
            print("Sequence already running")
            return

        self.sequence_task = asyncio.create_task(self._run_sequence())

    async def _run_sequence(self):
        """Execute the complete scare sequence."""
        try:
            # Phase 1: Countdown
            await self._transition_to(State.TRICK_COUNTDOWN)
            await self._countdown_phase()

            # Phase 2: Active scare
            await self._transition_to(State.TRICK_ACTIVE)
            await asyncio.sleep(self.active_duration)

            # Phase 3: Reset
            await self._transition_to(State.TRICK_RESET)
            await asyncio.sleep(self.reset_duration)

            # Phase 4: Return to normal
            await self._transition_to(State.NON_TRICK)

        except asyncio.CancelledError:
            print("Sequence cancelled")
            await self._transition_to(State.NON_TRICK)

    async def _countdown_phase(self):
        """Execute countdown phase with progress updates."""
        steps = 20
        step_duration = self.countdown_duration / steps

        for step in range(steps):
            remaining = self.countdown_duration - (step * step_duration)

            # Notify listeners of countdown progress
            event = StateChangeEvent(
                timestamp=time.time(),
                from_state=self.current_state,
                to_state=self.current_state,
                countdown_remaining=remaining,
            )
            self._notify_state_change(event)

            await asyncio.sleep(step_duration)

    async def _transition_to(self, new_state: State):
        """Transition to new state and notify listeners."""
        old_state = self.current_state
        self.current_state = new_state

        event = StateChangeEvent(
            timestamp=time.time(),
            from_state=old_state,
            to_state=new_state,
        )

        self._notify_state_change(event)
        print(f"State: {old_state.value} -> {new_state.value}")

    def register_state_change_callback(
        self, callback: Callable[[StateChangeEvent], None]
    ):
        """Register callback for state changes."""
        self.state_change_callbacks.append(callback)

    def _notify_state_change(self, event: StateChangeEvent):
        """Notify all registered callbacks."""
        for callback in self.state_change_callbacks:
            try:
                # Handle both sync and async callbacks
                result = callback(event)
                if asyncio.iscoroutine(result):
                    asyncio.create_task(result)
            except Exception as e:
                print(f"Error in state change callback: {e}")

    def update_timing(
        self,
        countdown_duration: Optional[float] = None,
        active_duration: Optional[float] = None,
        reset_duration: Optional[float] = None,
    ):
        """Update timing configuration."""
        if countdown_duration is not None:
            self.countdown_duration = countdown_duration
        if active_duration is not None:
            self.active_duration = active_duration
        if reset_duration is not None:
            self.reset_duration = reset_duration

    async def stop(self):
        """Stop any running sequence and reset to normal."""
        if self.sequence_task and not self.sequence_task.done():
            self.sequence_task.cancel()
            await asyncio.sleep(0.1)

        await self._transition_to(State.NON_TRICK)
