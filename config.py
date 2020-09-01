import os


class Config:
    SERVICE_NAME = os.environ.get('SERVICE_NAME')
    GIT_TAG = os.environ.get('GIT_TAG')
    ENVIRONMENT = os.environ.get('ENVIRONMENT')
    LOG_PATH = os.environ.get('LOG_PATH')
    WATCH_FOLDER_PATH = os.environ.get('WATCH_FOLDER_PATH')
    EXTENSIONS = str(os.environ.get('EXTENSIONS'))
    TIMEOUT_DETECTION = os.environ.get('TIMEOUT_DETECTION')
    DETX_API = os.environ.get('DETX_API')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'pre-production': ProductionConfig,
    'default': DevelopmentConfig
}
