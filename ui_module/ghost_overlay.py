"""
Ghost Text Overlay - VS Code-style inline ghost suggestions
Displays AI suggestions as inline ghost text without stealing focus
True inline rendering with accurate caret position tracking
"""
import sys
import ctypes
from ctypes import wintypes
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QFont, QColor, QPalette, QFontMetrics, QCursor
from ui_module.config import *

# Windows API for accurate caret position tracking
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

class GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('flags', wintypes.DWORD),
        ('hwndActive', wintypes.HWND),
        ('hwndFocus', wintypes.HWND),
        ('hwndCapture', wintypes.HWND),
        ('hwndMenuOwner', wintypes.HWND),
        ('hwndMoveSize', wintypes.HWND),
        ('hwndCaret', wintypes.HWND),
        ('rcCaret', wintypes.RECT),
    ]


class GhostTextOverlay(QWidget):
    """
    VS Code-style inline ghost text suggestion overlay.
    - Appears exactly at caret position
    - Light gray, semi-transparent text
    - Matches system font rendering
    - Always-on-top, click-through, no focus stealing
    - Auto-dismisses on typing/cursor movement
    """
    
    suggestion_accepted = pyqtSignal(str)  # Signal when user accepts
    suggestion_rejected = pyqtSignal()  # Signal when user rejects
    
    def __init__(self):
        super().__init__()
        self.current_text = ""
        self.ghost_text = ""
        self.confidence = 0.0
        self.is_visible = False
        
        # Caret tracking
        self.last_caret_pos = None
        self.caret_check_timer = QTimer()
        self.caret_check_timer.timeout.connect(self._check_caret_position)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the transparent overlay UI with VS Code-style rendering"""
        # Window flags for always-on-top, no focus stealing, click-through
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.Tool |  # Prevents taskbar icon
            Qt.WindowTransparentForInput |  # Click-through
            Qt.WindowDoesNotAcceptFocus |  # Never accepts focus
            Qt.X11BypassWindowManagerHint  # Bypass window manager
        )
        
        # Make window fully transparent (no background)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)  # Click-through
        self.setAttribute(Qt.WA_ShowWithoutActivating)  # Show without stealing focus
        self.setWindowOpacity(1.0)
        
        # Will be positioned at caret dynamically
        self.setGeometry(100, 100, 400, 20)
        
        # Layout - minimal margins for inline appearance
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Text display - VS Code-style ghost text (light gray, italic)
        self.text_display = QLabel()
        
        # Use system default font for better matching
        system_font = QFont("Consolas", 10)  # Monospace for better alignment
        system_font.setItalic(True)  # VS Code uses italic for suggestions
        self.text_display.setFont(system_font)
        
        # VS Code ghost text color: light gray with low opacity
        self.text_display.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: rgba(128, 128, 128, 180);
                border: none;
                padding: 0px;
                margin: 0px;
            }
        """)
        self.text_display.setWordWrap(False)  # No wrapping for inline text
        
        layout.addWidget(self.text_display)
        
        self.setLayout(layout)
        
    def get_caret_position(self):
        """Get accurate caret position using Windows GUI Thread Info API"""
        try:
            gui_info = GUITHREADINFO(cbSize=ctypes.sizeof(GUITHREADINFO))
            if user32.GetGUIThreadInfo(0, ctypes.byref(gui_info)):
                if gui_info.hwndCaret:
                    # Get caret position relative to its window
                    caret_rect = gui_info.rcCaret
                    
                    # Convert to screen coordinates
                    point = wintypes.POINT()
                    point.x = caret_rect.left
                    point.y = caret_rect.top
                    
                    if user32.ClientToScreen(gui_info.hwndCaret, ctypes.byref(point)):
                        return QPoint(point.x, point.y)
        except Exception as e:
            print(f"⚠️ Caret position detection failed: {e}")
        
        # Fallback to cursor position
        return QCursor.pos()
    
    def _check_caret_position(self):
        """Monitor caret position and auto-dismiss if it moves"""
        if not self.is_visible:
            self.caret_check_timer.stop()
            return
        
        current_pos = self.get_caret_position()
        
        # If caret moved, dismiss ghost text (VS Code behavior)
        if self.last_caret_pos and current_pos != self.last_caret_pos:
            print("🔄 Caret moved - auto-dismissing ghost text")
            self.clear_suggestion()
        
        self.last_caret_pos = current_pos
    
    def display_suggestion(self, current_text: str, suggestion: str, confidence: float = 0.9):
        """
        Display VS Code-style inline ghost text suggestion at caret position.
        
        Args:
            current_text: User's current typed text (not displayed, just for context)
            suggestion: AI suggested completion text
            confidence: AI confidence score (0.0 to 1.0)
        """
        print(f"👻 display_suggestion() called!")
        print(f"   Current: '{current_text}'")
        print(f"   Suggestion: '{suggestion}'")
        print(f"   Confidence: {confidence}")
        
        self.current_text = current_text
        self.ghost_text = suggestion
        self.confidence = confidence
        
        # Display only the suggestion text (VS Code style - just the completion)
        self.text_display.setText(suggestion)
        
        # Calculate text width for proper sizing
        font_metrics = QFontMetrics(self.text_display.font())
        text_width = font_metrics.horizontalAdvance(suggestion)
        text_height = font_metrics.height()
        
        # Get accurate caret position
        caret_pos = self.get_caret_position()
        self.last_caret_pos = caret_pos
        
        # Position overlay exactly at caret (inline)
        # Slight offset to appear right after cursor
        x = caret_pos.x() + 2
        y = caret_pos.y() - 2  # Align with text baseline
        
        # Set geometry to fit text exactly
        self.setGeometry(x, y, min(text_width + 10, 600), text_height + 4)
        
        print(f"   📍 Positioned at caret: x={x}, y={y}, width={text_width}")
        
        # Show overlay
        if not self.is_visible:
            print("   📢 Showing ghost overlay...")
            self.show()
            self.raise_()  # Bring to front
            self.is_visible = True
            print("   ✅ Ghost text visible!")
        else:
            print("   ℹ️ Already visible, updating content")
        
        # Start caret position monitoring
        self.caret_check_timer.start(100)  # Check every 100ms
            
    def accept_suggestion(self):
        """User accepted the suggestion (Tab key)"""
        if self.ghost_text:
            accepted_text = self.ghost_text
            print(f"✅ Ghost text accepted: '{accepted_text}'")
            self.clear_suggestion()
            self.suggestion_accepted.emit(accepted_text)
            return accepted_text
        return None
    
    def reject_suggestion(self):
        """User rejected the suggestion (Esc key or auto-dismiss)"""
        print(f"❌ Ghost text rejected")
        self.clear_suggestion()
        self.suggestion_rejected.emit()
    
    def clear_suggestion(self):
        """Clear ghost text and hide overlay (VS Code auto-dismiss behavior)"""
        self.ghost_text = ""
        self.current_text = ""
        self.confidence = 0.0
        self.last_caret_pos = None
        
        # Stop caret monitoring
        self.caret_check_timer.stop()
        
        if self.is_visible:
            self.hide()
            self.is_visible = False
            print("   👻 Ghost text cleared")
    
    def show_ghost_text(self, text: str):
        """
        Public API: Show ghost text at current caret position.
        Simplified interface for external use.
        
        Args:
            text: Ghost text to display
        """
        self.display_suggestion("", text, 0.9)
    
    def accept_ghost_text(self):
        """Public API: Accept and commit ghost text"""
        return self.accept_suggestion()
    
    def reject_ghost_text(self):
        """Public API: Clear ghost text"""
        self.reject_suggestion()
    
    def keyPressEvent(self, event):
        """
        Handle keyboard events (Tab/Esc).
        Note: Due to WindowTransparentForInput, this may not receive events.
        Actual key handling is done by keyboard_hook.py
        """
        if event.key() == Qt.Key_Tab:
            self.accept_suggestion()
        elif event.key() == Qt.Key_Escape:
            self.reject_suggestion()
        else:
            super().keyPressEvent(event)


# Public API functions (for external use without Qt)
_ghost_overlay_instance = None

def get_ghost_overlay():
    """Get or create the global ghost overlay instance"""
    global _ghost_overlay_instance
    if _ghost_overlay_instance is None:
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        _ghost_overlay_instance = GhostTextOverlay()
    return _ghost_overlay_instance

def show_ghost_text(text: str):
    """Public API: Render VS Code–style inline ghost suggestion"""
    overlay = get_ghost_overlay()
    overlay.show_ghost_text(text)

def accept_ghost_text():
    """Public API: Commit ghost text into active application"""
    overlay = get_ghost_overlay()
    return overlay.accept_ghost_text()

def reject_ghost_text():
    """Public API: Clear ghost text immediately"""
    overlay = get_ghost_overlay()
    overlay.reject_ghost_text()



def create_overlay_app():
    """Create QApplication and overlay (singleton pattern)"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    overlay = GhostTextOverlay()
    return app, overlay
