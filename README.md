# Scare Box

> An overhaul of the traditional trick-or-treat experience

A web-controlled Halloween scare system with synchronized audio, lighting, and atmospheric effects. Control everything from your phone or laptop with real-time monitoring and manual triggers.

https://github.com/user-attachments/assets/0cce78f0-bcf4-485d-9ef2-c15b00aa6448

[![Tests](https://img.shields.io/badge/tests-18%20passed-brightgreen)]() [![Python](https://img.shields.io/badge/python-3.9+-blue)]() [![TypeScript](https://img.shields.io/badge/typescript-5.2+-blue)]()

## Overview

Scare Box is a self-contained shipping box that includes several components to enhance the "scare factor" of trick-or-treating by including visual, auditory, and atmospheric effects.

The box and its components include 2 settings: one for children (less scary) and a second for adults (full intensity). Both settings use a suite of components to produce an honest scare for those who dare take more than one treat, or if they're simply too loud.

## Hardware Components

- **Fog Machine** - With its output directed into the shipping box, filling the container and spilling out of the gap in the lid and through randomly placed holes in the box. Controlled by a set timer
- **LIFX Light Bars** - Producing lighting effects to draw in trick-or-treaters, highlighting the fog as it escapes the container, and producing the visual trick component. Controlled by the laptop via WiFi
- **USB-C Microphone** - Listens for ambient sound to determine when to initiate the trick. Uses FFT analysis to detect specific frequencies (metallic hinge sounds). Controlled by the laptop
- **Bluetooth Speaker** - Produces auditory "siren songs" to draw in trick-or-treaters, switching to a loud BOO when triggered. Controlled by the laptop
- **Laptop** - Orchestrates the complete experience, running the backend server and controlling all components

The treat component is housed inside the container at knee height for an average adult.

### Operation

At all times, a fog machine introduces atmospheric effects into the box to hide the internal components from view, while the microphone is always listening. Spooky?!

#### Non-trick

 Music is played through the speaker that matches the tone of halloween, lights are a calming, but bright pattern which react to the music being played.

 #### Trick

 When noise is detected on a frequency matched with the hinges of the box opening, or manually triggered, a timer is started. As the timer ticks down, the lights start to "glitch" and the audio becomes distorted. Once the timer ends, the music and lights are stopped abruptly, then a loud boo and flash of lights is played, followed by a HAPPY HALLOWEEN. The system then resets back to normal operation using a timer, reversing the distortion to the audio.

 ### Modes

 #### Child

 Softer, less scary trick. Mostly just flashing lights

 #### Adult

 Full output, brightness/audio/woofer, much scarier trick. Meant to actually scare you.

 ### Configuration

 - Manual trigger of trick or non-trick operation
 - Configuration of randomness in non-trick to trick switch
 - Manual switch of child to adult mode
 - Configuration of non-trick to trick delay (may want to delay longer for larger groups holding the lid open)
 - Configuration of trick to non-trick reset timing

## Quick Start

### One Command to Start Everything

```bash
./start.sh
```

This will:
- Install dependencies (if needed)
- Start backend on http://localhost:8000
- Start frontend on http://localhost:3000
- Show live logs
- Press Ctrl+C to stop

### Select Audio Device (Optional)

```bash
source backend/venv/bin/activate
python3 list-devices.py
```

Then edit `backend/config.yaml` to set your preferred microphone:
```yaml
hardware:
  microphone_device: "Your Device Name"
```

### Run Tests

```bash
cd backend
source venv/bin/activate
pytest  # 18/18 tests passing
```

## Architecture

- **Backend**: FastAPI server with REST API, WebSocket streaming, hardware controllers, state machine, event logging
- **Frontend**: React + TypeScript dashboard with real-time updates, controls, and monitoring
- **Hardware**: USB-C microphone, LIFX lights (WiFi), Bluetooth speaker
- **Tests**: Comprehensive unit tests that work without hardware
