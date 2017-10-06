from server.database import db


class DbWordType(db.Model):
    __tablename__ = 'dc_word_types'

    NOUN = 1
    VERB = 2
    ADJECTIVE = 3
    ADVERB = 4
    PREPOSITION = 5
    PHRASAL_VERB = 6

    id_type = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)

    def __init__(self, id_type=None, name=None):
        self.id_type = id_type
        self.name = name

    def __repr__(self):
        return '<DbWordType {}>'.format(self.name)

    @staticmethod
    def get_id_by_name(name):
        if not name:
            return None

        filtered = list(filter(lambda item: item.name == name, DbWordType.get_all()))

        if not filtered:
            return None

        return filtered[0].id_type

    @staticmethod
    def get_all():
        return [
            DbWordType(DbWordType.NOUN, 'noun'),
            DbWordType(DbWordType.VERB, 'verb'),
            DbWordType(DbWordType.ADJECTIVE, 'adjective'),
            DbWordType(DbWordType.ADVERB, 'adverb'),
            DbWordType(DbWordType.PREPOSITION, 'preposition'),
            DbWordType(DbWordType.PHRASAL_VERB, 'phrasal verb')
        ]
