"""Модели данных ExpenseBot."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Expense:
    """Одна запись о расходе.

    Attributes:
        user_id: Идентификатор пользователя в Telegram.
        amount: Сумма расхода в рублях.
        category: Категория расхода в нижнем регистре.
        note: Произвольный комментарий (может быть пустым).
        spent_on: Дата расхода.
    """

    user_id: int
    amount: Decimal
    category: str
    note: str
    spent_on: date
