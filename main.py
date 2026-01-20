import asyncio
import os
from dotenv import load_dotenv

# DroidRun Imports
from droidrun import DroidAgent
from droidrun.config import DroidrunConfig
from droidrun.tools import load_tools

# Import our custom tool
from src.tools import dark_pattern_tool

load_dotenv()

async def run_dead_hand():
    # 1. Define the Goal with strict instructions
    user_prompt = "Open amazon app and search for realme buds t310 and add them to cart."
    
    system_instruction = """
    You are Dead Hand, an auditor agent.
    IMPORTANT: You must call the tool 'check_for_dark_patterns' after EVERY major UI change (like opening an app, clicking search, or viewing a product).
    Don't just navigate; audit the screen.
    """
    
    full_goal = f"{system_instruction}\n\nTask: {user_prompt}"

    # 2. Load Standard Tools (ADB, etc.)
    tools_list, _ = await load_tools()
    
    # 3. Add our Custom Tool
    tools_list.append(dark_pattern_tool)

    # 4. Configure Agent (Using OpenRouter/OpenAI compatible)
    # Note: DroidRun usually auto-detects from .env or config.yaml
    # We ensure it uses the CodeAct agent pattern which handles tools well.
    agent = DroidAgent(
        goal=full_goal,
        tools=tools_list,
        vision=True, # Let DroidRun see the screen too
    )

    print(f"💀 Starting Dead Hand Agent...")
    print(f"🎯 Goal: {user_prompt}")
    
    # 5. Run!
    await agent.run()

if __name__ == "__main__":
    asyncio.run(run_dead_hand())