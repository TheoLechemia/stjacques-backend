import os
from pathlib import Path

from flask import Blueprint, request, current_app, send_file
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import NotFound
from sqlalchemy import func
from PIL import Image, ImageOps


routes = Blueprint("main", __name__)

from app.models import (
    MonumentLieu,
    MobilierImage,
    PersonneMorale,
    PersonnePhysique,
    Pays,
    Region,
    Departement,
    Commune,
    BibSiecle,
    BibEtatConservation,
    BibMonuLieuNature,
    BibDesignationMobImg,
    BibTechniquesMob,
    BibNaturesPersonnesMorales,
    BibProfessions,
    BibDeplacements,
)
from app.env import db
from app.schemas import (
    MonumentLieuSchema,
    MobilierImageSchema,
    PersonneMoraleSchema,
    PersonnePhysiqueSchema,
    PaysSchema,
    RegionSchema,
    DepartementSchema,
    CommuneSchema,
    BibSiecleSchema,
    BibEtatConservationSchema,
    BibMonuLieuNatureSchema,
    BibDesignationMobImgSchema,
    BibTechniquesMobSchema,
    BibNaturesPersonnesMoralesSchema,
    BibProfessionSchema,
    BibDeplacementsSchema,
)


@routes.route("/media", methods=["GET"])
def media():
    params = request.args
    if "filename" not in params:
        raise NotFound()

    file = Path(current_app.config["MEDIAS_FOLDER"], request.args["filename"])
    if not file.exists():
        raise NotFound()

    if ("h" in params) or ("w" in params):
        size = (int(params.get("h", -1)), int(params.get("w", -1)))
        file_dir = file.parent

        thum_path = file_dir / "thumb" / file.stem / f"{size[0]}_{size[1]}.png"
        if thum_path.exists():
            return send_file(thum_path)

        else:
            if not thum_path.parent.exists():
                os.makedirs(thum_path.parent)
            image = Image.open(file)

            # resize_img = ImageOps.fit(image, (size[1], size[0]), Image.ANTIALIAS)
            resize_img = image.copy()
            resize_img = ImageOps.fit(image, (size[1], size[0]), Image.ANTIALIAS)

            resize_img.save(thum_path)
            return send_file(thum_path)

    return send_file(file)


@routes.route("/pays", methods=["GET"])
def get_all_countries():
    return PaysSchema().dump(
        db.session.execute(Pays.select.order_by(Pays.name)).scalars(), many=True
    )


@routes.route("/regions", methods=["GET"])
def get_all_regions():
    return RegionSchema().dump(
        db.session.execute(Region.select.order_by(Region.name)).scalars(), many=True
    )


@routes.route("/departements", methods=["GET"])
def get_all_departments():
    return DepartementSchema().dump(
        db.session.execute(Departement.select.order_by(Departement.name)).scalars(),
        many=True,
    )


@routes.route("/siecles", methods=["GET"])
def get_all_siecles():
    return BibSiecleSchema().dump(
        db.session.execute(BibSiecle.select.order_by(BibSiecle.id)).scalars(),
        many=True,
    )


@routes.route("/etats_conservation", methods=["GET"])
def get_all_etat_conservation():
    return BibEtatConservationSchema().dump(
        db.session.execute(
            BibEtatConservation.select.order_by(BibEtatConservation.name)
        ).scalars(),
        many=True,
    )


@routes.route("/natures_monu", methods=["GET"])
def get_all_natures_monu():
    return BibMonuLieuNatureSchema().dump(
        db.session.execute(
            BibMonuLieuNature.select.order_by(BibMonuLieuNature.name)
        ).scalars(),
        many=True,
    )


@routes.route("/designations_mob", methods=["GET"])
def get_all_designations_mob():
    return BibDesignationMobImgSchema().dump(
        db.session.execute(
            BibDesignationMobImg.select.order_by(BibDesignationMobImg.name)
        ).scalars(),
        many=True,
    )


@routes.route("/techniques_mob", methods=["GET"])
def get_all_techniques_mob():
    return BibTechniquesMobSchema().dump(
        db.session.execute(
            BibTechniquesMob.select.order_by(BibTechniquesMob.name)
        ).scalars(),
        many=True,
    )


@routes.route("/natures_personnes_morales", methods=["GET"])
def get_all_natures_personnes_morales():
    return BibNaturesPersonnesMoralesSchema().dump(
        db.session.execute(
            BibNaturesPersonnesMorales.select.order_by(BibNaturesPersonnesMorales.name)
        ).scalars(),
        many=True,
    )


@routes.route("/professions", methods=["GET"])
def get_all_natures_professions():
    return BibProfessionSchema().dump(
        db.session.execute(
            BibProfessions.select.order_by(BibProfessions.name)
        ).scalars(),
        many=True,
    )


@routes.route("/deplacements", methods=["GET"])
def get_all_deplacements():
    return BibDeplacementsSchema().dump(
        db.session.execute(
            BibDeplacements.select.order_by(BibDeplacements.name)
        ).scalars(),
        many=True,
    )


@routes.route("/communes", methods=["GET"])
def get_all_communes():
    params = MultiDict(request.args)
    limit = params.get("limit", 50)

    query = Commune.select.order_by(Commune.name).limit(limit)
    if "name" in params:
        query = query.filter(Commune.name.ilike(params["name"] + "%"))
    return CommuneSchema().dump(
        db.session.execute(query).scalars(),
        many=True,
    )


############################################################
#################### END BIBS ##############################
############################################################


@routes.route("/monuments_lieux", methods=["GET", "POST"])
def get_all_monuments_lieux():
    params = MultiDict(request.args)
    if request.method == "POST" and request.is_json:
        json_data = request.get_json()
        params.update(json_data)

    fields = params.pop("fields", default=[])

    if fields:
        fields = fields.split(",")

    q = MonumentLieu.select.auto_joinload(MonumentLieu, fields=fields).auto_filters(
        params, MonumentLieu, False
    )

    monuments_lieux = db.session.execute(q).unique().scalars()
    # TODO : paginate ?

    return MonumentLieuSchema(only=fields).dump(monuments_lieux, many=True)


@routes.route("/monuments_lieux/<int:id>", methods=["GET"])
def get_one_monument_lieu(id):
    fields = [
        "etats_conservation",
        "auteurs",
        "contributeurs",
        "redacteurs",
        "materiaux",
        "medias",
        "natures",
        "siecles",
        "pays",
        "commune",
    ]
    q = MonumentLieu.select.auto_joinload(MonumentLieu, fields=fields).filter_by(id=id)
    monument_lieu = db.session.execute(q).unique().scalars().one_or_none()
    if not monument_lieu:
        raise NotFound()
    return MonumentLieuSchema(only=fields).dump(monument_lieu)


##### MOBILIER IMAGE


@routes.route("/mobiliers_images", methods=["GET", "POST"])
def get_all_mobiliers_images():
    params = MultiDict(request.args)
    if request.method == "POST" and request.is_json:
        json_data = request.get_json()
        params.update(json_data)

    fields = params.pop("fields", default=[])
    if fields:
        fields = fields.split(",")

    q = MobilierImage.select.auto_joinload(MobilierImage, fields=fields).auto_filters(
        params, MobilierImage
    )

    mobilier_images = db.session.execute(q).unique().scalars()
    return MobilierImageSchema(only=fields).dump(mobilier_images, many=True)


@routes.route("/mobiliers_images/<int:id>", methods=["GET"])
def get_one_mobiliers_images(id):
    fields = [
        "designations",
        "commune",
        "pays",
        "siecles",
        "etats_conservation",
        "materiaux",
        "medias",
    ]
    q = MobilierImage.select.auto_joinload(MobilierImage, fields=fields).filter_by(
        id=id
    )
    mobilier_image = db.session.execute(q).unique().scalars().one_or_none()
    if not mobilier_image:
        raise NotFound()
    return MobilierImageSchema(only=fields).dump(mobilier_image)


## Personnes morales


@routes.route("/personnes_morales", methods=["GET", "POST"])
def get_all_personnes_morales():
    params = MultiDict(request.args)
    if request.method == "POST" and request.is_json:
        json_data = request.get_json()
        params.update(json_data)
    fields = params.pop("fields", default=[])
    if fields:
        fields = fields.split(",")

    q = PersonneMorale.select.auto_joinload(PersonneMorale, fields=fields).auto_filters(
        params, PersonneMorale, False
    )

    personnes_morales = db.session.execute(q).unique().scalars()
    return PersonneMoraleSchema(only=fields).dump(personnes_morales, many=True)


@routes.route("/personnes_morales/<int:id>", methods=["GET"])
def get_one_personne_morale(id):
    fields = ["natures", "pays", "commune", "siecles", "medias"]
    q = PersonneMorale.select.auto_joinload(PersonneMorale, fields=fields).filter_by(
        id=id
    )
    persone_morale = db.session.execute(q).unique().scalars().one_or_none()
    if not persone_morale:
        raise NotFound()
    return PersonneMoraleSchema(only=fields).dump(persone_morale)


@routes.route("/personnes_physiques", methods=["GET", "POST"])
def get_all_personnes_physiques():
    params = MultiDict(request.args)
    if request.method == "POST" and request.is_json:
        json_data = request.get_json()
        params.update(json_data)
    fields = params.pop("fields", default=[])
    if fields:
        fields = fields.split(",")

    q = PersonnePhysique.select.auto_joinload(
        PersonnePhysique, fields=fields
    ).auto_filters(params, PersonnePhysique, False)

    personnes_physiques = db.session.execute(q).unique().scalars()
    return PersonnePhysiqueSchema(only=fields).dump(personnes_physiques, many=True)


@routes.route("/personnes_physiques/<int:id>", methods=["GET"])
def get_one_personne_physique(id):
    fields = [
        "medias",
        "siecles",
        "pays",
        "commune",
        "modes_deplacements",
        "periodes_historiques",
    ]
    q = PersonnePhysique.select.auto_joinload(
        PersonnePhysique, fields=fields
    ).filter_by(id=id)
    persone_physique = db.session.execute(q).unique().scalars().one_or_none()
    if not persone_physique:
        raise NotFound()
    return PersonnePhysiqueSchema(only=fields).dump(persone_physique)
