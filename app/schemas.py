from marshmallow import post_dump, fields
from marshmallow.decorators import post_dump
from marshmallow.exceptions import ValidationError
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.fields import Nested
from markdown import markdown

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
    BibPerdiodesHisto,
)


class FlattenMixin:
    __flatten_key__ = "name"

    @post_dump
    def flat(self, data, **kw):
        return data[self.__flatten_key__]


class MardownField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return markdown(value)

class BibSiecleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibSiecle


class BibSiecleFlattenSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibSiecle


class BibPerdiodesHistoFlattenSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibPerdiodesHisto


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


class BibNaturesPersonnesMoralesFlattendSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibNaturesPersonnesMorales


class BibProfessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibProfessions


class BibProfessionNestedSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibProfessions


class BibMonuLieuNatureFlattenSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibMonuLieuNature


class BibDeplacementsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibDeplacements


class BibDeplacementsFlattenSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibDeplacements


class BibDesignationMobImgSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibDesignationMobImg


class BibDesignationMobImgSchemaFlatten(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibDesignationMobImg


class BibTechniquesMobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibTechniquesMob


class MediaSchema(SmartRelationshipsMixin, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Media

    url = fields.String()


class PaysSchemaFlatten(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = Pays


class PaysSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pays


class RegionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Region


class RegionFlattenSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = Region


class DepartementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Departement

    region = fields.Nested(RegionSchema)


class DepartementFlattenSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = Departement


class CommuneSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Commune

    departement = fields.Nested(DepartementSchema)


class CommuneSchemaFlatten(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = Commune


class FlatteLocaliteMixin:
    @post_dump
    def flat_loc(self, data, **kw):
        if (
            "commune" in data
            and type(data["commune"]) is dict
            and data["commune"] is not None
        ):
            data["_departement"] = (
                data.get("commune", {}).get("departement", {}).get("name", "")
            )
            data["_region"] = (
                data.get("commune", {})
                .get("departement", {})
                .get("region")
                .get("name", "")
            )
            data["_commune"] = data.get("commune", {}).get("name")
            data["commune"] = data.pop("_commune")
            data["departement"] = data.pop("_departement")
            data["region"] = data.pop("_region")
        return data


class MonumentLieuSchema(
    SmartRelationshipsMixin, FlatteLocaliteMixin, ma.SQLAlchemyAutoSchema
):
    class Meta:
        model = MonumentLieu
        include_fk = True

    description = MardownField()
    histoire = MardownField()
    siecles = Nested(BibSiecleFlattenSchema, many=True)
    natures = Nested(BibMonuLieuNatureFlattenSchema, many=True)
    etats_conservation = Nested(BibEtatConservationFlattenSchema, many=True)
    auteurs = Nested(BibSourceAuteurSchema, many=True)
    pays = Nested(PaysSchemaFlatten)
    commune = Nested(CommuneSchema)
    contributeurs = Nested(BibContributeur, many=True)
    redacteurs = Nested(BibRedacteurSchema, many=True)
    materiaux = Nested(BibMateriauxSchema, many=True)

    medias = Nested(MediaSchema, many=True)
    categorie = fields.Constant("Monuments & Lieux")
    meta_categorie = fields.Constant("monuments_lieux")

    mobiliers_images_liees = Nested("MobilierImageSchema", many=True)
    personnes_morales_liees = Nested("PersonneMoraleSchema", many=True)
    personnes_physiques_liees = Nested("PersonnePhysiqueSchema", many=True)


class MobilierImageSchema(
    SmartRelationshipsMixin, FlatteLocaliteMixin, ma.SQLAlchemyAutoSchema
):
    class Meta:
        model = MobilierImage
        include_fk = True

    description = MardownField()
    histoire = MardownField()

    medias = Nested(MediaSchema, many=True)
    siecles = Nested(BibSiecleFlattenSchema, many=True)
    pays = Nested(PaysSchemaFlatten)
    commune = Nested(CommuneSchema)
    departement = Nested(DepartementFlattenSchema)
    region = Nested(RegionFlattenSchema)
    designations = Nested(BibDesignationMobImgSchemaFlatten, many=True)
    etats_conservation = Nested(BibEtatConservationFlattenSchema, many=True)
    materiaux = Nested(BibMateriauxSchema, many=True)
    personnes_morales_liees = Nested("PersonneMoraleSchema", many=True)
    monuments_lieux_liees = Nested(MonumentLieuSchema, many=True)
    auteurs = Nested(BibSourceAuteurSchema, many=True)
    contributeurs = Nested(BibContributeur, many=True)
    redacteurs = Nested(BibRedacteurSchema, many=True)

    categorie = fields.Constant("Mobilier & Images")
    meta_categorie = fields.Constant("mobiliers_images")


class PersonneMoraleSchema(
    SmartRelationshipsMixin, FlatteLocaliteMixin, ma.SQLAlchemyAutoSchema
):
    class Meta:
        model = PersonneMorale
        include_fk = True

    medias = Nested(MediaSchema, many=True)
    siecles = Nested(BibSiecleFlattenSchema, many=True)
    natures = Nested(BibNaturesPersonnesMoralesFlattendSchema, many=True)
    pays = Nested(PaysSchemaFlatten)
    commune = Nested(CommuneSchema)
    contributeurs = Nested(BibContributeur, many=True)
    redacteurs = Nested(BibRedacteurSchema, many=True)

    mobiliers_images_liees = Nested("MobilierImageSchema", many=True)
    personnes_physiques_liees = Nested("PersonnePhysiqueSchema", many=True)
    monuments_lieux_liees = Nested(MonumentLieuSchema, many=True)

    categorie = fields.Constant("Personnes morales")
    meta_categorie = fields.Constant("personnes_morales")


class PersonnePhysiqueSchema(
    SmartRelationshipsMixin, FlatteLocaliteMixin, ma.SQLAlchemyAutoSchema
):
    class Meta:
        model = PersonnePhysique
        include_fk = True

    medias = Nested(MediaSchema, many=True)
    modes_deplacements = Nested(BibDeplacementsFlattenSchema, many=True)
    periodes_historiques = Nested(BibPerdiodesHistoFlattenSchema, many=True)

    siecles = Nested(BibSiecleFlattenSchema, many=True)
    professions = Nested(BibProfessionNestedSchema, many=True)
    pays = Nested(PaysSchemaFlatten)
    commune = Nested(CommuneSchema)
    personnes_morales_liees = Nested(PersonneMoraleSchema, many=True)
    monuments_lieux_liees = Nested(MonumentLieuSchema, many=True)
    contributeurs = Nested(BibContributeur, many=True)
    redacteurs = Nested(BibRedacteurSchema, many=True)

    categorie = fields.Constant("Personnes physiques")
    meta_categorie = fields.Constant("personnes_physiques")


# MonumentLieu.personnes_morales_liees = Nested(PersonneMoraleSchema, many=True)
# MonumentLieu.personnes_physiques_liees = Nested(PersonnePhysiqueSchema, many=True)
