from email import message
import sqlite3
from unicodedata import name
from datetime import datetime

currentId = None

try:
    db = sqlite3.connect('./data/tdsgnBotBase.db')
    c = db.cursor()
except:
    pass

def get_members():
    c.execute("SELECT * FROM members")
    return c.fetchall()
def format_members():
    members = get_members()
    for i in members:
        members_string = 'ID: ' + str(i[0]) + '\n' \
            + 'Name: ' + i[1] + '\n' \
            + 'Department: ' + i[2] + '\n' \
            + 'Grade: ' + i[3] + '\n' \
            + 'Birthday: ' + i[4] + '\n' \
            + 'Employer: ' + i[5] + '\n'
    return members_string
print(format_members())

def get_current_id():
    currentId =  len(get_members()) + 1
    return currentId

def set_member(id, name, department, grade, birthday, employer):
    c.execute("INSERT INTO members VALUES (?, ?, ?, ?, ?, ?)", (id, name, department, grade, birthday, employer))
    db.commit()
get_current_id()

async def sql_add_deception(state):
    async with state.proxy() as data:
        c.execute("INSERT INTO deseption VALUES (?, ?, ?)", tuple(data.values()))
        db.commit()

async def sql_add_distant(state):
    async with state.proxy() as data:
        c.execute("INSERT INTO distant VALUES (?, ?)", tuple(data.values()))
        db.commit()

def sql_get_last_deception():
    last_deception = c.execute("SELECT * FROM deseption").fetchall()
    for el in last_deception:
        last_deception_text = 'Имя лжеца: ' + str(el[0]) + '\n' \
            + 'Дата обмана: ' + el[1] + '\n' \
            + 'Текст обмана: ' + el[2] + '\n'
        return last_deception_text
print(sql_get_last_deception())

test_date = datetime.strptime('22/10/2022', "%d/%m/%Y")
print(test_date)