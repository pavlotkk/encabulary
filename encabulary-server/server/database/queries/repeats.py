from server.database import db
from server.database.model import DbRepeat


def get_min_db_repeat():
    """:rtype: DbRepeat"""
    db_repeat = db.session.query(
        DbRepeat
    ).order_by(
        DbRepeat.repeat_days
    ).first()

    return db_repeat
