import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models.activities import Activities as ActivitiesModel


class Activities(SQLAlchemyObjectType):
    activity_category = graphene.String()

    class Meta:
        model = ActivitiesModel
        interfaces = (graphene.relay.Node,)

    def resolve_activity_categories(self, info):
        return self.category.name if self.category else None
