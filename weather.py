import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

class WeatherState(StatesGroup):
    waiting_for_city = State()

async def get_weather(city_name):
    # weather_url = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid=05a9fb1cecaca7a61f846213566c28f9"
    #weather_url = "https://wttr.in/{}?0&m&T&q&lang=ru".format(city_name)
    weather_url = "https://wttr.in/{}?m&format=2&lang=ru".format(city_name)
    response = requests.get(weather_url)
    return response.text
    print(response)
    if response["cod"] != "404":
        weather_data = response["weather"][0]["description"]
        temp_data = response["main"]["temp"]
        return f"Сегодня в {city_name} {weather_data}, температура {temp_data}°C"
    else:
        return "Город не найден"

async def weather_handler(message: types.Message, state: FSMContext):
    await message.answer("Введи название города, чтобы узнать погоду")
    await WeatherState.waiting_for_city.set()

async def process_weather_command(message: types.Message, state: FSMContext):
    await weather_handler(message, state)

async def process_city_name(message: types.Message, state: FSMContext):
    city_name = message.text
    await state.finish()
    await message.answer(await get_weather(city_name), parse_mode=ParseMode.HTML)

def register_handlers_weather(dp: Dispatcher):
    dp.register_message_handler(weather_handler, Command("weather"), state="*")
    dp.register_message_handler(process_city_name, state=WeatherState.waiting_for_city)