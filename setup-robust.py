#!/usr/bin/env python3
"""
Robust QAgenie Setup Script
Handles dependency installation issues better
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class RobustQAGenieSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.env_file = self.project_root / ".env"
        
    def run(self):
        """Main setup process"""
        print("🧩 QAgenie - Robust Setup")
        print("=" * 50)
        
        try:
            # Check prerequisites
            self.check_prerequisites()
            
            # Install dependencies with better error handling
            self.install_dependencies_robust()
            
            # Setup environment
            self.setup_environment()
            
            # Install Playwright browsers
            self.install_playwright_browsers()
            
            print("\n✅ Setup completed successfully!")
            print("\n🚀 Next steps:")
            print("1. Add your OpenAI API key to .env file")
            print("2. Run: python scripts/generate_testcases.py")
            print("3. Run: node scripts/generatePlaywrightTests.js")
            print("4. Run: npm test")
            print("5. Run: streamlit run dashboard.py")
            
        except Exception as e:
            print(f"❌ Setup failed: {str(e)}")
            print("\n🔧 Manual installation steps:")
            print("1. pip install openai python-dotenv streamlit pandas requests")
            print("2. npm install")
            print("3. npx playwright install")
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
        
        # Check npm
        npm_commands = ["npm", "npm.cmd", "npm.exe"]
        npm_found = False
        
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
            raise Exception("npm is not installed or not accessible")
        
        print("✅ All prerequisites met!")
    
    def install_dependencies_robust(self):
        """Install dependencies with better error handling"""
        print("\n📦 Installing dependencies...")
        
        # Upgrade pip first
        print("Upgrading pip...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         capture_output=True, timeout=60)
        except Exception as e:
            print(f"⚠️ Warning: Failed to upgrade pip: {e}")
        
        # Try simplified requirements first
        print("Installing Python dependencies (simplified)...")
        requirements_file = self.project_root / "requirements-simple.txt"
        
        if requirements_file.exists():
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-simple.txt"], 
                             capture_output=True, timeout=300)
                print("✅ Python dependencies installed (simplified)")
                return
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Simplified requirements failed: {e}")
        
        # Fallback: install core packages individually
        print("Installing core packages individually...")
        core_packages = [
            "openai>=1.3.0",
            "python-dotenv>=1.0.0", 
            "streamlit>=1.28.0",
            "pandas>=2.1.0",
            "requests>=2.31.0",
            "beautifulsoup4>=4.12.0",
            "youtube-transcript-api>=0.6.1"
        ]
        
        failed_packages = []
        for package in core_packages:
            try:
                print(f"Installing {package}...")
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                             capture_output=True, timeout=120)
                print(f"✅ {package} installed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                failed_packages.append(package)
        
        if failed_packages:
            print(f"⚠️ Warning: Failed to install packages: {failed_packages}")
            print("You may need to install them manually later.")
        
        # Install Node.js dependencies
        print("Installing Node.js dependencies...")
        npm_commands = ["npm", "npm.cmd", "npm.exe"]
        npm_installed = False
        
        for npm_cmd in npm_commands:
            try:
                subprocess.run([npm_cmd, "install"], capture_output=True, timeout=300)
                print("✅ Node.js dependencies installed")
                npm_installed = True
                break
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        if not npm_installed:
            raise Exception("Failed to install Node.js dependencies")
    
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
            subprocess.run(["npx", "playwright", "install"], capture_output=True, timeout=600)
            print("✅ Playwright browsers installed")
        except Exception as e:
            print(f"⚠️ Warning: Failed to install Playwright browsers: {e}")
            print("You can install them manually later with: npx playwright install")

def main():
    """Main entry point"""
    setup = RobustQAGenieSetup()
    setup.run()

if __name__ == "__main__":
    main() 