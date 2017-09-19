from sqlalchemy import Column, Integer, Text

from server.database import Base


class DbLanguage(Base):
    __tablename__ = 'dc_languages'

    EN = 1
    RU = 2

    id_language = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)

    def __init__(self, id_lang=None, name=None):
        self.id_language = id_lang
        self.name = name

    def __repr__(self):
        return '<DbLanguage [{}] - {}>'.format(self.id_language, self.name)
