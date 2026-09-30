"""Конфигурация приложения из переменных окружения."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Настройки приложения.

    Attributes:
        bot_token: Токен Telegram-бота.
        db_path: Путь к файлу базы данных SQLite.
    """

    bot_token: str
    db_path: str


def load_settings() -> Settings:
    """Загружает настройки из переменных окружения.

    Returns:
        Объект настроек.

    Raises:
        RuntimeError: Если переменная BOT_TOKEN не задана.

    Examples:
        >>> os.environ["BOT_TOKEN"] = "123:abc"
        >>> load_settings().bot_token
        '123:abc'
    """
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("Переменная окружения BOT_TOKEN не задана")
    return Settings(bot_token=token, db_path=os.environ.get("DB_PATH", "expenses.db"))
