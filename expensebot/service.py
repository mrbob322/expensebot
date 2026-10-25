import sqlite3
from datetime import date as Date
from decimal import Decimal
from typing import Optional

from .exceptions import NotFoundError, StorageError, ValidationError
from .models import Category, Expense


class ExpenseService:
    """Работа с расходами в SQLite."""

    def __init__(self, db_path: str = "expenses.db"):
        try:
            self._db = sqlite3.connect(db_path)
            self._db.execute(
                "CREATE TABLE IF NOT EXISTS categories("
                "id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL)")
            self._db.execute(
                "CREATE TABLE IF NOT EXISTS expenses("
                "id INTEGER PRIMARY KEY, amount TEXT NOT NULL, category TEXT NOT NULL,"
                "comment TEXT, date TEXT NOT NULL)")
            self._db.commit()
        except sqlite3.Error as e:
            raise StorageError(str(e)) from e

    @staticmethod
    def _row(r) -> Expense:
        return Expense(r[0], Decimal(r[1]), r[2], r[3], Date.fromisoformat(r[4]))

    def add(self, amount, category: str, comment: Optional[str] = None,
            date: Optional[Date] = None) -> Expense:
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValidationError("Сумма должна быть больше 0")
        if not category or len(category) > 50:
            raise ValidationError("Категория: от 1 до 50 символов")
        date = date or Date.today()
        self._db.execute("INSERT OR IGNORE INTO categories(name) VALUES(?)", (category,))
        cur = self._db.execute(
            "INSERT INTO expenses(amount, category, comment, date) VALUES(?,?,?,?)",
            (str(amount), category, comment, date.isoformat()))
        self._db.commit()
        return Expense(cur.lastrowid, amount, category, comment, date)

    def get(self, expense_id: int) -> Expense:
        r = self._db.execute(
            "SELECT id, amount, category, comment, date FROM expenses WHERE id=?",
            (expense_id,)).fetchone()
        if not r:
            raise NotFoundError(f"Расход {expense_id} не найден")
        return self._row(r)

    def list(self, limit: int = 20, category: Optional[str] = None,
             date_from: Optional[Date] = None, date_to: Optional[Date] = None):
        q, args = "SELECT id, amount, category, comment, date FROM expenses WHERE 1=1", []
        if category:
            q += " AND category=?"; args.append(category)
        if date_from:
            q += " AND date>=?"; args.append(date_from.isoformat())
        if date_to:
            q += " AND date<=?"; args.append(date_to.isoformat())
        q += " ORDER BY date DESC, id DESC LIMIT ?"; args.append(limit)
        return [self._row(r) for r in self._db.execute(q, args)]

    def delete(self, expense_id: int) -> None:
        self.get(expense_id)
        self._db.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        self._db.commit()

    def summary(self, date_from: Date, date_to: Date) -> dict:
        res = {}
        for e in self.list(limit=100000, date_from=date_from, date_to=date_to):
            res[e.category] = res.get(e.category, Decimal(0)) + e.amount
        return res

    def categories(self):
        return [Category(r[0], r[1]) for r in
                self._db.execute("SELECT id, name FROM categories ORDER BY name")]
