import os

# Configuration settings
MOCK_MODE = os.getenv("MOCK_MODE", "False").lower() in ("true", "1", "t")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2") # Default model
