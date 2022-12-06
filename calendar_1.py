import calendar
from datetime import datetime
from aiogram import types, Dispatcher, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import dp, bot

#создать клавиатуру, в кнопках которого будет календарь на текущий месяц. По нажатию на кнопку будеты выводиться дата
#при нажатии на кнопку с датой, будет выводиться сообщение с датой

#создаем клавиатуру
def create_calendar(year: int, month: int):
    markup = InlineKeyboardMarkup(row_width=7)
    #создаем кнопки с датами
    #получаем все даты для текущего месяца
    data = calendar.monthcalendar(year, month)
    #проходимся по всем неделям и дням недели, записываем кнопки с датами
    for week in data:
        for day in week:
            #если день = 0, то кнопка пустая
            if day == 0:
                markup.insert(InlineKeyboardButton(text=' ', callback_data='pass'))
            else:
                markup.insert(InlineKeyboardButton(text=str(day), callback_data=f'day-{day}'))
    #добавляем кнопки "назад" и "вперед"
    markup.row(InlineKeyboardButton(text='<', callback_data='previous-month'),
               InlineKeyboardButton(text='>', callback_data='next-month'))
    return markup

#обработчик нажатия на кнопку
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('day-'))
async def process_calendar_selection(callback_query: types.CallbackQuery):
    #получаем выбранную дату
    selected, day = callback_query.data.split('-')
    await bot.send_message(callback_query.from_user.id, f'Вы выбрали {day} число')

#обработчик нажатия на кнопку "назад" и "вперед"
@dp.callback_query_handler(lambda c: c.data in ('previous-month', 'next-month'))
async def process_calendar_selection(callback_query: types.CallbackQuery):
    print('123')
    #получаем текущую дату
    current = datetime.now()
    #получаем выбранную дату
    selected, day = callback_query.data.split('-')
    #получаем год и месяц
    year, month = current.year, current.month
    #если выбрана кнопка "назад", то вычитаем месяц
    if selected == 'previous-month':
        month -= 1
        #если месяц = 0, то вычитаем год и ставим декабрь
        if month == 0:
            month = 12
            year -= 1
    #если выбрана кнопка "вперед", то прибавляем месяц
    elif selected == 'next-month':
        month += 1
        #если месяц = 13, то прибавляем год и ставим январь
        if month == 13:
            month = 1
            year += 1
    #создаем новую клавиатуру
    markup = create_calendar(year, month)
    #отправляем сообщение с новой клавиатурой
    await bot.send_message(callback_query.from_user.id, 'Месяц: ' + str(month) + ' Год: ' + str(year), reply_markup=markup)

#обработчик команды /calendar
async def process_calendar_command(message: types.Message):
    #получаем текущую дату
    current = datetime.now()
    #создаем клавиатуру
    markup = create_calendar(current.year, current.month)
    #отправляем сообщение с клавиатурой
    await bot.send_message(message.from_user.id, 'Выберите дату', reply_markup=markup)

def register_handlers_calendar(dp: Dispatcher):
    dp.register_message_handler(process_calendar_command, commands=['calendar'])