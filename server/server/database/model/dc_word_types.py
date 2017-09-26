from server.database import db


class DbWordType(db.Model):
    __tablename__ = 'dc_word_types'

    id_type = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<DbWordType {}>'.format(self.name)
