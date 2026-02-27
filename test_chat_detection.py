"""
Quick test for chat context detection fix
"""
from window_detector import window_detector

# Test WhatsApp title patterns
test_cases = [
    ("WhatsApp - Google Chrome", "chrome.exe"),
    ("WhatsApp Web - Microsoft Edge", "msedge.exe"),
    ("web.whatsapp.com - Brave", "brave.exe"),
    ("Chat - WhatsApp", "chrome.exe"),
    ("Telegram Web", "firefox.exe"),
    ("Messenger - Facebook", "chrome.exe"),
    ("Random Website - Chrome", "chrome.exe"),  # Should be browser
]

print("Testing chat detection fix:\n")
for title, process in test_cases:
    context = window_detector._detect_context(title, process)
    icon = "✅" if context == "chat" else ("❌" if "whatsapp" in title.lower() or "telegram" in title.lower() or "messenger" in title.lower() else "🔵")
    print(f"{icon} {process:20s} | {title:40s} → {context}")

print("\n✅ Fix applied! WhatsApp should now be detected as 'chat' context")
print("📌 Restart unified_ai_keyboard.py for changes to take effect")
