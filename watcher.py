import time
import os
import json
import base64
import requests
import hashlib
import threading
import queue
from datetime import datetime
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL_NAME")
TIMEOUT_SECONDS = 15     
MAX_STEPS = 40
CHECK_INTERVAL = 1.0     
COOLDOWN_SECONDS = 2.0   

RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
RUN_DIR = os.path.join("data", "runs", RUN_ID)
os.makedirs(RUN_DIR, exist_ok=True)
REPORT_FILE = os.path.join(RUN_DIR, "report.json")

analysis_queue = queue.Queue()
file_lock = threading.Lock()

report_data = {
    "id": RUN_ID,
    "prompt": "Unnamed Mission",
    "start_time": str(datetime.now()),
    "steps": []
}

print(f"💀 Dead Hand Watcher Active | ID: {RUN_ID}")
mission_name = input("Enter mission name: ") or "Unnamed Mission"
report_data["prompt"] = mission_name

def get_screen_hash(image_path):
    """
    Creates a hash of the screen.
    Improvements:
    1. Crops the top 10% (Status bar/Clock) so time changes don't trigger capture.
    2. Converts to Grayscale to reduce noise.
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            
            crop_box = (0, int(height * 0.1), width, height)
            cropped = img.crop(crop_box)
            
            # Convert to grayscale ('L') and resize small
            small = cropped.convert('L').resize((32, 32)) 
            return hashlib.md5(small.tobytes()).hexdigest()
    except Exception:
        return "error"

def analyze_darkness_worker():
    """
    Background worker that silently processes images.
    """
    while True:
        item = analysis_queue.get()
        if item is None: break

        step_number, image_path = item

        try:
            # Resize for speed and API cost
            with Image.open(image_path) as img:
                img.thumbnail((800, 1600)) 
                from io import BytesIO
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                b64_img = base64.b64encode(buffered.getvalue()).decode('utf-8')

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://droidrun.ai",
                "X-Title": "Dead Hand"
            }
            
            prompt = "Analyze this UI for Dark Patterns. Return JSON with {score, findings, verdict}."
            
            data = {
                "model": MODEL,
                "messages": [{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}}
                ]}],
                "response_format": {"type": "json_object"}
            }

            resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            
            result = {"score": 0, "findings": ["Error"], "verdict": "Error"}
            if resp.status_code == 200:
                try:
                    content = resp.json()['choices'][0]['message']['content']
                    parsed = json.loads(content)
                    if isinstance(parsed, list): parsed = parsed[0]
                    result = parsed
                except:
                    pass
            
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

print(f"\n📊 Monitoring... (Auto-stop if screen static for {TIMEOUT_SECONDS}s)")

try:
    while True:
        
        time.sleep(CHECK_INTERVAL)
        
        temp_path = os.path.join(RUN_DIR, "temp_check.png")
        os.system(f"adb exec-out screencap -p > {temp_path}")
        
        if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
            continue

        try:
            current_hash = get_screen_hash(temp_path)
        except:
            continue

        if current_hash == last_hash:
            idle_timer += CHECK_INTERVAL
            
            remaining = TIMEOUT_SECONDS - idle_timer
            print(f"\r⏳ Idle: {int(idle_timer)}s | Auto-stop in {int(remaining)}s", end="")
            
            if idle_timer >= TIMEOUT_SECONDS:
                print("\n\n✅ Done. Screen static.")
                break
            continue
        
        idle_timer = 0
        last_hash = current_hash
        
        final_path = os.path.join(RUN_DIR, f"step_{step_count}.png")
        if os.path.exists(final_path): os.remove(final_path)
        os.rename(temp_path, final_path)
        
        print(f"\n📸 New Screen detected! (Step {step_count})")
        
        analysis_queue.put((step_count, final_path))
        
        step_count += 1
        
        # Wait here to let animations finish and prevent duplicate "mid-animation" grabs
        print(f"   ...cooling down for {COOLDOWN_SECONDS}s...")
        time.sleep(COOLDOWN_SECONDS) 

        if step_count > MAX_STEPS:
            print(f"\n🛑 Limit ({MAX_STEPS}) reached.")
            break

except KeyboardInterrupt:
    print("\n🛑 Stopped manually.")

remaining = analysis_queue.qsize()
if remaining > 0:
    print(f"📝 Finalizing {remaining} pending reports in background...")

analysis_queue.join() 
analysis_queue.put(None)
print(f"🏁 Report saved: {REPORT_FILE}")