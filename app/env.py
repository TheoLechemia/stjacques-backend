from pathlib import Path

from flask_marshmallow import Marshmallow

from utils_flask_sqla.models import SelectModel
from utils_flask_sqla.sqlalchemy import CustomSQLAlchemy


APP_DIR = Path(__file__).absolute().parent
db = CustomSQLAlchemy(model_class=SelectModel)
ma = Marshmallow()
