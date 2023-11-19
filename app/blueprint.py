import os
from pathlib import Path

from flask import Blueprint, request, current_app, send_file
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import NotFound
from sqlalchemy import func
from PIL import Image, ImageOps


routes = Blueprint("main", __name__)

from app.models import MonumentLieu, MobilierImage, PersonneMorale, PersonnePhysique
from app.env import db
from app.schemas import (
    MonumentLieuSchema,
    MobilierImageSchema,
    PersonneMoraleSchema,
    PersonnePhysiqueSchema,
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


@routes.route("/monuments_lieux", methods=["GET"])
def get_all_monuments_lieux():
    params = MultiDict(request.args)

    fields = params.get("fields", type=str, default=[])
    limit = params.get("limit", type=str, default=100)
    if fields:
        fields = fields.split(",")

    q = MonumentLieu.select.auto_joinload(MonumentLieu, fields=fields).where_publish()
    if limit:
        q = q.limit(limit)
    if "random" in params:
        q = q.order_by(func.random())

    monuments_lieux = db.session.execute(q).unique().scalars()
    # TODO : paginate ?

    return MonumentLieuSchema(only=fields).dump(monuments_lieux, many=True)


@routes.route("/monuments_lieux/<int:id>", methods=["GET"])
def get_one_monument_lieu(id):
    fields = [
        "etat_conservation",
        "auteurs",
        "contributeurs",
        "redacteurs",
        "materiaux",
        "medias",
    ]
    q = MonumentLieu.select.auto_joinload(MonumentLieu, fields=fields).filter_by(id=id)
    monument_lieu = db.session.execute(q).unique().scalars().one_or_none()
    if not monument_lieu:
        raise NotFound()
    return MonumentLieuSchema(only=fields).dump(monument_lieu)


##### MOBILIER IMAGE


@routes.route("/mobiliers_images", methods=["GET"])
def get_all_mobiliers_images():
    params = MultiDict(request.args)

    fields = params.get("fields", type=str, default=[])
    limit = params.get("limit", type=str, default=100)
    if fields:
        fields = fields.split(",")

    q = MobilierImage.select.auto_joinload(MobilierImage, fields=fields).where_publish()
    if limit:
        q = q.limit(limit)
    if "random" in params:
        q = q.order_by(func.random())

    mobilier_images = db.session.execute(q).unique().scalars()
    return MonumentLieuSchema(only=fields).dump(mobilier_images, many=True)


@routes.route("/mobiliers_images/<int:id>", methods=["GET"])
def get_one_mobiliers_images(id):
    fields = []
    q = MobilierImage.select.auto_joinload(MobilierImage, fields=fields).filter_by(
        id=id
    )
    mobilier_image = db.session.execute(q).unique().scalars().one_or_none()
    if not mobilier_image:
        raise NotFound()
    return MobilierImageSchema(only=fields).dump(mobilier_image)


## Personnes morales


@routes.route("/personnes_morales", methods=["GET"])
def get_all_personnes_morales():
    params = MultiDict(request.args)
    fields = params.get("fields", type=str, default=[])
    limit = params.get("limit", type=str, default=100)
    if fields:
        fields = fields.split(",")

    q = PersonneMorale.select.auto_joinload(PersonneMorale, fields=fields)
    if limit:
        q = q.limit(limit)
    if "random" in params:
        q = q.order_by(func.random())

    personnes_morales = db.session.execute(q).unique().scalars()
    return PersonneMoraleSchema(only=fields).dump(personnes_morales, many=True)


@routes.route("/personnes_morales/<int:id>", methods=["GET"])
def get_one_personne_morale(id):
    fields = []
    q = PersonneMorale.select.auto_joinload(PersonneMorale, fields=fields).filter_by(
        id=id
    )
    persone_morale = db.session.execute(q).unique().scalars().one_or_none()
    if not persone_morale:
        raise NotFound()
    return PersonneMoraleSchema(only=fields).dump(persone_morale)


@routes.route("/personnes_physiques", methods=["GET"])
def get_all_personnes_physiques():
    params = MultiDict(request.args)
    fields = params.get("fields", type=str, default=[])
    limit = params.get("limit", type=str, default=100)
    if fields:
        fields = fields.split(",")

    q = PersonnePhysique.select.auto_joinload(PersonnePhysique, fields=fields)
    if limit:
        q = q.limit(limit)
    if "random" in params:
        q = q.order_by(func.random())

    personnes_physiques = db.session.execute(q).unique().scalars()
    return PersonnePhysiqueSchema(only=fields).dump(personnes_physiques, many=True)


@routes.route("/personnes_physiques/<int:id>", methods=["GET"])
def get_one_personne_physique(id):
    fields = []
    q = PersonnePhysique.select.auto_joinload(
        PersonnePhysique, fields=fields
    ).filter_by(id=id)
    persone_physique = db.session.execute(q).unique().scalars().one_or_none()
    if not persone_physique:
        raise NotFound()
    return PersonnePhysiqueSchema(only=fields).dump(persone_physique)
