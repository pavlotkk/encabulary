from server.globals import get_root_dir

DEBUG = True
SERVER_NAME = 'localhost:8888'

SQLALCHEMY_DATABASE_URI = 'sqlite:///{path}/{db_name}'.format(path=get_root_dir(), db_name='local.dictionary.db')
