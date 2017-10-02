import datetime

from server.database import db
from server.database.model import DbUser


class DbWord(db.Model):
    __tablename__ = 'words'

    id_word = db.Column(db.Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey(DbUser.id_user), index=True, nullable=False)

    word = db.Column(db.Text, nullable=False, index=True, unique=True)
    transcription = db.Column(db.Text, nullable=True)

    score = db.Column(db.Integer, nullable=False, index=True, default=0)
    is_learnt = db.Column(db.Boolean, nullable=False, default=False)
    last_learn_db_dts = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    add_db_dts = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    is_in_use = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, id_user=None, word=None, transcription=None):
        self.id_user = id_user
        self.word = word
        self.transcription = transcription

    def __repr__(self):
        return '<DbWord [{}] - {}>'.format(self.id_word, self.word)
