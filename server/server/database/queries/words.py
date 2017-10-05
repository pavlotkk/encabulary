from server.database import db
from server.database.model import DbWord


def get_db_user_word_by_id(user_id, word_id):
    """:rtype: DbWord"""
    db_word = db.session.query(
        DbWord
    ).filter(
        DbWord.id_word == word_id,
        DbWord.id_user == user_id,
        DbWord.is_in_use == True
    ).first()

    return db_word
