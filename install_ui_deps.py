"""
Installation Script for UI Module
Installs all required dependencies
"""
import subprocess
import sys


def install_package(package):
    """Install a package using pip"""
    print(f"📦 Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False


def main():
    """Install all UI module dependencies"""
    print("\n" + "="*70)
    print("INSTALLING UI MODULE DEPENDENCIES")
    print("="*70 + "\n")
    
    packages = [
        "PyQt5",
        "requests",
        "SpeechRecognition"
    ]
    
    optional_packages = [
        ("pyaudio", "For voice input - may require manual installation on Windows"),
        ("pocketsphinx", "For offline speech recognition - optional")
    ]
    
    # Install required packages
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
        print()
    
    print("\n" + "="*70)
    print(f"INSTALLATION SUMMARY: {success_count}/{len(packages)} required packages installed")
    print("="*70)
    
    # Try optional packages
    print("\n📋 OPTIONAL PACKAGES:")
    print("-"*70)
    
    for package, description in optional_packages:
        print(f"\n{package}: {description}")
        choice = input(f"Install {package}? (y/n): ").strip().lower()
        
        if choice == 'y':
            if package == "pyaudio" and sys.platform == "win32":
                print("\n⚠️  PyAudio on Windows may require pipwin:")
                print("   1. pip install pipwin")
                print("   2. pipwin install pyaudio")
                print("\nTrying standard installation first...")
                
                if not install_package(package):
                    print("\n💡 If failed, try:")
                    print("   pip install pipwin")
                    print("   pipwin install pyaudio")
            else:
                install_package(package)
    
    print("\n" + "="*70)
    print("✅ INSTALLATION COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("1. Test installation: python -c \"from ui_module import interface; print('✅ Ready!')\"")
    print("2. Run demo: python demo_ui_module.py")
    print("3. Read docs: ui_module/README.md")
    print()


if __name__ == "__main__":
    main()
