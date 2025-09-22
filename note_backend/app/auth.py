from functools import wraps
from typing import Optional, Tuple
from flask import current_app, request, jsonify
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from . import db

TOKEN_MAX_AGE_SECONDS = 60 * 60 * 24 * 7  # 7 days

def _get_serializer() -> URLSafeTimedSerializer:
    secret = current_app.config["SECRET_KEY"]
    return URLSafeTimedSerializer(secret_key=secret, salt="note-keeper-auth")

# PUBLIC_INTERFACE
def hash_password(password: str) -> str:
    """Hash a password using Werkzeug's generate_password_hash."""
    return generate_password_hash(password)

# PUBLIC_INTERFACE
def verify_password(pw_hash: str, password: str) -> bool:
    """Verify a plaintext password against a stored hash."""
    return check_password_hash(pw_hash, password)

# PUBLIC_INTERFACE
def create_token(user: User) -> str:
    """Create a signed token for the given user."""
    s = _get_serializer()
    return s.dumps({"uid": user.id, "email": user.email})

# PUBLIC_INTERFACE
def verify_token(token: str) -> Optional[Tuple[int, str]]:
    """Verify a signed token and return (user_id, email) if valid."""
    s = _get_serializer()
    try:
        data = s.loads(token, max_age=TOKEN_MAX_AGE_SECONDS)
        return int(data["uid"]), data.get("email")
    except SignatureExpired:
        return None
    except BadSignature:
        return None

# PUBLIC_INTERFACE
def auth_required(fn):
    """Decorator to require Bearer token auth on routes.

    Expects Authorization header: 'Bearer <token>'.
    On success, injects g.current_user with the User instance.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        from flask import g
        auth_header = request.headers.get("Authorization", "")
        prefix = "Bearer "
        if not auth_header.startswith(prefix):
            return jsonify({"message": "Missing or invalid Authorization header"}), 401
        token = auth_header[len(prefix):].strip()
        vt = verify_token(token)
        if not vt:
            return jsonify({"message": "Invalid or expired token"}), 401
        user_id, _email = vt
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"message": "User not found"}), 401
        g.current_user = user
        return fn(*args, **kwargs)
    return wrapper
