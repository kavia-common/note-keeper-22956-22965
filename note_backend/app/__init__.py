from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from .config import Config
import os

# Initialize SQLAlchemy globally for model modules to import
db = SQLAlchemy()

def create_app():
    """Application factory to create and configure the Flask app."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Basic CORS for frontend consumption
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Load config
    app.config.from_object(Config)

    # Validate SECRET_KEY presence (used for token signing)
    if not app.config.get("SECRET_KEY"):
        # For CI/docs generation, we set a fallback; in production, set via env.
        app.config["SECRET_KEY"] = "dev-insecure-secret-change-me"

    # Ensure SQLite instance directory exists if using file-based sqlite path
    if app.config.get("SQLALCHEMY_DATABASE_URI", "").startswith("sqlite:///"):
        # Extract path after sqlite:/// and create parent dirs if needed
        db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "", 1)
        instance_dir = os.path.dirname(db_path)
        if instance_dir and not os.path.exists(instance_dir):
            os.makedirs(instance_dir, exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Configure OpenAPI/Docs
    app.config["API_TITLE"] = app.config.get("API_TITLE", "Note Keeper API")
    app.config["API_VERSION"] = app.config.get("API_VERSION", "v1")
    app.config["OPENAPI_VERSION"] = app.config.get("OPENAPI_VERSION", "3.0.3")
    app.config["OPENAPI_SWAGGER_UI_PATH"] = app.config.get("OPENAPI_SWAGGER_UI_PATH", "")
    app.config["OPENAPI_SWAGGER_UI_URL"] = app.config.get("OPENAPI_SWAGGER_UI_URL", "https://cdn.jsdelivr.net/npm/swagger-ui-dist/")
    app.config["OPENAPI_URL_PREFIX"] = app.config.get("OPENAPI_URL_PREFIX", "/docs")

    # Single Api initialization; avoid duplicate Api(app) at module level
    api = Api(app)

    # Import and register blueprints
    from .routes.health import blp as health_blp
    from .routes.auth import blp as auth_blp
    from .routes.notes import blp as notes_blp

    api.register_blueprint(health_blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(notes_blp)

    # Create database tables if not exist
    with app.app_context():
        from . import models  # noqa: F401  ensure models are registered
        db.create_all()

    return app

# Expose app for external imports like run.py and generate_openapi.py
app = create_app()
