from marshmallow import Schema, fields


class MeasurementSchema(Schema):
    id = fields.Integer(dump_only=True)
    measurement = fields.String(required=True)
    timestamp = fields.DateTime(dump_only=True)
    energy = fields.Float(dump_only=True)
    tags_id = fields.Integer(dump_only=True)
