import asyncio
from asyncio import sleep
from random import randint
import globals
from datetime import datetime as dt, timedelta
from aiohttp import ClientSession
import logging
from typing import Optional
from aiogram import types, Dispatcher

log = logging.getLogger('congratulations_module')


async def congrats_from_porfirii(session: ClientSession, base_congrats: str, **kwargs) -> Optional[str]:
    """
    Функция обращается к API сайта https://porfirevich.ru для генерации текста поздравления.

    :base_congrats -- шаблон поздравления передаваемый Порфирьевичу\n
    :length -- задаёт длину генерируемой последовательности (кол-во слов). По умолчанию 50.\n
    """
    generated_text_lenght = 50 if len(kwargs) == 0 else kwargs["length"]
    post_payload = {"prompt": base_congrats, "length": generated_text_lenght}
    log.info('Trying to connect to porfirii API...')
    async with session.post('https://pelevin.gpt.dobro.ai/generate/', json=post_payload, ssl=False) as resp:
        if resp.status == 200:
            log.info(
                'Connection to porfirii API successfull. Generating congratulations.')
            json_data = await resp.json()
            replies_list = json_data.get('replies')
            replies_list.sort(key=len, reverse=True)
            return replies_list[0]
        else:
            log.error(
                f'Connection to porfirii failed! Response status: {resp.status}.')
            return None

async def get_new_year_fortune(message: types.Message):
    sender_member = message.from_user.first_name
    if sender_member is None:
        log.info(f"In get_new_year_fortune got unknown telegram_id. From user: {message.from_user.first_name}")
    sender_name = sender_member if sender_member is not None else message.from_user.first_name
    fortune_template = f"{sender_name}, в этом году в Студии ты обязательно"
    generated_fortune = None
    reply_message = await message.reply("Составляю прогноз на год...📝")
    aiohttp_session = ClientSession(trust_env=True)

    generated_fortune = await congrats_from_porfirii(aiohttp_session, fortune_template, length=40)
    generated_fortune = generated_fortune if generated_fortune is not None else \
        f" сможешь всё. А вот мои нейромозги пока не работают..."
    await aiohttp_session.close()
    await reply_message.edit_text("Сверяюсь с прогнозом астролога...🌠")
    await sleep(2)
    await reply_message.edit_text(f"{fortune_template}{generated_fortune}")

async def get_new_year_fortune_t(message: types.Message):
    sender_member = message.from_user.first_name
    if sender_member is None:
        log.info(f"In get_new_year_fortune got unknown telegram_id. From user: {message.from_user.first_name}")
    sender_name = sender_member if sender_member is not None else message.from_user.first_name
    # fortune_template = f"В этом году диджитал агенство «Студии Т»"
    fortune_template = f"В этом году диджитал агентство «Студия Т» обязательно"
    generated_fortune = None
    reply_message = await message.reply("Провожу ретроспективу 2022...💾")
    aiohttp_session = ClientSession(trust_env=True)

    generated_fortune = await congrats_from_porfirii(aiohttp_session, fortune_template, length=40)
    generated_fortune = generated_fortune if generated_fortune is not None else \
        f" сможешь всё. А вот мои нейромозги пока не работают..."
    await aiohttp_session.close()
    await reply_message.edit_text("Составляю прогноз на 2023...📝")
    await sleep(2)
    await reply_message.edit_text(f"{fortune_template}{generated_fortune}")


def register_handlers_ny(dp: Dispatcher):
    dp.register_message_handler(get_new_year_fortune, commands=['newyear'])
    dp.register_message_handler(get_new_year_fortune_t, commands=['newyeart'])