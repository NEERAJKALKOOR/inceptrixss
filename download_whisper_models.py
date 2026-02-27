"""
Download Whisper models manually (for offline use)
Run this script when you have internet connection
"""
import whisper
import os

def download_models():
    models = {
        'tiny': '39MB - Fastest, good for testing',
        'base': '140MB - Good balance',
        'small': '470MB - Better accuracy (recommended)',
        'medium': '1.5GB - High accuracy',
        'large': '3GB - Best accuracy'
    }
    
    print("=" * 60)
    print("WHISPER MODEL DOWNLOADER")
    print("=" * 60)
    
    cache_dir = os.path.expanduser("~/.cache/whisper")
    print(f"\n📁 Models will be saved to: {cache_dir}")
    
    print("\nAvailable models:")
    for name, desc in models.items():
        print(f"  - {name}: {desc}")
    
    print("\n" + "=" * 60)
    
    for model_name in ['tiny', 'base', 'small']:
        try:
            print(f"\n🔄 Downloading {model_name} model...")
            model = whisper.load_model(model_name)
            print(f"✅ {model_name} model downloaded successfully!")
            del model  # Free memory
        except Exception as e:
            print(f"❌ Failed to download {model_name}: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Download complete!")
    print("\nYou can now use Whisper offline.")

if __name__ == "__main__":
    try:
        download_models()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have internet connection and whisper installed:")
        print("   pip install openai-whisper")
