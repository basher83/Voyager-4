#!/usr/bin/env python3
"""
Setup script for Claude Code Prompt Development Framework

This script initializes the development environment and installs dependencies.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a shell command with error handling."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def setup_environment():
    """Set up the development environment."""
    print("🚀 Setting up Claude Code Prompt Development Framework")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("💡 Tip: Consider using a virtual environment:")
        print("   python -m venv venv")
        print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("   pip install -r requirements.txt")
        return False
    
    # Install Claude Code CLI (if not already installed)
    print("🔧 Checking Claude Code CLI installation...")
    result = subprocess.run("claude --version", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("📦 Claude Code CLI not found. Installing...")
        if not run_command("npm install -g @anthropic-ai/claude-code", "Installing Claude Code CLI"):
            print("💡 Tip: You may need to install Node.js first: https://nodejs.org/")
            return False
    else:
        print("✅ Claude Code CLI is already installed")
    
    # Download required models for sentence transformers
    print("🔧 Downloading sentence transformer models...")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Sentence transformer models downloaded successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not download sentence transformer models: {e}")
        print("   Models will be downloaded automatically when first used")
    
    # Create necessary directories (if they don't exist)
    directories = [
        "evaluations/results",
        "test-cases/real-world",
        "test-cases/synthetic", 
        "test-cases/edge-cases",
        "prompts/codebase-understanding/examples",
        "prompts/bug-fixing/examples",
        "prompts/code-generation/examples",
        "prompts/testing/examples",
        "prompts/project-management/examples"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directory structure verified")
    
    # Set up environment variables template
    env_template = """# Claude Code Prompt Development Framework Environment Variables

# Anthropic API Key (required)
ANTHROPIC_API_KEY=your_api_key_here

# Optional: Claude Code specific settings
CLAUDE_CODE_MODEL=claude-3-opus-20240229
CLAUDE_CODE_MAX_TOKENS=2048

# Evaluation settings
EVAL_PARALLEL_REQUESTS=false
EVAL_RETRY_ATTEMPTS=3

# Logging
LOG_LEVEL=INFO
"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_template)
        print("✅ Created .env template file")
        print("   Please add your ANTHROPIC_API_KEY to .env file")
    else:
        print("✅ .env file already exists")
    
    # Create .gitignore if it doesn't exist
    gitignore_content = """# Environment variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Evaluation results
evaluations/results/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Test outputs
test_output/
temp/
"""
    
    if not os.path.exists(".gitignore"):
        with open(".gitignore", "w") as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore file")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Add your ANTHROPIC_API_KEY to the .env file")
    print("2. Review the ROADMAP.md for project milestones")
    print("3. Explore the documentation in docs/ directory")
    print("4. Run a test evaluation:")
    print("   python evaluations/scripts/evaluate_prompt.py --prompt templates/base/codebase-overview-template.md --test-cases test-cases/examples/codebase_understanding_examples.json")
    
    return True

def main():
    """Main setup function."""
    try:
        success = setup_environment()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()