from sqlalchemy.orm import raiseload, joinedload

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.sql.expression import Select


class MySelectModel(Model):
    __abstract__ = True

    @classmethod
    @property
    def select(cls, *entities):
        if hasattr(cls, "__select_class__"):
            select_cls = cls.__select_class__
        else:
            select_cls = Select
        return select_cls(cls)
