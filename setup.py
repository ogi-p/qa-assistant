#!/usr/bin/env python3
"""
QA Assistant Setup Script

This script helps you set up the QA Assistant project quickly.
It will guide you through the setup process and test your configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Print the setup header."""
    print("=" * 60)
    print("🚀 QA Assistant - Setup Script")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_requirements_file():
    """Check if requirements.txt exists."""
    print("\n📦 Checking requirements file...")
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False
    
    print("✅ requirements.txt found")
    return True

def install_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        # Try pip first
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            # Try pip3
            result = subprocess.run([sys.executable, "-m", "pip3", "install", "-r", "requirements.txt"], 
                                  capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Failed to install dependencies")
            print("   Error:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_env_file():
    """Check if .env file exists and has required fields."""
    print("\n⚙️ Checking environment configuration...")
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("   You'll need to create it manually")
        return False
    
    # Read .env file
    env_vars = {}
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False
    
    # Check required variables
    required_vars = ['JIRA_SERVER', 'JIRA_EMAIL', 'JIRA_API_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        if var not in env_vars or not env_vars[var]:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("   Please add them to your .env file")
        return False
    
    print("✅ Environment configuration looks good")
    return True

def test_jira_connection():
    """Test Jira connection with a sample ticket."""
    print("\n🔍 Testing Jira connection...")
    
    try:
        # Import the ticket reader
        sys.path.append('jira_scripts')
        from jira_ticket_reader import JiraTicketReader
        
        reader = JiraTicketReader()
        ticket_info = reader.read_ticket("AP-20641")
        
        if ticket_info:
            print("✅ Jira connection successful!")
            print(f"   Tested with ticket: AP-20641")
            return True
        else:
            print("❌ Failed to read test ticket")
            return False
            
    except Exception as e:
        print(f"❌ Jira connection failed: {e}")
        return False

def create_env_template():
    """Create a template .env file if it doesn't exist."""
    print("\n📝 Creating .env template...")
    
    env_template = """# QA Assistant Environment Configuration
# Replace these values with your actual Jira credentials

JIRA_SERVER=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@domain.com
JIRA_API_TOKEN=your-api-token-here
JIRA_DEFAULT_PROJECT=AP
"""
    
    try:
        with open(".env.template", 'w') as f:
            f.write(env_template)
        print("✅ .env.template created")
        print("   Copy it to .env and add your credentials")
    except Exception as e:
        print(f"❌ Error creating template: {e}")

def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print("1. If you haven't created .env file yet:")
    print("   cp .env.template .env")
    print("   # Edit .env with your Jira credentials")
    print()
    print("2. Test your setup:")
    print("   python3 jira_scripts/jira_ticket_reader.py AP-20641")
    print()
    print("3. Check your workload:")
    print("   python3 jira_scripts/qa_workload_reader.py")
    print()
    print("4. Read the documentation:")
    print("   - QUICK_START_GUIDE.md (this file)")
    print("   - jira_scripts/quick_reference.md")
    print()
    print("🚀 You're ready to use the QA Assistant!")

def main():
    """Main setup function."""
    print_header()
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_requirements_file():
        print("\n❌ Setup cannot continue without requirements.txt")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  Dependencies installation failed")
        print("   You may need to install them manually:")
        print("   pip install -r requirements.txt")
    
    # Check environment
    env_ok = check_env_file()
    
    if not env_ok:
        create_env_template()
        print("\n⚠️  Please configure your .env file before testing")
    else:
        # Test connection
        test_jira_connection()
    
    print_next_steps()

if __name__ == "__main__":
    main()
