from server.config.default_config import DefaultConfig
from server.globals import get_root_dir


class LocalConfig(DefaultConfig):
    DEBUG = True

    class db:
        URI = 'sqlite:///{path}/{db_name}'.format(path=get_root_dir(), db_name='local.dictionary.db')

