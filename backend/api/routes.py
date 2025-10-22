"""REST API routes for Scare Box."""

from fastapi import APIRouter, HTTPException
from .models import (
    ConfigUpdate,
    ModeUpdate,
    TriggerRequest,
    DevicesResponse,
    StateResponse,
    EventsResponse,
    StatsResponse,
    SuccessResponse,
    EventResponse,
)
from typing import Optional

router = APIRouter(prefix="/api")

# Global controller reference (set by main.py)
controller = None


def set_controller(ctrl):
    """Set the controller instance."""
    global controller
    controller = ctrl


@router.get("/config")
async def get_config():
    """Get current configuration."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    return controller.get_config()


@router.put("/config")
async def update_config(config: ConfigUpdate):
    """Update configuration."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    controller.update_config(config.model_dump(exclude_none=True))

    return SuccessResponse(success=True, message="Configuration updated")


@router.get("/mode")
async def get_mode():
    """Get current mode."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    return {"mode": controller.state_machine.get_mode().value}


@router.put("/mode")
async def set_mode(mode: ModeUpdate):
    """Set operating mode."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    controller.set_mode(mode.mode)

    return SuccessResponse(success=True, message=f"Mode set to {mode.mode}")


@router.post("/trigger")
async def manual_trigger(request: TriggerRequest = TriggerRequest()):
    """Manually trigger scare sequence."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    if not controller.state_machine.can_trigger():
        raise HTTPException(status_code=400, detail="Cannot trigger in current state")

    await controller.trigger_sequence()

    return SuccessResponse(success=True, message="Scare sequence triggered")


@router.post("/start")
async def start_system():
    """Start the Scare Box system."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    await controller.start()

    return SuccessResponse(success=True, message="System started")


@router.post("/stop")
async def stop_system():
    """Stop the Scare Box system."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    await controller.stop()

    return SuccessResponse(success=True, message="System stopped")


@router.get("/state")
async def get_state():
    """Get current system state."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    return StateResponse(
        state=controller.state_machine.get_state().value,
        mode=controller.state_machine.get_mode().value,
        is_running=controller.is_running,
    )


@router.get("/devices")
async def get_devices():
    """Get all device statuses."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    return DevicesResponse(
        microphone=controller.microphone.get_status(),
        lights=controller.lights.get_status(),
        speaker=controller.speaker.get_status(),
    )


@router.get("/devices/microphone")
async def get_microphone_status():
    """Get microphone status."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    return controller.microphone.get_status()


@router.get("/devices/lights")
async def get_lights_status():
    """Get lights status."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    return controller.lights.get_status()


@router.get("/devices/speaker")
async def get_speaker_status():
    """Get speaker status."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    return controller.speaker.get_status()


@router.get("/events")
async def get_events(limit: Optional[int] = 100):
    """Get event history."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    events = controller.event_logger.get_events(limit=limit)
    event_responses = [EventResponse(**event.to_dict()) for event in events]

    return EventsResponse(events=event_responses, total=len(events))


@router.get("/events/stats")
async def get_event_stats():
    """Get event statistics."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    stats = controller.event_logger.get_stats()

    return StatsResponse(**stats)
