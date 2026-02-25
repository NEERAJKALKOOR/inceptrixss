"""
Simple PyQt5 window test
"""
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)

# Create a simple visible window
window = QWidget()
window.setWindowTitle("Test Window")
window.setGeometry(100, 100, 400, 200)

label = QLabel("If you see this, PyQt5 works!", window)
label.setStyleSheet("font-size: 24px; color: red; background: yellow; padding: 20px;")
label.setGeometry(50, 50, 300, 100)

window.show()

print("✅ Window should be visible on screen!")
print("Close the window to exit.")

sys.exit(app.exec_())
