#!/usr/bin/env python3
"""
OpenManus Setup and Error Diagnosis Script
This script helps identify and fix common setup errors in OpenManus.
"""

import subprocess
import sys
from pathlib import Path
import importlib.util

def check_python_version():
    """Check if Python version is compatible."""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 10):
        print("❌ ERROR: Python 3.10 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    else:
        print(f"✅ Python version OK: {sys.version}")
        return True

def check_config_file():
    """Check if config.toml exists."""
    print("\n🔍 Checking configuration file...")
    config_path = Path("config/config.toml")
    if not config_path.exists():
        print("❌ ERROR: config/config.toml is missing!")
        print("   Run: cp config/config.example.toml config/config.toml")
        print("   Then edit config/config.toml with your API keys")
        return False
    else:
        print("✅ Configuration file exists")
        # Check if API key is set
        try:
            with open(config_path, 'r') as f:
                content = f.read()
                if "YOUR_API_KEY_HERE" in content:
                    print("⚠️  WARNING: You still need to set your API key in config/config.toml")
                    return False
                else:
                    print("✅ API key appears to be configured")
                    return True
        except Exception as e:
            print(f"❌ ERROR: Could not read config file: {e}")
            return False

def check_essential_dependencies():
    """Check if essential Python packages are installed."""
    print("\n🔍 Checking essential dependencies...")
    essential_packages = [
        'pydantic',
        'openai', 
        'loguru',
        'fastapi',
        'uvicorn'
    ]
    
    missing_packages = []
    for package in essential_packages:
        try:
            spec = importlib.util.find_spec(package)
            if spec is None:
                missing_packages.append(package)
                print(f"❌ Missing: {package}")
            else:
                print(f"✅ Found: {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ Missing: {package}")
    
    if missing_packages:
        print(f"\n❌ ERROR: Missing {len(missing_packages)} essential packages!")
        print("   Install with: pip install " + " ".join(missing_packages))
        return False
    else:
        print("✅ All essential dependencies found")
        return True

def check_optional_dependencies():
    """Check optional dependencies."""
    print("\n🔍 Checking optional dependencies...")
    optional_packages = [
        ('playwright', 'Browser automation'),
        ('docker', 'Sandbox functionality'),
        ('pytest', 'Testing')
    ]
    
    for package, description in optional_packages:
        try:
            spec = importlib.util.find_spec(package)
            if spec is None:
                print(f"⚠️  Optional: {package} ({description})")
            else:
                print(f"✅ Optional: {package} ({description})")
        except ImportError:
            print(f"⚠️  Optional: {package} ({description})")

def check_workspace_directory():
    """Check if workspace directory exists."""
    print("\n🔍 Checking workspace directory...")
    workspace_path = Path("workspace")
    if not workspace_path.exists():
        print("⚠️  Creating workspace directory...")
        workspace_path.mkdir(exist_ok=True)
        print("✅ Workspace directory created")
    else:
        print("✅ Workspace directory exists")
    return True

def run_basic_import_test():
    """Test basic imports."""
    print("\n🔍 Testing basic imports...")
    try:
        # Test configuration loading
        from app.config import config
        print("✅ Configuration module imports successfully")
        
        # Test basic agent import
        from app.agent.base import BaseAgent
        print("✅ Base agent imports successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def create_basic_readme():
    """Create a basic troubleshooting README."""
    readme_content = """# OpenManus Setup Troubleshooting

## Common Errors and Solutions

### 1. ModuleNotFoundError: No module named 'pydantic'
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Config file missing
**Solution:** Create config file
```bash
cp config/config.example.toml config/config.toml
# Edit config/config.toml and set your API key
```

### 3. API Key not set
**Solution:** Edit config/config.toml and replace YOUR_API_KEY_HERE with your actual API key

### 4. Network timeouts during pip install
**Solution:** Try installing core packages individually:
```bash
pip install pydantic openai loguru fastapi uvicorn
```

### 5. Browser automation not working
**Solution:** Install playwright browsers:
```bash
pip install playwright
playwright install
```

## Quick Setup Check
Run the setup script to diagnose issues:
```bash
python setup_check.py
```
"""
    
    with open("TROUBLESHOOTING.md", "w") as f:
        f.write(readme_content)
    print("✅ Created TROUBLESHOOTING.md")

def main():
    """Main setup check function."""
    print("🚀 OpenManus Setup Diagnostic")
    print("=" * 40)
    
    all_good = True
    
    # Run all checks
    all_good &= check_python_version()
    all_good &= check_config_file()
    all_good &= check_essential_dependencies()
    check_optional_dependencies()
    all_good &= check_workspace_directory()
    all_good &= run_basic_import_test()
    
    # Create troubleshooting guide
    create_basic_readme()
    
    print("\n" + "=" * 40)
    if all_good:
        print("🎉 All checks passed! OpenManus should work correctly.")
        print("   You can now run: python main.py")
    else:
        print("❌ Some issues found. Please fix the errors above.")
        print("   Check TROUBLESHOOTING.md for detailed solutions.")
    
    return all_good

if __name__ == "__main__":
    main()