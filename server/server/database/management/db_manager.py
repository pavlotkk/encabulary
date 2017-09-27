from server.database import db
from server.database.model import DbLanguage, DbWordType, DbRepeat, DbUser


def delete_db():
    db.drop_all()


def create_db():
    db.create_all()


def save_db_changes():
    db.session.commit()


def init_db_with_default_values():
    db_languages = [
        DbLanguage(DbLanguage.EN, 'English'),
        DbLanguage(DbLanguage.RU, 'Russian')
    ]
    db.session.add_all(db_languages)

    db_repeats = [
        DbRepeat(1),
        DbRepeat(3),
        DbRepeat(7),
        DbRepeat(30)
    ]
    db.session.add_all(db_repeats)

    db_word_types = [
        DbWordType("Noun"),
        DbWordType("Verb"),
        DbWordType("Adjective"),
        DbWordType("Adverb"),
        DbWordType("Preposition"),
        DbWordType("Phrasal verb")
    ]
    db.session.add_all(db_word_types)

    db_users = [
        DbUser("demo", DbLanguage.RU, "demo"),
        DbUser("tkachuk.pavel13@gmail.com", DbLanguage.RU, "dEFFOrad2umP")
    ]
    db.session.add_all(db_users)

    db.session.commit()
