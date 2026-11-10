# Database utilities for EnQue backend
import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

# Fallback gracefully to SQLite if PostgreSQL/psycopg2 is not yet configured or in local test mode
connect_args = {}
db_url = DATABASE_URL

if "postgresql" in db_url:
    try:
        import psycopg2
    except ImportError:
        # Use local SQLite database file to avoid crashes when local postgres is offline
        db_url = "sqlite:///./enque_dev.db"
        connect_args = {"check_same_thread": False}
elif "sqlite" in db_url:
    connect_args = {"check_same_thread": False}

engine = create_engine(db_url, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for FastAPI routes – yields a DB session and closes it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
