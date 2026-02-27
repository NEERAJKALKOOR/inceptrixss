"""
Window Detection Module - Detect active app for context-aware AI
"""
import sys

# Try to import win32gui for Windows
try:
    import win32gui
    import win32process
    import psutil
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("⚠️ win32gui not available. Install with: pip install pywin32 psutil")


class WindowDetector:
    """
    Detects active window and maps to context categories
    """
    
    # Context mapping: app keywords -> context type
    CONTEXT_MAP = {
        "outlook": "email",
        "gmail": "email",
        "thunderbird": "email",
        "mail": "email",
        
        "vscode": "code",
        "visual studio code": "code",
        "pycharm": "code",
        "intellij": "code",
        "sublime": "code",
        "notepad++": "code",
        "atom": "code",
        "vim": "code",
        "jupyter": "code",
        
        "slack": "chat",
        "discord": "chat",
        "teams": "chat",
        "telegram": "chat",
        "whatsapp": "chat",
        "messenger": "chat",
        
        "word": "document",
        "winword": "document",
        "writer": "document",
        "libreoffice": "document",
        "pages": "document",
        
        "chrome": "browser",
        "firefox": "browser",
        "edge": "browser",
        "brave": "browser",
        "safari": "browser",
        
        "notepad": "notes",
        "onenote": "notes",
        "notion": "notes",
        "evernote": "notes",
    }
    
    def __init__(self):
        self.last_detected_app = None
        self.last_detected_context = "general"
    
    def get_active_window_info(self):
        """Get active window title and process name"""
        if not WIN32_AVAILABLE:
            return {"title": "Unknown", "process": "unknown", "context": "general"}
        
        try:
            # Get active window
            hwnd = win32gui.GetForegroundWindow()
            
            # Get window title
            title = win32gui.GetWindowText(hwnd)
            
            # Get process ID
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            
            # Get process name
            try:
                process = psutil.Process(pid)
                process_name = process.name().lower()
            except:
                process_name = "unknown"
            
            # Detect context
            context = self._detect_context(title, process_name)
            
            self.last_detected_app = process_name
            self.last_detected_context = context
            
            return {
                "title": title,
                "process": process_name,
                "context": context
            }
            
        except Exception as e:
            print(f"⚠️ Could not detect window: {e}")
            return {
                "title": "Unknown",
                "process": "unknown",
                "context": "general"
            }
    
    def _detect_context(self, title: str, process_name: str) -> str:
        """
        Detect context type based on window title and process name
        Returns: email, code, chat, document, browser, notes, or general
        """
        title_lower = title.lower()
        process_lower = process_name.lower()
        
        # FIRST: Check browser URL/title patterns (for web apps)
        # This must come BEFORE process check to catch WhatsApp Web, Gmail, etc.
        if any(browser in process_lower for browser in ["chrome", "firefox", "edge", "brave"]):
            if any(site in title_lower for site in ["gmail", "outlook.com", "mail.yahoo"]):
                return "email"
            elif any(site in title_lower for site in ["github", "stackoverflow", "repl.it", "leetcode", "codepen"]):
                return "code"
            elif any(site in title_lower for site in ["whatsapp", "web.whatsapp", "telegram", "messenger", "discord.com", "slack.com", "teams.microsoft"]):
                return "chat"
            elif any(site in title_lower for site in ["docs.google.com", "office.com"]):
                return "document"
            # Generic browser (not a recognized web app)
            return "browser"
        
        # SECOND: Check process name for native apps
        for keyword, context in self.CONTEXT_MAP.items():
            # Skip browser keywords - already handled above
            if keyword in ["chrome", "firefox", "edge", "brave", "safari"]:
                continue
            if keyword in process_lower:
                return context
        
        # THIRD: Check window title as fallback
        for keyword, context in self.CONTEXT_MAP.items():
            if keyword in title_lower:
                return context
        
        return "general"
    
    def get_context(self) -> str:
        """Get current context (cached)"""
        return self.last_detected_context
    
    def get_app_name(self) -> str:
        """Get current app name (cached)"""
        return self.last_detected_app or "unknown"


# Singleton instance
window_detector = WindowDetector()


def get_active_context():
    """Quick function to get current context"""
    info = window_detector.get_active_window_info()
    return info["context"]


def get_active_app_info():
    """Get full window info"""
    return window_detector.get_active_window_info()


if __name__ == "__main__":
    """Test window detection"""
    print("🔍 Window Detection Test")
    print("="*60)
    
    for i in range(5):
        info = get_active_app_info()
        print(f"\n🪟 Active Window:")
        print(f"   Title: {info['title']}")
        print(f"   Process: {info['process']}")
        print(f"   Context: {info['context']}")
        
        import time
        time.sleep(3)
        print("\n   Switch to a different app in 3 seconds...")
