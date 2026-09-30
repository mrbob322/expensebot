# ExpenseBot

Telegram-бот для учёта личных расходов: записывает траты одним сообщением и показывает отчёт по категориям за месяц.

![CI](https://img.shields.io/badge/CI-passing-brightgreen)
![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Coverage](https://img.shields.io/badge/coverage-70%25%2B-yellowgreen)

## Пример

```text
Вы:  250 кофе утренний
Бот: Записано: 250.00 ₽ — кофе

Вы:  /report
Бот: Расходы за месяц:
     кофе — 250.00 ₽
```

## Требования

- Python 3.11 или новее
- Токен бота от [@BotFather](https://t.me/BotFather)

## Установка

```bash
git clone https://github.com/<mrbob322>/expensebot.git
cd expensebot
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pre-commit install --install-hooks
pre-commit install --hook-type commit-msg
cp .env.example .env             # впишите BOT_TOKEN
```

## Быстрый старт

```python
from datetime import date
from expensebot.repository import ExpenseRepository
from expensebot.service import ExpenseService

service = ExpenseService(ExpenseRepository(":memory:"))
service.add_from_text(1, "250 кофе", date.today())
print(service.month_report(1, date.today()))
```

## Запуск бота

```bash
pip install -e .
python -m expensebot.bot
```

## Использование

| Сообщение | Действие |
|---|---|
| `/start` | Инструкция по использованию |
| `<сумма> <категория> [комментарий]` | Добавить расход |
| `/report` | Отчёт за текущий месяц |

## Конфигурация

| Переменная | Описание | По умолчанию |
|---|---|---|
| `BOT_TOKEN` | Токен Telegram-бота | — (обязательна) |
| `DB_PATH` | Путь к файлу SQLite | `expenses.db` |

## Структура проекта

```text
src/expensebot/   исходный код (parser, service, repository, models, config)
tests/            тесты
docs/             документация (PRD, ADR, руководство по стилю)
```

## Тестирование

```bash
pytest
```

## Документация

Сборка: `mkdocs build`; локальный просмотр: `mkdocs serve`. Ссылка на опубликованную версию: *будет добавлена после настройки GitHub Pages*.

## Лицензия

[MIT](LICENSE). Выбор обоснован тем, что лицензия проста, разрешает свободное использование и подходит для учебного открытого проекта.

## Контакты автора

Тетюшкин Никита Денисович, группа РПО 23-1, Академия ТОП.
