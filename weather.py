import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

class WeatherState(StatesGroup):
    waiting_for_city = State()

async def get_weather(city_name):
    weather_url = "https://wttr.in/{}?m&format=2&lang=ru".format(city_name)
    response = requests.get(weather_url)
    return response.text

async def weather_handler(message: types.Message, state: FSMContext):
    if (message.chat.type == 'private'):
        await message.answer("Введи название города, чтобы узнать погоду")
        await WeatherState.waiting_for_city.set()
    else:
        await message.answer("Эта команда доступна только в личных сообщениях")
        await state.finish()

async def process_weather_command(message: types.Message, state: FSMContext):
    await weather_handler(message, state)

async def process_city_name(message: types.Message, state: FSMContext):
    city_name = message.text
    await state.finish()
    await message.answer(await get_weather(city_name), parse_mode=ParseMode.HTML)

def register_handlers_weather(dp: Dispatcher):
    dp.register_message_handler(weather_handler, Command("weather"), state="*")
    dp.register_message_handler(process_city_name, state=WeatherState.waiting_for_city)