"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import List, Optional


class ConfigUpdate(BaseModel):
    """Configuration update request."""
    mode: Optional[str] = None
    trigger_frequency_min: Optional[float] = None
    trigger_frequency_max: Optional[float] = None
    trigger_amplitude_threshold: Optional[float] = None
    countdown_duration: Optional[float] = None
    active_duration: Optional[float] = None
    reset_duration: Optional[float] = None
    scream_delay: Optional[float] = None


class ModeUpdate(BaseModel):
    """Mode change request."""
    mode: str = Field(..., pattern="^(child|adult)$")


class TriggerRequest(BaseModel):
    """Manual trigger request."""
    pass


class DeviceStatus(BaseModel):
    """Individual device status."""
    id: str
    name: str
    connected: bool
    details: dict = {}


class DevicesResponse(BaseModel):
    """All devices status response."""
    microphone: dict
    lights: dict
    speaker: dict


class StateResponse(BaseModel):
    """Current system state response."""
    state: str
    mode: str
    is_running: bool
    countdown_remaining: Optional[float] = None


class EventResponse(BaseModel):
    """Event data response."""
    timestamp: float
    level: str
    category: str
    message: str
    details: dict = {}


class EventsResponse(BaseModel):
    """List of events response."""
    events: List[EventResponse]
    total: int


class StatsResponse(BaseModel):
    """Event statistics response."""
    total_events: int
    by_level: dict
    by_category: dict


class SuccessResponse(BaseModel):
    """Generic success response."""
    success: bool
    message: str
