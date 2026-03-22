# CODEVAULT - Unified Multi-Agent System Dictionary

## 🎯 Purpose
This repository serves as the **central dictionary and orchestrator** for a complex multi-agent system spanning multiple drives (J:, K:, L:). It contains reusable math libraries, CLI tools, and configuration that unifies 33 agents, MFish predictor, CONDUCTOR RAG, NEMO-Ralph multimodal, and USB skill injection.

## 📂 System Overview

### Drive Structure
```
J: DRIVE (Execution Engine)
├── CONDUCTOR/           # Multi-LLM RAG Framework
├── nemo-workspace/     # NEMO Council Configuration
├── .skills/           # NEMO-Ralph Multimodal Formation
├── Conduit-UI-JET-v12/ # UI Framework
└── [various AI tools]

K: DRIVE (Logic DNA)
├── .obsidian/         # Knowledge Graph
├── dev-tools/         # Development utilities
├── opencode-main/     # OpenCode projects
└── [system files]

L: DRIVE (Swarm Memory)
└── [to be mapped]
```

### Core Components

1. **33-Agent Swarm** - Independent prediction/execution agents
2. **MFish Predictor** - Universal swarm intelligence engine
3. **CONDUCTOR RAG** - Multi-LLM routing framework
4. **NEMO-Ralph** - Multimodal agent formation
5. **USB Skill Injection** - Hardware as modular capabilities
6. **5-key + 13-key Inputs** - Physical trigger system

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/Neutro916/Junk.git
cd Junk
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Scan System
```bash
python scan_system.py --analyze
```

### 4. Start Unified Dispatcher
```bash
python unified_dispatcher.py --start-all
```

## 🔧 Core Tools

### `unified_dispatcher.py`
Central event bus connecting all 33 agents. Features:
- Real-time agent monitoring
- USB device detection & skill injection
- Predictor-RAG integration
- Consensus scoring system

### `math_reuse_library.py`
Reusable mathematical patterns from across drives:
- 3-6-9 vortex mathematics
- Geometric pattern recognition
- Frequency analysis (83.33Hz base)
- Consensus algorithms

### `skill_tree_visualizer.py`
Interactive visualization of:
- Agent relationships
- USB device capabilities
- Skill dependencies
- Performance metrics

### `drive_mapper.py`
Creates unified symlink core:
```python
# Creates logical mapping without moving files
# J: → /execution_engine
# K: → /logic_dna  
# L: → /swarm_memory
```

## 🎮 Usage Examples

### Query Agent System
```python
from unified_dispatcher import UnifiedDispatcher

dispatcher = UnifiedDispatcher()
result = dispatcher.query(
    "Predict market impact of policy change",
    agents=["MFish", "CONDUCTOR", "NEMO"],
    use_rag=True
)
```

### Inject USB Skill
```python
from skill_injector import SkillInjector

injector = SkillInjector()
injector.detect_usb_devices()
# USB labeled "RESEARCH" → adds #signal-intelligence skill
# ESP32-C6 → adds #hardware-security skill
```

### Visualize System
```bash
python skill_tree_visualizer.py --live
# Opens web UI at http://localhost:8080
```

## 📊 System Architecture

```
┌─────────────────────────────────────────┐
│         UNIFIED DISPATCHER              │
├───────────┬───────────┬─────────────────┤
│  AGENTS   │   RAG     │   PREDICTOR     │
│  (33)     │ (CONDUCTOR)│   (MFish)      │
├───────────┼───────────┼─────────────────┤
│   USB     │   SKILL   │   VISUAL        │
│  DEVICES  │   TREE    │   ANALYZER      │
└───────────┴───────────┴─────────────────┘
            │
┌───────────▼───────────┐
│   CENTRAL EVENT BUS   │
│   • Real-time events  │
│   • Consensus scoring │
│   • Skill injection   │
└───────────────────────┘
```

## 🔐 Security Notes

- **API Keys**: Stored in environment variables only
- **Local First**: Works offline with Ollama/DeepSeek
- **Hardware Auth**: ESP32-C6 FIDO2 integration optional
- **No Cloud Required**: All components run locally

## 📈 Performance

### Alienware 24GB RAM
- 33 agents: ~8GB RAM
- MFish predictor: ~4GB RAM  
- CONDUCTOR RAG: ~2GB RAM
- NEMO-Ralph: ~3GB RAM
- **Total**: ~17GB RAM (72% utilization)

### uConsole (ARM)
- Reduced agent count: 15 agents
- Memory-optimized models
- Docker container limits
- Hardware acceleration

## 🤝 Contributing

This is a living dictionary of reusable patterns. Add:

1. **Math patterns** from your research
2. **CLI tools** that work across systems
3. **Agent configurations** for specific tasks
4. **Integration scripts** for new hardware

## 📄 License

MIT - Same as upstream projects (Llama Index, Ollama, LangChain)

## 🔗 Related Projects

- [MFish-great](https://github.com/Neutro916/MFish-great) - Swarm intelligence engine
- [NEMO-Ralph](J:\.skills\nemo-ralph) - Multimodal formation
- [CONDUCTOR](J:\CONDUCTOR) - Multi-LLM RAG framework
- [OpenCode](K:\opencode-main) - Developer environment

---

**Built as the "One Folder" source of truth for a fragmented multi-drive AI system.**