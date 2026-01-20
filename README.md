# Dead Hand: The Anti-Frustration Agent

<div align="center">

[![Built with Droidrun](https://img.shields.io/badge/Built_with-Droidrun-0D9373)](https://droidrun.ai)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## ✨ Overview

Dead Hand is an AI agent built on the Droidrun framework that automates complex mobile interactions through natural language. It helps users navigate frustrating app designs and streamline common tasks with simple commands.

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/divyanshthakurx/dead-hand.git
cd dead-hand
pip install -r requirements.txt
```

### Basic Usage
```python
from dead_hand import DeadHandAgent

# Initialize the agent
agent = DeadHandAgent(device_id="your_device_id")

# Execute commands
agent.execute_command("Cancel my Audible subscription")
agent.execute_command("Fill my passport info here")
agent.execute_command("Buy this laptop, avoid extras")
```

## 📋 Features

- **Subscription Management**: Handles cancellation flows for various services
- **Smart Form Filling**: Inputs data while maintaining privacy and context
- **Safe Shopping**: Navigates checkout processes and avoids unwanted additions
- **Cross-App Workflows**: Manages tasks that span multiple applications
- **UI Adaptation**: Responds to changing interfaces and unexpected dialogs

## 🏗️ Architecture

Built on Droidrun's automation capabilities with:
- LLM-based decision making
- Screen analysis and pattern recognition
- Multi-app context management
- Error recovery mechanisms

## 📁 Structure
```
dead-hand/
├── apps/              # Application-specific logic
├── core/              # Core agent functionality  
├── detectors/         # UI pattern detection
├── privacy/           # Privacy management
└── tests/             # Testing modules
```

## 🔧 Development

### Testing
```bash
pytest tests/
```

### Adding Support
1. Create app profile in `apps/your_app.py`
2. Define UI patterns and navigation
3. Add corresponding tests

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

## 👥 Team

**DroidTrex** - Google Developer Groups, IIT Patna  
**Repository**: https://github.com/divyanshthakurx/dead-hand.git

---

<div align="center">

A submission for Droidrun DevSprint 2026

</div>