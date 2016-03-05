# -*- coding:utf-8 -*-
import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_USE_TLS = False

    WOTER_MAIL_SUBJECT_PREFIX = '[Woter]'
    WOTER_ADMIN = os.environ.get('WOTER_ADMIN')

    WOTER_DOC_PER_PAGE = 20
    WOTER_FOLLOWERS_PER_PAGE = 30
    WOTER_COMMENTS_PER_PAGE = 30

    MYSQL_USER = 'root'
    MYSQL_PASS = 930816
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_DB = 'app_awoter'

    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' \
                          % (MYSQL_USER, MYSQL_PASS,
                             MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # google mail for development
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'fp544037857'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'otcccvkoridsepys'
    WOTER_MAIL_SENDER = 'Woter Admin <fp544037857@gmail.com>'
    # MYSQL debug mode
    SQLALCHEMY_ECHO = True
    WOTER_ADMIN = 'a@a.com'


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    import sae.const
    MYSQL_USER = sae.const.MYSQL_USER
    MYSQL_PASS = sae.const.MYSQL_PASS
    MYSQL_HOST = sae.const.MYSQL_HOST
    MYSQL_PORT = int(sae.const.MYSQL_PORT)
    MYSQL_DB   = sae.const.MYSQL_DB
    # Sina mail for production.
    # Using SAE mail API
    MAIL_SERVER = 'smtp.sina.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'tk_woter@sina.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'xg8z4BWXJn'
    # SAE only
    SQLALCHEMY_POOL_RECYCLE = 10
    WOTER_ADMIN = 'fp544037857@gmail.com'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
