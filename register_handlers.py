from aiogram import types, Dispatcher
# from database import format_members
from aiogram.types import InputFile

#группы пользователей
#администраторы
admins = [265007461, 1626350569, 178114342, 784075692, 297354649, 964660345]
#тестирование
translators = [265007461]

async def help_command(message: types.Message):
    if (message.chat.type == 'private'):
        await message.answer("Вот какие команды ты можешь использовать:\n\n " + 
        "/help - вывести список команд\n" +
        "/whats_new - узнать что нового в текущей версии\n\n" +
        "УДАЛЁНКА\n\n"
        "/distant - записаться на удалёнку\n" +
        "/my_distant - вывести свои удалёнки месяца\n" +
        "/distant_today - узнать кто сегодня на удалёнке\n\n" +
        "ОТПУСКИ\n\n" + 
        "/vacation - подать заявление на отпуск\n" + 
        "/my_vacations - посмотреть свои отпуска\n" + 
        "/today_vacations - посмотреть кто сегодня в отпуске\n\n" + 
        "БОЛЬНИЧНЫЕ\n\n" + 
        "/sick – сообщить о своём больничном\n" +
        "/who_is_sick_today – узнать кто сегодня на больничном\n\n" +
        "SSL\n\n" +
        "/add_new_ssl – получить текущий список сертификатов\n" +
        "/get_ssl_table – получить текущий список сертификатов\n\n" +
        "ОСТАЛЬНОЕ\n\n" +
        "/feedback - отправить обратную связь\n" +
        "/prediction - получить предсказание\n\n" +
        "v 2.1")
    else:
        await message.answer('Коллега, не нужно писать мне в общие чаты, я бот для личных сообщений.')

async def whatsnew(message: types.Message):
    await message.answer("v2.1\n Теперь ты можешь записываться на удаленку через календарь. "
                         "Также появилась табличка для отслеживания сроков SSL сертификатов проектов")

async def get_db_command(message: types.Message):
    if (message.chat.type == 'private' and message.from_id == 265007461):
        date_str = 'BD'
        filename = f'{date_str}.db'
        db_file = InputFile('./data/tdsgnBotBase.db', filename=filename)
        await message.answer_document(document=db_file, caption='Файл базы данных.')
    else:
        await message.answer('Команда доступна только администраторам.')

def register_handlers1(dp : Dispatcher):
    dp.register_message_handler(help_command, commands = ['help'])
    dp.register_message_handler(whatsnew, commands = ['whats_new'])
    dp.register_message_handler(get_db_command, commands = ['get_db'])