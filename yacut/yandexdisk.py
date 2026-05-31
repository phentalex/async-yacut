import http
import os
import uuid

import aiohttp
import asyncio
import urllib

from . import app


API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
AUTH_HEADERS = {'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'}
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'

yadisk_app = os.getenv('YADISK_APP')


async def async_upload_files_to_yandex_disk(files):
    """Асинхронная загрузка файлов на Яндекс.Диск."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for file in files:
            tasks.append(upload_file_and_get_download_url(session, file))
        return await asyncio.gather(*tasks)


async def upload_file_and_get_download_url(session, file):
    """Асинхронная загрузка одного файла на Яндекс.Диск."""
    filename = f'{uuid.uuid4().hex}_{file.filename}'
    yadisk_args = {
        'path': f'disk:/Приложения/{yadisk_app}/{filename}',
        'overwrite': 'true'
    }

    async with session.get(
        url=REQUEST_UPLOAD_URL,
        headers=AUTH_HEADERS,
        params=yadisk_args
    ) as response:
        if response.status != http.HTTPStatus.OK:
            raise Exception(
                f'Ошибка при получении URL для загрузки: {response.status}'
            )
        data = await response.json()
        print(data)
        upload_url = data.get('href')
        if not upload_url:
            raise Exception('URL для загрузки не найден в ответе API.')
        async with session.put(
            data=file.read(),
            url=upload_url
        ) as response:
            if response.status != http.HTTPStatus.CREATED:
                raise Exception(
                    f'Ошибка при загрузке файла: {response.status}'
                )
            location = response.headers.get('Location')
            location = urllib.parse.unquote(location)
            location = location.replace('/disk', '')
        async with session.get(
            headers=AUTH_HEADERS,
            url=DOWNLOAD_LINK_URL,
            params={'path': location}
        ) as response:
            if response.status != http.HTTPStatus.OK:
                raise Exception(
                    f'Ошибка при получении URL для '
                    f'скачивания: {response.status}'
                )
            data = await response.json()
            download_url = data.get('href')
            if not download_url:
                raise Exception('URL для скачивания не найден в ответе API.')
            return download_url
