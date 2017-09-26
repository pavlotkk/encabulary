import datetime

from server.database import db
from server.database.model import DbLanguage, DbWordType, DbWord


class DbTranslation(db.Model):
    __tablename__ = 'translations'

    id_translation = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id_word = db.Column(db.Integer, db.ForeignKey(DbWord.id_word), nullable=False)
    id_language = db.Column(db.Integer, db.ForeignKey(DbLanguage.id_language), nullable=False)
    id_type = db.Column(db.Integer, db.ForeignKey(DbWordType.id_type), nullable=False)

    translation = db.Column(db.Text, nullable=False, index=True)

    add_db_dts = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    is_in_use = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return '<DbTranslation [{}] - {}>'.format(self.id_translation, self.translation)
