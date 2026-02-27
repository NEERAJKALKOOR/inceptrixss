"""
Check and verify voice dependencies for real Whisper integration
Ensures all required packages are installed before running
"""

import sys
import subprocess

def check_dependency(module_name, pip_name=None):
    """Check if a Python module is installed"""
    if pip_name is None:
        pip_name = module_name
    
    try:
        __import__(module_name)
        return True, None
    except ImportError as e:
        return False, pip_name

def check_ffmpeg():
    """Check if ffmpeg is available on system"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def main():
    print("=" * 70)
    print("🔍 VOICE SETUP CHECKER")
    print("=" * 70)
    print()
    
    all_good = True
    missing_packages = []
    
    # Check Python packages
    print("📦 Checking Python packages...")
    print()
    
    dependencies = [
        ("pyaudio", "PyAudio"),
        ("whisper", "openai-whisper"),
        ("PyQt5", "PyQt5"),
        ("pynput", "pynput"),
        ("pyperclip", "pyperclip"),
    ]
    
    for module, pip_package in dependencies:
        is_installed, _ = check_dependency(module, pip_package)
        status = "✅" if is_installed else "❌"
        print(f"   {status} {pip_package}")
        
        if not is_installed:
            all_good = False
            missing_packages.append(pip_package)
    
    print()
    
    # Check ffmpeg
    print("🎬 Checking ffmpeg...")
    ffmpeg_installed = check_ffmpeg()
    status = "✅" if ffmpeg_installed else "❌"
    print(f"   {status} ffmpeg")
    print()
    
    if not ffmpeg_installed:
        all_good = False
    
    # Summary
    print("=" * 70)
    
    if all_good:
        print("✅ ALL DEPENDENCIES INSTALLED!")
        print()
        print("🚀 You can now run the AI keyboard with real voice:")
        print("   python unified_ai_keyboard.py")
        print()
        print("💡 Tip: On first run, Whisper will download the 'base' model (~140MB)")
        print("   This happens automatically and only once.")
    else:
        print("⚠️  MISSING DEPENDENCIES")
        print()
        
        if missing_packages:
            print("📦 Install missing Python packages:")
            print(f"   pip install {' '.join(missing_packages)}")
            print()
            print("   OR install from requirements file:")
            print("   pip install -r requirements_ui.txt")
            print()
        
        if not ffmpeg_installed:
            print("🎬 Install ffmpeg:")
            print("   Windows:")
            print("   - Option 1: choco install ffmpeg")
            print("   - Option 2: Download from https://ffmpeg.org/download.html")
            print()
            print("   Mac:")
            print("   - brew install ffmpeg")
            print()
            print("   Linux:")
            print("   - sudo apt install ffmpeg")
            print()
    
    print("=" * 70)
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
