from marshmallow import Schema, fields


class AnalyticsSchema(Schema):
    operation = fields.String()
    class_name = fields.String()
    field_name = fields.String()
    operation_value = fields.String()