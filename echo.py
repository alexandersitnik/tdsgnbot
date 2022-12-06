from create_bot import dp, bot
import random
import hashlib
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
epithets = ['ёлочки 🌲', 'сосульки 🧊', 'колокольчика 🔔', 'мишуры 🎊', 'морковки ⛄️','имбирного пряника 🥮','питарды 🧨','феерверка 🎆','бенгальского огонька 🎇','игрушки 🐰','волшебства 🪄', 'подарочка 🎁', 'мандаринки 🍊', 'гирлянды 💡', 'леденца 🍭']
async def inline_echo(inline_query: InlineQuery):
    print('отработала инлайн функция')
    # id affects both preview and content,
    # so it has to be unique for each result
    # (Unique identifier for this result, 1-64 Bytes)
    # you can set your unique id's
    # but for example i'll generate it based on text because I know, that
    # only text will be passed in this example
    cocksize_len = random.randint(1, 50)
    epithet = random.choice(epithets)
    text = 'Мой размер ' + epithet + ': ' + str(cocksize_len) + ' см'
    # text = str(cocksize_len) or 'Не могу разглядеть'
    input_content = InputTextMessageContent(text)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=f'Ну давай, покажи свой размер {epithet}',
        input_message_content=input_content,
    )
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)

def register_handlers_inline(dp):
    dp.register_inline_handler(inline_echo)