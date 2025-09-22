import os

# PUBLIC_INTERFACE
class Config:
    """Application configuration loaded from environment variables.

    Environment variables:
    - SECRET_KEY: Secret key for signing session tokens (required).
    - DATABASE_URL: Database connection string; defaults to sqlite database under instance folder.
    """

    SECRET_KEY = os.getenv("SECRET_KEY", None)
    # Default to sqlite database file in project instance dir
    DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "instance", "note.db")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.abspath(DEFAULT_DB_PATH)}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    # OpenAPI / Docs
    API_TITLE = "Note Keeper API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/docs"
    OPENAPI_SWAGGER_UI_PATH = ""
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
