import secrets

class Config:
    TESTING = False
    SQLALCHEMY_ECHO = True
    TABLES = ('edge', 'node', 'project', 'service')
    SECRET_KEY = secrets.token_hex()


class DevelopmentConfig(Config):
    EXPLAIN_TEMPLATE_LOADING = True
    DEBUG = True
    SQLALCHEMY_ECHO = True
    DB_PATH = "temp.db"
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = True
    DB_PATH = "test.db"
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'

class ProductionConfig(Config):
    pass
