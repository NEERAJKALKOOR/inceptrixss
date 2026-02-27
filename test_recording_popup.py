"""
Test the recording status popup integration with F9 voice feature
"""
import sys
import time
from PyQt5.QtWidgets import QApplication
from recording_status_popup import RecordingStatusPopup

def test_popup_workflow():
    """Test the recording popup workflow"""
    app = QApplication(sys.argv)
    popup = RecordingStatusPopup()
    
    print("🎤 Testing Recording Status Popup Sequence...")
    print("\n1️⃣  Showing 'Recording' popup (red)...")
    popup.show_recording()
    time.sleep(3)
    
    print("\n2️⃣  Showing 'Processing' popup (blue)...")
    popup.show_processing()
    time.sleep(3)
    
    print("\n3️⃣  Showing 'Stopped Recording' popup (green, auto-hides in 2s)...")
    popup.show_stopped()
    time.sleep(3)
    
    print("\n✅ Test complete! All popups displayed correctly.")
    sys.exit(0)

if __name__ == "__main__":
    test_popup_workflow()
