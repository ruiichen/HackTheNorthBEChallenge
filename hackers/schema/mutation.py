import graphene
from ..database.db_session import db_session
from ..models.hackers import Hackers as HackersModel
from ..models.categories import Categories as CategoriesModel
from ..types.hackers import Hackers
from ..models.activities import Activities as ActivitiesModel
from ..types.activities import Activities
from ..types.categories import Categories
from ..models.scans import Scans as ScansModel
from datetime import datetime

class CheckHackerIn(graphene.Mutation):
    class Arguments:
        uuid = graphene.String(required=True)
        badge_code = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    hacker = graphene.Field(Hackers)

    @staticmethod
    def mutate(parent, info, uuid, badge_code):
        q = Hackers.get_query(info)
        if q.filter(HackersModel.uuid == uuid).count() == 0:
            raise Exception(f"No hacker found with UUID {uuid}.")
        if q.filter(HackersModel.badge_code == badge_code).count() != 0:
            raise Exception(f"Another hacker is already using the badge {badge_code}.")
        hacker = q.filter(HackersModel.uuid == uuid).first()
        if hacker.badge_code:
            raise Exception(f"Hacker is already checked in using badge {hacker.badge_code}.")
        hacker.badge_code = badge_code
        hacker.updated_at = datetime.utcnow().isoformat() + "Z"
        db_session.commit()
        db_session.refresh(hacker)
        return UpdateHacker(success=True, message="Hacker checked-in successfully", hacker=hacker)

class UpdateHackerBadge(graphene.Mutation):
    class Arguments:
        uuid = graphene.String(required=True)
        badge_code = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    hacker = graphene.Field(Hackers)

    @staticmethod
    def mutate(root, info, uuid, badge_code):
        q = Hackers.get_query(info)
        if q.filter(HackersModel.badge_code == badge_code).count() != 0:
            raise Exception(f"A hacker is already using the badge {badge_code}.")
        hacker = q.filter(HackersModel.uuid == uuid).first()
        hacker.badge_code = badge_code
        hacker.updated_at = datetime.utcnow().isoformat() + "Z"
        db_session.commit()
        db_session.refresh(hacker)
        return UpdateHacker(success=True, message="Hacker checked-out successfully", hacker=hacker)


class CheckHackerOut(graphene.Mutation):
    class Arguments:
        badge_code = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    hacker = graphene.Field(Hackers)

    @staticmethod
    def mutate(root, info, badge_code):
        q = Hackers.get_query(info)
        if q.filter(HackersModel.badge_code == badge_code).count() == 0:
            raise Exception(f"No hacker is using the badge {badge_code}.")
        hacker = q.filter(HackersModel.badge_code == badge_code).first()
        hacker.badge_code = None
        hacker.updated_at = datetime.utcnow().isoformat() + "Z"
        db_session.commit()
        db_session.refresh(hacker)
        return UpdateHacker(success=True, message="Hacker checked-out successfully", hacker=hacker)

class ScanHacker(graphene.Mutation):
    class Arguments:
        badge_code = graphene.String(required=True)
        activity_name = graphene.String(required=True)
        activity_category = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    hacker = graphene.Field(Hackers)

    @staticmethod
    def mutate(self, info, badge_code, activity_name, activity_category):
        q = Categories.get_query(info).filter(CategoriesModel.category_name == activity_category)
        cat = None
        if q.count() == 0:
            cat = CategoriesModel(category_name= activity_category, created_at=datetime.utcnow().isoformat() + "Z")
            db_session.add(cat)
        else:
            cat = q.first()

        q = Activities.get_query(info).filter(ActivitiesModel.activity_name == activity_name)
        act = None
        if q.count() == 0:
            act = ActivitiesModel(activity_name = activity_name, category_id = cat.id, created_at=datetime.utcnow().isoformat() + "Z", category=cat)
            db_session.add(act)
        else:
            act = q.first()

        q = Hackers.get_query(info).filter(HackersModel.badge_code == badge_code)
        if q.count() == 0:
            raise Exception(f"No hacker found with badge code {badge_code}.")
        hack = q.first()
        new_scan = ScansModel(hacker_uuid=hack.uuid,
                         activity_id=act.activity_id,
                         scanned_at=datetime.utcnow().isoformat() + "Z",
                         hacker=hack,
                         activity=act)
        hack.updated_at = datetime.utcnow().isoformat() + "Z"
        db_session.add(new_scan)
        db_session.commit()
        db_session.refresh(hack)
        return ScanHacker(success=True, message="Scan added successfully", hacker=hack)

class UpdateUserInput(graphene.InputObjectType):
    name = graphene.String()
    email = graphene.String()
    phone = graphene.String()

class UpdateHacker(graphene.Mutation):
    class Arguments:
        uuid = graphene.String(required=True)
        data = UpdateUserInput()

    success = graphene.Boolean()
    message = graphene.String()
    hacker = graphene.Field(Hackers)

    @staticmethod
    def mutate(self, info, uuid, data):
        email = data.get("email")
        name = data.get("name")
        phone = data.get("phone")

        q = Hackers.get_query(info).filter(HackersModel.uuid == uuid)
        if q.count() == 0:
            raise Exception(f"No hacker found with UUID {uuid}.")
        hacker = q.first()

        if email:
            q = Hackers.get_query(info).filter(HackersModel.email == email)
            if q.count() == 0:
                hacker.email = email
            else:
                raise Exception(f"Hacker with email {email} already exists.")
        if name:
            hacker.name = name
        if phone:
            hacker.phone = phone
        hacker.updated_at = datetime.utcnow().isoformat() + "Z"
        db_session.commit()
        db_session.refresh(hacker)
        return UpdateHacker(success=True, message="Hacker updated successfully", hacker=hacker)

class Mutation(graphene.ObjectType):
    updateHacker = UpdateHacker.Field()
    scanHacker = ScanHacker.Field()
    checkHackerIn = CheckHackerIn.Field()
    checkHackerOut = CheckHackerOut.Field()
    updateHackerBadge = UpdateHackerBadge.Field()
