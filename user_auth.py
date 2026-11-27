"""Sign-up / sign-in for ProjectMentor AI.

Standard library only: passwords are hashed with PBKDF2-HMAC-SHA256 and a
random per-user salt. Plain-text passwords are never stored or logged.

Accounts live in a new `users` table in the same database your app already
uses (via database.db.get_connection). Your existing `students` table is
untouched; a user is linked to their students row through the email address.
"""

import hashlib
import hmac
import re
import secrets
import sqlite3

from database.db import get_connection

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_ROUNDS = 240_000


def _hash(password, salt_hex):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        _ROUNDS,
    ).hex()


def init_auth_tables():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_login TEXT
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def validate_password(password):
    """Return an error message, or None if the password is acceptable."""
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return "Password must contain at least one letter and one number."
    return None


def register_user(full_name, email, password):
    """Create an account. Returns (ok, message, user_dict_or_None)."""
    full_name = full_name.strip()
    email = email.strip().lower()

    salt = secrets.token_hex(16)
    password_hash = _hash(password, salt)

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT 1 FROM users WHERE email = ?",
            (email,),
        )
        if cursor.fetchone():
            return False, "An account with this email already exists. Please sign in.", None

        try:
            cursor.execute(
                """
                INSERT INTO users (full_name, email, password_hash, salt)
                VALUES (?, ?, ?, ?)
                """,
                (full_name, email, password_hash, salt),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            return False, "An account with this email already exists. Please sign in.", None

        user_id = cursor.lastrowid
    finally:
        connection.close()

    return True, "Account created.", {
        "user_id": user_id,
        "full_name": full_name,
        "email": email,
    }


def authenticate_user(email, password):
    """Check credentials. Returns (ok, message, user_dict_or_None)."""
    email = email.strip().lower()
    generic_error = "Invalid email or password."

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT user_id, full_name, email, password_hash, salt
            FROM users WHERE email = ?
            """,
            (email,),
        )
        row = cursor.fetchone()

        if row is None:
            # Hash anyway so "unknown email" and "wrong password" take similar time.
            _hash(password, "00" * 16)
            return False, generic_error, None

        user_id, full_name, user_email, stored_hash, salt = (
            row[0], row[1], row[2], row[3], row[4]
        )

        if not hmac.compare_digest(_hash(password, salt), stored_hash):
            return False, generic_error, None

        cursor.execute(
            "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?",
            (user_id,),
        )
        connection.commit()
    finally:
        connection.close()

    return True, "Signed in.", {
        "user_id": user_id,
        "full_name": full_name,
        "email": user_email,
    }