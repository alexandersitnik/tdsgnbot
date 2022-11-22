from aiogram import types, Dispatcher, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import dp
import sqlite3

try:
    db = sqlite3.connect('./data/tdsgnBotBase.db')
    c = db.cursor()
except:
    pass

async def members_kb(message: types.Message):
    if(message.chat.type == 'private'):
        membersKeyboardList = []
        for el in c.execute("SELECT * FROM members WHERE TelegramID IS NULL").fetchall():
            membersKeyboardList.append(InlineKeyboardButton(el[1], callback_data=el[0]))
        membersKeyboard = InlineKeyboardMarkup(row_width=2)
        membersKeyboard.add(*membersKeyboardList)
        await message.answer('Приветствую!\nЯ бот-камикадзе. Совсем скоро Международный Bitrix Разработчик выкатит апдейт для CRM, в котором будут те же функции, только лучше😉 А мой сервер отключат и я перестану работать... \n\n Но не будем о грустном! Дело в том, что пока ты не зарегистрирован, я не могу тебе помочь. Так что давай, не устраивай годзильник и найди своё имя из списка ниже.')
        await message.answer_sticker(r'CAACAgIAAxkBAAEGWNVjaUo4P20YoAcjmGvAlQHRP4ZcMgACJxgAApd54UvWARYS3sXfTysE')
        await message.answer('Найди себя: ', reply_markup=membersKeyboard)
    else:
        await message.answer('Команда доступна только в личных сообщениях')

@dp.callback_query_handler()
async def callback_kb(callback_query: types.CallbackQuery):
    try:
        c.execute("UPDATE members SET TelegramID = ? WHERE ID = ?", (callback_query.from_user.id, callback_query.data))
        db.commit()
        await callback_query.message.answer('Ты успешно зарегистрирован!\n Теперь введи команду: /help чтобы узнать, что я умею')
    except:
        await callback_query.message.answer('Ты, видимо, уже зарегистрирован. Ну или кто-то нехороший сделал это за тебя. Жмякай /help и давай смотреть что можно сделать')
async def log_out(message: types.Message):
    if(message.chat.type == 'private'):
        c.execute("UPDATE members SET TelegramID = NULL WHERE TelegramID = ?", (message.from_user.id,))
        db.commit()
        await message.answer('Теперь ты не зарегистрирован. Пожалуй, нам действительно будет лучше друг без друга. \n\nВведи команду /start чтобы зарегистрироваться заново.\n\n ⚠️ И ПОМНИ, пока ты не зарегистрирован, я не могу тебе помочь')
        await message.answer_photo(r'https://click-or-die.ru/wp-content/uploads/2020/12/4kaaagga0ua-960-680x524.jpg')
    else:
        await message.answer('Команда доступна только в личных сообщениях')

def register_handlers_members_kb(dp: Dispatcher):
    dp.register_message_handler(members_kb, commands=['start'])
    dp.register_message_handler(log_out, commands=['log_out'])
