import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey

from server.database import Base
from server.database.model import DbRepeat, DbUserWord


class DbUserWordRepeat(Base):
    __tablename__ = 'user_words_repeats'

    id_user_word_repeat = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    id_user_word = Column(Integer, ForeignKey(DbUserWord.id_user_word), nullable=False)
    id_repeat = Column(Integer, ForeignKey(DbRepeat.id_repeat), nullable=False)

    repeat_after_db_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<DbUserWordRepeat [{}] - repeat_after={}>'.format(self.id_user_word, self.repeat_after_db_dts)
