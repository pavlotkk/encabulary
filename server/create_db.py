from server.database import Base, engine, db_session
from server.database.model import *
from server.tools.stopwatch import Stopwatch


def delete_db():
    Base.metadata.drop_all(bind=engine)


def create_db():
    Base.metadata.create_all(bind=engine)


def init_db_with_default_values():
    db_languages = [
        DbLanguage(DbLanguage.EN, 'English'),
        DbLanguage(DbLanguage.RU, 'Russian')
    ]
    db_session.add_all(db_languages)

    db_repeats = [
        DbRepeat(1),
        DbRepeat(3),
        DbRepeat(7),
        DbRepeat(30)
    ]
    db_session.add_all(db_repeats)

    db_word_types = [
        DbWordType("Noun"),
        DbWordType("Verb"),
        DbWordType("Adjective"),
        DbWordType("Adverb"),
        DbWordType("Preposition"),
        DbWordType("Phrasal verb")
    ]
    db_session.add_all(db_word_types)

    db_users = [
        DbUser("demo", DbLanguage.RU, "demo")
    ]
    db_session.add_all(db_users)


def save_changes():
    db_session.commit()


def restore_backup():
    print("restoring is not supported. Yet.")


stopwatch = Stopwatch(auto_start=True)

print('delete db')
delete_db()

print('create db')
create_db()

print('init db with default values')
init_db_with_default_values()

print('restore db')
restore_backup()

print('commit')
save_changes()

stopwatch.stop()

print('==========')
print('DONE at {}'.format(stopwatch))
