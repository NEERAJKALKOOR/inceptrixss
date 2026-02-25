"""
Ghost Text Overlay - Transparent always-on-top window
Displays AI suggestions as inline ghost text without stealing focus
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette
from ui_module.config import *


class GhostTextOverlay(QWidget):
    """
    Transparent overlay window that displays ghost text suggestions.
    Always-on-top, non-intrusive, does not steal focus.
    """
    
    suggestion_accepted = pyqtSignal(str)  # Signal when user accepts
    suggestion_rejected = pyqtSignal()  # Signal when user rejects
    
    def __init__(self):
        super().__init__()
        self.current_text = ""
        self.ghost_text = ""
        self.confidence = 0.0
        self.is_visible = False
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the transparent overlay UI"""
        # Window flags for always-on-top, no focus stealing
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.Tool  # Prevents taskbar icon
            # Removed WindowTransparentForInput to make it more visible for testing
        )
        
        # Make window semi-transparent (more visible for testing)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)  # More visible than default
        
        # Fixed position for testing (top-right corner)
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen.width() - 650, 50, 600, 150)
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Text display area
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFont(QFont("Segoe UI", 12))
        self.text_display.setStyleSheet(f"""
            QTextEdit {{
                background-color: rgba(255, 255, 255, 240);
                border: 2px solid #cccccc;
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        
        # Confidence indicator
        self.confidence_label = QLabel("")
        self.confidence_label.setFont(QFont("Segoe UI", 8))
        self.confidence_label.setAlignment(Qt.AlignRight)
        self.confidence_label.setStyleSheet("color: #666666;")
        
        layout.addWidget(self.text_display)
        layout.addWidget(self.confidence_label)
        
        self.setLayout(layout)
        
    def display_suggestion(self, current_text: str, suggestion: str, confidence: float = 0.9):
        """
        Display ghost text suggestion
        
        Args:
            current_text: User's current typed text
            suggestion: AI suggested completion/replacement
            confidence: AI confidence score (0.0 to 1.0)
        """
        print(f"👻 display_suggestion() called!")
        print(f"   Current: '{current_text}'")
        print(f"   Suggestion: '{suggestion}'")
        print(f"   Confidence: {confidence}")
        
        self.current_text = current_text
        self.ghost_text = suggestion
        self.confidence = confidence
        
        # Build HTML with ghost text styling
        html = self._build_ghost_html(current_text, suggestion, confidence)
        self.text_display.setHtml(html)
        
        # Update confidence indicator
        self._update_confidence_display(confidence)
        
        # Show overlay
        print(f"   Is visible: {self.is_visible}")
        if not self.is_visible:
            print("   📢 Calling self.show()...")
            self.show()
            self.is_visible = True
            print("   ✅ Ghost text should be visible now!")
        else:
            print("   ℹ️ Already visible, just updating content")
            
    def _build_ghost_html(self, current_text: str, suggestion: str, confidence: float) -> str:
        """Build HTML with ghost text styling"""
        # Determine ghost text color based on confidence
        if confidence >= HIGH_CONFIDENCE:
            ghost_color = "#808080"  # Dark gray - high confidence
            opacity = "1.0"
        elif confidence >= MEDIUM_CONFIDENCE:
            ghost_color = "#999999"  # Medium gray
            opacity = "0.8"
        else:
            ghost_color = "#aaaaaa"  # Light gray - low confidence
            opacity = "0.6"
        
        html = f"""
        <div style="font-family: 'Segoe UI', sans-serif; font-size: 14px;">
            <span style="color: #000000; font-weight: 500;">{self._escape_html(current_text)}</span>
            <span style="color: {ghost_color}; opacity: {opacity}; font-style: italic;">
                {self._escape_html(suggestion)}
            </span>
        </div>
        """
        return html
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        return (text.replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;")
                   .replace('"', "&quot;"))
    
    def _update_confidence_display(self, confidence: float):
        """Update confidence indicator"""
        if confidence >= HIGH_CONFIDENCE:
            emoji = "🟢"
            text = "High"
        elif confidence >= MEDIUM_CONFIDENCE:
            emoji = "🟡"
            text = "Medium"
        else:
            emoji = "🔴"
            text = "Low"
        
        self.confidence_label.setText(f"{emoji} Confidence: {text} ({confidence:.0%}) | Tab to accept | Esc to reject")
    
    def accept_suggestion(self):
        """User accepted the suggestion"""
        if self.ghost_text:
            accepted_text = self.ghost_text
            self.clear_suggestion()
            self.suggestion_accepted.emit(accepted_text)
            return accepted_text
        return None
    
    def reject_suggestion(self):
        """User rejected the suggestion"""
        self.clear_suggestion()
        self.suggestion_rejected.emit()
    
    def clear_suggestion(self):
        """Clear ghost text and hide overlay"""
        self.ghost_text = ""
        self.current_text = ""
        self.confidence = 0.0
        
        if self.is_visible:
            self.hide()
            self.is_visible = False
    
    def keyPressEvent(self, event):
        """Handle keyboard events (Tab/Esc)"""
        if event.key() == Qt.Key_Tab:
            self.accept_suggestion()
        elif event.key() == Qt.Key_Escape:
            self.reject_suggestion()
        else:
            super().keyPressEvent(event)


def create_overlay_app():
    """Create QApplication and overlay (singleton pattern)"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    overlay = GhostTextOverlay()
    return app, overlay
