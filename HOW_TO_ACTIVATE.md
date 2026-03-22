# 🚀 How to Activate the 33-Agent System

## Quick Start

### From Opencode Session:
```
# Clone the repository (if not already done)
git clone https://github.com/Neutro916/Junk.git
cd Junk

# Run activation command
python cmd/activate.py
```

### From Windows:
```bash
# Method 1: Batch file (easiest)
activate.bat

# Method 2: PowerShell
.\activate.ps1

# Method 3: Direct Python
python boot_sequence.py
```

### From Anywhere:
```bash
# Navigate to Junk directory first
cd C:\Users\natra\Junk
python cmd/activate.py
```

## What Gets Activated

When you run the activation command, the following systems start:

1. **Unified Dispatcher** - Central event bus for 33 agents
2. **Agent Swarm** - 33 specialized AI agents (predictors, executors, validators, etc.)
3. **USB Skill Monitor** - Auto-detects USB devices and injects skills
4. **Drive Mapping** - Creates logical view of J:/K:/L: drives
5. **Web Dashboard** - Visual interface at http://localhost:8080/dashboard.html
6. **External System Integration** - Connects to MFish, CONDUCTOR, NEMO-Ralph if present

## System Requirements

- **Python 3.11+** (will be installed if missing)
- **J: Drive** (Execution Engine) - Contains CONDUCTOR, NEMO-Ralph
- **K: Drive** (Logic DNA) - Contains Obsidian vault, dev tools  
- **L: Drive** (Swarm Memory) - Optional, for agent memory storage
- **Internet** - For downloading models (optional, works offline with Ollama)

## Available Commands After Activation

Once the system is running, you can:

### Query the Agent System
```bash
python query_system.py "What is the weather prediction for tomorrow?"
python query_system.py --agents predictor validator --query "Analyze this code"
```

### Check System Status
```bash
python query_system.py --status
python query_system.py --list-agents
python query_system.py --usb-scan
```

### Use the Web Dashboard
Open in browser: http://localhost:8080/dashboard.html

### Interactive Mode
Run `python cmd/activate.py` and choose from menu:
1. Full boot sequence
2. Dispatcher only  
3. Query system
4. Scan USB devices
5. Open dashboard
6. Exit

## Drive Structure

The system expects this drive layout:
```
J: (Execution Engine)
├── CONDUCTOR/          # Multi-LLM RAG framework
├── nemo-workspace/    # NEMO council config
├── .skills/          # NEMO-Ralph multimodal
└── Conduit-UI-JET-v12/ # UI framework

K: (Logic DNA)
├── .obsidian/        # Knowledge graph
├── dev-tools/        # Development utilities
└── opencode-main/    # OpenCode projects

L: (Swarm Memory) [Optional]
└── agent_memory/     # Long-term agent memory
```

## Troubleshooting

### "Python not found"
Install Python 3.11+ from https://python.org

### "J: drive not found"
The system will work without drives, but some features will be limited.

### "Module not found"
Run: `pip install -r requirements.txt`

### Dashboard not loading
Make sure boot sequence is running first.

## For uConsole Deployment

1. Copy the Junk directory to uConsole
2. Install Python 3.11+ on uConsole
3. Run: `python boot_sequence.py`
4. Access via uConsole browser: http://localhost:8080

## API Endpoints

Once running, these REST endpoints are available:

- `GET /api/health` - System health status
- `GET /api/agents` - List all agents
- `GET /api/usb-devices` - List USB devices
- `POST /api/query` - Query agent system

---

**Built as the unified activation point for your multi-drive, 33-agent AI system.**