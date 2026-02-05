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
        Hashes a tiny, grayscale, cropped version of the screen.
        Ignores the Status Bar (top 8%) and small pixel changes (clock/battery).
        """
        try:
            with Image.open(image_path) as img:
                # 1. Convert to Grayscale to ignore color shifts
                gray = img.convert("L")
                
                # 2. Crop out the Status Bar (Top 8% of the screen)
                w, h = gray.size
                status_bar_height = int(h * 0.08)
                cropped = gray.crop((0, status_bar_height, w, h))
                
                # 3. Resize to a tiny thumbnail (16x32)
                # This makes it very blurry, ignoring small text changes like time.
                small = cropped.resize((16, 32), Image.Resampling.BILINEAR)
                
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