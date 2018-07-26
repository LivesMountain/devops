import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    ALLOWED_HOSTS = ['*']
    DEBUG = os.environ.get("DEBUG") or True

    # DEBUG, INFO, WARNING, ERROR, CRITICAL can set. See https://docs.djangoproject.com/en/1.10/topics/logging/
    LOG_LEVEL = os.environ.get("LOG_LEVEL") or 'DEBUG'
    # MySQL or postgres setting like:
    DB_ENGINE = os.environ.get("DB_ENGINE") or 'mysql'
    DB_HOST = os.environ.get("DB_HOST") or '172.17.17.3'
    DB_PORT = os.environ.get("DB_PORT") or 3306
    DB_USER = os.environ.get("DB_USER") or 'root'
    DB_PASSWORD = os.environ.get("DB_PASSWORD") or 'Wangxiaobao,123456'
    DB_NAME = os.environ.get("DB_NAME") or 'devops'
    def __init__(self):
        pass

    def __getattr__(self, item):
        return None


class DevelopmentConfig(Config):
    pass


class TestConfig(Config):
    pass


class ProductionConfig(Config):
    pass


# Default using Config settings, you can write if/else for different env
config = DevelopmentConfig()