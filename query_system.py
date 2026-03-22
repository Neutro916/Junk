#!/usr/bin/env python3
"""
QUERY SYSTEM - Interface for interacting with 33-agent system

Usage:
  python query_system.py "What is the weather prediction?"
  python query_system.py --agents predictor --query "Market analysis"
  python query_system.py --list-agents
  python query_system.py --status
"""

import asyncio
import argparse
import json
import sys
from pathlib import Path
from unified_dispatcher import UnifiedDispatcher, AgentType

async def query_agents(query: str, agent_types=None, use_rag=False):
    """Query the agent system"""
    dispatcher = UnifiedDispatcher()
    
    try:
        # Start dispatcher
        await dispatcher.start()
        
        # Map agent type strings to enums
        type_map = {
            "predictor": AgentType.PREDICTOR,
            "executor": AgentType.EXECUTOR,
            "validator": AgentType.VALIDATOR,
            "observer": AgentType.OBSERVER,
            "ghost": AgentType.GHOST,
            "shadow": AgentType.SHADOW,
            "monk": AgentType.MONK,
            "architect": AgentType.ARCHITECT,
            "nemo": AgentType.NEMO,
            "ralph": AgentType.RALPH
        }
        
        mapped_types = None
        if agent_types:
            mapped_types = [type_map.get(t.lower()) for t in agent_types if t.lower() in type_map]
        
        print(f"🔍 Querying agents: '{query}'")
        if mapped_types:
            print(f"   Target agent types: {[t.value for t in mapped_types]}")
        
        result = await dispatcher.query_agents(query, mapped_types, use_rag)
        
        print("\n" + "="*60)
        print("📊 QUERY RESULT")
        print("="*60)
        print(f"Query: {result.get('query', query)}")
        print(f"Agents consulted: {result.get('agents_queried', 'Unknown')}")
        print(f"Consensus score: {result.get('consensus', 0.0):.2f}")
        print(f"Timestamp: {result.get('timestamp', 'Unknown')}")
        print("\nResponse:")
        print("-"*40)
        print(result.get('response', 'No response generated'))
        print("="*60)
        
        return result
        
    finally:
        await dispatcher.stop()

async def list_agents():
    """List all registered agents"""
    dispatcher = UnifiedDispatcher()
    
    try:
        await dispatcher.start()
        agents = dispatcher.get_agent_status()
        
        print("\n" + "="*60)
        print("🤖 REGISTERED AGENTS")
        print("="*60)
        
        agent_groups = {}
        for agent in agents:
            agent_type = agent.get('type', 'unknown')
            if agent_type not in agent_groups:
                agent_groups[agent_type] = []
            agent_groups[agent_type].append(agent)
        
        for agent_type, type_agents in agent_groups.items():
            print(f"\n{agent_type.upper()} ({len(type_agents)} agents):")
            print("-"*40)
            for agent in type_agents:
                status_icon = "🟢" if agent.get('status') == 'active' else "⚪"
                print(f"  {status_icon} {agent['name']} (ID: {agent['id']})")
                if agent.get('capabilities'):
                    print(f"     Capabilities: {', '.join(agent['capabilities'][:3])}")
        
        print(f"\nTotal: {len(agents)} agents")
        print("="*60)
        
    finally:
        await dispatcher.stop()

async def system_status():
    """Get overall system status"""
    dispatcher = UnifiedDispatcher()
    
    try:
        await dispatcher.start()
        status = dispatcher.get_system_status()
        usb_devices = dispatcher.get_usb_devices()
        
        print("\n" + "="*60)
        print("📊 SYSTEM STATUS")
        print("="*60)
        
        print(f"\nAgent System:")
        print(f"  Total agents: {status.get('total_agents', 0)}")
        print(f"  Active agents: {status.get('active_agents', 0)}")
        print(f"  Consensus score: {status.get('consensus_score', 0.0):.2f}")
        print(f"  System health: {status.get('system_health', 'unknown')}")
        
        print(f"\nHardware Integration:")
        print(f"  USB devices: {status.get('usb_devices', 0)}")
        for device in usb_devices[:3]:  # Show first 3 devices
            print(f"    • {device.get('product', 'Unknown')} ({device.get('drive_letter', 'N/A')})")
            if device.get('skills'):
                print(f"      Skills: {', '.join(device['skills'][:3])}")
        if len(usb_devices) > 3:
            print(f"    ... and {len(usb_devices) - 3} more")
        
        print(f"\nTimestamp: {status.get('timestamp', 'Unknown')}")
        print("="*60)
        
    finally:
        await dispatcher.stop()

async def usb_scan():
    """Scan for USB devices"""
    dispatcher = UnifiedDispatcher()
    
    try:
        await dispatcher.start()
        devices = dispatcher.get_usb_devices()
        
        print("\n" + "="*60)
        print("🔌 USB DEVICES")
        print("="*60)
        
        if not devices:
            print("No USB devices detected")
            return
        
        for i, device in enumerate(devices, 1):
            print(f"\n{i}. {device.get('product', 'Unknown Device')}")
            print(f"   Vendor: {device.get('vendor', 'Unknown')}")
            print(f"   Drive: {device.get('drive_letter', 'Not mounted')}")
            print(f"   Detected: {device.get('detected_at', 'Unknown')}")
            
            skills = device.get('skills', [])
            if skills:
                print(f"   Skills: {', '.join(skills)}")
                print(f"   Status: Ready for skill injection")
            else:
                print(f"   Skills: No skills detected")
                print(f"   Status: Generic storage")
        
        print(f"\nTotal: {len(devices)} USB devices")
        print("="*60)
        
    finally:
        await dispatcher.stop()

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Query the 33-agent system")
    parser.add_argument("query", nargs="?", help="Query to send to agents")
    parser.add_argument("--agents", nargs="+", help="Agent types to query (predictor, executor, validator, etc.)")
    parser.add_argument("--rag", action="store_true", help="Use RAG for context retrieval")
    parser.add_argument("--list-agents", action="store_true", help="List all registered agents")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--usb-scan", action="store_true", help="Scan for USB devices")
    parser.add_argument("--output", help="Output file for results (JSON)")
    
    args = parser.parse_args()
    
    if args.list_agents:
        asyncio.run(list_agents())
    elif args.status:
        asyncio.run(system_status())
    elif args.usb_scan:
        asyncio.run(usb_scan())
    elif args.query:
        result = asyncio.run(query_agents(args.query, args.agents, args.rag))
        
        # Save output if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n📁 Result saved to: {args.output}")
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python query_system.py 'Predict market trends for next week'")
        print("  python query_system.py --agents predictor validator --query 'Analyze this code'")
        print("  python query_system.py --list-agents")
        print("  python query_system.py --status")
        print("  python query_system.py --usb-scan")

if __name__ == "__main__":
    main()