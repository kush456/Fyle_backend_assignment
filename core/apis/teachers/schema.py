# was empty beforehand, there was no teacher schema 
from marshmallow import Schema, fields

class TeacherSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()