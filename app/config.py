import logging
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, '../app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    from flask.logging import default_handler

    default_handler.setFormatter(logging.Formatter(
        ' * [%(levelname)s][%(filename)s:%(lineno)d]: %(message)s'
    ))

    log_level = logging.DEBUG
