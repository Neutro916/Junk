#!/usr/bin/env python3
"""
CMD ACTIVATE - Simple activation command for opencode

Usage in opencode: /cmd activate
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def main():
    """Activate the 33-agent system"""
    print("🚀 Activating 33-Agent System...")
    print(f"Working directory: {Path.cwd()}")
    
    # Check if we're in the right directory
    required_files = ["boot_sequence.py", "unified_dispatcher.py", "agent_config.json"]
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"⚠ Missing files: {missing_files}")
        print("Please run from the Junk directory containing the system files.")
        return 1
    
    # Check Python
    try:
        import asyncio
        import aiohttp
        import websockets
        import requests
        import dotenv
        print("✓ All Python dependencies available")
    except ImportError as e:
        print(f"⚠ Missing dependency: {e}")
        print("Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Check drives
    print("\n🔍 Checking system configuration:")
    
    drives_to_check = [
        ("J:", "Execution Engine", ["CONDUCTOR", "nemo-workspace", ".skills"]),
        ("K:", "Logic DNA", [".obsidian", "dev-tools", "opencode-main"]),
        ("L:", "Swarm Memory", [])  # L: might be empty
    ]
    
    for drive_letter, drive_name, expected_dirs in drives_to_check:
        drive_path = Path(drive_letter)
        if drive_path.exists():
            print(f"  ✓ {drive_letter}: {drive_name}")
            
            # Check for expected directories
            for expected_dir in expected_dirs:
                check_path = drive_path / expected_dir
                if check_path.exists():
                    print(f"    • {expected_dir}: Found")
                else:
                    print(f"    • {expected_dir}: Not found")
        else:
            print(f"  ⚠ {drive_letter}: {drive_name} not found")
    
    # Offer options
    print("\n🎮 Available activation options:")
    print("  1. Start full boot sequence (dashboard + agents)")
    print("  2. Start dispatcher only (no web UI)")
    print("  3. Query system (interactive)")
    print("  4. Scan USB devices")
    print("  5. Open dashboard only")
    print("  6. Exit")
    
    try:
        choice = input("\nSelect option [1-6]: ").strip()
        
        if choice == "1":
            print("\nStarting full boot sequence...")
            subprocess.run([sys.executable, "boot_sequence.py"])
            
        elif choice == "2":
            print("\nStarting dispatcher only...")
            # Import and run dispatcher directly
            import asyncio
            from unified_dispatcher import UnifiedDispatcher
            
            async def run_dispatcher():
                dispatcher = UnifiedDispatcher()
                await dispatcher.start()
                print("Dispatcher started. Press Ctrl+C to stop.")
                try:
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    await dispatcher.stop()
            
            asyncio.run(run_dispatcher())
            
        elif choice == "3":
            print("\nStarting interactive query...")
            query = input("Enter query: ").strip()
            if query:
                subprocess.run([sys.executable, "query_system.py", query])
            else:
                print("No query provided")
                
        elif choice == "4":
            print("\nScanning USB devices...")
            subprocess.run([sys.executable, "query_system.py", "--usb-scan"])
            
        elif choice == "5":
            print("\nOpening dashboard...")
            # Create dashboard if it doesn't exist
            dashboard_path = Path("dashboard.html")
            if not dashboard_path.exists():
                print("Creating dashboard...")
                # We need to run boot sequence to create dashboard
                # But for now, just open port 8080
                pass
            
            webbrowser.open("http://localhost:8080/dashboard.html")
            print("Dashboard opened in browser")
            print("Note: Start boot sequence first for live data")
            
        elif choice == "6":
            print("Exiting...")
            return 0
            
        else:
            print(f"Invalid choice: {choice}")
            
    except KeyboardInterrupt:
        print("\n\nActivation cancelled")
        return 0
    
    return 0

if __name__ == "__main__":
    sys.exit(main())