class Config(object):
    # Flask Configs
    DEBUG = True
    DEVELOPMENT = True

    # True Pill Configs
    TRUSTED_SOURCES = []
    NUM_SUGGESTIONS = 4
    MEDIA_BIAS_SOURCE = "https://mediabiasfactcheck.com"
    BIAS_DB_PATH = 'something'

class ProdConfig(Config):
    DEBUG = False
    DEVELOPMENT = False