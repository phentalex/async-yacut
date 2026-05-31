from flask import jsonify, request

from .error_handlers import InvalidAPIUsage

from . import app
from .models import URLMap
from .views import create_url_map


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    """
    Создать короткую ссылку
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            original:
              type: string
              example: https://example.com
            custom_id:
              type: string
              example: my-link
    responses:
      201:
        description: Ссылка создана
        schema:
          properties:
            short:
              type: string
              example: http://localhost/my-link
      400:
        description: Ошибка валидации
    """
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage(r'"url" является обязательным полем!')
    try:
        url_map = create_url_map(data['url'], data.get('custom_id'))
    except ValueError as e:
        raise InvalidAPIUsage(str(e))
    if not url_map:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    return jsonify({
        'url': url_map.original,
        'short_link': f'{request.host}/{url_map.short}'
    }), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """
    Получить оригинальную ссылку по короткому идентификатору
    ---
    parameters:
      - name: short_id
        in: path
        required: true
        type: string
        example: my-link
    responses:
      200:
        description: Оригинальная ссылка
        schema:
          properties:
            original:
              type: string
              example: https://example.com
      404:
        description: Идентификатор не найден
    """
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage(
            'Указанный id не найден', 404
        )
    return jsonify({'url': url_map.original}), 200
