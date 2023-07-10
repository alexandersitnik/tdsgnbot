# from calendar import monthrange
# import calendar
# import random
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram import types, Dispatcher
# from aiogram.dispatcher.filters import Text
# from create_bot import bot
# from datetime import datetime, timedelta
# from register_handlers import admins
# import sqlite3
#
# try:
#     db = sqlite3.connect('./data/tdsgnBotBase.db')
#     c = db.cursor()
# except:
#     pass
#
#
# def get_most_distant_member (message: types.Message):
#     global MemberID
#     try:
#         c.execute('SELECT MemberID, COUNT(MemberID) FROM distant GROUP BY MemberID ORDER BY COUNT(MemberID) DESC '
#                   'LIMIT 1')
#         result = c.fetchall()
#         for row in result:
#             member_id = row[0]
#             count = row[1]
#         c.execute('SELECT name FROM members WHERE id = ?', (MemberID,))
#         result = c.fetchall()
#         for row in result:
#             name = row[0]
#         await bot.send_message(message.from_user.id, text=f'Самый дальний участник: {name} ({count} раз)')
#         return name, count
#     except:
#         return False
#
#
# def register_handlers_statistics(dp: Dispatcher):
#     dp.register_message_handler(get_most_distant_member, commands=['most_distant'])
