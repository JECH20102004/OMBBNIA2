#!/usr/bin/env python3
"""
Minimal dependency installer for OpenManus
This script tries to install essential packages with various fallback strategies.
"""

import subprocess
import sys
import time

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def install_package(package, timeout=60):
    """Install a single package with timeout."""
    cmd = f"pip install --user --timeout {timeout} {package}"
    return run_command(cmd, f"Installing {package}")

def install_minimal_deps():
    """Install minimal dependencies needed to run OpenManus."""
    print("🚀 Installing minimal OpenManus dependencies")
    print("=" * 50)
    
    # Essential packages in order of importance
    essential_packages = [
        "pydantic",
        "loguru", 
        "openai",
        "fastapi",
        "uvicorn"
    ]
    
    success_count = 0
    
    for package in essential_packages:
        print(f"\n📦 Installing {package}...")
        if install_package(package, timeout=120):
            success_count += 1
        else:
            print(f"⚠️  Trying alternative installation for {package}...")
            # Try with different flags
            alt_cmd = f"pip install --user --no-deps --timeout 30 {package}"
            if run_command(alt_cmd, f"Alternative install {package}"):
                success_count += 1
        
        # Small delay between installs to avoid overwhelming the connection
        time.sleep(1)
    
    print(f"\n{'='*50}")
    print(f"📊 Installation Summary: {success_count}/{len(essential_packages)} packages installed")
    
    if success_count == len(essential_packages):
        print("🎉 All essential packages installed successfully!")
        return True
    elif success_count > 0:
        print("⚠️  Some packages installed. You may need to install remaining ones manually.")
        return False
    else:
        print("❌ No packages installed. Check your internet connection.")
        return False

def create_requirements_minimal():
    """Create a minimal requirements file."""
    minimal_reqs = """# Minimal requirements for OpenManus core functionality
pydantic>=2.0.0
loguru>=0.6.0
openai>=1.0.0
fastapi>=0.100.0
uvicorn>=0.20.0

# Optional but recommended
PyYAML>=6.0
tenacity>=8.0.0
"""
    
    with open("requirements-minimal.txt", "w") as f:
        f.write(minimal_reqs)
    print("✅ Created requirements-minimal.txt")

def main():
    """Main installation function."""
    create_requirements_minimal()
    
    # Try to install packages
    success = install_minimal_deps()
    
    if not success:
        print("\n💡 Alternative installation methods:")
        print("   1. Try: pip install -r requirements-minimal.txt")
        print("   2. Install packages individually:")
        print("      pip install pydantic")
        print("      pip install loguru")
        print("      pip install openai")
        print("   3. Use conda: conda install -c conda-forge pydantic loguru")
        print("   4. Check your internet connection and proxy settings")
    
    print(f"\n🔍 Run 'python setup_check.py' to verify installation")

if __name__ == "__main__":
    main()