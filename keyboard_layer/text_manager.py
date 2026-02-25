"""
Text Manager - Handles active window detection, text capture, and insertion
"""
import time
from typing import Optional, Tuple
import pyperclip
import pyautogui


try:
    import win32gui
    import win32process
    import psutil
    WINDOWS_API_AVAILABLE = True
except ImportError:
    WINDOWS_API_AVAILABLE = False
    print("⚠️ pywin32 not installed. Window detection limited.")


class TextManager:
    """
    Manages text operations:
    - Detect active window/app
    - Get selected text
    - Insert/replace text inline
    - Track cursor position
    """
    
    def __init__(self):
        self.last_active_window = None
        self.last_app_name = None
        
    def get_active_window_info(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Get active window title and application name.
        
        Returns:
            (window_title, app_name)
        """
        if not WINDOWS_API_AVAILABLE:
            return ("Unknown Window", "Unknown App")
        
        try:
            # Get active window handle
            hwnd = win32gui.GetForegroundWindow()
            
            # Get window title
            window_title = win32gui.GetWindowText(hwnd)
            
            # Get process ID
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            
            # Get process name
            try:
                process = psutil.Process(pid)
                app_name = process.name()
            except:
                app_name = "Unknown"
            
            self.last_active_window = window_title
            self.last_app_name = app_name
            
            return (window_title, app_name)
            
        except Exception as e:
            return (self.last_active_window, self.last_app_name)
    
    def get_selected_text(self) -> str:
        """
        Get currently selected text by simulating Ctrl+C.
        
        Returns:
            Selected text or empty string
        """
        try:
            # Save current clipboard
            original_clipboard = pyperclip.paste()
            
            # Clear clipboard
            pyperclip.copy("")
            
            # Simulate Ctrl+C to copy selected text
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)  # Wait for clipboard
            
            # Get copied text
            selected_text = pyperclip.paste()
            
            # Restore original clipboard
            pyperclip.copy(original_clipboard)
            
            return selected_text if selected_text else ""
            
        except Exception as e:
            print(f"❌ Error getting selected text: {e}")
            return ""
    
    def insert_text(self, text: str, replace_selection: bool = False):
        """
        Insert text at cursor position.
        
        Args:
            text: Text to insert
            replace_selection: If True, replaces selected text
        """
        try:
            if replace_selection:
                # Delete selected text first
                pyautogui.press('delete')
                time.sleep(0.05)
            
            # Type the text
            # Use paste for better reliability with special characters
            original_clipboard = pyperclip.paste()
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            pyperclip.copy(original_clipboard)
            
        except Exception as e:
            print(f"❌ Error inserting text: {e}")
    
    def replace_text(self, old_text: str, new_text: str):
        """
        Replace old_text with new_text inline.
        Simulates backspace and types new text.
        
        Args:
            old_text: Text to replace
            new_text: New text to insert
        """
        try:
            # Delete old text (character by character)
            for _ in range(len(old_text)):
                pyautogui.press('backspace')
                time.sleep(0.01)  # Small delay for reliability
            
            # Insert new text
            self.insert_text(new_text, replace_selection=False)
            
        except Exception as e:
            print(f"❌ Error replacing text: {e}")
    
    def get_cursor_position(self) -> Tuple[int, int]:
        """
        Get current cursor position (approximate).
        
        Returns:
            (x, y) coordinates
        """
        try:
            # Get mouse position as approximation
            # Note: True cursor position requires accessibility APIs
            x, y = pyautogui.position()
            return (x, y)
        except:
            return (0, 0)
    
    def is_text_editor(self) -> bool:
        """
        Check if active app is a text editor.
        
        Returns:
            True if text editor detected
        """
        if not self.last_app_name:
            self.get_active_window_info()
        
        # Common text editors and apps
        text_apps = [
            'notepad.exe', 'code.exe', 'sublime_text.exe',
            'atom.exe', 'pycharm64.exe', 'devenv.exe',
            'word.exe', 'excel.exe', 'chrome.exe', 'firefox.exe',
            'slack.exe', 'discord.exe', 'teams.exe',
            'thunderbird.exe', 'outlook.exe'
        ]
        
        if self.last_app_name:
            return any(app in self.last_app_name.lower() for app in text_apps)
        
        return True  # Assume yes if unknown


# Singleton instance
text_manager = TextManager()
