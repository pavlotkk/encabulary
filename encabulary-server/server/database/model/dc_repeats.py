from server.database import db


class DbRepeat(db.Model):
    __tablename__ = 'dc_repeats'

    id_repeat = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repeat_days = db.Column(db.Integer, unique=True)

    def __init__(self, repeat_days=None):
        self.repeat_days = repeat_days

    def __repr__(self):
        return '<DbRepeat {} days>'.format(self.repeat_days)
