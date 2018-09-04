import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    ALLOWED_HOSTS = ['*']
    DEBUG = os.environ.get("DEBUG") or True

    ADMIN_MAIL=os.environ.get("ADMIN_MAIL") or '845437607@qq.com'
    # 管理用户：每台机器上拥有nopass（root）权限的账号
    ROOT_USER=os.environ.get("ROOT_USER") or 'q'
    ROOT_PASSWD=os.environ.get("ROOT_PASSWD") or 'q'
    # DEBUG, INFO, WARNING, ERROR, CRITICAL can set. See https://docs.djangoproject.com/en/1.10/topics/logging/
    LOG_LEVEL = os.environ.get("LOG_LEVEL") or 'DEBUG'
    DB_ENGINE = os.environ.get("DB_ENGINE") or 'mysql'
    DB_HOST = os.environ.get("DB_HOST") or '192.168.1.1'
    DB_PORT = os.environ.get("DB_PORT") or 3306
    DB_USER = os.environ.get("DB_USER") or 'root'
    DB_PASSWORD = os.environ.get("DB_PASSWORD") or '123'
    DB_NAME = os.environ.get("DB_NAME") or 'devops'
    NAGIOS_IP = os.environ.get("NAGIOS_IP") or '127.0.0.1'

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
