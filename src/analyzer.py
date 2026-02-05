import os
import base64
import requests
import json
from .config import Config

class DarknessAnalyzer:
    def __init__(self):
        self._load_prompt()

    def _load_prompt(self):
        prompt_path = os.path.join("prompts", "dpdp_enforcer.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.prompt_template = f.read()
            print(f"📄 Loaded DPDP Enforcer prompt from {prompt_path}")
        except Exception as e:
            print(f"⚠️ Could not load prompt file: {e}")
            self.prompt_template = "Analyze this UI for DPDP Violations. Return JSON with {actor, request, necessity_check, verdict, section_6_status}."

    def analyze(self, image_path):
        if not Config.OPENROUTER_API_KEY:
            return {"error": "API Key Missing", "score": 0}
            
        if not os.path.exists(image_path):
            return {"error": "Screenshot not found"}

        try:
            from PIL import Image
            from io import BytesIO
            
            with Image.open(image_path) as img:
                img.thumbnail((800, 1600)) 
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                b64_img = base64.b64encode(buffered.getvalue()).decode('utf-8')

            headers = {
                "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://droidrun.ai",
                "X-Title": "Dead Hand"
            }
            
            data = {
                "model": Config.MODEL_NAME,
                "messages": [{"role": "user", "content": [
                    {"type": "text", "text": self.prompt_template},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}}
                ]}],
                "response_format": {"type": "json_object"}
            }

            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions", 
                headers=headers, 
                json=data,
                timeout=30 
            )
            
            if resp.status_code == 200:
                content = resp.json()['choices'][0]['message']['content']
                parsed = json.loads(content)
                if isinstance(parsed, list): parsed = parsed[0]
                return parsed
            else:
                return {"error": f"API Error {resp.status_code}", "score": 0}

        except Exception as e:
            return {"error": str(e), "score": 0}