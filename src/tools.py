from droidrun.tools import Tool
from src.analyzer import DarknessAnalyzer
from droidrun.tools import AdbTools
import os
import json

analyzer = DarknessAnalyzer()
adb = AdbTools()

def check_for_dark_patterns(step_name: str) -> str:
    """
    Call this function to analyze the current screen for dark patterns.
    Args:
        step_name: A brief description of what you just did (e.g., "Opened Amazon").
    """
    # 1. Capture strict screenshot for analysis
    temp_path = "latest_analysis.png"
    adb.shell("screencap -p /data/local/tmp/analyze.png")
    adb.pull("/data/local/tmp/analyze.png", temp_path)
    
    # 2. Analyze
    result = analyzer.analyze(temp_path, step_name)
    
    # 3. Log to a local file for the dashboard
    log_entry = {
        "step": step_name,
        "result": result,
        "image": temp_path # In production, rename this with timestamp to keep history
    }
    
    try:
        with open("report.json", "r+") as f:
            data = json.load(f)
            data["steps"].append(log_entry)
            f.seek(0)
            json.dump(data, f)
    except FileNotFoundError:
        with open("report.json", "w") as f:
            json.dump({"steps": [log_entry]}, f)

    return f"Darkness Score: {result.get('score')}/10. Findings: {result.get('findings')}"

dark_pattern_tool = Tool(
    name="check_for_dark_patterns",
    description="Analyzes the current screen for dark patterns. Use this after every navigation action.",
    func=check_for_dark_patterns
)