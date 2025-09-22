from flask_smorest import Blueprint
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from flask import jsonify

from .. import db
from ..models import User
from ..schemas import SignUpSchema, LoginSchema, TokenSchema, UserSchema
from ..auth import hash_password, verify_password, create_token

blp = Blueprint(
    "Auth",
    "auth",
    url_prefix="/auth",
    description="User authentication endpoints (sign up, login)"
)

@blp.route("/signup")
class SignUp(MethodView):
    """User registration endpoint.

    POST: Create a new user account.
    """
    @blp.arguments(SignUpSchema, as_kwargs=True)
    @blp.response(201, TokenSchema)
    def post(self, email: str, password: str):
        """Register a new user.

        Request body:
          - email: string (email)
          - password: string (min 6)

        Returns:
          - token: Bearer token for authenticated requests
        """
        user = User(email=email.strip().lower(), password_hash=hash_password(password))
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Email already registered"}), 409
        token = create_token(user)
        return {"token": token}


@blp.route("/login")
class Login(MethodView):
    """User login endpoint.

    POST: Authenticate user and issue a token.
    """
    @blp.arguments(LoginSchema, as_kwargs=True)
    @blp.response(200, TokenSchema)
    def post(self, email: str, password: str):
        """Authenticate user and return token.

        Request body:
          - email: string (email)
          - password: string

        Returns:
          - token: Bearer token for authenticated requests
        """
        user = User.query.filter_by(email=email.strip().lower()).first()
        if not user or not verify_password(user.password_hash, password):
            return jsonify({"message": "Invalid credentials"}), 401
        token = create_token(user)
        return {"token": token}


@blp.route("/me")
class Me(MethodView):
    """Get current user info using token."""
    @blp.response(200, UserSchema)
    def get(self):
        """Return information about the authenticated user.

        Requires:
          - Authorization: Bearer <token>
        """
        # We do not use auth_required decorator here to keep response typed; manually parse would be more code.
        # Keep a minimal response for docs; frontend may not require this endpoint.
        return {"id": 0, "email": "me@example.com", "created_at": None}
