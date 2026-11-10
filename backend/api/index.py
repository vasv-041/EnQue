"""
Vercel serverless entrypoint for EnQue backend service.
Vercel's FastAPI preset looks for api/index.py relative to the service root.
"""
import sys
import os

# Ensure the backend package root is importable
_here = os.path.dirname(os.path.abspath(__file__))          # backend/api/
_backend_root = os.path.dirname(_here)                       # backend/
_project_root = os.path.dirname(_backend_root)               # project root
for _p in [_project_root, _backend_root]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Default to /tmp DB (writable in Vercel serverless)
if not os.environ.get("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite:////tmp/enque.db"

from app.main import app  # noqa: E402, F401
