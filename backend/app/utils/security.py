"""Security & Password hashing utilities.
Uses hashlib PBKDF2 HMAC SHA-256 for maximum reliability across modern Python versions,
avoiding passlib bcrypt 5.0 compatibility bug in Python 3.14.
"""

import hashlib
import os
import secrets

def hash_password(password: str) -> str:
    """Hashes a password using PBKDF2-HMAC-SHA256 with 100,000 rounds and a random salt."""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()
    return f"{salt}${pwd_hash}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against the stored salt$hash."""
    try:
        salt, stored_hash = hashed_password.split("$", 1)
        check_hash = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt.encode("utf-8"),
            100000
        ).hex()
        return secrets.compare_digest(stored_hash, check_hash)
    except Exception:
        return False
