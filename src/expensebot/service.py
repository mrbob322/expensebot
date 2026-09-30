"""Бизнес-логика учёта расходов."""

from datetime import date
from decimal import Decimal

from .models import Expense
from .parser import parse_expense_text
from .repository import ExpenseRepository


class ExpenseService:
    """Сценарии работы с расходами, не зависящие от Telegram."""

    def __init__(self, repository: ExpenseRepository) -> None:
        """Создаёт сервис.

        Args:
            repository: Хранилище расходов.
        """
        self._repository = repository

    def add_from_text(self, user_id: int, text: str, today: date) -> Expense:
        """Создаёт и сохраняет расход из текста сообщения.

        Args:
            user_id: Идентификатор пользователя.
            text: Текст вида «250 кофе».
            today: Дата, которая записывается как дата расхода.

        Returns:
            Сохранённый расход.

        Raises:
            ParseError: Если текст не удалось разобрать.

        Examples:
            >>> service = ExpenseService(ExpenseRepository(":memory:"))
            >>> service.add_from_text(1, "100 такси", date(2026, 9, 1)).category
            'такси'
        """
        amount, category, note = parse_expense_text(text)
        expense = Expense(user_id, amount, category, note, today)
        self._repository.add(expense)
        return expense

    def month_report(self, user_id: int, today: date) -> dict[str, Decimal]:
        """Возвращает расходы текущего месяца по категориям.

        Args:
            user_id: Идентификатор пользователя.
            today: Любая дата внутри нужного месяца.

        Returns:
            Словарь «категория → сумма».
        """
        first_day = today.replace(day=1)
        return self._repository.totals_by_category(user_id, first_day, today)
