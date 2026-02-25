"""
Keyboard Hook - Captures keystrokes and detects hotkeys at OS level
Uses pynput for cross-platform keyboard monitoring
"""
import time
from typing import Callable, Optional, Set
from pynput import keyboard
from pynput.keyboard import Key, KeyCode
from keyboard_layer.config import (
    ACTION_KEY, VOICE_KEY, ACCEPT_KEY, REJECT_KEY,
    MIN_TEXT_LENGTH, DEBOUNCE_TIME, DEBUG_MODE
)
import threading


class KeyboardMonitor:
    """
    Monitors keyboard input at OS level.
    Detects hotkeys and tracks typed text.
    """
    
    def __init__(self):
        self.listener = None
        self.current_keys: Set[Key] = set()
        self.text_buffer = ""
        self.last_keystroke_time = time.time()
        
        # Callbacks
        self.on_action_key: Optional[Callable[[str], None]] = None
        self.on_voice_key: Optional[Callable[[], None]] = None
        self.on_accept_key: Optional[Callable[[], None]] = None
        self.on_reject_key: Optional[Callable[[], None]] = None
        self.on_text_change: Optional[Callable[[str], None]] = None
        
        # State
        self.is_running = False
        self.suggestion_active = False  # True when ghost text is showing
        
        # Debounce timer
        self.debounce_timer = None
        
    def start(self):
        """Start monitoring keyboard input"""
        if self.is_running:
            return
        
        self.is_running = True
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
        print("🎹 Keyboard monitor started")
        
    def stop(self):
        """Stop monitoring"""
        self.is_running = False
        if self.listener:
            self.listener.stop()
        print("🎹 Keyboard monitor stopped")
        
    def set_suggestion_active(self, active: bool):
        """Update state when ghost text is shown/hidden"""
        self.suggestion_active = active
        
    def _on_press(self, key):
        """Handle key press events"""
        try:
            self.current_keys.add(key)
            
            # Check for hotkey combinations
            if self._is_hotkey_pressed(ACTION_KEY):
                if self.on_action_key:
                    self.on_action_key(self.text_buffer)
                return
            
            if self._is_hotkey_pressed(VOICE_KEY):
                if self.on_voice_key:
                    self.on_voice_key()
                return
            
            # Tab to accept suggestion (only when suggestion is active)
            if key == Key.tab and self.suggestion_active:
                if self.on_accept_key:
                    self.on_accept_key()
                return False  # Suppress tab key
            
            # Esc to reject suggestion
            if key == Key.esc and self.suggestion_active:
                if self.on_reject_key:
                    self.on_reject_key()
                return False  # Suppress esc key
            
            # Track typed characters
            self._handle_text_input(key)
            
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Error in key press: {e}")
    
    def _on_release(self, key):
        """Handle key release events"""
        try:
            self.current_keys.discard(key)
        except:
            pass
    
    def _is_hotkey_pressed(self, hotkey: str) -> bool:
        """Check if a hotkey combination is pressed"""
        # Parse hotkey string (e.g., "ctrl+alt+k")
        parts = hotkey.lower().split('+')
        
        # Build required modifiers and key
        needs_ctrl = 'ctrl' in parts
        needs_shift = 'shift' in parts
        needs_alt = 'alt' in parts
        
        # Get the non-modifier key
        char_key = None
        special_key = None
        for part in parts:
            if part not in ['ctrl', 'shift', 'alt']:
                if part == 'space':
                    special_key = Key.space
                elif part == 'tab':
                    special_key = Key.tab
                elif part == 'esc':
                    special_key = Key.esc
                elif part == 'f12':
                    special_key = Key.f12
                elif part == 'f11':
                    special_key = Key.f11
                elif part == 'f10':
                    special_key = Key.f10
                elif part == 'f9':
                    special_key = Key.f9
                elif part == 'f8':
                    special_key = Key.f8
                elif len(part) == 1:
                    char_key = part
        
        # Check modifiers
        has_ctrl = Key.ctrl_l in self.current_keys or Key.ctrl_r in self.current_keys
        has_shift = Key.shift_l in self.current_keys or Key.shift_r in self.current_keys
        has_alt = Key.alt_l in self.current_keys or Key.alt_r in self.current_keys
        
        # Check if all required modifiers are pressed
        if needs_ctrl and not has_ctrl:
            return False
        if needs_shift and not has_shift:
            return False
        if needs_alt and not has_alt:
            return False
        
        # Check if the main key is pressed
        if special_key:
            return special_key in self.current_keys
        elif char_key:
            # Check for both upper and lower case
            return (KeyCode.from_char(char_key) in self.current_keys or
                    KeyCode.from_char(char_key.upper()) in self.current_keys)
        
        return False
    
    def _handle_text_input(self, key):
        """Track text being typed"""
        # Handle character keys
        if hasattr(key, 'char') and key.char:
            self.text_buffer += key.char
            self.last_keystroke_time = time.time()
            
            # Debounce: trigger AI after user stops typing
            if self.debounce_timer:
                self.debounce_timer.cancel()
            
            self.debounce_timer = threading.Timer(
                DEBOUNCE_TIME,
                self._trigger_text_change
            )
            self.debounce_timer.start()
        
        # Handle special keys
        elif key == Key.space:
            self.text_buffer += " "
            self.last_keystroke_time = time.time()
        
        elif key == Key.backspace:
            if self.text_buffer:
                self.text_buffer = self.text_buffer[:-1]
            self.last_keystroke_time = time.time()
        
        elif key == Key.enter:
            self.text_buffer = ""  # Reset on new line
            self.last_keystroke_time = time.time()
    
    def _trigger_text_change(self):
        """Trigger AI suggestion after debounce period"""
        if len(self.text_buffer) >= MIN_TEXT_LENGTH:
            if self.on_text_change:
                self.on_text_change(self.text_buffer)
    
    def clear_buffer(self):
        """Clear the text buffer"""
        self.text_buffer = ""
    
    def get_buffer(self) -> str:
        """Get current text buffer"""
        return self.text_buffer


# Singleton instance
keyboard_monitor = KeyboardMonitor()
