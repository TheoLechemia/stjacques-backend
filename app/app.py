from flask import Flask

# from flask_sqlalchemy_app.env import db
# from .config.config import config

from app.config.config import config

from app.env import APP_DIR, db, ma


def create_app():
    app = Flask(__name__)
    app.config.update(config)
    db.init_app(app)
    ma.init_app(app)

    from app.blueprint import routes

    app.register_blueprint(routes)
    return app
