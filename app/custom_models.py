from sqlalchemy.orm import raiseload, joinedload

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model


from utils_flask_sqla.sqlalchemy import CustomSelect


class MyCustomSelect(CustomSelect):
    inherit_cache = True

    def auto_joinload(self, model, fields=[]):
        query_option = [raiseload("*")]
        for f in fields:
            if f in model.__mapper__.relationships:
                query_option.append(joinedload(getattr(model, f)))
        self = self.options(*tuple(query_option))
        return self


class MySelectModel(Model):
    __abstract__ = True

    @classmethod
    @property
    def select(cls, *entities):
        if hasattr(cls, "__select_class__"):
            select_cls = cls.__select_class__
        else:
            select_cls = MyCustomSelect
        return select_cls(cls)


class CustomSQLAlchemy(SQLAlchemy):
    @staticmethod
    def select(*entities):
        return MyCustomSelect(*entities)
