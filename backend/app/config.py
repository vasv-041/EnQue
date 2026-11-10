"""Configuration utilities for EnQue backend.
Loads environment variables (DATABASE_URL, GROQ_API_KEY, HINDSIGHT_API_KEY, OLLAMA_BASE_URL, etc.)
Safely handles missing python-dotenv by falling back to standard manual .env parser.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv_path = BASE_DIR / '.env'

if dotenv_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path)
    except ImportError:
        # Fallback manual parser if python-dotenv is not yet installed in venv
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

# Settings
APP_NAME = os.getenv("APP_NAME", "EnQue")
APP_ENV = os.getenv("APP_ENV", "development")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/enge")

# LLM Provider Configuration ("groq", "ollama", or "auto")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "auto")

# Groq API / LLM Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
PRIMARY_LLM_MODEL = os.getenv("PRIMARY_LLM_MODEL", "openai/gpt-oss-120b")
FALLBACK_LLM_MODEL = os.getenv("FALLBACK_LLM_MODEL", "qwen/qwen3-32b")

# Ollama Local LLM Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

# Hindsight Persistent Memory
HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "")

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_me_to_a_secure_random_string_dev_mode_only")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
