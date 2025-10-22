# Scare Box Implementation Plan

## Overview
A web-based Halloween trick-or-treat experience controller with real-time monitoring, configuration, and manual control accessible from any device (phone, tablet, laptop).

## Architecture

### Backend Service (Python)
- **Framework**: FastAPI (async, WebSocket support, modern)
- **Core Components**:
  - Hardware abstraction layer for USB-C microphone, LIFX lights, Bluetooth speaker
  - State machine for trick sequence orchestration
  - Real-time audio processing (FFT analysis for trigger detection)
  - Event system for logging and notifications
  - WebSocket server for live data streaming

### Frontend Application (Web)
- **Framework**: React with TypeScript
- **Styling**: Tailwind CSS (clean, modern, minimalist)
- **Key Features**:
  - Real-time audio level visualization
  - Live light status and control
  - Event timeline with notifications
  - Mobile-responsive design
  - Dark theme optimized for outdoor/nighttime use

### Communication
- **REST API**: Configuration and control endpoints
- **WebSockets**: Real-time bidirectional streaming for:
  - Audio levels (microphone input)
  - Light states (LIFX bars)
  - System events (triggers, state changes)
  - Notifications (errors, warnings)

## Backend Structure

```
scare-box/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Configuration management
│   ├── state_machine.py         # Scare sequence orchestration
│   ├── hardware/
│   │   ├── microphone.py        # USB-C mic handler
│   │   ├── lifx_controller.py   # LIFX Light Bar control
│   │   └── speaker.py           # Bluetooth speaker control
│   ├── websocket/
│   │   ├── manager.py           # WebSocket connection manager
│   │   └── streams.py           # Data streaming handlers
│   ├── api/
│   │   ├── routes.py            # REST API endpoints
│   │   └── models.py            # Pydantic models
│   └── utils/
│       ├── audio_processing.py  # FFT and signal analysis
│       └── event_logger.py      # Event tracking system
```

## Frontend Structure

```
scare-box/
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Main application
│   │   ├── components/
│   │   │   ├── Dashboard.tsx    # Main control dashboard
│   │   │   ├── AudioMeter.tsx   # Real-time audio level display
│   │   │   ├── LightControl.tsx # Light status and control
│   │   │   ├── EventLog.tsx     # Event timeline
│   │   │   ├── ConfigPanel.tsx  # Settings and configuration
│   │   │   └── TriggerButton.tsx # Manual trigger control
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts  # WebSocket connection hook
│   │   │   └── useApi.ts        # REST API hook
│   │   └── types/
│   │       └── index.ts         # TypeScript definitions
│   └── package.json
```

## API Endpoints

### REST API

**Configuration**
- `GET /api/config` - Get current configuration
- `PUT /api/config` - Update configuration
- `GET /api/mode` - Get current mode (child/adult)
- `PUT /api/mode` - Set mode

**Control**
- `POST /api/trigger` - Manual trigger scare sequence
- `POST /api/start` - Start system
- `POST /api/stop` - Stop system
- `GET /api/state` - Get current system state

**Hardware Status**
- `GET /api/devices` - Get connected device list
- `GET /api/devices/lights` - LIFX Light Bar status
- `GET /api/devices/microphone` - Microphone status
- `GET /api/devices/speaker` - Speaker status

**Events**
- `GET /api/events` - Get event history (paginated)
- `GET /api/events/stats` - Get event statistics

### WebSocket Streams

**Connection**: `ws://[host]:8000/ws`

**Message Types** (Server → Client):

```json
{
  "type": "audio_level",
  "data": {
    "timestamp": 1234567890,
    "rms": 0.45,
    "peak": 0.78,
    "frequency_peak": 950.5
  }
}
```

```json
{
  "type": "light_status",
  "data": {
    "timestamp": 1234567890,
    "devices": [
      {
        "id": "d073d5123456",
        "name": "Light Bar 1",
        "power": true,
        "brightness": 0.8,
        "color": {"hue": 30, "saturation": 0.9}
      }
    ]
  }
}
```

```json
{
  "type": "event",
  "data": {
    "timestamp": 1234567890,
    "level": "info",
    "category": "trigger",
    "message": "Scare sequence triggered",
    "details": {"trigger_type": "audio", "confidence": 0.95}
  }
}
```

```json
{
  "type": "state_change",
  "data": {
    "timestamp": 1234567890,
    "from": "NON_TRICK",
    "to": "TRICK_COUNTDOWN",
    "countdown_remaining": 3.0
  }
}
```

```json
{
  "type": "notification",
  "data": {
    "timestamp": 1234567890,
    "level": "warning",
    "title": "Speaker Disconnected",
    "message": "Bluetooth speaker connection lost"
  }
}
```

## Web Interface Layout

### Main Dashboard (Single Page)

```
┌─────────────────────────────────────────────────────────┐
│  🎃 SCARE BOX                    [Child Mode] [●Running] │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │ Audio Level │  │ Light Level │  │  [TRIGGER]      │ │
│  │             │  │             │  │   Manual        │ │
│  │   ▂▄▆█▆▄▂   │  │   ████      │  │   Activate      │ │
│  │   0.45 dB   │  │   80%       │  │                 │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Connected Devices                                   │ │
│  │  ✓ Microphone (USB-C)                              │ │
│  │  ✓ Light Bar 1, Light Bar 2 (WiFi)                │ │
│  │  ✓ Speaker (Bluetooth)                             │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Event Log                                           │ │
│  │  • 8:45 PM - Scare sequence complete                │ │
│  │  • 8:44 PM - Audio trigger detected (950Hz)        │ │
│  │  • 8:40 PM - Scare sequence complete                │ │
│  │  • 8:39 PM - Manual trigger activated               │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  [⚙ Settings] [📊 Statistics] [📋 Event History]        │
└─────────────────────────────────────────────────────────┘
```

### Settings Panel (Expandable/Modal)

- Mode selection (Child/Adult)
- Audio trigger sensitivity
- Countdown duration
- Light intensity multipliers
- Volume levels
- Frequency range configuration

## Technology Stack

### Backend
- **Python 3.11+**
- **FastAPI** - Web framework with WebSocket support
- **uvicorn** - ASGI server
- **lifxlan** - LIFX device control
- **pyaudio / sounddevice** - USB audio input
- **bleak** - Bluetooth communication
- **numpy** - Audio signal processing
- **pydantic** - Data validation

### Frontend
- **React 18+** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Socket.io-client** or native WebSocket - Real-time communication
- **React Query** - REST API state management

## Development Phases

### Phase 1: Backend Core
1. Set up FastAPI application structure
2. Implement hardware abstraction layer
3. Create state machine for scare sequences
4. Build REST API endpoints
5. Implement audio processing and trigger detection

### Phase 2: Real-time Streaming
1. Set up WebSocket infrastructure
2. Implement audio level streaming
3. Implement light status streaming
4. Create event logging and notification system
5. Build connection manager for multiple clients

### Phase 3: Frontend Application
1. Set up React + TypeScript + Tailwind project
2. Create main dashboard layout
3. Build real-time audio meter component
4. Build light control interface
5. Implement event log with live updates
6. Create settings panel

### Phase 4: Integration & Polish
1. Connect frontend to backend WebSocket streams
2. Implement REST API integration
3. Add error handling and reconnection logic
4. Optimize for mobile devices
5. Add dark theme and accessibility features

### Phase 5: Testing & Deployment
1. End-to-end testing with actual hardware
2. Performance optimization
3. Create deployment documentation
4. Build systemd service for auto-start
5. Set up local network access

## Deployment

### Running the System

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd frontend
npm install
npm run build
npm run preview  # or serve with nginx
```

### Access
- **Local**: `http://localhost:3000`
- **Network**: `http://[laptop-ip]:3000` (accessible from phone)

### System Service (Linux/macOS)
Create systemd service or launchd plist for automatic startup on boot.

## Configuration File Example

```yaml
# config.yaml
mode: child

audio:
  trigger_frequency_min: 800.0
  trigger_frequency_max: 1200.0
  trigger_amplitude_threshold: 0.3
  sample_rate: 44100

timing:
  countdown_duration: 3.0
  active_duration: 2.0
  reset_duration: 5.0

hardware:
  microphone_device: "USB Audio Device"
  speaker_address: "AA:BB:CC:DD:EE:FF"
  lifx_devices:
    - "Light Bar 1"
    - "Light Bar 2"

intensity:
  child:
    brightness: 0.6
    volume: 0.5
  adult:
    brightness: 1.0
    volume: 1.0
```

## Security Considerations

- WebSocket authentication (optional token-based)
- CORS configuration for frontend origin
- Rate limiting on trigger endpoint
- Input validation on all configuration updates
- No external internet exposure (local network only)

## Future Enhancements

- Multi-user support (multiple control devices)
- Scare statistics and analytics dashboard
- Custom sound effect uploads
- Light pattern customization
- Scheduled mode switching
- Integration with other smart home devices
- Mobile app (React Native)
