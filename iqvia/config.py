

class Testing(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///iqvia.db'


class Development(object):
    DEBUG = True
    # Use development database here
    SQLALCHEMY_DATABASE_URI = 'sqlite:///iqvia.db'


class Production(object):
    # We don't want the debug logs in production
    DEBUG = False
    # Use production database here
    SQLALCHEMY_DATABASE_URI = 'sqlite:///iqvia.db'
