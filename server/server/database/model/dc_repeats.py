from sqlalchemy import Column, Integer

from server.database import Base


class DbRepeat(Base):
    __tablename__ = 'dc_repeats'

    id_repeat = Column(Integer, primary_key=True, autoincrement=True)
    repeat_days = Column(Integer, unique=True)

    def __init__(self, repeat_days=None):
        self.repeat_days = repeat_days

    def __repr__(self):
        return '<DbRepeat {} days>'.format(self.repeat_days)
