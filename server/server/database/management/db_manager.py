import os
from server.tools import csv_reader, dates
from server.database import db
from server.database.model import DbLanguage, DbWordType, DbRepeat, DbUser, DbWord, DbTranslation
from server.globals import get_root_dir


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
        DbUser("demo", DbLanguage.RU, "demo")
    ]
    db.session.add_all(db_users)

    save_db_changes()

    all_users = db.session.query(DbUser).all()
    for user in all_users:
        add_db_words(user)


def add_db_words(db_user):
    words_fixtures_path = os.path.join(get_root_dir(), 'fixtures', 'user_init_words.csv')
    for line in csv_reader.lines(words_fixtures_path, delimiter=','):
        db_word = DbWord(db_user.id_user, line['en'], line['transcription'])
        db_word.add_db_dts = dates.from_iso(line['add_dts'])
        db.session.add(db_word)
        db.session.flush()

        for tr in line['ru'].split(';'):
            db_translation = DbTranslation(
                db_word.id_word,
                DbLanguage.RU,
                DbWordType.get_id_by_name(line['id_type']),
                tr
            )

            db.session.add(db_translation)

    save_db_changes()
