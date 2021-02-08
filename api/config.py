class Config(object):
    # Flask Configs
    DEBUG = True
    DEVELOPMENT = True

    # True Pill Configs
    TRUSTED_SOURCES = []
    NUM_SUGGESTIONS = 4
    BIAS_DB_PATH = 'media_bias_db.json'

class ProdConfig(Config):
    DEBUG = False
    DEVELOPMENT = False