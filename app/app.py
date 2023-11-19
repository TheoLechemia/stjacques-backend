from flask import Flask, send_from_directory
from pathlib import Path

from flask_cors import CORS

# from flask_sqlalchemy_app.env import db
# from .config.config import config

from app.config.config import config

from app.env import APP_DIR, db, ma


def create_app():
    app = Flask(__name__)
    app.config.update(config)
    db.init_app(app)
    ma.init_app(app)
    CORS(app, supports_credentials=True)

    media_path = Path(app.config["MEDIAS_FOLDER"]).absolute()

    # Enable serving of media files
    # app.add_url_rule(
    #     "/media/<path:filename>",
    #     view_func=lambda filename: send_from_directory(media_path, filename),
    #     endpoint="media",
    # )

    from app.blueprint import routes

    app.register_blueprint(routes)
    return app
