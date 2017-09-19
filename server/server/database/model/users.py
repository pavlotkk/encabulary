from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from server.database import Base
from server.database.model import DbLanguage


class DbUser(Base):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    id_session = Column(Text, nullable=True)
    id_language = Column(Integer, ForeignKey(DbLanguage.id_language), nullable=False)

    email = Column(Text, nullable=False, index=True)
    password = Column(Text, nullable=False)
    password_salt = Column(Text, nullable=False)

    is_in_use = Column(Boolean, nullable=False, default=True)

    def __init__(self, email=None, lang=None, password=None):
        self.email = email
        self.id_language = lang

        if password is not None:
            from server.tools.passwords import create_password_hash_and_salt
            self.password, self.password_salt = create_password_hash_and_salt(password)

    def __repr__(self):
        return '<DbUser [{}] - {}>'.format(self.id_user, self.email)
