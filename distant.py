from calendar import monthrange
import calendar
import random
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot
from datetime import datetime, timedelta
from register_handlers import admins
import sqlite3

superAdmin_ID = 265007461
epithets = ['Ёлочки 🌲', 'Сосульки 🧊', 'Колокольчика 🔔', 'Мишуры 🎊', 'Морковки ⛄️','Имбирного пряника 🥮','Питарды 🧨','Феерверка 🎆','Бингальского огонька 🎇','Игрушки 🐰','Волшебства 🪄', 'Подарочка 🎁']

try:
    db = sqlite3.connect('./data/tdsgnBotBase.db')
    c = db.cursor()
except:
    pass

# Словарь для хранения данных о выбранной дате для каждого чата
users_calendar = {}


# Функция для создания разметки календаря
def create_calendar(year, month):
    markup = types.InlineKeyboardMarkup(row_width=7)
    # days = [types.InlineKeyboardButton(calendar.day_abbr[i], callback_data=str(i)) for i in range(7)]
    # markup.row(*days)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        days = [
            types.InlineKeyboardButton(str(day) if day != 0 else " ", callback_data=str(day))
            for day in week
        ]
        markup.row(*days)

    markup.row(
        types.InlineKeyboardButton("<<", callback_data="PREV_MONTH"),
        types.InlineKeyboardButton(">>", callback_data="NEXT_MONTH"),
    )

    return markup


# Функция для отображения календаря
async def show_calendar(chat_id, current_year, current_month):
    calendar_markup = create_calendar(current_year, current_month)
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    await bot.send_message(chat_id, f"{months[current_month-1]} {current_year}", reply_markup=calendar_markup)


# Обработчик команды /calendar
async def start_command(message: types.Message):
    chat_id = message.chat.id
    users_calendar[chat_id] = {}

    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    users_calendar[chat_id]['year'] = current_year
    users_calendar[chat_id]['month'] = current_month

    await show_calendar(chat_id, current_year, current_month)


# Обработчик нажатий на кнопки календаря
async def handle_callback_query(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    year = users_calendar[chat_id].get('year', datetime.now().year)
    month = users_calendar[chat_id].get('month', datetime.now().month)

    if query.data == 'PREV_MONTH':
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
    elif query.data == 'NEXT_MONTH':
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1

    users_calendar[chat_id]['year'] = year
    users_calendar[chat_id]['month'] = month

    # Изменяем существующее сообщение с календарем
    await show_calendar(chat_id, year, month)
    await query.message.delete()


# Обработчик нажатий на кнопки с датами календаря
async def handle_date_selection(query: types.CallbackQuery, state: FSMContext):
    chat_id = query.message.chat.id
    current_date = datetime.now()
    selected_date = query.data
    selected_year = current_date.year
    try:
        user_selected_date = datetime(selected_year, int(users_calendar[chat_id]['month']), int(selected_date)).strftime("%d.%m.%Y")
        user_selected_obj = datetime.strptime(user_selected_date, "%d.%m.%Y")
        user_selected_obj_minus_day = current_date - timedelta(days=1)
        fd = user_selected_obj.strftime("%Y-%m-%d %H:%M:%S")
        if user_selected_obj < user_selected_obj_minus_day:
            await bot.send_message(chat_id, "Это прошлое. Прошлого уже не вернуть. ")
            return
        await bot.send_message(chat_id, f"Вы выбрали {selected_date} число и месяц: {users_calendar[chat_id]['month']}")

    # Записываем выбранную дату в формате ДД.ММ.ГГГГ
        async with state.proxy() as data:
            # formated_date = datetime.strptime(user_selected_date, "%d").strftime("%d.%m.%Y")
            data['distantMemberDate'] = fd
    except:
        await bot.send_message(chat_id, "Это не число. Рекомендую запустить команду поверки IQ")
        return
    # await bot.send_message(chat_id, user_selected_date)

    # Запускаем функцию distant_distantMember с выбранной датой
    await distant_distantMember(query.message, state)
    await query.message.delete()


#-------------------------------Запись удаленки через машину состояний------------------------------------------------

class Distants(StatesGroup):
    distantMember = State()
    distantMemberDate = State()

async def distant(message: types.Message, state: FSMContext):
    if (message.chat.type == 'private'):
        await Distants.distantMember.set()
        memberName = c.execute("SELECT Name FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0]
        await message.answer("Начинаю процедуру записи удалёнки 🧐\n\nТы идентифицирован как: " + memberName + ".\n\n Если это не ты или просто хочешь остановить запись, то напиши /stop или «отмена»")
        async with state.proxy() as data:
            data['distantMember'] = c.execute("SELECT ID FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0]
        # await message.answer("Введи дату удалёнки в формате ДД.ММ.ГГГГ")
        await start_command(message)
        now_date = datetime.now()
        await Distants.next()
    else:
        await message.answer("Эта команда доступна только в личных сообщениях")

async def stop_distant(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Запись ответов отменена")

async def distant_distantMember(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        # formated_date = ''
        # try:
        #     formated_date = datetime.strptime(message.text, "%d.%m.%Y")
        #     # print(formated_date)
        #     # 2022-02-22 00:00:00
        # except:
        #     await message.reply("Неверный формат даты, попробуй еще раз. Либо введи /stop, чтобы сбросить запись")
        #     return
        # data['distantMemberDate'] = formated_date
        try:
            c.execute("INSERT INTO distant (MemberID, DistantDate) VALUES (?, ?)", (data['distantMember'], data['distantMemberDate']))
            db.commit()
        except:
            await message.reply("Такая запись уже есть в базе.\n Посмотри свои удалёнки: /my_distant")
            await state.finish()
            return
        # await database.sql_add_distant(state)
        await message.answer("Ваша удалёнка записана, коллега 🫡")
        for el in admins:
            await bot.send_message(el, "#удалёнки\nНовая удалёнка:\n\n" + c.execute("SELECT Name FROM members WHERE ID = ?", (data['distantMember'],)).fetchone()[0] + "\n" + str(data['distantMemberDate']).split(" ")[0])
        await state.finish()

class Feedback(StatesGroup):
    feedbackMember = State()
    feedbackMemberText = State()

async def feedback(message: types.Message, state: FSMContext):
    if (message.chat.type == 'private'):
        await Feedback.feedbackMember.set()
        memberName = c.execute("SELECT Name FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0]
        await message.answer("Ох... Наверное что-то работает не так, как надо... Хотя... Может ты хочешь написать положительный отзыв? 🧐\n\nТы идентифицирован как: " + memberName + ".\n\n Если это не ты или просто хочешь остановить запись, то напиши /stop или «отмена»")
        async with state.proxy() as data:
            data['feedbackMember'] = c.execute("SELECT ID FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0]
        await Feedback.next()
        await message.answer("Введи текст обратной связи: ")
    else:
        await message.answer("Эта команда доступна только в личных сообщениях")

async def stop_feedback(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Запись ответов отменена")

async def feedback_feedbackMember(message: types.Message, state: FSMContext):
    
        async with state.proxy() as data:
            data['feedbackMemberText'] = message.text
            try:
                await bot.send_message(superAdmin_ID, "#feedback\n\n" + " " + message.from_user.first_name + " Пишет: \n\n" + data['feedbackMemberText'] + "\n\n" + "Дата обращения: \n\n" + str(datetime.now()).split(" ")[0])
            except:
                await message.reply("Почему-то не получилось отправить сообщение. Скорее всего у тебя не указано имя в телеге.")
                await state.finish()
                return
            # await database.sql_add_distant(state)
            await message.reply("Ваше обращение очень важно для нас! Продолжайте пользоваться ботом!\n Я передал информацию @AlexanderSitnik")
            await state.finish()

#----------------------------Выводы в клиентскую часть----------------------------------------------------

#вывести имена пользователей, у которых сегодня удалёнка
async def distant_today(message: types.Message):
    today = datetime.today().strftime('%Y-%m-%d')
    today += ' 00:00:00'
    distant_today = c.execute("SELECT Name FROM members WHERE ID IN (SELECT MemberID FROM distant WHERE DistantDate = ?)", (today,)).fetchall()
    distant_today_list = ''
    if distant_today != []:
        for el in distant_today:
            distant_today_list += '– ' + str(el[0]) + '\n'
        await message.answer("*Сегодня удалёнка у:* \n\n" + str(distant_today_list), parse_mode= 'Markdown')
    else:
        await message.answer("*Сегодня удалёнок ни у кого нет*", parse_mode= 'Markdown')
    return distant_today_list

async def distant_today_personal():
    today = datetime.today().strftime('%Y-%m-%d')
    today += ' 00:00:00'
    distant_today = c.execute("SELECT Name FROM members WHERE ID IN (SELECT MemberID FROM distant WHERE DistantDate = ?)", (today,)).fetchall()
    distant_today_list = ''
    if distant_today != []:
        for el in distant_today:
            distant_today_list += '– ' + str(el[0]) + '\n'
    await bot.send_message(superAdmin_ID, "Сегодня удалёнка у: \n\n" + str(distant_today_list))

#вывести свои удалёнки
async def my_distant(message: types.Message):
    distant_member = c.execute("SELECT DistantDate FROM distant WHERE MemberID IN (SELECT ID FROM members WHERE TelegramID = ?) AND DistantDate BETWEEN date('now', 'start of month') AND date('now', 'start of month', '+1 month')", (message.from_user.id,)).fetchall()
    distant_member_list = ''
    distant_member_remainder = 3 - len(distant_member)
    for el in distant_member:
        distant_member_list += str(el[0])[0:10] + '\n'
    if distant_member_list != []:
        await message.answer("Твои удалёнки этого месяца:\n" + "\n" + distant_member_list + "\n" + "Осталось удалёнок: " + str(distant_member_remainder))
    else:
        await message.answer("У тебя ещё нет удалёнок в этом месяце")

#по нажатию на команду из базы данных удаляется последняя удаленка пользователя
async def delete_distant(message: types.Message):
    try:
        c.execute("DELETE FROM distant WHERE MemberID IN (SELECT ID FROM members WHERE TelegramID = ?) AND DistantDate IN (SELECT MAX(DistantDate) FROM distant WHERE MemberID IN (SELECT ID FROM members WHERE TelegramID = ?))", (message.from_user.id, message.from_user.id))
        db.commit()
        await message.answer("Последняя запись о удаленой работе удалена")
    except:
        await message.answer("Удалёнки нет")

async def get_sudo_command(message: types.Message):
    if message.from_user.id == superAdmin_ID:
        await message.answer("Вот список команд для суперадмина:\n/get_all_id – получить TelergamID всех пользователей в базе\n/get_my_id – получить ID чата или беседы\n/get_db – получить файл базы данных")
    else:
        await message.answer("Ты не суперадмин!")

async def get_all_id(message: types.Message):
    if message.from_user.id == superAdmin_ID:
        all_id = c.execute("SELECT Name, TelegramID FROM members").fetchall()
        all_id_list = ''
        for el in all_id:
            all_id_list += str(el[0]) + ' - ' + str(el[1]) + '\n'
        await message.answer("Все пользователи и их id:\n" + "\n" + all_id_list)
    else:
        await message.answer("Ты не суперадмин!")

async def get_my_id(message: types.Message):
    await message.answer("Твой TelegramID: " + str(message.chat.id) + '\n P.S. TelegramID бесед начинается с минуса')

async def who_am_i(message: types.Message):
    # получить информацию о пользователе: Name, Department, Grade, Birthday, Employment
    try:
        member_info = c.execute("SELECT Name, Grade, Birthday, Employment FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchall()
        await message.answer("Твои данные:\n\n" + "Имя: " + str(member_info[0][0]) + "\n" + "Грейд: " + str(member_info[0][1]) + "\n" + "Дата рождения: " + str(member_info[0][2]) + "\n" + "Дата трудоустройства: " + str(member_info[0][3]) + '\n' + "\nP.S. Если что-то не так, напиши /feedback и сообщи об ошибке")   
    except:
        await message.answer("Ты не зарегистрирован в базе данных")
        return

async def what_time_is_it(message: types.Message):
    await bot.send_message(message.from_user.id, "Сейчас " + str(datetime.now().strftime('%H:%M:%S')))

async def cocksize(message: types.Message):
    await message.answer("Эта команда устарела. Воспользуйся инлайн режимом")

async def in_jail(message: types.Message):
    if message.from_user.id == 640370572:
        await message.answer("Я в тюрьме, потому что ездил без водительских прав. Все задачи сдвигаются на 15 суток. Приношу свои извинения за неудобства")
        await message.answer_sticker(r'CAACAgIAAxkBAAEHaGhjz3IZQhAd4L_p-LFAtGHXz0RjxQACVBYAAtl0gElO0rj0_1bJXC0E')
    else:
        await message.answer("Ты не можешь использовать эту команду")

async def clearIQ():
    c.execute("DELETE FROM iq")
    db.commit()

async def iq_staistics(message: types.Message):
    iq = c.execute("SELECT * FROM iq").fetchall()
    iq_list = ''
    #подсчитать все значения IQNum и вычислить среднее
    iq_sum = 0
    for el in iq:
        iq_sum += int(el[1])
    iq_average = iq_sum / len(iq)
    await message.answer("Средний IQ в Студии сегодня: " + str(iq_average))

def register_handlers_distant(dp: Dispatcher):
    dp.register_message_handler(distant, commands=['distant'])
    dp.register_message_handler(stop_distant, commands=['stop'], state="*")
    dp.register_message_handler(stop_distant, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(distant_distantMember, state=Distants.distantMemberDate)
    dp.register_message_handler(distant_today, commands=['distant_today'])
    dp.register_message_handler(my_distant, commands=['my_distant'])
    dp.register_message_handler(feedback, commands=['feedback'])
    dp.register_message_handler(stop_feedback, commands=['stop'], state="*")
    dp.register_message_handler(stop_feedback, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(feedback_feedbackMember, state=Feedback.feedbackMemberText)
    dp.register_message_handler(get_all_id, commands=['get_all_id'])
    dp.register_message_handler(get_my_id, commands=['get_my_id'])
    dp.register_message_handler(get_sudo_command, commands=['sudo'])
    dp.register_message_handler(who_am_i, commands=['who_am_i'])
    dp.register_message_handler(what_time_is_it, commands=['time'])
    dp.register_message_handler(cocksize, commands=['cocksize'])
    dp.register_message_handler(delete_distant, commands=['delete_last_distant'])
    dp.register_message_handler(in_jail, commands=['jail'])
    dp.register_message_handler(iq_staistics, commands=['iq'])
    # dp.register_message_handler(start_command, commands=['calendar'])
    dp.register_callback_query_handler(handle_callback_query, lambda query: query.data in ['PREV_MONTH', 'NEXT_MONTH'], state=Distants.distantMemberDate)
    dp.register_callback_query_handler(handle_date_selection, lambda query: query.data.isdigit(), state=Distants.distantMemberDate)
