from marshmallow import Schema, fields


class TagsSchema(Schema):
    id = fields.Integer()
    muid = fields.UUID()
    quality = fields.String()
