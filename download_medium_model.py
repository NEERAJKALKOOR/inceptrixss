"""
Download Whisper MEDIUM Model (~1.5GB)
High accuracy for better voice transcription
Run this once with internet connection
"""
import whisper

print("=" * 70)
print("📥 DOWNLOADING WHISPER MEDIUM MODEL")
print("=" * 70)
print()
print("📊 Model Info:")
print("   • Size: ~1.5GB")
print("   • Accuracy: HIGH (better than base and small)")
print("   • Speed: 2-4 seconds transcription time")
print("   • Languages: 99+ supported")
print("   • Offline: Yes (after download)")
print()
print("⚠️  This will download 1.5GB - may take 5-15 minutes")
print()
print("=" * 70)
print()

import time
print("Starting download in 3 seconds...")
print("Press Ctrl+C to cancel")
time.sleep(3)

try:
    print("\n🔄 Downloading 'medium' model...")
    print("   📡 Downloading from OpenAI...")
    print("   ⏳ This may take several minutes depending on your internet speed")
    print()
    
    model = whisper.load_model("medium")
    
    print()
    print("=" * 70)
    print("✅ ✅ ✅ MEDIUM MODEL DOWNLOADED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("📁 Model cached at:")
    import os
    cache_dir = os.path.expanduser("~/.cache/whisper")
    print(f"   {cache_dir}")
    print()
    print("🚀 Benefits:")
    print("   • Much better accuracy than base model")
    print("   • Handles accents and background noise better")
    print("   • More accurate punctuation")
    print("   • Better for technical/specialized vocabulary")
    print()
    print("💡 The AI keyboard will now use this model automatically!")
    print()
    
except KeyboardInterrupt:
    print("\n\n❌ Download cancelled")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure you have:")
    print("   • Stable internet connection")
    print("   • Enough disk space (~1.5GB)")
    print("   • Whisper installed: pip install openai-whisper")

print()
print("=" * 70)
