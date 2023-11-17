from marshmallow import Schema, fields
from marshmallow.validate import OneOf, Regexp, Email, Length


class ConfigSchema(Schema):
    SQLALCHEMY_DATABASE_URI = fields.String(
        required=True,
        validate=Regexp(
            "^postgresql:\/\/.*:.*@[^:]+:\w+\/\w+",
            error="Database uri is invalid ex: postgresql://monuser:monpass@server:port/db_name",
        ),
    )
