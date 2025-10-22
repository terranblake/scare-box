"""Browser audio control for macOS."""

import subprocess


class BrowserController:
    """Controls browser audio playback."""

    @staticmethod
    def pause_soundcloud():
        """Find and click Soundcloud's play/pause button."""
        script = '''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    try
                        set tabURL to URL of t
                        if tabURL contains "soundcloud.com" then
                            execute t javascript "
                                // Find the play/pause button
                                let playButton = document.querySelector('.playControl, .playControls__play, [title=\\"Pause current\\"], [title=\\"Play current\\"]');
                                if (playButton) {
                                    playButton.click();
                                    'CLICKED';
                                } else {
                                    'NOT FOUND';
                                }
                            "
                        end if
                    end try
                end repeat
            end repeat
        end tell
        '''
        try:
            result = subprocess.run(['osascript', '-e', script],
                                  capture_output=True,
                                  text=True,
                                  timeout=3,
                                  check=False)
            if 'CLICKED' in result.stdout:
                print("⏸️  Paused Soundcloud")
                return True
            else:
                print("⚠️  Soundcloud tab not found or button not found")
                return False
        except Exception as e:
            print(f"Soundcloud pause failed: {e}")
            return False

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
    def pause_youtube():
        """Find and pause YouTube videos."""
        script = '''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    try
                        set tabURL to URL of t
                        if tabURL contains "youtube.com" then
                            execute t javascript "
                                let video = document.querySelector('video');
                                if (video && !video.paused) {
                                    video.pause();
                                    'PAUSED';
                                } else {
                                    'NOT PLAYING';
                                }
                            "
                        end if
                    end try
                end repeat
            end repeat
        end tell
        '''
        try:
            result = subprocess.run(['osascript', '-e', script],
                                  capture_output=True,
                                  text=True,
                                  timeout=3,
                                  check=False)
            if 'PAUSED' in result.stdout:
                print("⏸️  Paused YouTube")
                return True
            return False
        except:
            return False

    @staticmethod
    def resume_youtube():
        """Resume YouTube videos."""
        script = '''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    try
                        set tabURL to URL of t
                        if tabURL contains "youtube.com" then
                            execute t javascript "
                                let video = document.querySelector('video');
                                if (video && video.paused) {
                                    video.play();
                                    'PLAYED';
                                }
                            "
                        end if
                    end try
                end repeat
            end repeat
        end tell
        '''
        try:
            result = subprocess.run(['osascript', '-e', script],
                                  capture_output=True,
                                  text=True,
                                  timeout=3,
                                  check=False)
            if 'PLAYED' in result.stdout:
                print("▶️  Resumed YouTube")
                return True
            return False
        except:
            return False

    @staticmethod
    def pause_all_music():
        """Pause all known music sites (Soundcloud, YouTube, etc)."""
        print("Pausing all music sites...")
        BrowserController.pause_soundcloud()
        BrowserController.pause_youtube()
        # Add more sites as needed

    @staticmethod
    def resume_all_music():
        """Resume all known music sites."""
        print("Resuming all music sites...")
        BrowserController.pause_soundcloud()  # Toggle (click play/pause again)
        BrowserController.resume_youtube()

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
