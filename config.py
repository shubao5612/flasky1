import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or "hard guess"
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True

    FLASKY_MAIL_SUBJECT_PREFIX='[主题]'
    FLASKY_MAIL_SENDER='403308946@qq.com'
    FLASKY_ADMIN= 'wangshen5612@163.com'
    #
    MAIL_USERNAME = '403308946'
    MAIL_PASSWORD = 'qhzmkrzihikvbhie'
    FLASKY_POSTS_PER_PAGE=5
    FLASKY_FOLLOWERS_PER_PAGE=5
    FLASKY_COMMENTS_PER_PAGE=6

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True
    MAIL_SERVER= 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data_dev.sqlite') or os.environ.get('DEV_DATABASE_URL')

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data_test.sqlite') or os.environ.get(
        'TEST_DATABASE_URL')
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite') or os.environ.get(
        'DATABASE_URL')


config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}