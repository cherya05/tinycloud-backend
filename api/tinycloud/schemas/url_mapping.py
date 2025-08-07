from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from models.url_mapping import UrlMapping

class UrlSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UrlMapping

        load_instance = True