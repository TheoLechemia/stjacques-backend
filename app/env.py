from pathlib import Path

from flask_marshmallow import Marshmallow

from app.custom_models import MySelectModel, CustomSQLAlchemy


APP_DIR = Path(__file__).absolute().parent
db = CustomSQLAlchemy(model_class=MySelectModel)
ma = Marshmallow()
