import datetime

from server.database import db
from server.database.model import DbRepeat, DbWord


class DbUserWordRepeat(db.Model):
    __tablename__ = 'user_words_repeats'

    id_user_word_repeat = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id_word = db.Column(db.Integer, db.ForeignKey(DbWord.id_word), nullable=False)
    id_repeat = db.Column(db.Integer, db.ForeignKey(DbRepeat.id_repeat), nullable=False)

    repeat_after_db_dts = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<DbUserWordRepeat [{}] - repeat_after={}>'.format(self.id_user_word, self.repeat_after_db_dts)
