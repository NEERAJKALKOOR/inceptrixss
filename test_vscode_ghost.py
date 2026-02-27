"""
Test VS Code-style Ghost Suggestion UI
Demonstrates the inline ghost text overlay with accurate caret tracking
"""
import sys
import time
sys.path.insert(0, '.')

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from ui_module.ghost_overlay import GhostTextOverlay, show_ghost_text, accept_ghost_text, reject_ghost_text


class TestWindow(QMainWindow):
    """Test window with text editor to demonstrate ghost suggestions"""
    
    def __init__(self):
        super().__init__()
        self.ghost_overlay = GhostTextOverlay()
        self.init_ui()
        
    def init_ui(self):
        """Initialize test window UI"""
        self.setWindowTitle("VS Code Ghost Suggestion Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central = QWidget()
        layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel("""
<h2>VS Code-Style Ghost Suggestion Demo</h2>
<p><b>How to test:</b></p>
<ul>
<li>Type some text in the editor below</li>
<li>Press <b>Ctrl+Space</b> to trigger a ghost suggestion</li>
<li>You'll see light gray, italic text appear inline at your cursor</li>
<li>Press <b>Tab</b> to accept the suggestion</li>
<li>Press <b>Esc</b> to reject it</li>
<li>Or just start typing - ghost text will auto-dismiss (VS Code behavior)</li>
</ul>
<p><b>Features demonstrated:</b></p>
<ul>
<li>✅ Inline rendering at caret position</li>
<li>✅ Light gray, italic text (VS Code style)</li>
<li>✅ Always-on-top, click-through window</li>
<li>✅ No focus stealing</li>
<li>✅ Auto-dismiss on typing</li>
<li>✅ Auto-dismiss on cursor movement</li>
<li>✅ Tab to accept, Esc to reject</li>
</ul>
        """)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Text editor
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 11))
        self.editor.setPlaceholderText("Start typing here... Press Ctrl+Space to show ghost suggestion")
        layout.addWidget(self.editor)
        
        # Status label
        self.status = QLabel("Ready. Press Ctrl+Space to show ghost suggestion.")
        self.status.setStyleSheet("padding: 5px; background: #f0f0f0;")
        layout.addWidget(self.status)
        
        central.setLayout(layout)
        self.setCentralWidget(central)
        
        # Connect signals
        self.editor.textChanged.connect(self.on_text_changed)
        self.ghost_overlay.suggestion_accepted.connect(self.on_suggestion_accepted)
        self.ghost_overlay.suggestion_rejected.connect(self.on_suggestion_rejected)
        
        # State
        self.ghost_showing = False
        
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        # Ctrl+Space to show ghost suggestion
        if event.key() == Qt.Key_Space and event.modifiers() == Qt.ControlModifier:
            self.show_test_suggestion()
            event.accept()
            return
        
        # Tab to accept (when ghost is showing)
        if event.key() == Qt.Key_Tab and self.ghost_showing:
            self.ghost_overlay.accept_suggestion()
            event.accept()
            return
        
        # Esc to reject
        if event.key() == Qt.Key_Escape and self.ghost_showing:
            self.ghost_overlay.reject_suggestion()
            event.accept()
            return
        
        # Any other key while ghost is showing - auto-dismiss
        if self.ghost_showing:
            self.ghost_overlay.reject_suggestion()
        
        super().keyPressEvent(event)
    
    def show_test_suggestion(self):
        """Show a test ghost suggestion at current cursor position"""
        cursor = self.editor.textCursor()
        current_text = cursor.block().text()
        
        # Generate a relevant suggestion based on what's typed
        suggestions = {
            "hello": " world! How are you doing today?",
            "the": " quick brown fox jumps over the lazy dog",
            "vs code": " is an amazing text editor with great features",
            "ghost": " text suggestions help predict what you'll type next",
            "python": " is a powerful and versatile programming language",
            "function": " definition with type hints and docstrings",
            "": "Start typing something..."
        }
        
        # Find matching suggestion
        suggestion = suggestions.get(current_text.lower().strip(), " and continue writing...")
        
        print(f"\n{'='*60}")
        print(f"🎯 Showing ghost suggestion")
        print(f"   Current text: '{current_text}'")
        print(f"   Suggestion: '{suggestion}'")
        print(f"{'='*60}\n")
        
        # Show ghost overlay at caret
        self.ghost_overlay.display_suggestion(current_text, suggestion, 0.95)
        self.ghost_showing = True
        self.status.setText(f"👻 Ghost suggestion shown. Press Tab to accept, Esc to reject, or type to dismiss.")
        self.status.setStyleSheet("padding: 5px; background: #e8f4f8; color: #0066cc;")
    
    def on_text_changed(self):
        """Auto-dismiss ghost text when user types (VS Code behavior)"""
        if self.ghost_showing:
            # Small delay to avoid interfering with the triggering keystroke
            QTimer.singleShot(10, self.auto_dismiss_ghost)
    
    def auto_dismiss_ghost(self):
        """Auto-dismiss helper"""
        if self.ghost_showing:
            print("📝 Text changed - auto-dismissing ghost (VS Code behavior)")
            self.ghost_overlay.reject_suggestion()
            self.ghost_showing = False
    
    def on_suggestion_accepted(self, text):
        """Handle suggestion acceptance"""
        print(f"✅ Suggestion accepted: '{text}'")
        
        # Insert the accepted text at cursor
        cursor = self.editor.textCursor()
        cursor.insertText(text)
        self.editor.setTextCursor(cursor)
        
        self.ghost_showing = False
        self.status.setText(f"✅ Suggestion accepted: '{text[:50]}...'")
        self.status.setStyleSheet("padding: 5px; background: #d4edda; color: #155724;")
        
        # Reset status after 3 seconds
        QTimer.singleShot(3000, lambda: self.status.setText("Ready. Press Ctrl+Space to show ghost suggestion."))
        QTimer.singleShot(3000, lambda: self.status.setStyleSheet("padding: 5px; background: #f0f0f0;"))
    
    def on_suggestion_rejected(self):
        """Handle suggestion rejection"""
        print(f"❌ Suggestion rejected")
        
        self.ghost_showing = False
        self.status.setText("❌ Suggestion rejected")
        self.status.setStyleSheet("padding: 5px; background: #f8d7da; color: #721c24;")
        
        # Reset status after 2 seconds
        QTimer.singleShot(2000, lambda: self.status.setText("Ready. Press Ctrl+Space to show ghost suggestion."))
        QTimer.singleShot(2000, lambda: self.status.setStyleSheet("padding: 5px; background: #f0f0f0;"))


def main():
    """Run the test"""
    print("=" * 60)
    print("VS CODE-STYLE GHOST SUGGESTION TEST")
    print("=" * 60)
    print()
    print("This demonstrates a true VS Code-style inline ghost suggestion UI")
    print("that works at the system level.")
    print()
    print("Features:")
    print("  ✅ Inline rendering at caret position")
    print("  ✅ Light gray, italic text")
    print("  ✅ Always-on-top, click-through")
    print("  ✅ No focus stealing")
    print("  ✅ Auto-dismiss on typing")
    print("  ✅ Auto-dismiss on cursor movement")
    print("  ✅ Tab to accept, Esc to reject")
    print()
    print("=" * 60)
    print()
    
    app = QApplication.instance() or QApplication(sys.argv)
    
    window = TestWindow()
    window.show()
    
    print("✅ Test window opened")
    print("📝 Start typing in the editor")
    print("⌨️  Press Ctrl+Space to show ghost suggestion")
    print()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
