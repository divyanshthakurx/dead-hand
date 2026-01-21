import time
import os
import json
import threading
import queue
from datetime import datetime
from PIL import Image
from dotenv import load_dotenv

from src.config import Config
from src.analyzer import DarknessAnalyzer
from src.droid_utils import DeviceController

load_dotenv()

run_id, run_dir = Config.setup_run_dir()
REPORT_FILE = os.path.join(run_dir, "report.json")

analyzer = DarknessAnalyzer()
device = DeviceController()

analysis_queue = queue.Queue()
file_lock = threading.Lock()

report_data = {
    "id": run_id,
    "prompt": "Unnamed Mission",
    "start_time": str(datetime.now()),
    "steps": []
}

print(f"💀 Dead Hand Watcher Active | ID: {run_id}")
mission_name = input("Enter mission name: ") or "Unnamed Mission"
report_data["prompt"] = mission_name

def analyze_darkness_worker():
    """
    Background worker that silently processes images.
    """
    while True:
        item = analysis_queue.get()
        if item is None: break

        step_number, image_path = item

        try:
            result = analyzer.analyze(image_path)
            
            with file_lock:
                step_entry = {
                    "step": step_number,
                    "timestamp": str(datetime.now()),
                    "screenshot": image_path,
                    "analysis": result
                }
                report_data["steps"].append(step_entry)
                with open(REPORT_FILE, "w") as f:
                    json.dump(report_data, f, indent=4)

        except Exception:
            pass 
        finally:
            analysis_queue.task_done()

worker = threading.Thread(target=analyze_darkness_worker, daemon=True)
worker.start()

last_hash = None
step_count = 1
idle_timer = 0

print(f"\n📊 Monitoring... (Auto-stop if screen static for {Config.TIMEOUT_SECONDS}s)")

try:
    while True:
        
        time.sleep(Config.CHECK_INTERVAL)
        
        temp_path = os.path.join(run_dir, "temp_check.png")
        device.capture_screen(temp_path)
        
        if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
            continue

        current_hash = device.get_screen_hash(temp_path)
        if current_hash == "error":
            continue

        if current_hash == last_hash:
            idle_timer += Config.CHECK_INTERVAL
            
            remaining = Config.TIMEOUT_SECONDS - idle_timer
            print(f"\r⏳ Idle: {int(idle_timer)}s | Auto-stop in {int(remaining)}s", end="")
            
            if idle_timer >= Config.TIMEOUT_SECONDS:
                print("\n\n✅ Done. Screen static.")
                break
            continue
        
        idle_timer = 0
        last_hash = current_hash
        
        final_path = os.path.join(run_dir, f"step_{step_count}.png")
        if os.path.exists(final_path): os.remove(final_path)
        os.rename(temp_path, final_path)
        
        print(f"\n📸 New Screen detected! (Step {step_count})")
        
        analysis_queue.put((step_count, final_path))
        
        step_count += 1
        
        # Wait here to let animations finish and prevent duplicate "mid-animation" grabs
        print(f"   ...cooling down for {Config.COOLDOWN_SECONDS}s...")
        time.sleep(Config.COOLDOWN_SECONDS) 

        if step_count > Config.MAX_STEPS:
            print(f"\n🛑 Limit ({Config.MAX_STEPS}) reached.")
            break

except KeyboardInterrupt:
    print("\n🛑 Stopped manually.")

remaining = analysis_queue.qsize()
if remaining > 0:
    print(f"📝 Finalizing {remaining} pending reports in background...")

analysis_queue.join() 
analysis_queue.put(None)
print(f"🏁 Report saved: {REPORT_FILE}")