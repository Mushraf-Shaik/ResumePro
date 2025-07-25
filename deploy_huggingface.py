#!/usr/bin/env python3
"""
Hugging Face Spaces Deployment Helper Script
This script helps prepare and deploy ResumePro to Hugging Face Spaces
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if all requirements are met for deployment"""
    print("🔍 Checking deployment requirements...")
    
    # Check if git is installed
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print("✅ Git is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git is not installed. Please install Git first.")
        return False
    
    # Check if required files exist
    required_files = [
        "app.py",
        "Dockerfile", 
        "requirements.txt",
        "README.md",
        "backend/app.py",
        "frontend/landing.html"
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Required file missing: {file}")
            return False
        print(f"✅ Found: {file}")
    
    return True

def setup_environment():
    """Setup environment configuration"""
    print("\n🔧 Setting up environment configuration...")
    
    if not Path(".env").exists():
        if Path(".env.example").exists():
            print("📝 Creating .env file from template...")
            shutil.copy(".env.example", ".env")
            print("⚠️  Please edit .env file and add your GEMINI_API_KEY")
        else:
            print("⚠️  No .env.example found. Please create .env manually.")
    else:
        print("✅ .env file already exists")

def validate_huggingface_config():
    """Validate Hugging Face Spaces configuration"""
    print("\n🚀 Validating Hugging Face Spaces configuration...")
    
    # Check README.md header
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
        if content.startswith("---"):
            print("✅ README.md has Hugging Face Spaces header")
        else:
            print("❌ README.md missing Hugging Face Spaces header")
            return False
    
    # Check Dockerfile port configuration
    with open("Dockerfile", "r") as f:
        dockerfile_content = f.read()
        if "EXPOSE 7860" in dockerfile_content:
            print("✅ Dockerfile configured for port 7860")
        else:
            print("❌ Dockerfile not configured for Hugging Face Spaces (port 7860)")
            return False
    
    return True

def deploy_instructions():
    """Print deployment instructions"""
    print("\n📋 Deployment Instructions:")
    print("1. Create a new Space at https://huggingface.co/spaces")
    print("2. Choose 'Docker' as SDK")
    print("3. Clone your space repository:")
    print("   git clone https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME")
    print("4. Copy all files to the cloned directory")
    print("5. Set environment variables in Space settings:")
    print("   - GEMINI_API_KEY: Your Google Gemini API key")
    print("   - SECRET_KEY: A random secret key")
    print("   - FLASK_ENV: production")
    print("6. Push to deploy:")
    print("   git add .")
    print("   git commit -m 'Deploy ResumePro'")
    print("   git push origin main")

def main():
    """Main deployment helper function"""
    print("🚀 ResumePro - Hugging Face Spaces Deployment Helper")
    print("=" * 55)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please fix the issues above.")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Validate configuration
    if not validate_huggingface_config():
        print("\n❌ Configuration validation failed. Please fix the issues above.")
        sys.exit(1)
    
    print("\n✅ All checks passed! Your project is ready for Hugging Face Spaces deployment.")
    
    # Print deployment instructions
    deploy_instructions()
    
    print("\n📚 For detailed instructions, see: HUGGINGFACE_DEPLOYMENT.md")
    print("🎉 Good luck with your deployment!")

if __name__ == "__main__":
    main()
