from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy import desc

from .. import db
from ..models import Note
from ..schemas import NoteSchema, NoteCreateSchema, NoteUpdateSchema
from ..auth import auth_required

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="CRUD operations for user notes (requires authentication)"
)

@blp.route("/")
class NotesList(MethodView):
    """List and create notes for the authenticated user."""

    @auth_required
    @blp.response(200, NoteSchema(many=True))
    def get(self):
        """Get all notes for the current user, sorted by updated_at desc.

        Requires:
          - Authorization: Bearer <token>
        """
        from flask import g
        notes = Note.query.filter_by(user_id=g.current_user.id).order_by(desc(Note.updated_at)).all()
        return notes

    @auth_required
    @blp.arguments(NoteCreateSchema, as_kwargs=True)
    @blp.response(201, NoteSchema)
    def post(self, title: str, content: str = ""):
        """Create a new note for the current user.

        Requires:
          - Authorization: Bearer <token>

        Request body:
          - title: string (required)
          - content: string
        """
        from flask import g
        note = Note(user_id=g.current_user.id, title=title, content=content or "")
        db.session.add(note)
        db.session.commit()
        return note


@blp.route("/<int:note_id>")
class NoteDetail(MethodView):
    """Retrieve, update, or delete a specific note."""

    @auth_required
    @blp.response(200, NoteSchema)
    def get(self, note_id: int):
        """Get a note by ID belonging to the current user."""
        from flask import g
        note = Note.query.filter_by(id=note_id, user_id=g.current_user.id).first()
        if not note:
            abort(404, message="Note not found")
        return note

    @auth_required
    @blp.arguments(NoteUpdateSchema, as_kwargs=True)
    @blp.response(200, NoteSchema)
    def patch(self, note_id: int, title=None, content=None):
        """Update note fields (partial)."""
        from flask import g
        note = Note.query.filter_by(id=note_id, user_id=g.current_user.id).first()
        if not note:
            abort(404, message="Note not found")
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        db.session.commit()
        return note

    @auth_required
    @blp.response(204)
    def delete(self, note_id: int):
        """Delete a note."""
        from flask import g
        note = Note.query.filter_by(id=note_id, user_id=g.current_user.id).first()
        if not note:
            abort(404, message="Note not found")
        db.session.delete(note)
        db.session.commit()
        return ""
