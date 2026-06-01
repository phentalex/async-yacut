class YandexDiskError(Exception):
    """Базовый класс для ошибок, связанных с Яндекс.Диском."""
    pass


class YandexDiskUploadError(YandexDiskError):
    """Ошибка при загрузке файла на Яндекс.Диск."""
    pass


class YandexDiskDownloadLinkError(YandexDiskError):
    """Ошибка при получении ссылки для скачивания с Яндекс.Диска."""
    pass
