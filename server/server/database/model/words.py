import datetime

from sqlalchemy import Column, Integer, Text, Boolean, DateTime

from server.database import Base


class DbWord(Base):
    __tablename__ = 'words'

    id_word = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    word = Column(Text, nullable=False, index=True)
    transcription = Column(Text, nullable=True)

    add_db_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    is_in_use = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return '<DbWord [{}] - {}>'.format(self.id_word, self.word)
