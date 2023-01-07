import calendar
from globals import month_list
from datetime import datetime, timedelta
from aiogram import types, Dispatcher, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import dp, bot

tempdate = datetime.now()

def create_calendar(year: int, month: int):
    markup = InlineKeyboardMarkup(row_width=7)
    data = calendar.monthcalendar(year, month)
    for week in data:
        for day in week:
            if day == 0:
                markup.insert(InlineKeyboardButton(text=' ', callback_data='pass'))
            else:
                markup.insert(InlineKeyboardButton(text=str(day), callback_data=f'day-{day}'))
    markup.row(InlineKeyboardButton(text='<', callback_data='previous-month'),
               InlineKeyboardButton(text='>', callback_data='next-month'))
    return markup

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('day-'))
async def process_calendar_selection(callback_query: types.CallbackQuery):
    selected, day = callback_query.data.split('-')
    await bot.send_message(callback_query.from_user.id, f'Вы выбрали {day} число')

@dp.callback_query_handler(lambda c: c.data == 'pass')
async def process_pass_button(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Дата не выбрана')

@dp.callback_query_handler(lambda c: c.data == 'previous-month')
async def process_previous_month_button(callback_query: types.CallbackQuery):
    global tempdate
    previous_month = tempdate - timedelta(days=30)
    tempdate = previous_month
    client_date = str(month_list[tempdate.month]) + ' ' + str(tempdate.year)
    markup = create_calendar(previous_month.year, previous_month.month)
    await bot.edit_message_text(f"Дата: {client_date}", callback_query.from_user.id, callback_query.message.message_id, reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'next-month')
async def process_previous_month_button(callback_query: types.CallbackQuery):
    global tempdate
    next_month = tempdate + timedelta(days=30)
    tempdate = next_month
    client_date = str(month_list[tempdate.month]) + ' ' + str(tempdate.year)
    markup = create_calendar(next_month.year, next_month.month)
    await bot.edit_message_text(f"Дата: {client_date}", callback_query.from_user.id, callback_query.message.message_id, reply_markup=markup)

async def process_calendar_command(message: types.Message):
    current = datetime.now()
    client_date = month_list[current.month] + ' ' + str(current.year)
    markup = create_calendar(current.year, current.month)
    await bot.send_message(message.from_user.id, f"Дата: {client_date}", reply_markup=markup)

def register_handlers_calendar(dp: Dispatcher):
    dp.register_message_handler(process_calendar_command, commands=['calendar'])