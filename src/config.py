import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "google/gemini-2.0-flash-001")
    RUNS_DIR = os.path.join(os.getcwd(), "data", "runs")
    
    os.makedirs(RUNS_DIR, exist_ok=True)  