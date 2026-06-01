from string import ascii_letters, digits

from .constants import CUSTOM_ID_MAX_LENGTH, RESERVED_SHORT_IDS


def validate_custom_id(custom_id):
    """Проверяет, что пользовательский идентификатор валиден и уникален."""
    if custom_id in RESERVED_SHORT_IDS:
        raise ValueError(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    if (
        len(custom_id) > CUSTOM_ID_MAX_LENGTH
        or not all(c in ascii_letters + digits for c in custom_id)
    ):
        raise ValueError('Указано недопустимое имя для короткой ссылки')