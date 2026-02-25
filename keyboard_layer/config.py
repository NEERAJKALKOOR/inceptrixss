"""
Keyboard Layer Configuration
"""
import os

# Hotkey Configuration
ACTION_KEY = "f9"  # Trigger AI suggestion
VOICE_KEY = "ctrl+shift+v"  # Push-to-talk voice input
ACCEPT_KEY = "tab"  # Accept AI suggestion (when ghost text visible)
REJECT_KEY = "esc"  # Reject AI suggestion

# Text Capture Settings
MIN_TEXT_LENGTH = 3  # Minimum characters before triggering AI
DEBOUNCE_TIME = 0.5  # Seconds to wait after last keystroke before AI call
MAX_CONTEXT_LENGTH = 500  # Maximum characters to send to AI

# UI Integration
SHOW_GHOST_TEXT = True  # Display ghost text overlay
GHOST_TEXT_OFFSET = (0, 25)  # Pixels from cursor (x, y)

# Background Service
RUN_AS_SERVICE = True  # Run in background
AUTO_START = False  # Start on system boot (future feature)

# Debug
DEBUG_MODE = os.getenv("KEYBOARD_DEBUG", "False").lower() == "true"
LOG_KEYSTROKES = DEBUG_MODE  # Only log in debug mode (privacy)
