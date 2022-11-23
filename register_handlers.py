from aiogram import types, Dispatcher
from database import format_members
from aiogram.types import InputFile

#группы пользователей
#администраторы
admins = [265007461, 794933879, 187993761, 753790050]
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
        "/feedback - отправить обратную связь\n\n" +
        "/log_out - сбросить регистрацию\n\n" +
        "v 1.3")
    else:
        await message.answer('Коллега, не нужно писать мне в общие чаты, я бот для личных сообщений.')

async def whatsnew(message: types.Message):
    await message.answer("v1.3\nТеперь ты можешь измерить размер члена\n\nv1.2\nВ этой версии добавлены ежедневные отчёты, бота теперь можно добавлять в чаты\n\nv 1.1\nДобавлены команды /sick и /who_is_sick_today")

async def get_db_command(message: types.Message):
    if (message.chat.type == 'private' and message.from_id == 265007461):
        date_str = 'BD'
        filename = f'{date_str}.db'
        db_file = InputFile('./data/tdsgnBotBase.db', filename=filename)
        await message.answer_document(document=db_file, caption='Файл базы данных.')
    else:
        await message.answer('Команда доступна только администраторам.')

def register_handlers(dp : Dispatcher):
    dp.register_message_handler(help_command, commands = ['help'])
    dp.register_message_handler(whatsnew, commands = ['whats_new'])
    dp.register_message_handler(get_db_command, commands = ['get_db'])