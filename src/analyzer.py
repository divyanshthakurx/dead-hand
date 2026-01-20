import os
import base64
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class DarknessAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = "google/gemini-2.0-flash-001" 

    def analyze(self, image_path, context="Checking for dark patterns"):
        if not os.path.exists(image_path):
            return {"error": "Screenshot not found"}

        with open(image_path, "rb") as img:
            base64_image = base64.b64encode(img.read()).decode('utf-8')

        prompt = f"""
        You are 'Dead Hand'. Analyze this UI screenshot.
        Context: {context}
        
        Identify DARK PATTERNS:
        1. Forced Login / No Skip
        2. Hidden Costs / Pre-checked add-ons
        3. Countdown Timers (False Urgency)
        4. Hard to cancel subscriptions
        5. Visual Interference (Confusing X buttons)

        Return JSON:
        {{
            "score": <int 0-10, 10 is very dark>,
            "findings": ["finding 1", "finding 2"],
            "verdict": "Safe" or "Manipulative"
        }}
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]}
            ],
            "response_format": {"type": "json_object"}
        }

        try:
            resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            return json.loads(resp.json()['choices'][0]['message']['content'])
        except Exception as e:
            return {"error": str(e), "score": 0}