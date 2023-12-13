from pathlib import Path

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from app.custom_models import MySelectModel


APP_DIR = Path(__file__).absolute().parent
db = SQLAlchemy(model_class=MySelectModel)
ma = Marshmallow()
