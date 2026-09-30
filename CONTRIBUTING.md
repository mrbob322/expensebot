# Руководство для участников

## Как сообщить о баге

Создайте issue по шаблону:

```text
**Что произошло:**
**Ожидаемое поведение:**
**Шаги воспроизведения:**
1.
**Окружение:** ОС, версия Python, версия ExpenseBot
```

## Как предложить фичу

Создайте issue с меткой `enhancement`: опишите проблему, предлагаемое решение и пользовательскую историю в формате «Как <роль>, я хочу <действие>, чтобы <цель>».

## Настройка окружения

1. Сделайте fork и клонируйте репозиторий.
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements-dev.txt`
4. `pre-commit install --install-hooks && pre-commit install --hook-type commit-msg`
5. `cp .env.example .env` и заполните `BOT_TOKEN`.

## Именование веток

`feature/<кратко>`, `fix/<кратко>`, `docs/<кратко>`, `release/<версия>`, `hotfix/<кратко>`. Пример: `feature/undo-command`.

## Коммиты

Формат [Conventional Commits](https://www.conventionalcommits.org/ru/): `type(scope): описание` на английском. Типы: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`. Пример: `feat(parser): support comma as decimal separator`.

## Pull request

- Один PR — одна задача.
- Описание: что и зачем изменено, ссылка на issue.
- Все проверки (линтер, типы, тесты) проходят.
- Новый код покрыт тестами, публичные функции — docstrings.
- Минимум одно одобрение ревьюера.

## Тесты и линтеры

```bash
isort --check src
black --check src
flake8 src
mypy
pytest
```

## Кодекс поведения

Будьте вежливы, критикуйте код, а не людей, принимайте разные уровни опыта. Оскорбления и дискриминация недопустимы; о нарушениях сообщайте автору проекта.
