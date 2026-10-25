# Публичный API библиотеки `expensebot`

Версия: **1.0.0** (SemVer). Python 3.10+.

```python
from expensebot import ExpenseService, Expense, Category
```

## Классы

### `Expense`
Датакласс расхода.
Поля: `id: int`, `amount: Decimal`, `category: str`, `comment: str | None`, `date: date`.

### `Category`
Поля: `id: int`, `name: str`.

### `ExpenseService(db_path: str = "expenses.db")`
| Метод | Описание |
|---|---|
| `add(amount, category, comment=None, date=None) -> Expense` | Добавить расход. `ValueError`, если `amount <= 0` |
| `get(expense_id) -> Expense` | Получить расход. `NotFoundError`, если нет |
| `list(limit=20, category=None, date_from=None, date_to=None) -> list[Expense]` | Список с фильтрами |
| `delete(expense_id) -> None` | Удалить расход |
| `summary(date_from, date_to) -> dict[str, Decimal]` | Итоги по категориям |
| `categories() -> list[Category]` | Все категории |

### Исключения
`ExpenseBotError` (базовое) → `NotFoundError`, `ValidationError`, `StorageError`.

## Примеры использования
```python
from datetime import date
from expensebot import ExpenseService

svc = ExpenseService()
e = svc.add(350.5, "Еда", comment="Обед")
print(e.id, e.amount)

for item in svc.list(limit=5, date_from=date(2026, 10, 1)):
    print(item.date, item.category, item.amount)

print(svc.summary(date(2026, 10, 1), date(2026, 10, 31)))
```

## Политика совместимости (SemVer)
| Изменение | Версия | Пример |
|---|---|---|
| Новая функция, обратно совместимо | MINOR | 1.0.0 → 1.1.0 |
| Исправление ошибки | PATCH | 1.1.0 → 1.1.1 |
| Удаление / смена сигнатуры | MAJOR | 1.1.1 → 2.0.0 |

**Deprecation:** сначала `.. deprecated:: X.Y` в docstring и `DeprecationWarning`; удаляем не раньше чем через 1–2 MINOR-версии и только в MAJOR.

| Версия библиотеки | Python |
|---|---|
| 1.x | 3.10+ |
