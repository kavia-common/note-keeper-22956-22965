from datetime import datetime
from . import db

# PUBLIC_INTERFACE
class User(db.Model):
    """User account model for authentication."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    notes = db.relationship("Note", backref="user", lazy=True, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User {self.email}>"


# PUBLIC_INTERFACE
class Note(db.Model):
    """Note model representing a user's note."""
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, default="", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Note {self.id} user={self.user_id}>"
