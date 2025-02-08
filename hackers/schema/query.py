import graphene
from graphene import relay
from sqlalchemy.sql import func

from ..models.scans import Scans as ScansModel
from ..models.hackers import Hackers as HackersModel
from ..models.activities import Activities as ActivitiesModel
from ..models.categories import Categories as CategoriesModel
from ..types.hackers import Hackers
from ..types.scans import Scans


class ActivityFrequencyType(graphene.ObjectType):
    activity_name = graphene.String()
    frequency = graphene.Int()

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    hackers = graphene.List(Hackers)
    hackers_by_badge = graphene.Field(Hackers, badge_code=graphene.String())
    scans = graphene.List(ActivityFrequencyType, min_frequency=graphene.Int(), max_frequency=graphene.Int(), activity_category=graphene.String())

    @staticmethod
    def resolve_scans(parent, info, min_frequency = None, max_frequency = None, activity_category = None):
        base_query = Scans.get_query(info)
        select_query = base_query.join(ActivitiesModel, ScansModel.activity_id == ActivitiesModel.activity_id).with_entities(
            ActivitiesModel.activity_name.label("activity_name"),
            func.count(ScansModel.scan_id).label("frequency")
        )
        grouped_query = select_query.group_by(ActivitiesModel.activity_id)

        if min_frequency is not None:
            grouped_query = grouped_query.having(func.count(ScansModel.scan_id) >= min_frequency)
        if max_frequency is not None:
            grouped_query = grouped_query.having(func.count(ScansModel.scan_id) <= max_frequency)
        if activity_category is not None:
            grouped_query = grouped_query.join(CategoriesModel, ActivitiesModel.category_id == CategoriesModel.id).filter(CategoriesModel.category_name == activity_category)
        return [ActivityFrequencyType(activity_name=activity_name, frequency=frequency) for activity_name, frequency in grouped_query]

    @staticmethod
    def resolve_hackers(parent, info, **args):
        query = Hackers.get_query(info)
        return query.all()

    @staticmethod
    def resolve_hackers_by_badge(parent, info, **args):
        q = args.get("badge_code")
        query = Hackers.get_query(info)
        return query.filter(HackersModel.badge_code == q).first()
