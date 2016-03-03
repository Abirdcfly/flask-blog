# -*- coding:utf-8 -*-
import os
import sae.const
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'fp544037857'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'otcccvkoridsepys'
    WOTER_MAIL_SUBJECT_PREFIX = '[WOTER]'
    WOTER_MAIL_SENDER = 'WOTER Admin <fp544037857@gmail.com>'
    WOTER_ADMIN = os.environ.get('WOTER_ADMIN')
    WOTER_DOC_PER_PAGE = 20
    WOTER_FOLLOWERS_PER_PAGE = 30
    WOTER_COMMENTS_PER_PAGE = 30

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' \
                          % (sae.const.MYSQL_USER, sae.const.MYSQL_PASS,
                             sae.const.MYSQL_HOST, int(sae.const.MYSQL_PORT), sae.const.MYSQL_DB)
    print "hahahaha", sae.const.MYSQL_USER, sae.const.MYSQL_PASS, sae.const.MYSQL_HOST, int(sae.const.MYSQL_PORT), sae.const.MYSQL_DB

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.WOTER_MAIL_SENDER,
            toaddrs=[cls.WOTER_ADMIN],
            subject=cls.WOTER_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    # 'default': DevelopmentConfig
    'default': ProductionConfig
}
