import datetime

from server.database import db
from server.database.model import DbRepeat, DbWord


class DbUserWordRepeat(db.Model):
    __tablename__ = 'user_words_repeats'

    id_user_word_repeat = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id_word = db.Column(db.Integer, db.ForeignKey(DbWord.id_word), nullable=False)
    id_repeat = db.Column(db.Integer, db.ForeignKey(DbRepeat.id_repeat), nullable=False)

    repeat_after_db_dts = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, id_word=None):
        self.id_word = id_word

    def __repr__(self):
        return '<DbUserWordRepeat [{}] - repeat_after={}>'.format(self.id_user_word, self.repeat_after_db_dts)

    def set_repeat(self, db_repeat):
        now = datetime.datetime.utcnow()

        self.id_repeat = db_repeat.id_repeat
        self.repeat_after_db_dts = now + datetime.timedelta(days=db_repeat.repeat_days)

    def set_next_repeat_dts(self):
        db_repeats = db.session.query(DbRepeat).order_by(DbRepeat.repeat_days).all()

        def get_min_db_repeat(min_days):
            for item in db_repeats:
                if item.repeat_days > min_days:
                    return item

            return db_repeats[len(db_repeats) - 1]

        if self.id_repeat is None:
            db_repeat = get_min_db_repeat(0)
            self.set_repeat(db_repeat)
            return

        current_db_repeat = [item for item in db_repeats if item.id_repeat == self.id_repeat][0]
        db_repeat = get_min_db_repeat(current_db_repeat.repeat_days)
        self.set_repeat(db_repeat)
