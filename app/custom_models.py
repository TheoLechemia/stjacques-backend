from sqlalchemy import func
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

    def where_publish(self):
        return self.filter_by(publie=True)

    def where_has_media(self, model):
        return self.filter(model.medias.any())

    def auto_filters(self, params, model, remove_publish=True):
        if "has_medias" in params and params["has_medias"] == "true":
            params.pop("has_medias")
            self = self.filter(model.medias.any())
        if "random" in params:
            self = self.order_by(func.random())
        if "limit" in params:
            self = self.limit(params.pop("limit"))

        # force publish
        if remove_publish:
            self = self.where_publish()
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
