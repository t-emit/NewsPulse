from database.mongo import db
from datetime import datetime


def log_activity(user, action, details=""):

    db.activity_logs.insert_one({
        "user": user,
        "action": action,
        "details": details,
        "timestamp": datetime.utcnow()
    })