from datetime import datetime
from string import ascii_letters, digits
from random import choices

from flask import request, url_for

from . import db
from .constants import (
    AUTO_GENERATED_ID_LENGTH, MAX_GENERATION_ATTEMPTS
)
from .validators import validate_custom_id


class URLMap(db.Model):
    """Модель для хранения информации о сокращённых ссылках."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String, nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def get_original_link(self):
        """Возвращает оригинальную ссылку."""
        return {'url': self.original}

    def get_short_url(self):
        """Генерация полной короткой ссылки."""
        return f'{request.host_url}{self.short}'

    def to_dict(self):
        """Преобразование модели в словарь."""
        return {
            'url': self.original,
            'short_link': url_for(
                'redirect_view',
                short=self.short,
                _external=True
            )
        }

    @staticmethod
    def get_by_short_id(short_id):
        """Получение объекта URLMap по короткому идентификатору."""
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def generate_short_id(length=AUTO_GENERATED_ID_LENGTH):
        """Генерирует случайный короткий идентификатор."""
        characters = ascii_letters + digits
        return ''.join(choices(characters, k=length))

    @staticmethod
    def get_unique_short_id():
        """Проверяет, что идентификатор уникален либо генерирует новый."""
        for _ in range(MAX_GENERATION_ATTEMPTS):
            short_id = URLMap.generate_short_id()
            if not URLMap.get_by_short_id(short_id):
                return short_id
        raise ValueError(
            'Не удалось сгенерировать уникальную короткую ссылку.'
        )

    @staticmethod
    def create(original, custom_id=None):
        """Создаёт объект URLMap с уникальным коротким идентификатором."""
        if custom_id:
            validate_custom_id(custom_id)
            if URLMap.get_by_short_id(custom_id):
                raise ValueError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
            short_id = custom_id
        else:
            short_id = URLMap.get_unique_short_id()
        url_map = URLMap(original=original, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map