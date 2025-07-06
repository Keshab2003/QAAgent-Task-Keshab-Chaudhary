#!/usr/bin/env python3
"""
QAgenie Setup Script
Automates the installation and configuration of the AI-powered QA agent
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class QAGenieSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.env_file = self.project_root / ".env"
        
    def run(self):
        """Main setup process"""
        print("🧩 QAgenie - AI-Powered QA Agent Setup")
        print("=" * 50)
        
        try:
            # Check prerequisites
            self.check_prerequisites()
            
            # Install dependencies
            self.install_dependencies()
            
            # Setup environment
            self.setup_environment()
            
            # Install Playwright browsers
            self.install_playwright_browsers()
            
            # Generate initial test cases
            self.generate_initial_tests()
            
            print("\n✅ Setup completed successfully!")
            print("\n🚀 Next steps:")
            print("1. Add your OpenAI API key to .env file")
            print("2. Run: python scripts/generate_testcases.py")
            print("3. Run: node scripts/generatePlaywrightTests.js")
            print("4. Run: npm test")
            print("5. Run: streamlit run dashboard.py")
            
        except Exception as e:
            print(f"❌ Setup failed: {str(e)}")
            sys.exit(1)
    
    def check_prerequisites(self):
        """Check if required software is installed"""
        print("🔍 Checking prerequisites...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            raise Exception("Python 3.8 or higher is required")
        print(f"✅ Python: {sys.version.split()[0]}")
        
        # Check Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise Exception("Node.js is not installed or not accessible")
            print(f"✅ Node.js: {result.stdout.strip()}")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            raise Exception("Node.js is not installed or not in PATH")
        
        # Check npm - try multiple approaches
        npm_found = False
        npm_commands = ["npm", "npm.cmd", "npm.exe"]
        
        for npm_cmd in npm_commands:
            try:
                result = subprocess.run([npm_cmd, "--version"], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ npm: {result.stdout.strip()}")
                    npm_found = True
                    break
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        if not npm_found:
            # Try alternative approach - check if npm is available via npx
            try:
                result = subprocess.run(["npx", "--version"], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ npx available: {result.stdout.strip()}")
                    npm_found = True
                else:
                    raise Exception("npm/npx is not installed or not accessible")
            except (FileNotFoundError, subprocess.TimeoutExpired):
                raise Exception("npm/npx is not installed or not in PATH")
        
        if not npm_found:
            raise Exception("npm is not installed or not accessible")
        
        print("✅ All prerequisites met!")
    
    def install_dependencies(self):
        """Install Python and Node.js dependencies"""
        print("\n📦 Installing dependencies...")
        
        # Install Python dependencies
        print("Installing Python dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True)
            print("✅ Python dependencies installed")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to install Python dependencies: {e}")
        
        # Install Node.js dependencies - try multiple npm commands
        print("Installing Node.js dependencies...")
        npm_commands = ["npm", "npm.cmd", "npm.exe"]
        npm_installed = False
        
        for npm_cmd in npm_commands:
            try:
                subprocess.run([npm_cmd, "install"], check=True, capture_output=True, timeout=300)
                print("✅ Node.js dependencies installed")
                npm_installed = True
                break
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        if not npm_installed:
            raise Exception("Failed to install Node.js dependencies - npm not found or failed")
    
    def setup_environment(self):
        """Setup environment configuration"""
        print("\n⚙️ Setting up environment...")
        
        # Create .env file if it doesn't exist
        if not self.env_file.exists():
            env_content = """# QAgenie Environment Configuration
# Add your OpenAI API key here
OPENAI_API_KEY=your_openai_api_key_here

# Test Configuration
BASE_URL=https://www.recruter.ai
DEFAULT_TIMEOUT=30
HEADLESS_MODE=true
PARALLEL_WORKERS=4
"""
            self.env_file.write_text(env_content)
            print("✅ Created .env file")
        else:
            print("✅ .env file already exists")
        
        # Create necessary directories
        directories = ["testcases", "test", "report", "screenshots"]
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(exist_ok=True)
            print(f"✅ Created directory: {directory}")
    
    def install_playwright_browsers(self):
        """Install Playwright browsers"""
        print("\n🌐 Installing Playwright browsers...")
        try:
            # Try npx first, then npm
            try:
                subprocess.run(["npx", "playwright", "install"], check=True, capture_output=True, timeout=600)
                print("✅ Playwright browsers installed")
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                # Fallback to npm
                subprocess.run(["npm", "exec", "playwright", "install"], check=True, capture_output=True, timeout=600)
                print("✅ Playwright browsers installed")
        except Exception as e:
            print(f"⚠️ Warning: Failed to install Playwright browsers: {e}")
            print("You can install them manually later with: npx playwright install")
    
    def generate_initial_tests(self):
        """Generate initial test cases if transcript exists"""
        transcript_file = self.project_root / "recruter_transcript.txt"
        
        if transcript_file.exists():
            print("\n📝 Generating initial test cases...")
            try:
                result = subprocess.run([sys.executable, "scripts/generate_testcases.py"], 
                                     capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    print("✅ Initial test cases generated")
                else:
                    print("⚠️ Test generation failed (check OpenAI API key)")
                    print(f"Error: {result.stderr}")
            except Exception as e:
                print(f"⚠️ Test generation failed: {e}")
        else:
            print("\n⚠️ No transcript file found. Please add recruter_transcript.txt to generate test cases.")

def main():
    """Main entry point"""
    setup = QAGenieSetup()
    setup.run()

if __name__ == "__main__":
    main() 