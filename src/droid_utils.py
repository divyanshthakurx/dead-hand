import os
import time
import hashlib
from PIL import Image

class DeviceController:
    def __init__(self):
        pass 
        
    def capture_screen(self, path):
        """Captures the screen to the specified local path."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        os.system("adb shell screencap -p /data/local/tmp/screen.png")
        os.system(f"adb pull /data/local/tmp/screen.png {path}")
        return path

    def get_screen_hash(self, image_path):
        """
        Hashes a tiny, blurry version of the screen. 
        This ignores small changes like the Clock, Battery, or Blinking Cursors.
        """
        try:
            with Image.open(image_path) as img:
                # Resize to a small thumbnail (50 pixels wide)
                # This "blurs" away the time text so 12:00 and 12:01 look the same.
                small = img.resize((50, 100)) 
                return hashlib.md5(small.tobytes()).hexdigest()
        except Exception:
            return "error"

    def execute_action(self, action_data):
        """Executes the adb command."""
        command = action_data.get("command", "")
        if not command: return

        print(f"🤖 Executing: adb shell {command}")
        
        if "input text" in command:
            text_content = command.split("input text ")[-1]
            formatted_text = text_content.replace(" ", "%s").replace("'", "")
            os.system(f"adb shell input text {formatted_text}")
        else:
            os.system(f"adb shell {command}")
            
        time.sleep(2) 