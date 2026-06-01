from re import compile

from .constants import (
    CUSTOM_ID_MAX_LENGTH, REGEX_CUSTOM_ID, RESERVED_SHORT_IDS
)


def validate_custom_id(custom_id):
    """Проверяет, что пользовательский идентификатор валиден и уникален."""
    if custom_id in RESERVED_SHORT_IDS:
        raise ValueError(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    pattern = compile(rf'^{REGEX_CUSTOM_ID}{{1,{CUSTOM_ID_MAX_LENGTH}}}$')
    if not pattern.match(custom_id):
        raise ValueError('Указано недопустимое имя для короткой ссылки')
