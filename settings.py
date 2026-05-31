import os


class Config(object):
    """Конфигурация приложения."""

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key')
    DISK_TOKEN = os.getenv('DISK_TOKEN')