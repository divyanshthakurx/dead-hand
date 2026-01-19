# agent/detector.py
import os
import base64
import json
import requests
from agent.prompts import DETECTOR_SYSTEM_PROMPT

def analyze_screenshot(screenshot_path):
    """
    Sends the screenshot to OpenRouter (Gemini Flash) for a Dark Pattern Audit.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {"error": "No API Key found"}

    # Encode image
    with open(screenshot_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemini-2.0-flash-exp:free", # Use free for analysis to save cost
        "messages": [
            {
                "role": "system",
                "content": DETECTOR_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Audit this screen for dark patterns."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{encoded_string}"}
                    }
                ]
            }
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content']
        return json.loads(result)
    except Exception as e:
        print(f"⚠️ Detector Failed: {e}")
        return {"darkness_score": 0, "patterns_detected": [], "analysis": "Analysis Failed"}