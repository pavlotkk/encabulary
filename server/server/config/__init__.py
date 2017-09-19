import os

from server.config.default_config import DefaultConfig

config_name = os.getenv('PYENCABULARY_CONFIG', 'default')
config = DefaultConfig()

if config_name == "development":
    from server.config.local_config import LocalConfig
    config = LocalConfig()
