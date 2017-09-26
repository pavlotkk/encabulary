from server.database import db


class DbLanguage(db.Model):
    __tablename__ = 'dc_languages'

    EN = 1
    RU = 2

    id_language = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)

    def __init__(self, id_lang=None, name=None):
        self.id_language = id_lang
        self.name = name

    def __repr__(self):
        return '<DbLanguage [{}] - {}>'.format(self.id_language, self.name)
