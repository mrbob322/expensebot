"""Разбор текстовых сообщений пользователя."""

import re
from decimal import Decimal

# Формат «<сумма> <категория> [комментарий]» выбран ради ввода одной строкой
# с телефона: диалог из нескольких шагов (ADR-001) слишком медленный.
_PATTERN = re.compile(
    r"^(?P<amount>\d+(?:[.,]\d{1,2})?)\s+(?P<category>\S+)(?:\s+(?P<note>.+))?$"
)


class ParseError(ValueError):
    """Сообщение не соответствует формату записи о расходе."""


def parse_expense_text(text: str) -> tuple[Decimal, str, str]:
    """Разбирает строку вида «250 кофе с пирожным».

    Args:
        text: Текст сообщения пользователя.

    Returns:
        Кортеж (сумма, категория, комментарий).

    Raises:
        ParseError: Если формат неверен или сумма не положительна.

    Examples:
        >>> parse_expense_text("250,50 Кофе утренний")
        (Decimal('250.50'), 'кофе', 'утренний')
    """
    match = _PATTERN.match(text.strip())
    if match is None:
        raise ParseError("Ожидается формат: <сумма> <категория> [комментарий]")
    # Запятую заменяем на точку: Decimal не понимает русский разделитель.
    amount = Decimal(match.group("amount").replace(",", "."))
    if amount <= 0:
        raise ParseError("Сумма должна быть больше нуля")
    return amount, match.group("category").lower(), match.group("note") or ""
