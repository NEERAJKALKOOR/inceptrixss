"""
Quick Keyboard Test - Does automation work on your system?
"""

import time
import pyautogui
from pynput.keyboard import Controller, Key

print("="*60)
print("🧪 Keyboard Automation Test")
print("="*60)
print()

# Test 1: PyAutoGUI
print("Test 1: PyAutoGUI typing")
print("-"*40)
print("⚠️  Open NOTEPAD and click inside it NOW!")
print("    Test will type 'Hello from PyAutoGUI' in 3 seconds")
for i in range(3, 0, -1):
    print(f"   {i}...", end="\r")
    time.sleep(1)

print("\n🎹 Typing with PyAutoGUI...")
pyautogui.write("Hello from PyAutoGUI", interval=0.05)
time.sleep(0.5)
print("✅ PyAutoGUI typing done\n")

# Test 2: PyAutoGUI Ctrl+V
print("Test 2: PyAutoGUI Ctrl+V")
print("-"*40)
import pyperclip
pyperclip.copy(" [PyAutoGUI Paste Test]")
time.sleep(0.5)

print("🎹 Sending Ctrl+V with hotkey()...")
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)
print("✅ PyAutoGUI Ctrl+V sent\n")

# Test 3: PyAutoGUI press/release
print("Test 3: PyAutoGUI press/release method")
print("-"*40)
pyperclip.copy(" [Press/Release Test]")
time.sleep(0.5)

print("🎹 Sending Ctrl+V with press/release...")
pyautogui.keyDown('ctrl')
time.sleep(0.05)
pyautogui.press('v')
time.sleep(0.05)
pyautogui.keyUp('ctrl')
time.sleep(0.5)
print("✅ PyAutoGUI press/release sent\n")

# Test 4: Pynput
print("Test 4: Pynput keyboard controller")
print("-"*40)
pyperclip.copy(" [Pynput Test]")
time.sleep(0.5)

print("🎹 Sending Ctrl+V with pynput...")
kb = Controller()
with kb.pressed(Key.ctrl):
    kb.press('v')
    kb.release('v')
time.sleep(0.5)
print("✅ Pynput Ctrl+V sent\n")

# Test 5: Pynput typing
print("Test 5: Pynput typing")
print("-"*40)
print("🎹 Typing with pynput...")
kb.type(" [Pynput Typing Test]")
time.sleep(0.5)
print("✅ Pynput typing done\n")

print("="*60)
print("🎯 Test Complete!")
print("="*60)
print()
print("📊 Check Notepad NOW - You should see:")
print("   Hello from PyAutoGUI [PyAutoGUI Paste Test]")
print("   [Press/Release Test] [Pynput Test] [Pynput Typing Test]")
print()
print("❓ What do you see in Notepad?")
print("   - If you see ALL text: PyAutoGUI works!")
print("   - If you see SOME text: Note which method works")
print("   - If you see NOTHING: Automation is blocked")
print()
print("💡 Next steps:")
print("   - If PyAutoGUI works: Something else is wrong")
print("   - If only Pynput works: We'll switch to pynput")
print("   - If nothing works: Need to run as Administrator")
print()
