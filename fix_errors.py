#!/usr/bin/env python3
"""
Fix Common OpenManus Errors
Automated script to fix the most common setup errors in OpenManus.
"""

import shutil
import subprocess
import sys
from pathlib import Path

def fix_config_file():
    """Fix missing or incomplete config file."""
    print("🔧 Fixing configuration file...")
    
    config_path = Path("config/config.toml")
    example_path = Path("config/config.example.toml")
    
    if not config_path.exists():
        if example_path.exists():
            print("   Copying from config.example.toml...")
            shutil.copy2(example_path, config_path)
            print("✅ Configuration file created")
        else:
            print("❌ No example config found")
            return False
    
    # Update config to use more accessible defaults
    try:
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Fix common config issues
        if 'api_type' not in content:
            content = content.replace(
                'api_key = "YOUR_API_KEY"',
                'api_key = "YOUR_API_KEY"\napi_type = "openai"'
            )
        
        if 'api_version' not in content:
            content = content.replace(
                'api_type = "openai"',
                'api_type = "openai"\napi_version = "2024-02-01"'
            )
        
        with open(config_path, 'w') as f:
            f.write(content)
        
        print("✅ Configuration file updated with required fields")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False

def create_workspace():
    """Create workspace directory if missing."""
    print("🔧 Creating workspace directory...")
    workspace_path = Path("workspace")
    workspace_path.mkdir(exist_ok=True)
    print("✅ Workspace directory ready")
    return True

def install_core_dependencies():
    """Try to install core dependencies."""
    print("🔧 Installing core dependencies...")
    
    core_packages = ["pydantic", "loguru"]
    success = True
    
    for package in core_packages:
        try:
            print(f"   Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--user", package], 
                         check=True, capture_output=True)
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"   ❌ Failed to install {package}")
            success = False
    
    return success

def create_env_example():
    """Create environment example file."""
    print("🔧 Creating environment example...")
    
    env_content = """# OpenManus Environment Variables
# Copy this file to .env and set your actual values

# OpenAI API Key (required)
OPENAI_API_KEY=your_openai_api_key_here

# Alternative: Anthropic API Key
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Workspace directory
WORKSPACE_ROOT=./workspace

# Optional: Debug mode
DEBUG=false
"""
    
    env_example_path = Path(".env.example")
    if not env_example_path.exists():
        with open(env_example_path, 'w') as f:
            f.write(env_content)
        print("✅ .env.example created")
    
    return True

def create_quick_start_guide():
    """Create a quick start guide."""
    guide_content = """# OpenManus Quick Start Guide

## 🚀 Getting Started in 3 Steps

### 1. Install Dependencies
```bash
# Option A: Full installation
pip install -r requirements.txt

# Option B: Minimal installation (if having network issues)
python install_minimal.py
```

### 2. Configure API Keys
```bash
# Edit the config file
nano config/config.toml

# Set your API key (replace YOUR_API_KEY_HERE)
api_key = "sk-your-actual-openai-api-key"
```

### 3. Run OpenManus
```bash
python main.py
```

## 🔧 Troubleshooting

### Common Issues:

1. **ModuleNotFoundError: No module named 'pydantic'**
   ```bash
   pip install pydantic loguru openai
   ```

2. **Config file missing**
   ```bash
   python fix_errors.py
   ```

3. **API key not working**
   - Check your OpenAI account balance
   - Verify API key is correct
   - Make sure you have API access

### Diagnostic Tools:
- `python setup_check.py` - Check your setup
- `python fix_errors.py` - Auto-fix common issues
- `python install_minimal.py` - Install core dependencies

## 📖 Need Help?
Check the full README.md or TROUBLESHOOTING.md for detailed instructions.
"""
    
    with open("QUICK_START.md", 'w') as f:
        f.write(guide_content)
    print("✅ QUICK_START.md created")

def main():
    """Main error fixing function."""
    print("🛠️  OpenManus Error Fixing Tool")
    print("=" * 40)
    
    fixes_applied = 0
    
    # Apply fixes
    if fix_config_file():
        fixes_applied += 1
    
    if create_workspace():
        fixes_applied += 1
    
    if install_core_dependencies():
        fixes_applied += 1
    
    if create_env_example():
        fixes_applied += 1
    
    create_quick_start_guide()
    
    print(f"\n{'='*40}")
    print(f"🎯 Applied {fixes_applied} fixes")
    
    print("\n📋 Next Steps:")
    print("1. Set your API key in config/config.toml")
    print("2. Run: python setup_check.py")
    print("3. If all good, run: python main.py")
    print("\n📚 Check QUICK_START.md for detailed instructions")

if __name__ == "__main__":
    main()