from marshmallow import Schema, fields

class LocationSchema(Schema):
    person_id = fields.Integer(required=True)
    longitude = fields.String(required=True)
    latitude = fields.String(required=True)
    creation_time = fields.DateTime(required=True)
