class Config:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    TABLES = ('edge', 'node', 'project', 'service')
    SQLALCHEMY_ECHO = True
