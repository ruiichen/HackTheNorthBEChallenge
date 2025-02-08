import graphene

from ..schema.query import Query
from ..schema.mutation import Mutation

from ..types.hackers import Hackers
from ..types.scans import Scans
from ..types.activities import Activities

schema = graphene.Schema(query=Query, mutation=Mutation, types=[Hackers, Scans, Activities])