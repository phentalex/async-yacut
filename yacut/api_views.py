import http

from flask import jsonify, request

from .error_handlers import InvalidAPIUsage
from . import app
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage(r'"url" является обязательным полем!')
    try:
        url_map = URLMap.create(data['url'], data.get('custom_id'))
    except ValueError as e:
        raise InvalidAPIUsage(str(e))
    return jsonify(url_map.to_dict()), http.HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap().get_by_short_id(short_id)
    if url_map is None:
        raise InvalidAPIUsage(
            'Указанный id не найден', http.HTTPStatus.NOT_FOUND
        )
    return jsonify(url_map.get_original_link()), http.HTTPStatus.OK
