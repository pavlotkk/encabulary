from server.database import db


class DbWordType(db.Model):
    __tablename__ = 'dc_word_types'

    id_type = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<DbWordType {}>'.format(self.name)

    @staticmethod
    def get_id_by_name(name):
        if not name:
            return None

        db_type = db.session.query(DbWordType).filter(DbWordType.name.ilike(name)).first()

        if not db_type:
            return None

        return db_type.id_type
