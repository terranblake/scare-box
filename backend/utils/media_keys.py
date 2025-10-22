"""macOS media key control to pause/play system audio."""

import subprocess


def send_play_pause():
    """Send play/pause media key command (pauses all audio)."""
    # Use osascript to simulate pressing play/pause key
    script = """
    tell application "System Events"
        key code 16 using {control down, command down}
    end tell
    """
    try:
        subprocess.run(['osascript', '-e', script],
                      check=False,
                      capture_output=True,
                      timeout=1)
        return True
    except:
        return False


def pause_all_media():
    """Pause all system media playback."""
    print("📻 Sending media PAUSE key...")
    # Send play/pause - if something is playing, this pauses it
    send_play_pause()


def resume_all_media():
    """Resume all system media playback."""
    print("📻 Sending media PLAY key...")
    # Send play/pause again - if paused, this resumes it
    send_play_pause()
