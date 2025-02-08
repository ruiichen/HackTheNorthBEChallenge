import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models.scans import Scans as ScansModel


class Scans(SQLAlchemyObjectType):
    activity_name = graphene.String()
    activity_category = graphene.String()

    class Meta:
        model = ScansModel
        interfaces = (graphene.relay.Node,)

    def resolve_activity_name(self, info):
        return self.activity.activity_name if self.activity else None

    def resolve_activity_category(self, info):
        return self.activity.category.category_name if self.activity and self.activity.category else None
