# Руководство по стилю кода

## Выбранный стандарт

Проект написан на Python, поэтому используется **PEP 8** (https://peps.python.org/pep-0008/). Выбор обоснован тем, что это официальный стандарт языка, для него есть зрелые инструменты автоматической проверки и форматирования.

## Инструменты и конфиги

| Задача | Инструмент | Конфиг |
|---|---|---|
| Линтер | flake8 | `.flake8` |
| Форматтер | black | `[tool.black]` в `pyproject.toml` |
| Сортировка импортов | isort | `[tool.isort]` в `pyproject.toml` |
| Проверка типов | mypy (`strict = true`) | `[tool.mypy]` в `pyproject.toml` |
| Автозапуск перед коммитом | pre-commit | `.pre-commit-config.yaml` |

Запуск всех проверок:

```bash
isort --check src && black --check src && flake8 src && mypy && pytest
```

Результат успешной проверки сохранён в `docs/lint-log.txt`.

## Правила именования

| Сущность | Стиль | Пример |
|---|---|---|
| Переменные и функции | `snake_case` | `parse_expense_text`, `first_day` |
| Классы | `PascalCase` | `ExpenseService`, `ParseError` |
| Константы | `UPPER_SNAKE_CASE` | `_SCHEMA` (с префиксом `_`, если приватная) |
| Модули и пакеты | `lowercase` | `repository.py`, `expensebot` |
| Приватные члены | префикс `_` | `self._repository` |

Имена должны быть осмысленными; однобуквенные допускаются только для счётчиков циклов.

## Импорты

Три группы, между ними пустая строка: стандартная библиотека, сторонние пакеты, локальные модули. Внутри группы — по алфавиту (обеспечивает isort). Один импорт на строку для `import`, запрещён `from x import *`. Внутри пакета используются относительные импорты.

```python
from datetime import date
from decimal import Decimal

from .models import Expense
from .parser import parse_expense_text
```

## Длина строки и отступы

- Максимальная длина строки — 88 символов (стандарт black).
- Отступ — 4 пробела, табуляция запрещена.
- Строки кодируются в UTF-8, перенос строки — LF, в конце файла — одна пустая строка (`.editorconfig`).

## Документирование кода

Используется **Google Style** docstrings. Обязательны для каждого модуля, публичного класса и функции. Структура: краткое описание в одну строку; при необходимости — развёрнутое; разделы `Args`, `Returns`, `Raises`, `Examples`. Комментарии `#` объясняют **почему**, а не **что**, и при необходимости ссылаются на ADR.

## Примеры «правильно / неправильно»

### 1. Имена функций

```python
# Неправильно
def ParseExp(t):
    ...

# Правильно (src/expensebot/parser.py)
def parse_expense_text(text: str) -> tuple[Decimal, str, str]:
    ...
```

### 2. Аннотации типов

```python
# Неправильно
def totals_by_category(self, user_id, start, end):
    ...

# Правильно (src/expensebot/repository.py)
def totals_by_category(
    self, user_id: int, start: date, end: date
) -> dict[str, Decimal]:
    ...
```

### 3. Импорты

```python
# Неправильно
from decimal import *
import re, os
from .models import Expense
import sqlite3

# Правильно (src/expensebot/repository.py)
import sqlite3
from datetime import date
from decimal import Decimal

from .models import Expense
```

### 4. Деньги: Decimal вместо float

```python
# Неправильно
amount = float(match.group("amount"))

# Правильно (src/expensebot/parser.py)
amount = Decimal(match.group("amount").replace(",", "."))
```

### 5. Комментарий: «почему», а не «что»

```python
# Неправильно
# умножаем на 100
kopecks = int(expense.amount * 100)

# Правильно (src/expensebot/repository.py)
# Сумма хранится в копейках: float даёт ошибки округления (ADR-002).
kopecks = int(expense.amount * 100)
```

### 6. Docstring

```python
# Неправильно
def load_settings():
    """Загрузка."""

# Правильно (src/expensebot/config.py)
def load_settings() -> Settings:
    """Загружает настройки из переменных окружения.

    Returns:
        Объект настроек.

    Raises:
        RuntimeError: Если переменная BOT_TOKEN не задана.
    """
```

### 7. Обработка исключений

```python
# Неправильно
if match is None:
    return None

# Правильно (src/expensebot/parser.py)
if match is None:
    raise ParseError("Ожидается формат: <сумма> <категория> [комментарий]")
```
