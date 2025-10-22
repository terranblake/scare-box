export interface AudioData {
  timestamp: number;
  rms: number;
  peak: number;
  frequency_peak: number;
}

export interface LightDevice {
  id: string;
  name: string;
  power: boolean;
  brightness: number;
  color: {
    hue: number;
    saturation: number;
  };
}

export interface LightStatus {
  connected: boolean;
  device_count?: number;
  devices: LightDevice[];
}

export interface Event {
  timestamp: number;
  level: string;
  category: string;
  message: string;
  details: Record<string, any>;
}

export interface StateChange {
  timestamp: number;
  from: string;
  to: string;
  countdown_remaining?: number;
}

export interface Notification {
  timestamp: number;
  level: string;
  title: string;
  message: string;
}

export interface WebSocketMessage {
  type: 'audio_level' | 'light_status' | 'event' | 'state_change' | 'notification' | 'connected';
  data: AudioData | LightStatus | Event | StateChange | Notification | any;
}

export interface SystemState {
  state: string;
  mode: string;
  is_running: boolean;
  countdown_remaining?: number;
}

export interface DeviceStatus {
  microphone: {
    connected: boolean;
    listening: boolean;
  };
  lights: LightStatus;
  speaker: {
    connected: boolean;
    playing: boolean;
    volume: number;
  };
}

export interface Config {
  mode: string;
  audio: {
    trigger_frequency_min: number;
    trigger_frequency_max: number;
    trigger_amplitude_threshold: number;
    sample_rate: number;
  };
  timing: {
    countdown_duration: number;
    active_duration: number;
    reset_duration: number;
  };
}
