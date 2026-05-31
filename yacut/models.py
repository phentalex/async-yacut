from datetime import datetime

from . import db


class URLMap(db.Model):
    """Модель для хранения информации о сокращённых ссылках."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String, nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)