import os


class Config(object):
    DEBUG = True
    TESTING = True
    Database_Url = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET")


class DevelopmentConfig(Config):
    DEBUG = True
    Database_Url = os.getenv("DATABASE_URL")


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    Database_Url = os.getenv("Test_Database")


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    Database_Url = os.getenv("DATABASE_URL")


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
