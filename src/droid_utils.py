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
        """Creates a hash of the screen (cropping status bar)."""
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                crop_box = (0, int(height * 0.1), width, height)
                
                small = img.crop(crop_box).convert('L').resize((32, 32)) 
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