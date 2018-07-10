from flask_io import fields, Schema, post_load, validate
from .models import Contact
from .services import validate_username


class ContactSchema(Schema):
    """
    Serialization-Deserialization class for User.
    """
    id = fields.UUID(dump_only=True)
    first_name = fields.String(50, required=True)
    surname = fields.String(50, required=True)
    username = fields.String(required=True, validator=validate_username,
                             error_messages={'validator_failed':
                                             {'message': 'Username must be 6-52 characters length and'
                                                         ' can only contain: a-zA-Z0-9.'}})
    email = fields.Email(required=True, validate=validate.Length(5, 128))

    @post_load
    def _post_load(self, data):
        if self.partial:
            return data
        return Contact(**data)
