"""Telegram-обработчики и запуск ExpenseBot (слой Handlers, ADR-003)."""

import asyncio
import logging
from datetime import date

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from .config import load_settings
from .parser import ParseError
from .repository import ExpenseRepository
from .service import ExpenseService

router = Router()

HELP_TEXT = (
    "Привет! Я записываю расходы.\n\n"
    "Отправь сообщение в формате:\n"
    "<сумма> <категория> [комментарий]\n"
    "Например: 250 кофе утренний\n\n"
    "/report — расходы за текущий месяц"
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Отправляет инструкцию по использованию бота."""
    await message.answer(HELP_TEXT)


@router.message(Command("report"))
async def cmd_report(message: Message, service: ExpenseService) -> None:
    """Отправляет отчёт о расходах за текущий месяц."""
    if message.from_user is None:
        return
    report = service.month_report(message.from_user.id, date.today())
    if not report:
        await message.answer("В этом месяце расходов пока нет.")
        return
    lines = [f"{category} — {total:.2f} ₽" for category, total in report.items()]
    await message.answer("Расходы за месяц:\n" + "\n".join(lines))


@router.message(F.text)
async def add_expense(message: Message, service: ExpenseService) -> None:
    """Сохраняет расход из текста сообщения."""
    if message.from_user is None or message.text is None:
        return
    try:
        expense = service.add_from_text(
            message.from_user.id, message.text, date.today()
        )
    except ParseError as error:
        await message.answer(f"Ошибка: {error}")
        return
    await message.answer(f"Записано: {expense.amount:.2f} ₽ — {expense.category}")


async def main() -> None:
    """Создаёт бота и запускает приём сообщений (long polling)."""
    settings = load_settings()
    service = ExpenseService(ExpenseRepository(settings.db_path))
    dispatcher = Dispatcher(service=service)
    dispatcher.include_router(router)
    await dispatcher.start_polling(Bot(settings.bot_token))


def run() -> None:
    """Точка входа: загружает .env и запускает бота."""
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())


if __name__ == "__main__":
    run()
