from create_bot import dp, bot
import random
import hashlib
import sqlite3
from aiogram import types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
epithets = ['ёлочки 🌲', 'сосульки 🧊', 'колокольчика 🔔', 'мишуры 🎊', 'морковки ⛄️','имбирного пряника 🥮','петарды 🧨','фейерверка 🎆','бенгальского огонька 🎇','игрушки 🐰','волшебства 🪄', 'подарочка 🎁', 'мандаринки 🍊', 'гирлянды 💡', 'леденца 🍭']
try:
    db = sqlite3.connect('./data/tdsgnBotBase.db')
    c = db.cursor()
except:
    pass
async def inline_echo(inline_query: InlineQuery):
    cocksize_len = random.randint(1, 160)
    epithet = random.choice(epithets)
    telegramID = inline_query.from_user.id
    memberID = c.execute("SELECT ID FROM members WHERE TelegramID = ?", (telegramID,)).fetchone()[0]
    if c.execute("SELECT * FROM iq WHERE MemberID = ?", (memberID,)).fetchone() == None:
        c.execute("INSERT INTO iq (MemberID, IQNum) VALUES (?, ?)", (memberID, cocksize_len))
        db.commit()
    else:
        cocksize_len = c.execute("SELECT IQNum FROM iq WHERE MemberID = ?", (memberID,)).fetchone()[0]
        db.commit()
    text = 'Твой IQ равен: ' + str(cocksize_len)
    input_content = InputTextMessageContent(text)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=f'Посмотрим какой у тебя IQ',
        input_message_content=input_content,
    )
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)

def register_handlers_inline(dp):
    dp.register_inline_handler(inline_echo)