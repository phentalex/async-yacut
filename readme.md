# YaCut

Сервис для сокращения ссылок и хранения файлов на Яндекс.Диске. Пользователи могут создавать короткие ссылки вручную или с автогенерацией, а также загружать файлы и получать на них короткие ссылки.

## Возможности

- Создание коротких ссылок с пользовательским идентификатором или автогенерацией
- Загрузка файлов на Яндекс.Диск с получением короткой ссылки
- REST API для управления ссылками
- Редирект по короткой ссылке на оригинальный URL

## Стек

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-WTF
- aiohttp
- SQLite
- Яндекс.Диск API

## Переменные окружения

Создай файл `.env` в корне проекта:

```env
SECRET_KEY=your-secret-key
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your-yandex-disk-oauth-token
YADISK_APP=yacut
```

Токен Яндекс.Диска получается через [oauth.yandex.ru](https://oauth.yandex.ru). Приложению необходимы права `cloud_api:disk.app_folder`

## Запуск локально

```bash
git clone https://github.com/phentalex/async-yacut.git
cd async-yacut
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
source venv/Scripts/activate

pip install -r requirements.txt
flask db upgrade
flask run
```

Доступно здесь → http://localhost:5000

## API эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/id/` | Создать короткую ссылку |
| GET | `/api/id/<short_id>/` | Получить оригинальную ссылку |

### Пример запроса

```json
POST /api/id/
{
    "url": "https://example.com",
    "custom_id": "my-link"
}
```

### Пример ответа

```json
{
    "url": "https://example.com",
    "short_link": "http://localhost:5000/my-link"
}
```

## Автор

**Александр Уваров** — [GitHub](https://github.com/phentalex)