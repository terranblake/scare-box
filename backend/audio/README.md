# Audio Files for Scare Box

Place your audio files in this directory:

## Required Files

### 1. `boo.wav`
The BOO sound effect that plays when the scare is triggered.

**Recommendations**:
- Format: WAV (for low latency)
- Duration: 1-3 seconds
- Content: Loud "BOO!" or scream
- Volume: Loud and clear

### 2. `happy_halloween.wav`
The friendly message that plays after the scare.

**Recommendations**:
- Format: WAV (for low latency)
- Duration: 2-5 seconds
- Content: "HAPPY HALLOWEEN!" greeting
- Volume: Cheerful and clear

## Audio Sequence

When triggered:
1. **BOO sound plays** (interrupts your ambient music)
2. **2 second delay** for screams/reactions (configurable in `config.yaml`)
3. **Happy Halloween plays**
4. Your ambient music continues naturally

## Ambient Music

You control ambient music yourself! Play whatever you want through:
- Soundcloud
- Spotify
- YouTube
- iTunes/Music app
- Any other music player

Just make sure your **Bluetooth speaker is set as the system default output** in:
**macOS System Settings > Sound > Output**

## Creating/Finding Audio

### Option 1: Record Your Own
```bash
# Record on Mac using QuickTime
# File > New Audio Recording
# Then export as .wav
```

### Option 2: Text-to-Speech
```bash
# macOS built-in TTS
say -v "Daniel" "BOO!" -o boo.aiff
ffmpeg -i boo.aiff boo.wav

say -v "Samantha" "Happy Halloween!" -o happy_halloween.aiff
ffmpeg -i happy_halloween.aiff happy_halloween.wav
```

### Option 3: Download Free Sound Effects
- [Freesound.org](https://freesound.org)
- [Zapsplat.com](https://www.zapsplat.com)
- Search for: "boo sound effect", "halloween greeting"

## Testing Your Audio

Start the system and trigger manually to test:
```bash
curl -X POST http://localhost:8000/api/trigger
```

You should hear:
1. BOO sound
2. 2 second pause
3. Happy Halloween sound

## Configuration

Adjust the scream delay in `backend/config.yaml`:
```yaml
timing:
  scream_delay: 2.0  # Delay between BOO and HAPPY HALLOWEEN (seconds)
```
