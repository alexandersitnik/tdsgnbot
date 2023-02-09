from aiogram import types, Dispatcher
from create_bot import bot
from datetime import datetime
from register_handlers import admins
import asyncio

restorans = {
    'Йоки': 'https://yokitoki.ru/',
    'Южане': 'https://yuzhanedostavka.ru/',
    'Ребро': 'https://tsk.rebrorussia.ru/tomsk/burgery',
    'Шава': 'https://eda.yandex.ru/restaurant/sochno_phadq?shippingType=delivery&utm_campaign=android&utm_medium=referral&utm_source=rst_shared_link',
    'KFC': 'https://www.kfc.ru/',
    'Make Love': 'https://makelovepizza.ru/tomsk',
    'Баракат': 'https://barakat70.ru/catalog/',
    'Антрекот': 'https://antrekot.tomsk.ru/',
    'Посмотреть результаты': 0,
}

async def create_poll():
    poll = types.Poll(
        question="Обэд",
        options=["Йоки", "Южане", "Ребро", "Шава", "KFC", "Make Love", "Баракат", "Антрекот", "Посмотреть результаты"],
        is_anonymous=False,
        type=types.PollType.REGULAR,
        allows_multiple_answers=True,
        # open_period=10,
    )
    poll_id = await bot.send_poll(chat_id=-1001723462410, question=poll.question, options=poll.options, is_anonymous=poll.is_anonymous, type=poll.type, allows_multiple_answers=poll.allows_multiple_answers)
    await asyncio.sleep(1800)
    poll_results = await bot.stop_poll(chat_id=-1001723462410, message_id=poll_id.message_id)
    print('Опрос закрыт')
    max = 0
    food = ''
    for poll_option in poll_results.options:
        if poll_option.voter_count > max:
            max = poll_option.voter_count
            food = poll_option.text
    if food == 'Посмотреть результаты':
        await bot.send_message(-1001723462410, f'Никто не ответил')
    await bot.send_message(-1001723462410, f'Сегодня обедаем в {food}')
    await bot.send_message(-1001723462410, f'Заказы принимаются в ЛС @KrisKladova до 12.20 {restorans[food]}')

    print(poll_results)
    return poll_id


# chat_id=-1001723462410