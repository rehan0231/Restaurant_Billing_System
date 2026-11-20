
import hashlib
import hmac
import secrets

from database import get_connection


# Password hashing function
def hash_password(password):

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )

    return salt.hex() + "$" + password_hash.hex()


# Password verification function
def verify_password(password, stored_hash):

    try:
        salt_hex, hash_hex = stored_hash.split("$")

        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)

    except (ValueError, AttributeError):
        return False

    actual_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )

    return hmac.compare_digest(actual_hash, expected_hash)


# Create default admin account
def ensure_default_admin():

    conn = get_connection()

    try:

        admin = conn.execute(
            "SELECT admin_id FROM admin LIMIT 1"
        ).fetchone()

        if admin is None:

            password_hash = hash_password("admin123")

            conn.execute("""
                INSERT INTO admin (username, password_hash)
                VALUES (?, ?)
            """, ("admin", password_hash))

            conn.commit()

            print("Default admin account created!")

    finally:
        conn.close()


# Verify login credentials
def verify_admin(username, password):

    conn = get_connection()

    try:

        admin = conn.execute("""
            SELECT password_hash
            FROM admin
            WHERE username = ?
        """, (username,)).fetchone()

        if admin is None:
            return False

        return verify_password(
            password,
            admin["password_hash"]
        )

    finally:
        conn.close()
