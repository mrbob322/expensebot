"""Хранилище расходов на SQLite."""

import sqlite3
from datetime import date
from decimal import Decimal

from .models import Expense

_SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount_kopecks INTEGER NOT NULL,
    category TEXT NOT NULL,
    note TEXT NOT NULL,
    spent_on TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_expenses_user_date ON expenses (user_id, spent_on);
"""


class ExpenseRepository:
    """Сохраняет и читает расходы из базы данных SQLite."""

    def __init__(self, db_path: str) -> None:
        """Открывает соединение и создаёт таблицы при необходимости.

        Args:
            db_path: Путь к файлу базы данных или ":memory:".
        """
        self._conn = sqlite3.connect(db_path)
        self._conn.executescript(_SCHEMA)

    def add(self, expense: Expense) -> int:
        """Сохраняет расход.

        Args:
            expense: Запись о расходе.

        Returns:
            Идентификатор созданной записи.
        """
        # Сумма хранится в копейках: float даёт ошибки округления (ADR-002).
        kopecks = int(expense.amount * 100)
        cursor = self._conn.execute(
            "INSERT INTO expenses (user_id, amount_kopecks, category, note, spent_on)"
            " VALUES (?, ?, ?, ?, ?)",
            (
                expense.user_id,
                kopecks,
                expense.category,
                expense.note,
                expense.spent_on.isoformat(),
            ),
        )
        self._conn.commit()
        return int(cursor.lastrowid or 0)

    def totals_by_category(
        self, user_id: int, start: date, end: date
    ) -> dict[str, Decimal]:
        """Считает сумму расходов по категориям за период.

        Args:
            user_id: Идентификатор пользователя.
            start: Первая дата периода (включительно).
            end: Последняя дата периода (включительно).

        Returns:
            Словарь «категория → сумма».
        """
        rows = self._conn.execute(
            "SELECT category, SUM(amount_kopecks) FROM expenses"
            " WHERE user_id = ? AND spent_on BETWEEN ? AND ?"
            " GROUP BY category",
            (user_id, start.isoformat(), end.isoformat()),
        ).fetchall()
        return {category: Decimal(total) / 100 for category, total in rows}
