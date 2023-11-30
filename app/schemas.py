from marshmallow import post_dump, fields
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
    Media,
    MobilierImage,
    PersonneMorale,
    PersonnePhysique,
    Pays,
    Region,
    Departement,
    Commune,
    BibDesignationMobImg,
    BibTechniquesMob,
    BibNaturesPersonnesMorales,
    BibProfessions,
    BibDeplacements,
)


class FlattenMixin:
    __flatten_key__ = "name"

    @post_dump
    def flat(self, data, **kw):
        return data[self.__flatten_key__]


class BibSiecleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibSiecle


class BibSiecleFlattenSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
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


class BibEtatConservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibEtatConservation


class BibEtatConservationFlattenSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibEtatConservation


class BibSourceAuteurSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibSourceAuteur


class BibMonuLieuNatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibMonuLieuNature


class BibNaturesPersonnesMoralesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibNaturesPersonnesMorales


class BibProfessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibProfessions


class BibMonuLieuNatureFlattenSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibMonuLieuNature


class BibDeplacementsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibDeplacements


class BibDesignationMobImgSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibDesignationMobImg


class BibTechniquesMobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibTechniquesMob


class MediaSchema(SmartRelationshipsMixin, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Media

    url = fields.String()


class PaysSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pays


class RegionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Region


class DepartementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Departement


class CommuneSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Commune


class MonumentLieuSchema(SmartRelationshipsMixin, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MonumentLieu
        include_fk = True

    siecles = Nested(BibSiecleFlattenSchema, many=True)
    natures = Nested(BibMonuLieuNatureFlattenSchema, many=True)
    etat_conservation = Nested(BibEtatConservationFlattenSchema, many=True)
    auteurs = Nested(BibSourceAuteurSchema, many=True)
    contributeurs = Nested(BibContributeur, many=True)
    redacteurs = Nested(BibRedacteurSchema, many=True)
    materiaux = Nested(BibMateriauxSchema, many=True)
    medias = Nested(MediaSchema, many=True)
    categorie = fields.Constant("Monuments & Lieux")
    meta_categorie = fields.Constant("monuments_lieux")


class MobilierImageSchema(SmartRelationshipsMixin, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MobilierImage
        include_fk = True

    medias = Nested(MediaSchema, many=True)
    categorie = fields.Constant("Mobilier & Images")
    meta_categorie = fields.Constant("mobiliers_images")


class PersonneMoraleSchema(SmartRelationshipsMixin, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PersonneMorale
        include_fk = True

    medias = Nested(MediaSchema, many=True)
    categorie = fields.Constant("Personnes morales")
    meta_categorie = fields.Constant("personnes_morales")


class PersonnePhysiqueSchema(SmartRelationshipsMixin, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PersonnePhysique
        include_fk = True

    medias = Nested(MediaSchema, many=True)
    categorie = fields.Constant("Personnes physiques")
    meta_categorie = fields.Constant("personnes_physiques")
