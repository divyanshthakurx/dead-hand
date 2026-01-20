import os
import time

class DeviceController:
    def __init__(self):
        pass 
        
    def capture_screen(self, run_dir, step_index):
        filename = f"step_{step_index}.png"
        local_path = os.path.join(run_dir, filename)
        
        os.system("adb shell screencap -p /data/local/tmp/screen.png")
        os.system(f"adb pull /data/local/tmp/screen.png {local_path}")
        return local_path

    def execute_action(self, action_data):
        """
        Executes the command returned by the Navigator.
        Expected input: {"action_type": "tap", "command": "input tap 500 500"}
        """
        command = action_data.get("command", "")
        
        if not command:
            return

        print(f"🤖 Executing: adb shell {command}")
        
        if "input text" in command:
            text_content = command.split("input text ")[-1]
            formatted_text = text_content.replace(" ", "%s").replace("'", "")
            os.system(f"adb shell input text {formatted_text}")
        else:
            os.system(f"adb shell {command}")
            
        time.sleep(2) 