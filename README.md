# Dead Hand: The Dark Pattern Detective

<div align="center">

<img src="assets/dead-hand_logo.png" width="300" alt="Dead Hand Logo">
<br>

[![Built with Droidrun](https://img.shields.io/badge/Built_with-Droidrun-0D9373)](https://droidrun.ai)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## ✨ Overview

Dead Hand is a smart agent that acts as a "Dark Pattern Detective". It passively watches your screen, analyzes UI elements using AI, and detects manipulative design patterns (Dark Patterns) in real-time. It provides a detailed dashboard to review findings and protect users from digital deception.

https://github.com/user-attachments/assets/1bbe1755-742e-4075-add6-b11c23db396b

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/divyanshthakurx/dead-hand.git
cd dead-hand
pip install -r requirements.txt
```

### Configuration
1. Create a `.env` file in the root directory.
2. Add your OpenRouter API key and model:
```env
OPENROUTER_API_KEY=your_key_here
MODEL_NAME=google/gemini-2.0-flash-exp:free
```
3. Ensure your Android device is connected via ADB:
```bash
adb devices
```

### Basic Usage

1. **Start the Watcher**:
The watcher monitors your screen and analyzes it for dark patterns.
```bash
python watcher.py
```

2. **Run the Droidrun Agent**:
You can control your device using natural language prompts. Run the following command to initiate an agent session.
```bash
droidrun run "<task for the agent>" --provider <provider_name> --model <model_name> --steps <limit>
```

| Argument / Flag | Description | Examples |
| :--- | :--- | :--- |
| `<task>` | The natural language instruction for the agent. | `"Turn on Dark Mode"` |
| `--provider` | The AI provider backend to use. | `OpenRouter`, `OpenAI`, `Anthropic` |
| `--model` | The specific model ID for inference. | `google/gemini-2.0-flash` |
| `--steps` | Maximum number of actions the agent can take. | `10` |

3. **View the Dashboard**:
Explore the detected patterns and analysis reports.
```bash
streamlit run dashboard.py
```

## 📋 Features

- **Real-time Screen Monitoring**: Automatically captures screen state changes.
- **AI-Powered Analysis**: Uses VLM (Vision Language Models) to detect dark patterns.
- **Interactive Dashboard**: Visualize findings, darkness scores, and verdicts.
- **Smart De-duplication**: Avoids processing static screens to save resources.

## 🏗️ Architecture

- **Watcher (`watcher.py`)**: Handles ADB connection, screen capture, and hashing.
- **Analyzer (`src/analyzer.py`)**: Interfaces with the AI model to score UI darkness.
- **Dashboard (`dashboard.py`)**: A Streamlit app for reporting and visualization.

## 📁 Structure
```
dead-hand/
├── src/
│   ├── analyzer.py
│   ├── config.py
│   ├── droid_utils.py
│   └── logger.py
├── data/
├── assets/
├── prompts/
├── trajectories/
├── dashboard.py
├── watcher.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```


## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

## 👥 Team

**DroidTrex** - Google Developer Groups, IIT Patna  
**Repository**: https://github.com/divyanshthakurx/dead-hand.git

---

<div align="center">

A submission for Droidrun DevSprint 2026

</div>
