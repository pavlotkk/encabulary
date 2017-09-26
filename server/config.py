from datetime import timedelta

from server.globals import get_root_dir

DEBUG = False
SERVER_NAME = "0.0.0.0:7777"
SECRET_KEY = "\x97\x04\x97\x19\xb8\xaeY\xcc\xc1\xfb\x99\xec\x80\xcbq\xa3\xb0'\x84GbN\xe8\xd2"

SQLALCHEMY_DATABASE_URI = 'sqlite:///{path}/{db_name}'.format(path=get_root_dir(), db_name='dictionary.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_HEADER_NAME = 'Authorization'
JWT_HEADER_TYPE = 'Bearer'
JWT_ALGORITHM = 'HS256'
JWT_TOKEN_EXPIRES = timedelta(days=120)
JWT_AUTO_UPDATE_AFTER = timedelta(days=60)

MAX_WORDS_TO_LEARN_BY_REQUEST = 10
WORD_LEARNED_SCORE = 6
SIMILAR_RATIO = 0.70
