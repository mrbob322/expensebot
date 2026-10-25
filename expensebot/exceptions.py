class ExpenseBotError(Exception):
    """Базовое исключение библиотеки."""


class NotFoundError(ExpenseBotError):
    """Объект не найден."""


class ValidationError(ExpenseBotError, ValueError):
    """Некорректные данные."""


class StorageError(ExpenseBotError):
    """Ошибка базы данных."""
