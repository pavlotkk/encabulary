import sqlalchemy as sql

from server import create_app
from server.database import db
from server.database.management import db_manager
from server.database.management.db_manager import save_db_changes
from server.database.model import DbUser, DbLanguage, DbUserWordRepeat, DbWord
from server.database.queries import get_min_db_repeat, get_db_user_by_email
from server.tools.stopwatch import Stopwatch


def patch_add_tpa_user():
    app = create_app()
    stopwatch = Stopwatch(auto_start=True)

    with app.app_context():
        db_user = DbUser('tpa', DbLanguage.RU, 'tpacabulary')
        db.session.add(db_user)
        save_db_changes()

        db_manager.add_db_words(db_user)

    stopwatch.stop()

    print('==========')
    print('DONE at {}'.format(stopwatch))


def patch_reset_repeat_dates():
    app = create_app()
    stopwatch = Stopwatch(auto_start=True)

    with app.app_context():
        db_user = get_db_user_by_email('tpa')

        db_repeats = db.session.query(
            DbUserWordRepeat
        ).join(
            DbWord,
            DbUserWordRepeat.id_word == DbWord.id_word
        ).filter(
            DbWord.id_user == db_user.id_user,
            DbUserWordRepeat.id_repeat != None
        ).all()

        min_db_repeat = get_min_db_repeat()

        for db_rep in db_repeats:
            db_rep.set_repeat(min_db_repeat)

        save_db_changes()

    stopwatch.stop()

    print('==========')
    print('DONE at {}'.format(stopwatch))


def patch_remove_duplicates():
    app = create_app()
    stopwatch = Stopwatch(auto_start=True)

    with app.app_context():
        db_user = get_db_user_by_email('tpa')

        db_repeats = db.session.query(
            DbWord.word,
            DbWord.id_word_type
        ).filter(
            DbWord.id_user == db_user.id_user
        ).group_by(
            DbWord.word,
            DbWord.id_word_type
        ).having(
            sql.func.count(DbWord.id_word) > 1
        ).all()

        print('Find {} duplicates'.format(len(db_repeats)))

        for (word, word_type) in db_repeats:
            word_to_del = db.session.query(
                DbWord
            ).filter(
                DbWord.id_user == db_user.id_user,
                DbWord.word == word,
                DbWord.id_word_type == word_type
            ).first()

            db.session.delete(word_to_del)
            db.session.flush()

        save_db_changes()

    stopwatch.stop()

    print('==========')
    print('DONE at {}'.format(stopwatch))


def run_patch():
    patch_remove_duplicates()


run_patch()
