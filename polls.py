from aiogram import types, Dispatcher
from create_bot import bot
from datetime import datetime
from register_handlers import admins
import asyncio

async def create_poll():
    poll = types.Poll(
        question="Обэд",
        options=["Йоки", "Южане", "Ребро", "Шава", "KFC", "Make Love", "Баракат", "Посмотреть результаты"],
        is_anonymous=False,
        type=types.PollType.REGULAR,
        allows_multiple_answers=True,
        open_period=5400,
    )
    await bot.send_poll(chat_id=-1001723462410, question=poll.question, options=poll.options, is_anonymous=poll.is_anonymous, type=poll.type, allows_multiple_answers=poll.allows_multiple_answers, open_period=poll.open_period)