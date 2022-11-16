from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot
from datetime import datetime
from register_handlers import admins
import sqlite3

superAdmin_ID = 265007461

try:
    db = sqlite3.connect('./data/tdsgnBotBase.db')
    c = db.cursor()
except:
    pass

#-------------------------------Запись удаленки через машину состояний------------------------------------------------

class Distants(StatesGroup):
    distantMember = State()
    distantMemberDate = State()

async def distant(message: types.Message, state: FSMContext):
    await Distants.distantMember.set()
    memberName = c.execute("SELECT Name FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0]
    await message.answer("Начинаю процедуру записи удалёнки 🧐\n\nТы идентифицирован как: " + memberName + ".\n\n Если это не ты или просто хочешь остановить запись, то напиши /stop или «отмена»")
    async with state.proxy() as data:
        data['distantMember'] = c.execute("SELECT ID FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0]
    await Distants.next()
    await message.answer("Введи дату удалёнки в формате ДД.ММ.ГГГГ")

async def stop_distant(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Запись ответов отменена")

async def distant_distantMember(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        formated_date = ''
        try:
            formated_date = datetime.strptime(message.text, "%d.%m.%Y")
        except:
            await message.reply("Неверный формат даты, попробуй еще раз")
            return
        data['distantMemberDate'] = formated_date
        try:
            c.execute("INSERT INTO distant (MemberID, DistantDate) VALUES (?, ?)", (data['distantMember'], data['distantMemberDate']))
            db.commit()
        except:
            await message.reply("Такая запись уже есть в базе.\n Посмотри свои удалёнки: /my_distant")
            await state.finish()
            return
        # await database.sql_add_distant(state)
        await message.reply("Ваша удалёнка записана, коллега 🫡")
        for el in admins:
            await bot.send_message(el, "#удалёнки\nНовая удалёнка:\n\n" + c.execute("SELECT Name FROM members WHERE ID = ?", (data['distantMember'],)).fetchone()[0] + "\n" + str(data['distantMemberDate']).split(" ")[0])
        await state.finish()

class Feedback(StatesGroup):
    feedbackMember = State()
    feedbackMemberText = State()

async def feedback(message: types.Message, state: FSMContext):
    await Feedback.feedbackMember.set()
    memberName = c.execute("SELECT Name FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0]
    await message.answer("Ох... Наверное что-то работает не так, как надо... Хотя... Может ты хочешь написать положительный отзыв? 🧐\n\nТы идентифицирован как: " + memberName + ".\n\n Если это не ты или просто хочешь остановить запись, то напиши /stop или «отмена»")
    async with state.proxy() as data:
        data['feedbackMember'] = c.execute("SELECT ID FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0]
    await Feedback.next()
    await message.answer("Введи текст обратной связи: ")

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
            await message.reply("Ваше обращение очень важно для нас! Продолжайте пользоваться ботом!")
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
            distant_today_list += '📌 ' + str(el[0]) + '\n'
        await message.answer("🏠 Сегодня удалёнка у: \n\n" + str(distant_today_list))
    else:
        await message.answer("Сегодня удалёнок ни у кого нет")

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