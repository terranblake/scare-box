"""Control Chrome's built-in media controls."""

from pynput.keyboard import Key, Controller

def click_chrome_media_button():
    keyboard = Controller()
    
    # Press play/pause media key to pause
    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)


def pause_chrome_media():
    """Pause all Chrome media by clicking the media control button."""
    print("⏸️  Pausing Chrome media...")
    return click_chrome_media_button()


def resume_chrome_media():
    """Resume all Chrome media by clicking the media control button again."""
    print("▶️  Resuming Chrome media...")
    return click_chrome_media_button()