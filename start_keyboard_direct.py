"""Direct launcher for AI Keyboard - no prompts"""
import sys
sys.path.insert(0, '.')

from keyboard_layer.integration import KeyboardService

print("=" * 60)
print("🚀 Starting AI Keyboard (Full Mode)")
print("=" * 60)
print()
print("✅ AI Integration: REAL MODE (Ollama)")
print()

try:
    service = KeyboardService(ui_mock_mode=False, ai_mock_mode=False)
    service.run_forever()
except KeyboardInterrupt:
    print("\n\n👋 Shutting down...")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
