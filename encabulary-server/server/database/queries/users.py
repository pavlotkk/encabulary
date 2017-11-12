from server.database import db
from server.database.model import DbUser


def get_db_user_by_id(user_id):
    """
    Get DbUser by id
    :param user_id:
    :rtype DbUser
    """
    db_user = db.session.query(
        DbUser
    ).filter(
        DbUser.id_user == user_id,
        DbUser.is_in_use == True
    ).first()

    return db_user


def get_db_user_by_email(user_email):
    """
    Get DbUser by email
    :param user_email:
    :rtype DbUser
    """
    db_user = db.session.query(
        DbUser
    ).filter(
        DbUser.email == user_email,
        DbUser.is_in_use == True
    ).first()

    return db_user
