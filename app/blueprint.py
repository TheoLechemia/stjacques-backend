from flask import Blueprint


routes = Blueprint("main", __name__)

from app.models import User
from app.env import db
from app.schemas import UserSchema


@routes.route("/test")
def test():
    users = db.session.execute(User.select.where_identifant("pierre.paul")).scalars()
    return UserSchema(only=["organism"]).dump(users, many=True)
