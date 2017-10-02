import datetime

from server.database import db


class DbWord(db.Model):
    __tablename__ = 'words'

    id_word = db.Column(db.Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    word = db.Column(db.Text, nullable=False, index=True, unique=True)
    transcription = db.Column(db.Text, nullable=True)

    add_db_dts = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    is_in_use = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, word=None, transcription=None):
        self.word = word
        self.transcription = transcription

    def __repr__(self):
        return '<DbWord [{}] - {}>'.format(self.id_word, self.word)
