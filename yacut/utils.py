from string import ascii_letters, digits
from random import choices

from .models import URLMap
from .constants import AUTO_GENERATED_ID_LENGTH


def generate_short_id(length=AUTO_GENERATED_ID_LENGTH):
    """Генерирует случайный короткий идентификатор."""
    characters = ascii_letters + digits
    return ''.join(choices(characters, k=length))


def get_unique_short_id(custom_id=None):
    """Проверяет, что идентификатор уникален либо генерирует новый."""
    if custom_id:
        if len(custom_id) > 16 or not all(
            c in ascii_letters + digits for c in custom_id
        ):
            raise ValueError('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=custom_id).first():
            return None
        return custom_id

    while True:
        short_id = generate_short_id()
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id