"""
Recording Status Popup - Shows recording/stopped status
Simple always-on-top popup for voice recording feedback
"""
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class RecordingStatusPopup(QWidget):
    """
    Simple popup to show recording status
    - Shows "🔴 Recording..." when recording
    - Shows "✅ Stopped Recording" when stopped
    - Always on top, semi-transparent
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the popup UI"""
        # Window flags for always-on-top, frameless
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.Tool  # Prevents taskbar icon
        )
        
        # CRITICAL: Don't steal focus from other apps
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Semi-transparent background
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        # Initial size
        self.resize(350, 80)
        self.position_center_top()
        
        # Auto-hide timer
        self.auto_hide_timer = QTimer()
        self.auto_hide_timer.timeout.connect(self.hide)
        
        # Start hidden
        self.hide()
    
    def position_center_top(self):
        """Position popup at top-center of screen"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = 50  # 50 pixels from top
        self.move(x, y)
    
    def show_recording(self):
        """Show recording status"""
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(220, 50, 50, 240);
                border-radius: 12px;
                border: 3px solid rgba(255, 100, 100, 255);
            }
            QLabel {
                color: white;
                padding: 10px;
            }
        """)
        self.status_label.setText("🔴 Recording...")
        self.position_center_top()
        self.show()
        self.raise_()
        self.activateWindow()
        
    def show_stopped(self):
        """Show stopped status, then auto-hide"""
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(50, 180, 80, 240);
                border-radius: 12px;
                border: 3px solid rgba(100, 220, 130, 255);
            }
            QLabel {
                color: white;
                padding: 10px;
            }
        """)
        self.status_label.setText("✅ Stopped Recording")
        self.position_center_top()
        self.show()
        self.raise_()
        self.activateWindow()
        
        # Auto-hide after 2 seconds
        self.auto_hide_timer.start(2000)
    
    def show_processing(self):
        """Show processing status"""
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(50, 120, 220, 240);
                border-radius: 12px;
                border: 3px solid rgba(100, 150, 255, 255);
            }
            QLabel {
                color: white;
                padding: 10px;
            }
        """)
        self.status_label.setText("🔄 Processing...")
        self.position_center_top()
        self.show()
        self.raise_()
        self.activateWindow()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    popup = RecordingStatusPopup()
    
    print("Testing recording popup...")
    print("Showing recording status...")
    popup.show_recording()
    
    QTimer.singleShot(3000, lambda: popup.show_stopped())
    QTimer.singleShot(5000, lambda: popup.show_processing())
    QTimer.singleShot(7000, app.quit)
    
    sys.exit(app.exec_())
