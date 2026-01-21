import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME")
    TIMEOUT_SECONDS = 15     
    MAX_STEPS = 40
    CHECK_INTERVAL = 1.0     
    COOLDOWN_SECONDS = 2.0   
    
    RUN_ID = None 
    RUNS_DIR = os.path.join("data", "runs")
    
    @staticmethod
    def setup_run_dir():
        from datetime import datetime
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = os.path.join(Config.RUNS_DIR, run_id)
        os.makedirs(run_dir, exist_ok=True)
        return run_id, run_dir  