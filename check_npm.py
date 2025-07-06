#!/usr/bin/env python3
"""
Simple script to check npm availability and help debug setup issues
"""

import subprocess
import sys
import os

def check_command(command, description):
    """Check if a command is available"""
    print(f"🔍 Checking {description}...")
    
    # Try different variations of the command
    variations = [command, f"{command}.cmd", f"{command}.exe"]
    
    for var in variations:
        try:
            result = subprocess.run([var, "--version"], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ {description} found: {result.stdout.strip()}")
                return True, var
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    print(f"❌ {description} not found")
    return False, None

def main():
    print("🔧 npm Detection Debug Tool")
    print("=" * 40)
    
    # Check Node.js
    node_ok, node_cmd = check_command("node", "Node.js")
    
    # Check npm
    npm_ok, npm_cmd = check_command("npm", "npm")
    
    # Check npx
    npx_ok, npx_cmd = check_command("npx", "npx")
    
    print("\n📋 Summary:")
    print(f"Node.js: {'✅ Available' if node_ok else '❌ Not found'}")
    print(f"npm: {'✅ Available' if npm_ok else '❌ Not found'}")
    print(f"npx: {'✅ Available' if npx_ok else '❌ Not found'}")
    
    if not npm_ok:
        print("\n🔧 Troubleshooting npm:")
        print("1. Make sure Node.js is properly installed")
        print("2. Try restarting your terminal/command prompt")
        print("3. Check if npm is in your PATH")
        print("4. On Windows, try running as administrator")
        print("5. Try: node --version && npm --version")
    
    # Show PATH for debugging
    print(f"\n📁 Current PATH:")
    for path in os.environ.get('PATH', '').split(os.pathsep):
        if 'node' in path.lower() or 'npm' in path.lower():
            print(f"  {path}")
    
    return npm_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 