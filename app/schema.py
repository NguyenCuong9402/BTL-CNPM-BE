import typing

from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow

ma = Marshmallow()


class ReviewsSchema(Schema):
    id = fields.String()
    user_id = fields.String()
    user_name = fields.String()
    comment = fields.String()
    created_date = fields.Integer()


