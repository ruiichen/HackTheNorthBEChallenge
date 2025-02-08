import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..models.hackers import Hackers as HackerModel
from ..types.scans import Scans

class Hackers(SQLAlchemyObjectType):
    scans = graphene.List(Scans)

    class Meta:
        model = HackerModel
        interfaces = (graphene.relay.Node,)
