from marshmallow import Schema, fields, validate

# PUBLIC_INTERFACE
class SignUpSchema(Schema):
    """Request schema for user registration."""
    email = fields.Email(required=True, description="User email address")
    password = fields.String(required=True, validate=validate.Length(min=6), description="User password (min 6 chars)")


# PUBLIC_INTERFACE
class LoginSchema(Schema):
    """Request schema for user login."""
    email = fields.Email(required=True, description="User email address")
    password = fields.String(required=True, description="User password")


# PUBLIC_INTERFACE
class TokenSchema(Schema):
    """Response schema for auth token."""
    token = fields.String(required=True, description="Bearer token for authenticated requests")


# PUBLIC_INTERFACE
class UserSchema(Schema):
    """Response schema for user info."""
    id = fields.Integer()
    email = fields.Email()
    created_at = fields.DateTime()


# PUBLIC_INTERFACE
class NoteCreateSchema(Schema):
    """Request schema for creating a note."""
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    content = fields.String(load_default="", required=False)


# PUBLIC_INTERFACE
class NoteUpdateSchema(Schema):
    """Request schema for updating a note."""
    title = fields.String(validate=validate.Length(min=1, max=255))
    content = fields.String()


# PUBLIC_INTERFACE
class NoteSchema(Schema):
    """Response schema for a note."""
    id = fields.Integer()
    user_id = fields.Integer()
    title = fields.String()
    content = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
