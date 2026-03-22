#!/usr/bin/env python3
"""
UNIFIED DISPATCHER - Central Event Bus for 33-Agent System

Connects:
- 33 prediction/execution agents
- MFish swarm predictor  
- CONDUCTOR RAG framework
- NEMO-Ralph multimodal formation
- USB skill injection
- 5-key + 13-key physical inputs

Provides single source of truth across J:, K:, L: drives.
"""

import asyncio
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
import threading
import queue

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentType(Enum):
    """Types of agents in the 33-agent swarm"""
    PREDICTOR = "predictor"
    EXECUTOR = "executor"
    VALIDATOR = "validator"
    OBSERVER = "observer"
    GHOST = "ghost"
    SHADOW = "shadow"
    MONK = "monk"
    ARCHITECT = "architect"
    NEMO = "nemo"
    RALPH = "ralph"

class EventType(Enum):
    """Event types for the central bus"""
    AGENT_START = "agent_start"
    AGENT_COMPLETE = "agent_complete"
    AGENT_ERROR = "agent_error"
    USB_DETECTED = "usb_detected"
    SKILL_INJECTED = "skill_injected"
    PREDICTION_REQUEST = "prediction_request"
    PREDICTION_RESULT = "prediction_result"
    RAG_QUERY = "rag_query"
    RAG_RESULT = "rag_result"
    KEY_PRESS = "key_press"
    CONSENSUS_UPDATE = "consensus_update"
    SYSTEM_HEALTH = "system_health"

@dataclass
class Agent:
    """Represents a single agent in the swarm"""
    id: str
    name: str
    agent_type: AgentType
    status: str = "inactive"
    capabilities: List[str] = field(default_factory=list)
    memory_usage: int = 0
    cpu_usage: float = 0.0
    last_active: float = field(default_factory=time.time)
    config_path: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.agent_type.value,
            "status": self.status,
            "capabilities": self.capabilities,
            "memory_usage": self.memory_usage,
            "cpu_usage": self.cpu_usage,
            "last_active": self.last_active
        }

@dataclass
class Event:
    """Event on the central bus"""
    event_id: str
    event_type: EventType
    source: str
    data: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    priority: int = 1  # 1=low, 5=critical
    
    def to_dict(self) -> Dict:
        return {
            "event_id": self.event_id,
            "type": self.event_type.value,
            "source": self.source,
            "data": self.data,
            "timestamp": self.timestamp,
            "priority": self.priority
        }

@dataclass
class USBDevice:
    """USB device for skill injection"""
    device_id: str
    vendor: str
    product: str
    serial: str
    drive_letter: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    detected_at: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            "device_id": self.device_id,
            "vendor": self.vendor,
            "product": self.product,
            "serial": self.serial,
            "drive_letter": self.drive_letter,
            "skills": self.skills,
            "detected_at": self.detected_at
        }

class UnifiedDispatcher:
    """Central dispatcher for the entire multi-agent system"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.agents: Dict[str, Agent] = {}
        self.usb_devices: Dict[str, USBDevice] = {}
        self.event_queue = queue.PriorityQueue()
        self.event_handlers: Dict[EventType, List[Callable]] = {}
        self.running = False
        self.consensus_score = 0.0
        self.system_health = "healthy"
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        self._init_event_handlers()
        
        logger.info(f"UnifiedDispatcher initialized with config: {self.config}")
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file or defaults"""
        default_config = {
            "max_agents": 33,
            "event_timeout": 30.0,
            "consensus_threshold": 0.7,
            "usb_poll_interval": 5.0,
            "health_check_interval": 10.0,
            "drive_mappings": {
                "J": "execution_engine",
                "K": "logic_dna", 
                "L": "swarm_memory"
            },
            "agent_types": [agt.value for agt in AgentType]
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
                    logger.info(f"Loaded config from {config_path}")
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
        
        return default_config
    
    def _init_event_handlers(self):
        """Initialize default event handlers"""
        self.register_handler(EventType.AGENT_START, self._handle_agent_start)
        self.register_handler(EventType.AGENT_COMPLETE, self._handle_agent_complete)
        self.register_handler(EventType.AGENT_ERROR, self._handle_agent_error)
        self.register_handler(EventType.USB_DETECTED, self._handle_usb_detected)
        self.register_handler(EventType.SKILL_INJECTED, self._handle_skill_injected)
        self.register_handler(EventType.PREDICTION_REQUEST, self._handle_prediction_request)
        self.register_handler(EventType.RAG_QUERY, self._handle_rag_query)
        self.register_handler(EventType.KEY_PRESS, self._handle_key_press)
        self.register_handler(EventType.SYSTEM_HEALTH, self._handle_system_health)
    
    def register_handler(self, event_type: EventType, handler: Callable):
        """Register an event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        logger.debug(f"Registered handler for {event_type.value}")
    
    def publish_event(self, event: Event):
        """Publish event to the central bus"""
        try:
            # Negative priority for correct ordering (higher priority = lower number)
            self.event_queue.put((-event.priority, time.time(), event))
            logger.debug(f"Published event: {event.event_type.value} from {event.source}")
        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
    
    async def start(self):
        """Start the dispatcher event loop"""
        if self.running:
            logger.warning("Dispatcher already running")
            return
        
        self.running = True
        logger.info("Starting UnifiedDispatcher...")
        
        # Start background tasks
        asyncio.create_task(self._event_processor())
        asyncio.create_task(self._usb_monitor())
        asyncio.create_task(self._health_monitor())
        
        # Load existing agents from drives
        await self._scan_existing_agents()
        
        logger.info(f"UnifiedDispatcher started with {len(self.agents)} agents")
    
    async def stop(self):
        """Stop the dispatcher"""
        self.running = False
        logger.info("Stopping UnifiedDispatcher...")
        
        # Stop all agents
        for agent_id, agent in self.agents.items():
            await self.stop_agent(agent_id)
        
        logger.info("UnifiedDispatcher stopped")
    
    async def _event_processor(self):
        """Process events from the queue"""
        logger.info("Event processor started")
        
        while self.running:
            try:
                # Get event with timeout
                priority, timestamp, event = self.event_queue.get(timeout=1.0)
                
                # Call handlers
                handlers = self.event_handlers.get(event.event_type, [])
                for handler in handlers:
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(event)
                        else:
                            handler(event)
                    except Exception as e:
                        logger.error(f"Handler error for {event.event_type.value}: {e}")
                
                self.event_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Event processor error: {e}")
    
    async def _usb_monitor(self):
        """Monitor for USB device changes"""
        logger.info("USB monitor started")
        
        while self.running:
            try:
                # Simulated USB detection - in real implementation would use platform-specific APIs
                await self._detect_usb_devices()
                
                # Wait for next poll
                await asyncio.sleep(self.config["usb_poll_interval"])
                
            except Exception as e:
                logger.error(f"USB monitor error: {e}")
                await asyncio.sleep(5.0)
    
    async def _health_monitor(self):
        """Monitor system health"""
        logger.info("Health monitor started")
        
        while self.running:
            try:
                health_data = await self._check_system_health()
                
                event = Event(
                    event_id=f"health_{int(time.time())}",
                    event_type=EventType.SYSTEM_HEALTH,
                    source="health_monitor",
                    data=health_data,
                    priority=2
                )
                self.publish_event(event)
                
                await asyncio.sleep(self.config["health_check_interval"])
                
            except Exception as e:
                logger.error(f"Health monitor error: {e}")
                await asyncio.sleep(5.0)
    
    async def _scan_existing_agents(self):
        """Scan drives for existing agent configurations"""
        logger.info("Scanning for existing agents...")
        
        # Check J: drive for NEMO-Ralph
        nemo_path = Path("J:/.skills/nemo-ralph")
        if nemo_path.exists():
            await self.register_agent(
                agent_id="nemo_ralph_01",
                name="NEMO-Ralph Multimodal",
                agent_type=AgentType.NEMO,
                capabilities=["multimodal", "vision", "consensus"],
                config_path=str(nemo_path)
            )
        
        # Check J: drive for CONDUCTOR
        conductor_path = Path("J:/CONDUCTOR")
        if conductor_path.exists():
            await self.register_agent(
                agent_id="conductor_01",
                name="CONDUCTOR RAG",
                agent_type=AgentType.ARCHITECT,
                capabilities=["rag", "multi_llm", "retrieval"],
                config_path=str(conductor_path)
            )
        
        # Check K: drive for OpenCode
        opencode_path = Path("K:/opencode-main")
        if opencode_path.exists():
            await self.register_agent(
                agent_id="opencode_01",
                name="OpenCode IDE",
                agent_type=AgentType.EXECUTOR,
                capabilities=["ide", "code_analysis", "git"],
                config_path=str(opencode_path)
            )
        
        logger.info(f"Found {len(self.agents)} existing agents")
    
    async def register_agent(self, agent_id: str, name: str, agent_type: AgentType, 
                           capabilities: List[str], config_path: Optional[str] = None):
        """Register a new agent"""
        agent = Agent(
            id=agent_id,
            name=name,
            agent_type=agent_type,
            capabilities=capabilities,
            config_path=config_path
        )
        
        self.agents[agent_id] = agent
        
        event = Event(
            event_id=f"agent_reg_{agent_id}",
            event_type=EventType.AGENT_START,
            source="dispatcher",
            data=agent.to_dict(),
            priority=3
        )
        self.publish_event(event)
        
        logger.info(f"Registered agent: {name} ({agent_type.value})")
        return agent
    
    async def stop_agent(self, agent_id: str):
        """Stop an agent"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent.status = "stopped"
            logger.info(f"Stopped agent: {agent.name}")
    
    async def query_agents(self, query: str, agent_types: Optional[List[AgentType]] = None,
                          use_rag: bool = False) -> Dict:
        """Query multiple agents and get consensus"""
        logger.info(f"Querying agents: {query}")
        
        # Filter agents by type
        target_agents = []
        for agent in self.agents.values():
            if agent_types is None or agent.agent_type in agent_types:
                target_agents.append(agent)
        
        if not target_agents:
            return {"error": "No agents available", "consensus": 0.0}
        
        # Create prediction request event
        event = Event(
            event_id=f"query_{int(time.time())}",
            event_type=EventType.PREDICTION_REQUEST,
            source="dispatcher",
            data={
                "query": query,
                "agent_ids": [a.id for a in target_agents],
                "use_rag": use_rag,
                "timestamp": time.time()
            },
            priority=4
        )
        self.publish_event(event)
        
        # Simulate response (in real implementation would wait for events)
        return {
            "query": query,
            "agents_queried": len(target_agents),
            "response": "Agent consensus processing initiated",
            "consensus": 0.5,  # Placeholder
            "timestamp": time.time()
        }
    
    async def _detect_usb_devices(self):
        """Detect USB devices (simulated)"""
        # In real implementation, would use platform-specific USB detection
        # For now, simulate detection based on drive letters
        
        drives = ["D:", "E:", "F:", "G:", "H:", "I:"]
        for drive in drives:
            drive_path = Path(drive)
            if drive_path.exists() and drive_path.is_dir():
                # Check if already registered
                device_id = f"usb_{drive.rstrip(':')}"
                if device_id not in self.usb_devices:
                    device = USBDevice(
                        device_id=device_id,
                        vendor="Unknown",
                        product="USB Drive",
                        serial=f"serial_{int(time.time())}",
                        drive_letter=drive,
                        skills=self._extract_usb_skills(drive_path)
                    )
                    
                    self.usb_devices[device_id] = device
                    
                    event = Event(
                        event_id=f"usb_{device_id}",
                        event_type=EventType.USB_DETECTED,
                        source="usb_monitor",
                        data=device.to_dict(),
                        priority=3
                    )
                    self.publish_event(event)
    
    def _extract_usb_skills(self, drive_path: Path) -> List[str]:
        """Extract skills from USB drive based on contents"""
        skills = []
        
        # Check for common patterns
        skill_patterns = {
            "RESEARCH": "#signal-intelligence",
            "AI_MODELS": "#ai-training",
            "CODE": "#development",
            "DATA": "#data-analysis",
            "HARDWARE": "#hardware-control",
            "ESP32": "#hardware-security",
            "SDR": "#radio-frequency"
        }
        
        for pattern, skill in skill_patterns.items():
            if (drive_path / pattern).exists() or pattern.lower() in drive_path.name.lower():
                skills.append(skill)
        
        # Default skill if none detected
        if not skills:
            skills.append("#storage")
        
        return skills
    
    async def _check_system_health(self) -> Dict:
        """Check overall system health"""
        active_agents = sum(1 for a in self.agents.values() if a.status == "active")
        total_agents = len(self.agents)
        
        health_score = (active_agents / max(total_agents, 1)) * 100
        
        # Update system health status
        if health_score >= 80:
            self.system_health = "healthy"
        elif health_score >= 50:
            self.system_health = "degraded"
        else:
            self.system_health = "critical"
        
        return {
            "health_score": health_score,
            "status": self.system_health,
            "active_agents": active_agents,
            "total_agents": total_agents,
            "usb_devices": len(self.usb_devices),
            "consensus_score": self.consensus_score,
            "timestamp": time.time()
        }
    
    # Event Handlers
    async def _handle_agent_start(self, event: Event):
        logger.info(f"Agent started: {event.data.get('name', 'unknown')}")
    
    async def _handle_agent_complete(self, event: Event):
        logger.info(f"Agent completed: {event.data.get('name', 'unknown')}")
    
    async def _handle_agent_error(self, event: Event):
        logger.error(f"Agent error: {event.data}")
    
    async def _handle_usb_detected(self, event: Event):
        device_data = event.data
        logger.info(f"USB detected: {device_data.get('product', 'unknown')} "
                   f"with skills: {device_data.get('skills', [])}")
        
        # Auto-inject skills
        skills = device_data.get('skills', [])
        if skills:
            inject_event = Event(
                event_id=f"skill_inject_{int(time.time())}",
                event_type=EventType.SKILL_INJECTED,
                source="usb_handler",
                data={
                    "device_id": device_data.get('device_id'),
                    "skills": skills,
                    "timestamp": time.time()
                },
                priority=3
            )
            self.publish_event(inject_event)
    
    async def _handle_skill_injected(self, event: Event):
        skills = event.data.get('skills', [])
        logger.info(f"Skills injected: {skills}")
    
    async def _handle_prediction_request(self, event: Event):
        query = event.data.get('query', '')
        agent_ids = event.data.get('agent_ids', [])
        logger.info(f"Prediction request: '{query}' for agents: {agent_ids}")
    
    async def _handle_rag_query(self, event: Event):
        query = event.data.get('query', '')
        logger.info(f"RAG query: '{query}'")
    
    async def _handle_key_press(self, event: Event):
        key = event.data.get('key', '')
        key_set = event.data.get('key_set', '')
        logger.info(f"Key press: {key} from {key_set}")
        
        # Map keys to actions
        key_actions = {
            "5-key": {
                "1": "toggle_agent_view",
                "2": "toggle_skill_tree",
                "3": "toggle_consensus",
                "4": "emergency_stop",
                "5": "force_consensus"
            },
            "13-key": {
                "1": "agent_1_focus",
                "2": "agent_2_focus",
                # ... etc
            }
        }
        
        if key_set in key_actions and key in key_actions[key_set]:
            action = key_actions[key_set][key]
            logger.info(f"Mapped key {key} to action: {action}")
    
    async def _handle_system_health(self, event: Event):
        health_data = event.data
        logger.info(f"System health: {health_data.get('status', 'unknown')} "
                   f"score: {health_data.get('health_score', 0):.1f}%")
        
        # Update consensus based on health
        if health_data.get('status') == 'healthy':
            self.consensus_score = min(1.0, self.consensus_score + 0.1)
        else:
            self.consensus_score = max(0.0, self.consensus_score - 0.2)
    
    # Public API Methods
    def get_agent_status(self) -> List[Dict]:
        """Get status of all agents"""
        return [agent.to_dict() for agent in self.agents.values()]
    
    def get_usb_devices(self) -> List[Dict]:
        """Get all detected USB devices"""
        return [device.to_dict() for device in self.usb_devices.values()]
    
    def get_system_status(self) -> Dict:
        """Get overall system status"""
        return {
            "total_agents": len(self.agents),
            "active_agents": sum(1 for a in self.agents.values() if a.status == "active"),
            "usb_devices": len(self.usb_devices),
            "consensus_score": self.consensus_score,
            "system_health": self.system_health,
            "timestamp": time.time()
        }

async def main():
    """Main entry point"""
    dispatcher = UnifiedDispatcher()
    
    try:
        await dispatcher.start()
        
        # Keep running
        while True:
            await asyncio.sleep(1)
            
            # Print status every 30 seconds
            if int(time.time()) % 30 == 0:
                status = dispatcher.get_system_status()
                logger.info(f"System Status: {status}")
                
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
    finally:
        await dispatcher.stop()

if __name__ == "__main__":
    asyncio.run(main())