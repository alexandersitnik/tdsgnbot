from aiogram import types, Dispatcher
from database import format_members

#группы пользователей
#администраторы
admins = [265007461, 794933879]
#тестирование
translators = [265007461]

async def send_members(message: types.Message):
    format_members()
    await message.answer("Members: " + format_members())

async def help_command(message: types.Message):
    await message.answer("Вот какие команды ты можешь использовать:\n\n " + 
    "/help - вывести список команд\n\n" +
    "УДАЛЁНКА\n\n"
    "/distant - записаться на удалёнку\n" +
    "/my_distant - вывести свои удалёнки месяца\n" +
    "/distant_today - узнать кто сегодня на удалёнке\n\n" +
    "ОТПУСКИ\n\n" + 
    "/vacation - подать заявление на отпуск\n" + 
    "/my_vacations - посмотреть свои отпуска\n" + 
    "/today_vacations - посмотреть кто сегодня в отпуске\n\n" + 
    "/feedback - отправить обратную связь\n\n" +
    "/log_out - сбросить регистрацию\n\n")

def register_handlers(dp : Dispatcher):
    dp.register_message_handler(send_members, commands = ['members'])
    dp.register_message_handler(help_command, commands = ['help'])