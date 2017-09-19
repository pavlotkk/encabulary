from sqlalchemy import Column, Integer, Text
from server.database import Base


class DbWordType(Base):
    __tablename__ = 'dc_word_types'

    id_type = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<DbWordType {}>'.format(self.name)
