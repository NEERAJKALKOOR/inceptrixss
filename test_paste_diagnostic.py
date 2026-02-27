"""
Diagnostic Test for Cross-App AI Rewriter
Tests clipboard and keyboard operations step-by-step
"""

import time
import pyperclip
import pyautogui

print("=" * 60)
print("🔧 Cross-App AI Rewriter - Diagnostic Test")
print("=" * 60)
print()

# Test 1: Clipboard Operations
print("Test 1: Clipboard Read/Write")
print("-" * 40)
original = pyperclip.paste()
print(f"✅ Original clipboard: '{original}'")

test_text = "Test clipboard content"
pyperclip.copy(test_text)
time.sleep(0.1)

retrieved = pyperclip.paste()
if retrieved == test_text:
    print(f"✅ Clipboard write/read: PASS")
else:
    print(f"❌ Clipboard FAILED: got '{retrieved}'")

# Restore
pyperclip.copy(original)
print()

# Test 2: Keyboard Simulation
print("Test 2: Keyboard Simulation")
print("-" * 40)
print("⚠️  In 3 seconds, open NOTEPAD and place cursor inside")
print("    The test will type 'Hello World'")
for i in range(3, 0, -1):
    print(f"   {i}...")
    time.sleep(1)

print("\n🎹 Typing 'Hello World'...")
pyautogui.write("Hello World", interval=0.05)
time.sleep(0.5)
print("✅ Typing complete")
print()

# Test 3: Ctrl+C Test
print("Test 3: Copy (Ctrl+C) Test")
print("-" * 40)
print("⚠️  SELECT THE TEXT 'Hello World' in Notepad")
print("    Test will copy it in 3 seconds")
for i in range(3, 0, -1):
    print(f"   {i}...")
    time.sleep(1)

print("\n📤 Executing Ctrl+C...")
pyperclip.copy("")  # Clear
time.sleep(0.1)
pyautogui.hotkey('ctrl', 'c')
time.sleep(0.2)

copied = pyperclip.paste()
print(f"📋 Clipboard content: '{copied}'")
if "Hello World" in copied:
    print("✅ Ctrl+C: PASS")
else:
    print("❌ Ctrl+C: FAILED (make sure text was selected)")
print()

# Test 4: Ctrl+V Test
print("Test 4: Paste (Ctrl+V) Test")
print("-" * 40)
print("⚠️  Place cursor at END of text in Notepad")
print("    Test will paste ' - AI Enhanced' in 3 seconds")
for i in range(3, 0, -1):
    print(f"   {i}...")
    time.sleep(1)

paste_text = " - AI Enhanced"
pyperclip.copy(paste_text)
time.sleep(0.15)

print("\n📥 Executing Ctrl+V with hotkey method...")
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.3)
print("✅ Paste attempt 1 complete")
print()

# Test 5: Alternative Paste Method
print("Test 5: Alternative Paste (Press/Release)")
print("-" * 40)
print("⚠️  Place cursor in Notepad again")
print("    Test will paste ' - Second Paste' in 3 seconds")
for i in range(3, 0, -1):
    print(f"   {i}...")
    time.sleep(1)

paste_text_2 = " - Second Paste"
pyperclip.copy(paste_text_2)
time.sleep(0.15)

print("\n📥 Executing Ctrl+V with press/release method...")
pyautogui.keyDown('ctrl')
time.sleep(0.05)
pyautogui.press('v')
time.sleep(0.05)
pyautogui.keyUp('ctrl')
time.sleep(0.3)
print("✅ Paste attempt 2 complete")
print()

# Test 6: Full Flow Test
print("Test 6: Complete Copy-Paste-Restore Flow")
print("-" * 40)
print("⚠️  SELECT some text in Notepad")
print("    Test will copy, modify, paste, and restore clipboard")
for i in range(5, 0, -1):
    print(f"   {i}...")
    time.sleep(1)

print("\n🔄 Starting full flow...")

# Save clipboard
original_clip = pyperclip.paste()
print(f"1. Saved clipboard: '{original_clip[:30]}...'")

# Copy
pyperclip.copy("")
time.sleep(0.1)
pyautogui.hotkey('ctrl', 'c')
time.sleep(0.2)
copied_text = pyperclip.paste()
print(f"2. Copied text: '{copied_text[:30]}...'")

# Modify
ai_text = f"{copied_text} [AI MODIFIED]"
print(f"3. AI result: '{ai_text[:30]}...'")

# Paste
pyperclip.copy(ai_text)
time.sleep(0.15)
pyautogui.keyDown('ctrl')
time.sleep(0.05)
pyautogui.press('v')
time.sleep(0.05)
pyautogui.keyUp('ctrl')
time.sleep(0.3)
print("4. Pasted AI result")

# Restore
pyperclip.copy(original_clip)
time.sleep(0.1)
final_clip = pyperclip.paste()
if final_clip == original_clip:
    print("5. ✅ Clipboard restored successfully")
else:
    print("5. ⚠️  Clipboard restore check failed")

print()
print("=" * 60)
print("🎯 Diagnostic Test Complete!")
print("=" * 60)
print()
print("📊 Results Summary:")
print("   - If all tests passed, the system should work")
print("   - If paste tests failed, pyautogui might have issues")
print("   - Try running as Administrator if paste doesn't work")
print("   - Some apps (like browsers) may block pyautogui")
print()
print("💡 Next steps:")
print("   1. If tests passed: python cross_app_ai_rewrite.py")
print("   2. If paste failed: Try cross_app_ai_simple.py")
print("   3. Still failing: Check Windows permissions")
print()
