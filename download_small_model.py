"""
Download Whisper SMALL Model (~470MB)
Better accuracy than base model
Run this once with internet connection
"""
import whisper

print("=" * 70)
print("📥 DOWNLOADING WHISPER SMALL MODEL")
print("=" * 70)
print()
print("📊 Model Info:")
print("   • Size: ~470MB")
print("   • Accuracy: Better than base")
print("   • Speed: Slightly slower than base")
print("   • Languages: 99+ supported")
print()
print("=" * 70)
print()

try:
    print("🔄 Downloading 'small' model...")
    print("   (This may take a few minutes depending on internet speed)")
    print()
    
    model = whisper.load_model("small")
    
    print()
    print("=" * 70)
    print("✅ SMALL MODEL DOWNLOADED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("The model is cached at:")
    import os
    cache_dir = os.path.expanduser("~/.cache/whisper")
    print(f"   {cache_dir}")
    print()
    print("🚀 You can now use the AI keyboard with better voice accuracy!")
    print()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure you have:")
    print("   • Internet connection")
    print("   • Whisper installed: pip install openai-whisper")
