class YandexDiskError(Exception):
    """Базовый класс для ошибок, связанных с Яндекс.Диском."""


class YandexDiskUploadError(YandexDiskError):
    """Ошибка при загрузке файла на Яндекс.Диск."""


class YandexDiskDownloadLinkError(YandexDiskError):
    """Ошибка при получении ссылки для скачивания с Яндекс.Диска."""


class CustomIDGenerationError(Exception):
    """Ошибка при генерации уникального идентификатора."""
