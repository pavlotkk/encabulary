import datetime

from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey

from server.database import Base
from server.database.model import DbLanguage, DbWordType, DbWord


class DbTranslation(Base):
    __tablename__ = 'translations'

    id_translation = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    id_word = Column(Integer, ForeignKey(DbWord.id_word), nullable=False)
    id_language = Column(Integer, ForeignKey(DbLanguage.id_language), nullable=False)
    id_type = Column(Integer, ForeignKey(DbWordType.id_type), nullable=False)

    translation = Column(Text, nullable=False, index=True)

    add_db_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    is_in_use = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return '<DbTranslation [{}] - {}>'.format(self.id_translation, self.translation)
