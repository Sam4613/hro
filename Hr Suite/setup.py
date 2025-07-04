#!/usr/bin/env python3
"""
HR Suite Setup Script
Built by Snashworld, Promoted by ETRA.AE
RiSa AI Assistant Integration
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print setup banner"""
    print("\n" + "="*60)
    print("🚀 HR Suite - AI-Powered Setup")
    print("💫 Built by Snashworld, Promoted by ETRA.AE")
    print("🧠 RiSa AI Assistant Ready!")
    print("="*60 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ Dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "static/uploads",
        "static/temp",
        "logs",
        "backups"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ Created: {directory}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("🔧 Creating .env file...")
        
        env_content = """
# HR Suite Environment Configuration
# Built by Snashworld, Promoted by ETRA.AE

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=snashworld_hr_quantum_key_2025

# API Keys (Replace with your actual keys)
GEMINI_API_KEY=AIzaSyDgeUDnW9KEpH8iwdbEHo_Guq6oBZC0Df0
DEEPSEEK_API_KEY=sk-e3a88e3fda874a54861e6535ee0cbc42
GOOGLE_MAPS_API_KEY=AIzaSyAxHySdYo4jdHd3m9Elr2c9BMCjAuRxZzU
ASSEMBLY_AI_API_KEY=71e56535fddf4323ab22d630868c652e
SECRET_GENERATOR_KEY=o6QgB8TMU3O0oK0UjP3CZrCeVCo=

# MongoDB Configuration
MONGODB_URI=mongodb+srv://aju4613:T89STr2tuhVbdMIW@cluster0.5amj29x.mongodb.net/
MONGODB_DB=hr_suite_snashworld

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216

# Security
JWT_EXPIRATION_HOURS=24
BCRYPT_ROUNDS=12

# Features
ENABLE_AI_ASSISTANT=True
ENABLE_FACE_RECOGNITION=True
ENABLE_GPS_TRACKING=True
ENABLE_BLOCKCHAIN=True
ENABLE_VOICE_COMMANDS=True
"""
        
        with open('.env', 'w') as f:
            f.write(env_content.strip())
        
        print("  ✅ .env file created")
    else:
        print("  ✅ .env file already exists")

def check_api_keys():
    """Check if API keys are configured"""
    print("🔑 Checking API configuration...")
    
    # Read from app.py to check current keys
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'AIzaSyDgeUDnW9KEpH8iwdbEHo_Guq6oBZC0Df0' in content:
            print("  ✅ Gemini AI API key configured")
        else:
            print("  ⚠️ Gemini AI API key needs configuration")
            
        if 'sk-e3a88e3fda874a54861e6535ee0cbc42' in content:
            print("  ✅ DeepSeek API key configured")
        else:
            print("  ⚠️ DeepSeek API key needs configuration")
            
        if 'AIzaSyAxHySdYo4jdHd3m9Elr2c9BMCjAuRxZzU' in content:
            print("  ✅ Google Maps API key configured")
        else:
            print("  ⚠️ Google Maps API key needs configuration")
            
        if '71e56535fddf4323ab22d630868c652e' in content:
            print("  ✅ AssemblyAI API key configured")
        else:
            print("  ⚠️ AssemblyAI API key needs configuration")
            
    except FileNotFoundError:
        print("  ❌ app.py not found")
        return False
    
    return True

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("🗄️ Testing MongoDB connection...")
    
    try:
        from pymongo import MongoClient
        
        client = MongoClient('mongodb+srv://aju4613:T89STr2tuhVbdMIW@cluster0.5amj29x.mongodb.net/')
        db = client['hr_suite_snashworld']
        
        # Test connection
        client.admin.command('ping')
        print("  ✅ MongoDB Atlas connection successful")
        
        # Check collections
        collections = db.list_collection_names()
        print(f"  ✅ Found {len(collections)} collections")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"  ❌ MongoDB connection failed: {e}")
        return False

def create_startup_script():
    """Create startup script for different platforms"""
    print("🚀 Creating startup scripts...")
    
    # Windows batch file
    windows_script = """
@echo off
echo Starting HR Suite - AI-Powered Platform
echo Built by Snashworld, Promoted by ETRA.AE
echo.
python app.py
pause
"""
    
    with open('start_windows.bat', 'w') as f:
        f.write(windows_script)
    print("  ✅ Created start_windows.bat")
    
    # Unix shell script
    unix_script = """
#!/bin/bash
echo "Starting HR Suite - AI-Powered Platform"
echo "Built by Snashworld, Promoted by ETRA.AE"
echo ""
python3 app.py
"""
    
    with open('start_unix.sh', 'w') as f:
        f.write(unix_script)
    
    # Make executable on Unix systems
    if platform.system() != 'Windows':
        os.chmod('start_unix.sh', 0o755)
    
    print("  ✅ Created start_unix.sh")

def print_completion_message():
    """Print setup completion message"""
    print("\n" + "="*60)
    print("🎉 HR Suite Setup Complete!")
    print("\n🚀 Quick Start:")
    
    if platform.system() == 'Windows':
        print("   • Run: start_windows.bat")
        print("   • Or: python app.py")
    else:
        print("   • Run: ./start_unix.sh")
        print("   • Or: python3 app.py")
    
    print("\n🌐 Access URLs:")
    print("   • Local: http://localhost:5000")
    print("   • Network: http://0.0.0.0:5000")
    
    print("\n🧠 AI Features Available:")
    print("   ✅ RiSa AI Assistant (Gemini-powered)")
    print("   ✅ Voice Commands (AssemblyAI)")
    print("   ✅ Face Recognition (OpenCV)")
    print("   ✅ GPS Tracking (Google Maps)")
    print("   ✅ Smart Automation (DeepSeek)")
    print("   ✅ Blockchain Security")
    
    print("\n💫 Built by Snashworld, Promoted by ETRA.AE")
    print("🧠 RiSa AI Assistant Ready!")
    print("="*60 + "\n")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Check API keys
    check_api_keys()
    
    # Test MongoDB
    test_mongodb_connection()
    
    # Create startup scripts
    create_startup_script()
    
    # Print completion message
    print_completion_message()

if __name__ == "__main__":
    main()