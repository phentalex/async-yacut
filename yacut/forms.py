from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import MultipleFileField, StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, URL

from .constants import CUSTOM_ID_MAX_LENGTH


class URLForm(FlaskForm):
    """Форма для ввода URL и желаемого короткого идентификатора."""

    original_link = URLField(
        'Оригинальная ссылка',
        validators=[
            DataRequired(message='Поле не может быть пустым.'),
            URL(message='Введите корректный URL.')
        ]
    )
    custom_id = StringField(
        'Желаемый короткий идентификатор',
        validators=[
            Length(
                max=CUSTOM_ID_MAX_LENGTH,
                message=(f'Максимальная длина идентификатора'
                         f' - {CUSTOM_ID_MAX_LENGTH} символов.')
            )
        ]
    )
    submit = SubmitField('Создать')


class UploadFileForm(FlaskForm):
    """Форма для загрузки файлов."""

    files = MultipleFileField(
        'Выберите файлы для загрузки',
        validators=[
            FileRequired(message='Пожалуйста, выберите хотя бы один файл.'),
        ]
    )
    submit = SubmitField('Загрузить')
