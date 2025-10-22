"""Browser audio control for macOS."""

import subprocess


class BrowserController:
    """Controls browser audio playback."""

    @staticmethod
    def mute_chrome():
        """Mute all Chrome tabs via JavaScript injection."""
        mute_script = '''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    try
                        execute t javascript "document.querySelectorAll('video, audio').forEach(el => el.muted = true);"
                    end try
                end repeat
            end repeat
        end tell
        '''
        try:
            subprocess.run(['osascript', '-e', mute_script],
                         capture_output=True,
                         timeout=2,
                         check=False)
            print("🔇 Muted Chrome tabs")
            return True
        except Exception as e:
            print(f"Chrome mute failed (may not be running): {e}")
            return False

    @staticmethod
    def unmute_chrome():
        """Unmute all Chrome tabs."""
        unmute_script = '''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    try
                        execute t javascript "document.querySelectorAll('video, audio').forEach(el => el.muted = false);"
                    end try
                end repeat
            end repeat
        end tell
        '''
        try:
            subprocess.run(['osascript', '-e', unmute_script],
                         capture_output=True,
                         timeout=2,
                         check=False)
            print("🔊 Unmuted Chrome tabs")
            return True
        except Exception as e:
            print(f"Chrome unmute failed: {e}")
            return False

    @staticmethod
    def mute_safari():
        """Mute Safari tabs."""
        mute_script = '''
        tell application "Safari"
            repeat with w in windows
                repeat with t in tabs of w
                    try
                        do JavaScript "document.querySelectorAll('video, audio').forEach(el => el.muted = true);" in t
                    end try
                end repeat
            end repeat
        end tell
        '''
        try:
            subprocess.run(['osascript', '-e', mute_script],
                         capture_output=True,
                         timeout=2,
                         check=False)
            print("🔇 Muted Safari tabs")
            return True
        except Exception as e:
            print(f"Safari mute failed (may not be running): {e}")
            return False

    @staticmethod
    def unmute_safari():
        """Unmute Safari tabs."""
        unmute_script = '''
        tell application "Safari"
            repeat with w in windows
                repeat with t in tabs of w
                    try
                        do JavaScript "document.querySelectorAll('video, audio').forEach(el => el.muted = false);" in t
                    end try
                end repeat
            end repeat
        end tell
        '''
        try:
            subprocess.run(['osascript', '-e', unmute_script],
                         capture_output=True,
                         timeout=2,
                         check=False)
            print("🔊 Unmuted Safari tabs")
            return True
        except Exception as e:
            print(f"Safari unmute failed: {e}")
            return False

    @staticmethod
    def mute_all_browsers():
        """Mute all supported browsers (Chrome, Safari)."""
        print("Muting all browser tabs...")
        BrowserController.mute_chrome()
        BrowserController.mute_safari()

    @staticmethod
    def unmute_all_browsers():
        """Unmute all supported browsers."""
        print("Unmuting all browser tabs...")
        BrowserController.unmute_chrome()
        BrowserController.unmute_safari()
