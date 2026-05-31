from flask import jsonify, request

from .error_handlers import InvalidAPIUsage

from . import app
from .models import URLMap
from .views import create_url_map


@app.route('/api/id/', methods=['POST'])
def get_short_link():
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
        'short_link': f'{request.host_url}{url_map.short}'
    }), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage(
            'Указанный id не найден', 404
        )
    return jsonify({'url': url_map.original}), 200
