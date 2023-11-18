from flask import Blueprint, request
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import NotFound


routes = Blueprint("main", __name__)

from app.models import MonumentLieu
from app.env import db
from app.schemas import MonumentLieuSchema


@routes.route("/monuments_lieux", methods=["GET"])
def get_all_monuments_lieux():
    params = MultiDict(request.args)

    fields = params.get("fields", type=str, default=[])
    if fields:
        fields = fields.split(",")
    q = MonumentLieu.select.auto_joinload(MonumentLieu, fields=fields)
    print(q)
    monuments_lieux = db.session.execute(q).unique().scalars()

    return MonumentLieuSchema(only=fields).dump(monuments_lieux, many=True)


@routes.route("/monuments_lieux/<int:id>", methods=["GET"])
def get_one_monument_lieu(id):
    fields = [
        "etat_conservation",
        "auteurs",
        "contributeurs",
        "redacteurs",
        "materiaux",
    ]
    q = MonumentLieu.select.auto_joinload(MonumentLieu, fields=fields).filter_by(id=id)
    print(q)
    monument_lieu = db.session.execute(q).unique().scalars().one_or_none()
    if not monument_lieu:
        raise NotFound()
    return MonumentLieuSchema(only=fields).dump(monument_lieu)
