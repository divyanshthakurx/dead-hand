# agent/main.py
import os
import yaml
import asyncio
import json
from datetime import datetime
from droidrun import DroidAgent, DroidrunConfig
from agent.prompts import get_context_prompt
from agent.detector import analyze_screenshot

# Load Secrets
def load_secrets():
    with open("config/secrets.yaml", "r") as f:
        return yaml.safe_load(f)['user_profile']

async def main():
    # 1. Get Dynamic User Input
    print("💀 WELCOME TO DEAD HAND 💀")
    task_prompt = input("Enter your mission (e.g., 'Cancel my Audible sub'): ")
    
    user_data = load_secrets()
    
    # 2. Configure DroidRun
    # We mix the user's task with our context prompt (secrets)
    full_instruction = f"{task_prompt}\n\nCONTEXT:\n{get_context_prompt(user_data)}"
    
    config = DroidrunConfig()
    config.provider = "OpenRouter"
    config.model = "google/gemini-2.0-flash-001" # Use stable paid model for actions
    
    agent = DroidAgent(goal=full_instruction, config=config)
    
    # 3. Initialize Audit Log
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = f"trajectories/run_{run_id}"
    os.makedirs(log_dir, exist_ok=True)
    audit_log = []

    print(f"🚀 Dead Hand Started... (Log: {log_dir})")
    
    # 4. Custom Execution Loop (The "Step-by-Step" Hook)
    # Instead of agent.run(), we step manually to inject our detector
    max_steps = 15
    for i in range(max_steps):
        print(f"\n--- Step {i+1} ---")
        
        # A. Execute one step
        step_result = await agent.step() 
        
        # B. Capture state
        screenshot_path = f"{log_dir}/step_{i}.png"
        # (Assuming DroidRun saves latest screenshot to a temp path, we copy it)
        # For Hackathon speed: Just instruct DroidRun to save locally or use its internal buffer
        # Here we assume agent.last_screenshot exists (pseudo-code depending on DroidRun internal API)
        # If DroidRun doesn't expose it easily, rely on the trajectories folder it creates automatically.
        
        # C. Run Dark Pattern Detector
        # (We simulate getting the path from DroidRun's trajectory folder)
        # In reality, DroidRun saves to a timestamp folder. You might need to find the latest file.
        print("🔍 Scanning for Dark Patterns...")
        
        # -- SIMULATION FOR DEMO CODE --
        # Pass the actual screenshot path here once generated
        # audit_result = analyze_screenshot(screenshot_path)
        
        # Placeholder for valid code structure:
        audit_result = {
            "step": i,
            "darkness_score": 0, # Replaced by actual detector call
            "analysis": "Pending integration with live screenshot path"
        }
        
        audit_log.append(audit_result)
        
        # Save Audit Log
        with open(f"{log_dir}/audit_report.json", "w") as f:
            json.dump(audit_log, f, indent=2)

        if step_result.is_done:
            print("✅ Mission Complete")
            break

if __name__ == "__main__":
    asyncio.run(main())