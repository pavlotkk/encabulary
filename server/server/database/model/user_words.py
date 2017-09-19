import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey

from server.database import Base
from server.database.model import DbLanguage, DbWordType, DbWord


class DbUserWord(Base):
    __tablename__ = 'user_words'

    id_user_word = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    id_word = Column(Integer, ForeignKey(DbWord.id_word), nullable=False)
    id_language = Column(Integer, ForeignKey(DbLanguage.id_language), nullable=False)
    id_type = Column(Integer, ForeignKey(DbWordType.id_type), nullable=False)

    score = Column(Integer, nullable=False, index=True)
    is_learnt = Column(Boolean, nullable=False, default=False)
    last_learn_db_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<DbUserWord [{}] - score={}, is_learnt={}>'.format(self.id_user_word, self.score, self.is_learnt)
