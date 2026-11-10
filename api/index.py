"""
Vercel serverless entrypoint for EnQue backend.
Sets up sys.path so backend package is importable, then exports the FastAPI app.
"""
import sys
import os

# Add project root to path so "backend" package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set default DATABASE_URL to /tmp (writable in Vercel serverless)
if not os.environ.get("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite:////tmp/enque.db"

from backend.app.main import app  # noqa: F401, E402
