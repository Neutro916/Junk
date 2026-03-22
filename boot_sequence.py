#!/usr/bin/env python3
"""
BOOT SEQUENCE - Unified System Startup

Starts all components of the 33-agent system:
1. Unified Dispatcher (central event bus)
2. Agent swarm initialization
3. USB device monitoring
4. Drive mapping (J:/K:/L:/ unification)
5. Skill tree visualization
6. External system integrations (MFish, CONDUCTOR, NEMO-Ralph)

This is the single entry point to launch everything.
"""

import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional
import threading
import webbrowser
import subprocess

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_dispatcher import UnifiedDispatcher, AgentType

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BootSequence:
    """Orchestrates system startup"""
    
    def __init__(self, config_path: str = "agent_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.dispatcher = None
        self.components = {}
        self.startup_time = time.time()
        
        # Status tracking
        self.status = {
            "dispatcher": False,
            "agents": 0,
            "usb_monitor": False,
            "drive_mapper": False,
            "external_systems": {},
            "web_ui": False,
            "total_time": 0.0
        }
    
    def _load_config(self) -> Dict:
        """Load configuration file"""
        config_path = Path(self.config_path)
        if not config_path.exists():
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return self._default_config()
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            "system_overview": {
                "total_agents": 33,
                "free_models_only": True,
                "local_first": True
            },
            "boot_sequence": {
                "start_dispatcher": True,
                "start_usb_monitor": True,
                "map_drives": True,
                "launch_web_ui": True,
                "check_external_systems": True,
                "auto_open_browser": False
            },
            "web_ui": {
                "port": 8080,
                "host": "localhost",
                "path": "dashboard.html"
            }
        }
    
    async def run(self):
        """Execute the full boot sequence"""
        logger.info("🚀 Starting 33-Agent System Boot Sequence...")
        logger.info(f"System Time: {time.ctime()}")
        
        steps = [
            ("🔍 Checking system requirements", self._check_system_requirements),
            ("🔄 Initializing unified dispatcher", self._init_dispatcher),
            ("🗺️ Mapping multi-drive structure", self._map_drives),
            ("🤖 Registering agent swarm", self._register_agents),
            ("🔌 Starting USB skill monitor", self._start_usb_monitor),
            ("🔗 Integrating external systems", self._integrate_external_systems),
            ("🌐 Launching web dashboard", self._launch_web_ui),
            ("📊 Starting health monitoring", self._start_health_monitor),
            ("✅ Boot sequence complete", self._finalize_boot)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"\n{'='*60}")
            logger.info(f"STEP: {step_name}")
            logger.info('='*60)
            
            start_time = time.time()
            try:
                if asyncio.iscoroutinefunction(step_func):
                    await step_func()
                else:
                    step_func()
                elapsed = time.time() - start_time
                logger.info(f"✓ Completed in {elapsed:.2f}s")
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"✗ Failed after {elapsed:.2f}s: {e}")
                # Continue with boot sequence even if some steps fail
        
        total_time = time.time() - self.startup_time
        self.status["total_time"] = total_time
        logger.info(f"\n{'='*60}")
        logger.info(f"🏁 BOOT SEQUENCE COMPLETE")
        logger.info(f"Total time: {total_time:.2f}s")
        logger.info(f"Status: {json.dumps(self.status, indent=2)}")
        logger.info('='*60)
        
        return self.status
    
    def _check_system_requirements(self):
        """Check if system meets requirements"""
        logger.info("Checking system requirements...")
        
        checks = [
            ("Python 3.11+", sys.version_info >= (3, 11)),
            ("Config file exists", Path(self.config_path).exists()),
            ("J: drive accessible", Path("J:/").exists()),
            ("K: drive accessible", Path("K:/").exists()),
            ("Write permissions", os.access(".", os.W_OK)),
        ]
        
        all_ok = True
        for check_name, check_result in checks:
            status = "✓" if check_result else "✗"
            logger.info(f"  {status} {check_name}")
            if not check_result:
                all_ok = False
        
        if not all_ok:
            logger.warning("Some requirements not met, continuing anyway...")
        
        return all_ok
    
    async def _init_dispatcher(self):
        """Initialize the unified dispatcher"""
        logger.info("Initializing unified dispatcher...")
        
        self.dispatcher = UnifiedDispatcher()
        await self.dispatcher.start()
        
        self.status["dispatcher"] = True
        logger.info("Unified dispatcher started")
    
    def _map_drives(self):
        """Create logical mapping of J:/K:/L: drives"""
        if not self.config.get("boot_sequence", {}).get("map_drives", True):
            logger.info("Skipping drive mapping")
            return
        
        logger.info("Mapping multi-drive structure...")
        
        # Create symbolic directory structure
        mapping_dir = Path("drive_mapping")
        mapping_dir.mkdir(exist_ok=True)
        
        drive_mappings = [
            ("J:", "execution_engine"),
            ("K:", "logic_dna"),
            ("L:", "swarm_memory")
        ]
        
        for drive_letter, mapping_name in drive_mappings:
            drive_path = Path(drive_letter)
            if drive_path.exists():
                # Create informational link file
                link_file = mapping_dir / f"{mapping_name}.info"
                with open(link_file, 'w') as f:
                    f.write(f"Drive: {drive_letter}\n")
                    f.write(f"Mapping: {mapping_name}\n")
                    f.write(f"Path: {drive_path.absolute()}\n")
                    f.write(f"Exists: {drive_path.exists()}\n")
                
                logger.info(f"  {drive_letter} → {mapping_name}")
        
        self.status["drive_mapper"] = True
        logger.info(f"Drive mapping created in: {mapping_dir.absolute()}")
    
    async def _register_agents(self):
        """Register all 33 agents with the dispatcher"""
        if not self.dispatcher:
            logger.error("Dispatcher not initialized, skipping agent registration")
            return
        
        logger.info("Registering agent swarm...")
        
        # Load agent definitions from config
        agent_groups = self.config.get("agent_groups", {})
        
        agent_id = 1
        for group_name, group_config in agent_groups.items():
            if "count" in group_config:
                count = group_config["count"]
                for i in range(count):
                    agent_name = f"{group_name}_{i+1:02d}"
                    
                    # Determine agent type
                    if group_name == "predictors":
                        agent_type = AgentType.PREDICTOR
                    elif group_name == "executors":
                        agent_type = AgentType.EXECUTOR
                    elif group_name == "validators":
                        agent_type = AgentType.VALIDATOR
                    elif group_name == "observers":
                        agent_type = AgentType.OBSERVER
                    else:
                        agent_type = AgentType.GHOST
                    
                    # Register agent
                    await self.dispatcher.register_agent(
                        agent_id=f"agent_{agent_id:03d}",
                        name=agent_name,
                        agent_type=agent_type,
                        capabilities=group_config.get("models", ["unknown"]),
                        config_path=None
                    )
                    
                    agent_id += 1
                    self.status["agents"] += 1
        
        # Register specialists
        specialists = agent_groups.get("specialists", {}).get("agents", [])
        for specialist in specialists:
            agent_name = specialist.get("name", f"specialist_{agent_id}")
            
            # Map specialist to agent type
            spec_type = specialist.get("type", "ghost")
            agent_type_map = {
                "predictor": AgentType.PREDICTOR,
                "executor": AgentType.EXECUTOR,
                "validator": AgentType.VALIDATOR,
                "nemo": AgentType.NEMO,
                "architect": AgentType.ARCHITECT,
                "shadow": AgentType.SHADOW,
                "monk": AgentType.MONK
            }
            agent_type = agent_type_map.get(spec_type, AgentType.GHOST)
            
            await self.dispatcher.register_agent(
                agent_id=f"specialist_{agent_id:03d}",
                name=agent_name,
                agent_type=agent_type,
                capabilities=[specialist.get("model", "unknown")],
                config_path=specialist.get("source")
            )
            
            agent_id += 1
            self.status["agents"] += 1
        
        logger.info(f"Registered {self.status['agents']} agents total")
    
    async def _start_usb_monitor(self):
        """Start USB device monitoring"""
        if not self.dispatcher:
            logger.error("Dispatcher not initialized, skipping USB monitor")
            return
        
        # USB monitoring is already started by dispatcher
        self.status["usb_monitor"] = True
        logger.info("USB skill monitor started")
        
        # Initial USB scan
        logger.info("Performing initial USB device scan...")
        # Note: Actual USB scanning happens in dispatcher's background task
    
    def _integrate_external_systems(self):
        """Integrate with existing external systems (MFish, CONDUCTOR, NEMO-Ralph)"""
        logger.info("Integrating external systems...")
        
        external_systems = [
            ("MFish Predictor", Path("J:/MFish-great")),
            ("CONDUCTOR RAG", Path("J:/CONDUCTOR")),
            ("NEMO-Ralph", Path("J:/.skills/nemo-ralph")),
            ("Conduit UI", Path("J:/Conduit-UI-JET-v12")),
            ("Obsidian Vault", Path("K:/.obsidian"))
        ]
        
        for system_name, system_path in external_systems:
            if system_path.exists():
                self.status["external_systems"][system_name] = {
                    "path": str(system_path),
                    "status": "found",
                    "accessible": os.access(system_path, os.R_OK)
                }
                logger.info(f"  ✓ {system_name}: {system_path}")
            else:
                self.status["external_systems"][system_name] = {
                    "path": str(system_path),
                    "status": "not_found"
                }
                logger.info(f"  ✗ {system_name}: Not found at {system_path}")
    
    def _launch_web_ui(self):
        """Launch web dashboard for system monitoring"""
        if not self.config.get("boot_sequence", {}).get("launch_web_ui", True):
            logger.info("Skipping web UI launch")
            return
        
        logger.info("Launching web dashboard...")
        
        # Create simple dashboard HTML
        dashboard_html = self._create_dashboard_html()
        dashboard_path = Path("dashboard.html")
        
        with open(dashboard_path, 'w') as f:
            f.write(dashboard_html)
        
        # Start simple HTTP server in background
        try:
            import http.server
            import socketserver
            
            port = self.config.get("web_ui", {}).get("port", 8080)
            host = self.config.get("web_ui", {}).get("host", "localhost")
            
            # Start server in background thread
            def start_server():
                os.chdir(".")
                handler = http.server.SimpleHTTPRequestHandler
                with socketserver.TCPServer((host, port), handler) as httpd:
                    logger.info(f"Web server started at http://{host}:{port}")
                    httpd.serve_forever()
            
            server_thread = threading.Thread(target=start_server, daemon=True)
            server_thread.start()
            
            # Give server time to start
            time.sleep(1)
            
            # Open browser if configured
            if self.config.get("boot_sequence", {}).get("auto_open_browser", False):
                webbrowser.open(f"http://{host}:{port}/dashboard.html")
            
            self.status["web_ui"] = True
            logger.info(f"Dashboard available at http://{host}:{port}/dashboard.html")
            
        except Exception as e:
            logger.error(f"Failed to start web server: {e}")
            self.status["web_ui"] = False
    
    def _create_dashboard_html(self) -> str:
        """Create HTML dashboard for system monitoring"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>33-Agent System Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: monospace; background: #0f0f0f; color: #e0e0e0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; padding: 20px; background: #1a1a1a; border-radius: 10px; }}
        .header h1 {{ color: #7c3aed; font-size: 2.5em; margin-bottom: 10px; }}
        .status-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{ background: #1a1a1a; border-radius: 10px; padding: 20px; border: 1px solid #333; }}
        .card h2 {{ color: #7c3aed; margin-bottom: 15px; font-size: 1.3em; }}
        .stat {{ display: flex; justify-content: space-between; margin-bottom: 10px; padding: 8px; background: #2a2a2a; border-radius: 5px; }}
        .stat .label {{ color: #888; }}
        .stat .value {{ color: #e0e0e0; font-weight: bold; }}
        .online {{ color: #10b981 !important; }}
        .offline {{ color: #ef4444 !important; }}
        .agent-list {{ max-height: 300px; overflow-y: auto; }}
        .agent-item {{ display: flex; justify-content: space-between; padding: 8px; margin-bottom: 5px; background: #2a2a2a; border-radius: 5px; }}
        .controls {{ display: flex; gap: 10px; margin-top: 20px; }}
        button {{ background: #7c3aed; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-family: monospace; }}
        button:hover {{ background: #6d28d9; }}
        .usb-device {{ background: #1e3a8a; border-left: 4px solid #3b82f6; }}
        .drive-mapping {{ background: #064e3b; border-left: 4px solid #10b981; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 33-Agent System Dashboard</h1>
            <p>Unified dispatcher for multi-drive, multi-agent AI system</p>
            <p>Boot time: {time.ctime(self.startup_time)}</p>
        </div>
        
        <div class="status-grid">
            <div class="card">
                <h2>System Status</h2>
                <div class="stat">
                    <span class="label">Dispatcher</span>
                    <span class="value {'online' if self.status['dispatcher'] else 'offline'}">
                        {'🟢 Online' if self.status['dispatcher'] else '🔴 Offline'}
                    </span>
                </div>
                <div class="stat">
                    <span class="label">Active Agents</span>
                    <span class="value">{self.status['agents']} / 33</span>
                </div>
                <div class="stat">
                    <span class="label">USB Monitor</span>
                    <span class="value {'online' if self.status['usb_monitor'] else 'offline'}">
                        {'🟢 Active' if self.status['usb_monitor'] else '🔴 Inactive'}
                    </span>
                </div>
                <div class="stat">
                    <span class="label">Drive Mapping</span>
                    <span class="value {'online' if self.status['drive_mapper'] else 'offline'}">
                        {'🟢 Active' if self.status['drive_mapper'] else '🔴 Inactive'}
                    </span>
                </div>
                <div class="stat">
                    <span class="label">Boot Time</span>
                    <span class="value">{self.status.get('total_time', 0):.2f}s</span>
                </div>
            </div>
            
            <div class="card">
                <h2>Drive Mapping</h2>
                <div class="stat drive-mapping">
                    <span class="label">J: Drive</span>
                    <span class="value">Execution Engine</span>
                </div>
                <div class="stat drive-mapping">
                    <span class="label">K: Drive</span>
                    <span class="value">Logic DNA</span>
                </div>
                <div class="stat drive-mapping">
                    <span class="label">L: Drive</span>
                    <span class="value">Swarm Memory</span>
                </div>
                <div class="stat">
                    <span class="label">External Systems</span>
                    <span class="value">{len(self.status.get('external_systems', {}))}</span>
                </div>
            </div>
            
            <div class="card">
                <h2>External Systems</h2>
                <div class="agent-list">
                    {' '.join([f'<div class="agent-item"><span>{name}</span><span>{info.get("status", "unknown")}</span></div>' 
                               for name, info in self.status.get('external_systems', {}).items()])}
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>System Controls</h2>
            <div class="controls">
                <button onclick="location.reload()">🔄 Refresh Status</button>
                <button onclick="fetch('/api/health').then(r => r.json()).then(console.log)">📊 Health Check</button>
                <button onclick="fetch('/api/agents').then(r => r.json()).then(console.log)">🤖 List Agents</button>
                <button onclick="fetch('/api/usb-scan').then(r => r.json()).then(console.log)">🔌 Scan USB</button>
            </div>
            <div style="margin-top: 15px; font-size: 0.9em; color: #888;">
                <p>API Endpoints:</p>
                <ul style="margin-left: 20px;">
                    <li>GET /api/health - System health status</li>
                    <li>GET /api/agents - List all agents</li>
                    <li>GET /api/usb-devices - List USB devices</li>
                    <li>POST /api/query - Query agent system</li>
                </ul>
            </div>
        </div>
        
        <div class="card">
            <h2>Live Updates</h2>
            <div id="live-updates" style="height: 100px; overflow-y: auto; background: #2a2a2a; padding: 10px; border-radius: 5px;">
                <p>Connecting to dispatcher event stream...</p>
            </div>
        </div>
    </div>
    
    <script>
        // Simple WebSocket connection for live updates
        const ws = new WebSocket('ws://localhost:8081');
        const updatesEl = document.getElementById('live-updates');
        
        ws.onopen = () => {{
            addUpdate('🟢 Connected to dispatcher event stream');
        }};
        
        ws.onmessage = (event) => {{
            addUpdate(`📡 ${event.data}`);
        }};
        
        ws.onerror = (error) => {{
            addUpdate('🔴 WebSocket error');
        }};
        
        function addUpdate(message) {{
            const p = document.createElement('p');
            p.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
            updatesEl.appendChild(p);
            updatesEl.scrollTop = updatesEl.scrollHeight;
        }}
        
        // Poll for updates every 5 seconds
        setInterval(() => {{
            fetch('/api/health')
                .then(r => r.json())
                .then(data => {{
                    // Update status display
                    document.querySelectorAll('.stat .value').forEach(el => {{
                        // Could update specific elements here
                    }});
                }});
        }}, 5000);
    </script>
</body>
</html>"""
    
    async def _start_health_monitor(self):
        """Start periodic health monitoring"""
        logger.info("Starting health monitoring...")
        
        # Health monitoring is handled by dispatcher
        # This just logs that it's enabled
        logger.info("Health monitor enabled - system status will be logged every 30s")
    
    async def _finalize_boot(self):
        """Final boot sequence steps"""
        logger.info("Finalizing boot sequence...")
        
        # Print system information
        if self.dispatcher:
            status = self.dispatcher.get_system_status()
            logger.info(f"Dispatcher Status: {json.dumps(status, indent=2)}")
        
        # Create ready file
        ready_file = Path("SYSTEM_READY.txt")
        with open(ready_file, 'w') as f:
            f.write(f"33-Agent System Ready\n")
            f.write(f"Boot completed: {time.ctime()}\n")
            f.write(f"Total agents: {self.status['agents']}\n")
            f.write(f"Dispatcher: {'🟢 Online' if self.status['dispatcher'] else '🔴 Offline'}\n")
            f.write(f"USB monitor: {'🟢 Active' if self.status['usb_monitor'] else '🔴 Inactive'}\n")
            f.write(f"\nAccess dashboard: http://localhost:8080/dashboard.html\n")
            f.write(f"API endpoint: http://localhost:8080/api/health\n")
        
        logger.info(f"System ready file created: {ready_file.absolute()}")
        logger.info("\n" + "="*60)
        logger.info("🎉 SYSTEM BOOT COMPLETE")
        logger.info("="*60)
        logger.info("Next steps:")
        logger.info("1. Open dashboard: http://localhost:8080/dashboard.html")
        logger.info("2. Query agents using: python query_system.py")
        logger.info("3. Monitor USB devices in real-time")
        logger.info("4. Check SYSTEM_READY.txt for status")

async def main():
    """Main entry point"""
    boot = BootSequence()
    
    try:
        status = await boot.run()
        
        # Keep running
        logger.info("\nSystem running. Press Ctrl+C to shutdown.")
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("\nShutdown requested")
    except Exception as e:
        logger.error(f"Boot sequence failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)