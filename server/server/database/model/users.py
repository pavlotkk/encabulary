from server.database import db
from server.database.model import DbLanguage


class DbUser(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    id_session = db.Column(db.Text, nullable=True)
    id_language = db.Column(db.Integer, db.ForeignKey(DbLanguage.id_language), nullable=False)

    email = db.Column(db.Text, nullable=False, index=True)
    password = db.Column(db.Text, nullable=False)
    password_salt = db.Column(db.Text, nullable=False)

    is_in_use = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, email=None, lang=None, password=None):
        self.email = email
        self.id_language = lang

        if password is not None:
            from server.tools.passwords import create_password_hash_and_salt
            self.password, self.password_salt = create_password_hash_and_salt(password)

    def __repr__(self):
        return '<DbUser [{}] - {}>'.format(self.id_user, self.email)
