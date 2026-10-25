# CLI: `expensebot`

Консольная утилита для управления расходами.

## Команды
| Команда | Описание |
|---|---|
| `expensebot add <сумма> <категория>` | Добавить расход |
| `expensebot list` | Показать расходы |
| `expensebot delete <id>` | Удалить расход |
| `expensebot categories` | Список категорий |
| `expensebot report` | Сводка за период |
| `expensebot export` | Выгрузка в файл |
| `expensebot run` | Запустить Telegram-бота |

## Флаги
| Флаг | Описание | По умолчанию |
|---|---|---|
| `-c, --comment TEXT` | Комментарий (для `add`) | — |
| `-d, --date YYYY-MM-DD` | Дата расхода | сегодня |
| `--from`, `--to` | Период (`list`, `report`, `export`) | текущий месяц |
| `--category TEXT` | Фильтр по категории | — |
| `--limit N` | Максимум записей | 20 |
| `-f, --format table\|json\|csv` | Формат вывода | table |
| `-o, --output PATH` | Файл для `export` | stdout |
| `-v, --verbose` | Подробный лог | выкл. |
| `-h, --help`, `--version` | Справка, версия | — |

## Примеры
```bash
expensebot add 350.5 Еда -c "Обед"
expensebot list --from 2026-10-01 --format json
expensebot report --from 2026-10-01 --to 2026-10-31
expensebot export --format csv -o october.csv
```

## Форматы вывода
`table` — для человека; `json` — для скриптов; `csv` — для Excel.

## Коды возврата
| Код | Значение |
|---|---|
| 0 | Успех |
| 1 | Общая ошибка |
| 2 | Неверные аргументы или флаги |
| 3 | Ошибка валидации (сумма, дата) |
| 4 | Не найдено (id, категория) |
| 5 | Нет доступа / неверный токен |
| 6 | Ошибка базы данных |
| 7 | Нет подключения к сети |
| 8 | Ошибка записи файла |
| 9 | Ошибка конфигурации |
| 10 | Прервано пользователем |

## Переменные окружения
| Переменная | Описание |
|---|---|
| `EXPENSEBOT_TOKEN` | Токен Telegram-бота (обязательно для `run`) |
| `EXPENSEBOT_DB` | Путь к БД SQLite (по умолчанию `./expenses.db`) |
| `EXPENSEBOT_API_URL` | Адрес REST API |
| `EXPENSEBOT_LANG` | Язык вывода: `ru` / `en` |
| `NO_COLOR` | Отключить цвета в выводе |
