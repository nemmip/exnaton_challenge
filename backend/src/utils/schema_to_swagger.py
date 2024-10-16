from flask_restx import fields as flask_fields
from marshmallow import fields as marshmallow_fields

TYPE_MAPPING = {
    marshmallow_fields.String: flask_fields.String,
    marshmallow_fields.Integer: flask_fields.Integer,
    marshmallow_fields.DateTime: flask_fields.DateTime,
    marshmallow_fields.Float: flask_fields.Float,
    marshmallow_fields.UUID: flask_fields.String
}


def schema_to_swagger(schema):
    schema_fields = getattr(schema, "_declared_fields")
    converted_schema = {}

    for field in schema_fields:
        converted_schema[field] = TYPE_MAPPING[type(schema_fields[field])]

    return converted_schema
