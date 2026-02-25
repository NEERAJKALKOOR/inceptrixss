import os

# UI Configuration
OVERLAY_OPACITY = float(os.getenv("OVERLAY_OPACITY", "0.95"))  # Slightly transparent
GHOST_TEXT_COLOR = "#808080"  # Light gray
NORMAL_TEXT_COLOR = "#000000"  # Black
BACKGROUND_COLOR = "#FFFFFF"  # White
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 100

# AI Engine Configuration
AI_ENGINE_URL = os.getenv("AI_ENGINE_URL", "http://localhost:8000/process_text")
MOCK_MODE = os.getenv("UI_MOCK_MODE", "True").lower() in ("true", "1", "t")

# Voice Configuration
VOICE_ENABLED = os.getenv("VOICE_ENABLED", "True").lower() in ("true", "1", "t")
PUSH_TO_TALK_KEY = os.getenv("PUSH_TO_TALK_KEY", "ctrl+shift+v")
SAMPLE_RATE = 16000  # For speech recognition

# Confidence thresholds for visual feedback
HIGH_CONFIDENCE = 0.85
MEDIUM_CONFIDENCE = 0.70
