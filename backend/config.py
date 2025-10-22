"""Configuration management for Scare Box."""

from typing import List, Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import yaml
from pathlib import Path


class AudioConfig(BaseModel):
    """Audio processing configuration."""
    trigger_frequency_min: float = 800.0
    trigger_frequency_max: float = 1200.0
    trigger_amplitude_threshold: float = 0.3
    sample_rate: int = 44100
    chunk_size: int = 1024


class TimingConfig(BaseModel):
    """Timing configuration for scare sequences."""
    countdown_duration: float = 3.0
    active_duration: float = 2.0
    reset_duration: float = 5.0
    scream_delay: float = 2.0


class HardwareConfig(BaseModel):
    """Hardware device configuration."""
    microphone_device: Optional[str] = None
    speaker_address: Optional[str] = None
    lifx_devices: List[str] = []


class IntensityLevel(BaseModel):
    """Intensity settings for a mode."""
    brightness: float = 1.0
    volume: float = 1.0


class IntensityConfig(BaseModel):
    """Intensity configuration for different modes."""
    child: IntensityLevel = IntensityLevel(brightness=0.6, volume=0.5)
    adult: IntensityLevel = IntensityLevel(brightness=1.0, volume=1.0)


class ServerConfig(BaseModel):
    """Server configuration."""
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]


class Config(BaseSettings):
    """Main configuration class."""
    mode: str = "child"
    audio: AudioConfig = AudioConfig()
    timing: TimingConfig = TimingConfig()
    hardware: HardwareConfig = HardwareConfig()
    intensity: IntensityConfig = IntensityConfig()
    server: ServerConfig = ServerConfig()

    @classmethod
    def load_from_file(cls, config_path: str = "config.yaml") -> "Config":
        """Load configuration from YAML file."""
        path = Path(config_path)
        if not path.exists():
            return cls()

        with open(path) as f:
            data = yaml.safe_load(f)

        return cls(**data)

    def save_to_file(self, config_path: str = "config.yaml"):
        """Save configuration to YAML file."""
        with open(config_path, "w") as f:
            yaml.safe_dump(self.model_dump(), f, default_flow_style=False)


# Global config instance
config = Config.load_from_file()
