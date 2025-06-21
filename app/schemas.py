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
    # BibContributeur,
    BibAutheurFiche,
    BibMateriaux,
    Media,
    MobilierImage,
    PersonneMorale,
    PersonnePhysique,
    Pays,
    Region,
    Departement,
    Commune,
    BibNatureMobImg,
    BibTechniquesMob,
    BibNaturesPersonnesMorales,
    BibProfessions,
    BibDeplacements,
    BibPerdiodesHisto,
    BibPersPhyAttestation
)


class FlattenMixin:
    __flatten_key__ = "name"

    @post_dump
    def flat(self, data, **kw):
        return data[self.__flatten_key__]


class MardownField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value:
            return markdown(value)
        else:
            return ""

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


class BibAutheurFicheSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibAutheurFiche


# class BibContributeur(ma.SQLAlchemyAutoSchema, FlattenMixin):
#     class Meta:
#         model = BibContributeur


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


class BibNatureMobImgSchema(ma.SQLAlchemyAutoSchema,):
    class Meta:
        model = BibNatureMobImg


class BibNatureMobImgSchemaFlatten(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibNatureMobImg


class BibTechniquesMobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibTechniquesMob

class BibTechniquesMobSchemaFlatten(ma.SQLAlchemyAutoSchema, FlattenMixin):
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


class BibPersPhyAttestationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BibPersPhyAttestation


class BibPersPhyAttestationFlattenSchema(ma.SQLAlchemyAutoSchema, FlattenMixin):
    class Meta:
        model = BibPersPhyAttestation

class FlatteLocaliteMixin:
    @post_dump
    def flat_loc(self, data, **kw):
        if (
            "commune" in data
            and type(data["commune"]) is dict
            and data["commune"] is not None
        ):
            if data["commune"]["departement"] is not None:
                data["_departement"] = (
                    data.get("commune", {}).get("departement", {}).get("name", "")
                )

            if data["commune"]["departement"]["region"] is not None:
                data["_region"] = (
                    data.get("commune", {})
                    .get("departement", {})
                    .get("region", {})
                    .get("name", "")
                )
            data["_commune"] = data.get("commune", {}).get("name")
            data["commune"] = data.pop("_commune")
            if "_departement" in data:
                data["departement"] = data.pop("_departement")
            if "_region" in data:
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
    bibliographie = MardownField()
    geolocalisation = MardownField()
    source = MardownField()
    
    siecles = Nested(BibSiecleFlattenSchema, many=True)
    natures = Nested(BibMonuLieuNatureFlattenSchema, many=True)
    etats_conservation = Nested(BibEtatConservationFlattenSchema, many=True)
    auteurs = Nested(BibSourceAuteurSchema, many=True)
    pays = Nested(PaysSchemaFlatten)
    commune = Nested(CommuneSchema)
    auteurs_fiche = Nested(BibAutheurFicheSchema, many=True)
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
    bibliographie = MardownField()
    source = MardownField()

    medias = Nested(MediaSchema, many=True)
    siecles = Nested(BibSiecleFlattenSchema, many=True)
    pays = Nested(PaysSchemaFlatten)
    commune = Nested(CommuneSchema)
    departement = Nested(DepartementFlattenSchema)
    region = Nested(RegionFlattenSchema)
    natures = Nested(BibNatureMobImgSchemaFlatten, many=True)
    etats_conservation = Nested(BibEtatConservationFlattenSchema, many=True)
    materiaux = Nested(BibMateriauxSchema, many=True)
    personnes_morales_liees = Nested("PersonneMoraleSchema", many=True)
    monuments_lieux_liees = Nested(MonumentLieuSchema, many=True)
    auteurs = Nested(BibSourceAuteurSchema, many=True)
    auteurs_fiche = Nested(BibAutheurFicheSchema, many=True)
    techniques = Nested(BibTechniquesMobSchemaFlatten, many=True)

    categorie = fields.Constant("Mobilier & Images")
    meta_categorie = fields.Constant("mobiliers_images")


class TranslateBoolField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value:
            return "Oui"
        else:
            return "Non"

class PersonneMoraleSchema(
    SmartRelationshipsMixin, FlatteLocaliteMixin, ma.SQLAlchemyAutoSchema
):
    class Meta:
        model = PersonneMorale
        include_fk = True

    bibliographie = MardownField()
    source = MardownField()
    acte_fondation = TranslateBoolField()

    medias = Nested(MediaSchema, many=True)
    siecles = Nested(BibSiecleFlattenSchema, many=True)
    natures = Nested(BibNaturesPersonnesMoralesFlattendSchema, many=True)
    pays = Nested(PaysSchemaFlatten)
    commune = Nested(CommuneSchema)
    auteurs_fiche = Nested(BibAutheurFicheSchema, many=True)

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

    bibliographie = MardownField()
    source = MardownField()

    medias = Nested(MediaSchema, many=True)
    modes_deplacement = Nested(BibDeplacementsFlattenSchema, many=True)
    periodes_historiques = Nested(BibPerdiodesHistoFlattenSchema, many=True)

    siecles = Nested(BibSiecleFlattenSchema, many=True)
    professions = Nested(BibProfessionNestedSchema, many=True)
    pays = Nested(PaysSchemaFlatten)
    commune = Nested(CommuneSchema)
    attestation = Nested(BibPersPhyAttestationFlattenSchema)
    personnes_morales_liees = Nested(PersonneMoraleSchema, many=True)
    monuments_lieux_liees = Nested(MonumentLieuSchema, many=True)
    auteurs_fiche = Nested(BibAutheurFicheSchema, many=True)

    categorie = fields.Constant("Personnes physiques")
    meta_categorie = fields.Constant("personnes_physiques")


# MonumentLieu.personnes_morales_liees = Nested(PersonneMoraleSchema, many=True)
# MonumentLieu.personnes_physiques_liees = Nested(PersonnePhysiqueSchema, many=True)
