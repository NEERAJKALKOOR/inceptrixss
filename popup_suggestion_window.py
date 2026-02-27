"""
Bottom-Right Popup Suggestion Window
Shows AI suggestions in a bottom-right popup that can be accepted with Tab
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QPalette, QColor


class SuggestionPopup(QWidget):
    """
    Bottom-right popup window for AI suggestions.
    - Always-on-top
    - Semi-transparent rounded box
    - Tab to accept, Esc to reject
    - Auto-hide after timeout
    """
    
    suggestion_accepted = pyqtSignal(str)  # Signal when user accepts
    suggestion_rejected = pyqtSignal()  # Signal when user rejects
    
    def __init__(self):
        super().__init__()
        self.current_suggestion = ""
        self.is_visible = False
        self.auto_hide_timer = QTimer()
        self.auto_hide_timer.timeout.connect(self.hide_popup)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the popup UI"""
        # Window flags for always-on-top, frameless
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.Tool  # Prevents taskbar icon
        )
        
        # Semi-transparent background
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(40, 40, 40, 240);
                border-radius: 10px;
                color: white;
            }
            QLabel#title {
                font-size: 12px;
                font-weight: bold;
                color: #4CAF50;
                padding: 5px;
            }
            QLabel#suggestion {
                font-size: 13px;
                color: #E0E0E0;
                padding: 10px;
                background-color: rgba(60, 60, 60, 200);
                border-radius: 5px;
                margin: 5px;
            }
            QLabel#hint {
                font-size: 10px;
                color: #888;
                padding: 5px;
            }
        """)
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)
        
        # Title
        self.title_label = QLabel("✨ AI Suggestion")
        self.title_label.setObjectName("title")
        layout.addWidget(self.title_label)
        
        # Suggestion text
        self.suggestion_label = QLabel("")
        self.suggestion_label.setObjectName("suggestion")
        self.suggestion_label.setWordWrap(True)
        self.suggestion_label.setMaximumWidth(400)
        layout.addWidget(self.suggestion_label)
        
        # Hint text
        self.hint_label = QLabel("⌨️ Tab to accept • Esc to reject")
        self.hint_label.setObjectName("hint")
        self.hint_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.hint_label)
        
        self.setLayout(layout)
        
        # Initial size and position
        self.resize(450, 150)
        self.position_bottom_right()
        
        # Start hidden
        self.hide()
        
    def position_bottom_right(self):
        """Position window at bottom-right of screen"""
        screen = QApplication.primaryScreen().geometry()
        margin = 20
        x = screen.width() - self.width() - margin
        y = screen.height() - self.height() - margin - 40  # Extra margin for taskbar
        self.move(x, y)
    
    def show_suggestion(self, suggestion: str, confidence: float = 0.9, auto_hide_ms: int = 15000):
        """
        Show a suggestion in the popup.
        
        Args:
            suggestion: The AI-generated suggestion text
            confidence: Confidence score (0-1) - affects title color
            auto_hide_ms: Auto-hide timeout in milliseconds (0 = no auto-hide)
        """
        self.current_suggestion = suggestion
        
        # Update text
        self.suggestion_label.setText(suggestion)
        
        # Update title based on confidence
        if confidence >= 0.8:
            emoji = "✨"
            color = "#4CAF50"  # Green
        elif confidence >= 0.5:
            emoji = "💡"
            color = "#FFC107"  # Yellow
        else:
            emoji = "💭"
            color = "#FF9800"  # Orange
        
        self.title_label.setText(f"{emoji} AI Suggestion")
        self.title_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 12px; padding: 5px;")
        
        # Adjust size based on content
        self.adjustSize()
        self.setMinimumWidth(400)
        self.setMaximumWidth(500)
        
        # Position at bottom-right
        self.position_bottom_right()
        
        # Show window with force
        self.show()
        self.raise_()
        self.activateWindow()  # Try to bring to front
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.is_visible = True
        
        # Start auto-hide timer
        if auto_hide_ms > 0:
            self.auto_hide_timer.start(auto_hide_ms)
        
    def hide_popup(self):
        """Hide the popup"""
        self.hide()
        self.is_visible = False
        self.auto_hide_timer.stop()
        
    def accept_suggestion(self):
        """User accepted the suggestion (Tab pressed)"""
        if self.is_visible and self.current_suggestion:
            self.suggestion_accepted.emit(self.current_suggestion)
            self.hide_popup()
            
    def reject_suggestion(self):
        """User rejected the suggestion (Esc pressed)"""
        if self.is_visible:
            self.suggestion_rejected.emit()
            self.hide_popup()
    
    def keyPressEvent(self, event):
        """Handle keyboard events (this won't work - keys are captured by pynput)"""
        # Note: This method won't work because the window doesn't have focus
        # Key handling must be done in the main keyboard listener
        pass


# Test the popup
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    popup = SuggestionPopup()
    
    # Show test suggestion
    popup.show_suggestion(
        "This is a test AI suggestion that appears in the bottom-right corner. "
        "Press Tab to accept or Esc to reject.",
        confidence=0.9
    )
    
    def on_accept(text):
        print(f"✅ Accepted: {text}")
        QTimer.singleShot(1000, app.quit)
    
    def on_reject():
        print("❌ Rejected")
        QTimer.singleShot(1000, app.quit)
    
    popup.suggestion_accepted.connect(on_accept)
    popup.suggestion_rejected.connect(on_reject)
    
    print("Popup shown! (It will close automatically after handling)")
    
    sys.exit(app.exec_())
