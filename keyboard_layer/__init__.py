"""
Keyboard Layer (Role 1) - OS-level keyboard integration
Captures keystrokes, detects hotkeys, manages text insertion
"""
from .keyboard_hook import KeyboardMonitor
from .text_manager import TextManager
from .integration import KeyboardService

__all__ = ['KeyboardMonitor', 'TextManager', 'KeyboardService']
