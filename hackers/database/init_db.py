from .db_session import db_session, engine
from .base import Base
import json
import uuid
from datetime import datetime

def init_db():
    from ..models.hackers import Hackers
    from ..models.activities import Activities
    from ..models.scans import Scans
    from ..models.categories import Categories
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with open("./hackers/database/example_data.json", "r") as file:
        entries = json.load(file)

    activities = dict()
    categories = dict()
    for entry in entries:
        hacker_uuid = str(uuid.uuid4())
        cur_hacker = Hackers(uuid=hacker_uuid,
                             badge_code= entry["badge_code"] if entry["badge_code"] != "" else None, name=entry["name"],
                             email=entry["email"], phone=entry["phone"], updated_at=datetime.utcnow().isoformat() + "Z")
        db_session.add(cur_hacker)
        for scan in entry["scans"]:
            if activities.get(scan["activity_name"]) is None:
                if categories.get(scan["activity_category"]) is None:
                    new_category = Categories(category_name=scan["activity_category"], created_at=datetime.utcnow().isoformat() + "Z")
                    categories[scan["activity_category"]] = new_category
                    db_session.add(new_category)
                new_activity = Activities(activity_name = scan["activity_name"],
                                          category_id = categories.get(scan["activity_category"]).id,
                                          created_at=datetime.utcnow().isoformat() + "Z",
                                          category = categories.get(scan["activity_category"]))
                activities[scan["activity_name"]] = new_activity
                db_session.add(new_activity)
            new_scan = Scans(hacker_uuid = hacker_uuid,
                             activity_id = activities.get(scan["activity_name"]).activity_id,
                             scanned_at = scan["scanned_at"],
                             hacker= cur_hacker,
                             activity = activities.get(scan["activity_name"]))
            db_session.add(new_scan)
    db_session.commit()
