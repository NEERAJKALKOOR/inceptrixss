"""
Debug version with VISIBLE ghost text (not transparent)
"""
import sys
sys.path.insert(0, '.')

from PyQt5.QtWidgets import QApplication
from ui_module.interface import UIController

app = QApplication.instance() or QApplication(sys.argv)

# Create UI controller
ui = UIController(mock_mode=True)

# Make overlay VISIBLE and SOLID (not transparent)
ui.overlay.setWindowOpacity(1.0)  # Solid, not transparent
ui.overlay.setStyleSheet("background-color: yellow;")  # Yellow background
ui.overlay.setGeometry(100, 100, 600, 100)  # Fixed position
ui.overlay.show()

print("=" * 60)
print("VISIBLE GHOST TEXT TEST")
print("=" * 60)
print("\n✅ Yellow window should be visible at top-left of screen")
print("\nSimulating AI suggestion...")

# Display a test suggestion
ui.overlay.display_suggestion(
    current_text="hello",
    suggestion="world! This is a test.",
    confidence=0.95
)

print("✅ Ghost text displayed")
print("\nYou should see:")
print("  - Yellow window")
print("  - Text: 'hello world! This is a test.'")
print("\nPress Ctrl+C to exit")

app.exec_()
