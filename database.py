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

try:
    db = sqlite3.connect('./data/tdsgnBotBase.db')
    c = db.cursor()
except:
    pass


class Database():
    def get_all_members (self):
        return c.execute("SELECT Name FROM members").fetchall()

    def delete_member_by_id (self, id):
        c.execute("DELETE FROM members WHERE ID = ?", (id,))
        db.commit()

    def get_member_by_id (self, id):
        return c.execute("SELECT * FROM members WHERE ID = ?", (id,)).fetchone()


temp = Database()
print(temp.get_member_by_id(1))
temp.delete_member_by_id(2)
