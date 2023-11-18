from marshmallow import post_dump
from marshmallow.decorators import post_dump
from marshmallow.exceptions import ValidationError
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.fields import Nested


from utils_flask_sqla.schema import SmartRelationshipsMixin


from app.env import ma
from app.models import (
    MonumentLieu,
    BibSiecle,
    BibMonuLieuNature,
    BibEtatConservation,
    BibSourceAuteur,
    BibContributeur,
    BibRedacteur,
    BibMateriaux,
)


class FlattenMixin:
    __flatten_key__ = "name"

    @post_dump
    def flat(self, data, **kw):
        return data[self.__flatten_key__]


class BibSiecleSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibSiecle


class BibMateriauxSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibMateriaux


class BibRedacteurSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibRedacteur


class BibContributeur(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibContributeur


class BibEtatConservationSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibEtatConservation


class BibSourceAuteurSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibSourceAuteur


class BibMonuLieuNatureSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibMonuLieuNature


class MonumentLieuSchema(SmartRelationshipsMixin, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MonumentLieu
        include_fk = True

    siecles = Nested(BibSiecleSchema, many=True)
    natures = Nested(BibMonuLieuNatureSchema, many=True)
    etat_conservation = Nested(BibEtatConservationSchema, many=True)
    auteurs = Nested(BibSourceAuteurSchema, many=True)
    contributeurs = Nested(BibContributeur, many=True)
    redacteurs = Nested(BibRedacteurSchema, many=True)
    materiaux = Nested(BibMateriauxSchema, many=True)
