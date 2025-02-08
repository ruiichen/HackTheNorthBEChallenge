from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models.categories import Categories as CategoriesModel


class Categories(SQLAlchemyObjectType):
    class Meta:
        model = CategoriesModel
        interfaces = (relay.Node,)
