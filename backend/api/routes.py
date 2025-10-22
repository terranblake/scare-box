"""REST API routes for Scare Box."""

from fastapi import APIRouter, HTTPException, UploadFile, File
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
from pathlib import Path

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


@router.get("/devices/available")
async def get_available_devices():
    """Get list of available audio input and output devices."""
    import sounddevice as sd

    devices = sd.query_devices()
    input_devices = []
    output_devices = []

    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            input_devices.append({
                "id": i,
                "name": device['name'],
                "channels": device['max_input_channels'],
                "sample_rate": device['default_samplerate'],
            })
        if device['max_output_channels'] > 0:
            output_devices.append({
                "id": i,
                "name": device['name'],
                "channels": device['max_output_channels'],
                "sample_rate": device['default_samplerate'],
            })

    return {"microphones": input_devices, "speakers": output_devices}


@router.put("/devices/microphone")
async def set_microphone_device(request: dict):
    """Change the microphone device."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    device_name = request.get("device_name")
    if not device_name:
        raise HTTPException(status_code=400, detail="device_name required")

    # Reinitialize microphone with new device
    try:
        controller.microphone.stop_listening()
        controller.microphone.initialize(device_name)
        await controller.microphone.start_listening()

        return SuccessResponse(success=True, message=f"Microphone changed to {device_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/devices/speaker")
async def set_speaker_device(request: dict):
    """Change the speaker/audio output device."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    device_name = request.get("device_name")
    if not device_name:
        raise HTTPException(status_code=400, detail="device_name required")

    # Reinitialize speaker with new device
    try:
        import pygame

        # Quit current mixer
        pygame.mixer.quit()

        # Reinitialize with new device
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512, devicename=device_name)

        # Reload audio files
        controller.speaker._load_audio_files()

        print(f"Speaker changed to: {device_name}")

        return SuccessResponse(success=True, message=f"Speaker changed to {device_name}")
    except Exception as e:
        # Try to reinitialize with default device if change fails
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            controller.speaker._load_audio_files()
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/audio/upload/boo")
async def upload_boo_audio(file: UploadFile = File(...)):
    """Upload BOO audio file."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    # Validate file type
    if not file.filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="Only WAV files are supported")

    try:
        # Get audio directory
        audio_dir = Path(__file__).parent.parent / "audio"
        audio_dir.mkdir(exist_ok=True)

        # Save file
        file_path = audio_dir / "boo.wav"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Reload audio files
        controller.speaker._load_audio_files()

        return SuccessResponse(success=True, message="BOO audio uploaded successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/audio/upload/happy-halloween")
async def upload_happy_halloween_audio(file: UploadFile = File(...)):
    """Upload Happy Halloween audio file."""
    if not controller:
        raise HTTPException(status_code=500, detail="Controller not initialized")

    # Validate file type
    if not file.filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="Only WAV files are supported")

    try:
        # Get audio directory
        audio_dir = Path(__file__).parent.parent / "audio"
        audio_dir.mkdir(exist_ok=True)

        # Save file
        file_path = audio_dir / "happy_halloween.wav"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Reload audio files
        controller.speaker._load_audio_files()

        return SuccessResponse(success=True, message="Happy Halloween audio uploaded successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
